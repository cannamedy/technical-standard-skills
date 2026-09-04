#!/usr/bin/env python3
"""Validate the visual design contract of a generated DOCX.

This validator checks deterministic typography and style signals. It does not
pretend that XML can replace page-image review; when a PDF is supplied it also
reports page-density signals and keeps a human visual-review requirement.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from docx import Document
from docx.oxml.ns import qn


@dataclass
class Finding:
    code: str
    message: str
    blocking: bool = True
    evidence: str = ""
    recommendation: str = ""


def _profile_text(path: Path | None) -> str:
    return path.read_text(encoding="utf-8") if path and path.exists() else ""


def _section(text: str, name: str) -> str:
    match = re.search(rf"^{re.escape(name)}:\s*$", text, re.MULTILINE)
    if not match:
        return ""
    tail = text[match.end():]
    next_section = re.search(r"^\S.*:\s*$", tail, re.MULTILINE)
    return tail[: next_section.start()] if next_section else tail


def _value(text: str, key: str, default: Any, section: str | None = None) -> Any:
    scope = _section(text, section) if section else text
    match = re.search(rf"^\s+{re.escape(key)}:\s*[\"']?([^\"'\n#]+?)[\"']?\s*$", scope, re.MULTILINE)
    if not match:
        return default
    value = match.group(1).strip()
    try:
        return float(value) if "." in value else int(value)
    except ValueError:
        return value


def _font_name(style) -> str | None:
    if style.font.name:
        return style.font.name
    rpr = style._element.rPr
    if rpr is None:
        return None
    fonts = rpr.find(qn("w:rFonts"))
    return fonts.get(qn("w:ascii")) if fonts is not None else None


def _eastasia_font_name(style) -> str | None:
    rpr = style._element.rPr
    if rpr is None:
        return None
    fonts = rpr.find(qn("w:rFonts"))
    return fonts.get(qn("w:eastAsia")) if fonts is not None else None


def _pt(value) -> float | None:
    return round(value.pt, 3) if value is not None else None


def _style_record(document: Document, name: str) -> dict[str, Any] | None:
    try:
        style = document.styles[name]
    except KeyError:
        return None
    pf = style.paragraph_format
    return {
        "font": _font_name(style),
        "size_pt": _pt(style.font.size),
        "bold": style.font.bold,
        "italic": style.font.italic,
        "space_before_pt": _pt(pf.space_before) or 0,
        "space_after_pt": _pt(pf.space_after) or 0,
        "line_spacing": pf.line_spacing,
        "keep_with_next": pf.keep_with_next,
        "page_break_before": pf.page_break_before,
        "left_indent_cm": round(pf.left_indent.cm, 3) if pf.left_indent else 0,
        "first_line_indent_cm": round(pf.first_line_indent.cm, 3) if pf.first_line_indent else 0,
    }


def _direct_formatting(document: Document) -> dict[str, Any]:
    paragraphs = list(document.paragraphs)
    direct_paragraphs = 0
    runs = []
    for paragraph in paragraphs:
        ppr = paragraph._p.pPr
        direct = False
        if ppr is not None:
            # pStyle selects the named semantic style and numPr carries the
            # intentional list instance; neither is paragraph-level styling.
            direct = any(child.tag not in {qn("w:pStyle"), qn("w:numPr")} for child in ppr)
        direct_paragraphs += int(direct)
        runs.extend(paragraph.runs)
    direct_runs = 0
    for run in runs:
        rpr = run._r.rPr
        if rpr is not None and len(list(rpr)):
            direct_runs += 1
    return {
        "paragraphs": len(paragraphs),
        "direct_paragraphs": direct_paragraphs,
        "paragraph_ratio": round(direct_paragraphs / max(len(paragraphs), 1), 4),
        "runs": len(runs),
        "direct_runs": direct_runs,
        "run_ratio": round(direct_runs / max(len(runs), 1), 4),
    }


def _font_available(font: str | None) -> bool | None:
    if not font or not shutil.which("fc-match"):
        return None
    result = subprocess.run(["fc-match", "-f", "%{family}", font], capture_output=True, text=True, check=False)
    return bool(result.stdout.strip())


def _pdf_signals(pdf: Path) -> dict[str, Any]:
    info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True, check=False).stdout
    pages_match = re.search(r"^Pages:\s+(\d+)", info, re.MULTILINE)
    pages = int(pages_match.group(1)) if pages_match else 0
    densities: list[int] = []
    missing_glyph_pages: list[int] = []
    for page in range(1, pages + 1):
        result = subprocess.run(["pdftotext", "-f", str(page), "-l", str(page), "-layout", str(pdf), "-"], capture_output=True, text=True, check=False)
        value = result.stdout
        densities.append(len(re.sub(r"\s+", "", value)))
        if "�" in value:
            missing_glyph_pages.append(page)
    interior = densities[1:-1] if len(densities) > 2 else densities
    offset = 1 if len(densities) > 2 else 0
    return {
        "page_count": pages,
        "character_density": {
            "min": min(interior) if interior else 0,
            "max": max(interior) if interior else 0,
            "median": sorted(interior)[len(interior) // 2] if interior else 0,
            "sparsest_pages": [index + offset + 1 for index, value in enumerate(interior) if value == min(interior)] if interior else [],
            "densest_pages": [index + offset + 1 for index, value in enumerate(interior) if value == max(interior)] if interior else [],
            "cover_density": densities[0] if densities else 0,
            "final_page_density": densities[-1] if densities else 0,
        },
        "missing_glyph_pages": missing_glyph_pages,
    }


def validate(docx_path: Path, profile_path: Path | None = None, pdf_path: Path | None = None, strict: bool = False) -> dict[str, Any]:
    document = Document(str(docx_path))
    profile = _profile_text(profile_path)
    findings: list[Finding] = []
    body = _style_record(document, "Normal") or {}
    heading_styles = {f"Heading {level}": _style_record(document, f"Heading {level}") for level in range(1, 7)}
    semantic_styles = {
        name: _style_record(document, name)
        for name in ("Lead-in", "Runtime Label", "Question Label", "Code", "ASCII Diagram", "Table Header", "Table Body", "Bullet 1", "Bullet 2", "Numbered 1", "Numbered 2", "TOC 1", "TOC 2", "TOC 3", "Header", "Footer")
    }
    required = ("Heading 1", "Heading 2", "Heading 3", "Code", "ASCII Diagram", "TOC 1", "TOC 2", "TOC 3")
    for name in required:
        if (not heading_styles.get(name) and name.startswith("Heading")) or (not semantic_styles.get(name) and not name.startswith("Heading")):
            findings.append(Finding("STYLE_MISSING", f"required named style {name!r} is missing", evidence=name, recommendation="define the semantic style in the publication design system"))

    sizes = {name: record.get("size_pt") for name, record in {"Body": body, **heading_styles}.items() if record and record.get("size_pt") is not None}
    if all(key in sizes for key in ("Heading 1", "Heading 2", "Heading 3", "Body")):
        h1, h2, h3, body_size = (sizes[key] for key in ("Heading 1", "Heading 2", "Heading 3", "Body"))
        if not h1 > h2 > h3 > body_size:
            findings.append(Finding("HEADING_SIZE_ORDER_INVALID", f"size order is H1={h1}, H2={h2}, H3={h3}, Body={body_size}", evidence=str(sizes), recommendation="make chapter, section, subsection, and body sizes strictly descend"))
        for name in ("Heading 1", "Heading 2"):
            if heading_styles[name].get("bold") is not True:
                findings.append(Finding("HEADING_NOT_BOLD", f"{name} is not bold", recommendation="use bold for major hierarchy levels"))
        body_after = body.get("space_after_pt", 0)
        body_before = body.get("space_before_pt", 0)
        if all(heading_styles[name].get("space_before_pt", 0) == body_before and heading_styles[name].get("space_after_pt", 0) == body_after for name in ("Heading 1", "Heading 2", "Heading 3")):
            findings.append(Finding("HEADING_SPACING_TOO_LOW", "H1/H2/H3 spacing is identical to body spacing", blocking=False, evidence=f"body before/after={body_before}/{body_after}", recommendation="give headings a distinct vertical rhythm"))
        thresholds = {
            "Heading 1": _value(profile, "minimum_h1_body_ratio", 1.4, "visual"),
            "Heading 2": _value(profile, "minimum_h2_body_ratio", 1.2, "visual"),
            "Heading 3": _value(profile, "minimum_h3_body_ratio", 1.08, "visual"),
        }
        for name, minimum in thresholds.items():
            ratio = sizes[name] / body_size
            if ratio < float(minimum):
                findings.append(Finding("HEADING_BODY_CONTRAST_TOO_LOW", f"{name}/Body ratio is {ratio:.3f}, below {minimum}", recommendation="increase size contrast or use a profile-approved weight/spacing distinction"))

    code = semantic_styles.get("Code") or {}
    diagram = semantic_styles.get("ASCII Diagram") or {}
    for name, record in (("Code", code), ("ASCII Diagram", diagram)):
        if record and body.get("size_pt") and record.get("size_pt") and record["size_pt"] >= body["size_pt"] * 0.95:
            findings.append(Finding("CODE_BODY_INDISTINGUISHABLE", f"{name} size is too close to body", recommendation="use a compact monospace size and block spacing"))
        if record and body.get("font") and record.get("font") == body.get("font"):
            findings.append(Finding("CODE_BODY_INDISTINGUISHABLE", f"{name} uses the body font", recommendation="use a monospace semantic style"))
    if diagram and code and diagram.get("font") != code.get("font"):
        findings.append(Finding("ASCII_FONT_MISMATCH", "ASCII Diagram and Code do not share the configured monospace family", blocking=False, recommendation="use a stable monospace family for whitespace-sensitive blocks"))

    toc = {name: semantic_styles.get(name) or {} for name in ("TOC 1", "TOC 2", "TOC 3")}
    if all(toc[name].get("size_pt") is not None for name in toc):
        if not toc["TOC 1"]["size_pt"] > toc["TOC 2"]["size_pt"] > toc["TOC 3"]["size_pt"]:
            findings.append(Finding("TOC_HIERARCHY_INSUFFICIENT", "TOC 1/2/3 sizes do not descend", recommendation="make TOC levels visibly distinct"))
        if not toc["TOC 1"]["left_indent_cm"] < toc["TOC 2"]["left_indent_cm"] < toc["TOC 3"]["left_indent_cm"]:
            findings.append(Finding("TOC_HIERARCHY_INSUFFICIENT", "TOC 1/2/3 indents do not increase", recommendation="indent deeper TOC levels consistently"))

    formatting = _direct_formatting(document)
    warning_ratio = float(_value(profile, "direct_formatting_warning_ratio", 0.35, "visual"))
    fail_ratio = float(_value(profile, "direct_formatting_fail_ratio", 0.75, "visual"))
    if max(formatting["paragraph_ratio"], formatting["run_ratio"]) > fail_ratio:
        findings.append(Finding("DIRECT_FORMATTING_EXCESSIVE", f"direct formatting ratio is {formatting}", recommendation="move repeatable font/spacing/indent decisions into named styles"))
    elif max(formatting["paragraph_ratio"], formatting["run_ratio"]) > warning_ratio:
        findings.append(Finding("DIRECT_FORMATTING_EXCESSIVE", f"direct formatting ratio is {formatting}", blocking=False, recommendation="reduce repeatable direct formatting through semantic styles"))

    fonts = {
        "body": body.get("font"),
        "cjk": _eastasia_font_name(document.styles["Normal"]),
        "code": code.get("font"),
        "ascii": diagram.get("font"),
    }
    font_availability = {name: _font_available(font) for name, font in fonts.items()}
    for name, available in font_availability.items():
        if available is False:
            findings.append(Finding("FONT_UNAVAILABLE", f"{name} font {fonts[name]!r} is not available to fc-match", blocking=False, recommendation="install or replace the profile font without collapsing CJK, Latin, and monospace roles"))

    pdf_report = _pdf_signals(pdf_path) if pdf_path and pdf_path.exists() and shutil.which("pdfinfo") and shutil.which("pdftotext") else None
    if pdf_report and pdf_report["missing_glyph_pages"]:
        findings.append(Finding("PDF_GLYPH_CORRUPTION", f"replacement glyph detected on pages {pdf_report['missing_glyph_pages']}", recommendation="repair font fallback and rerender"))
    if pdf_report and pdf_report["page_count"] and pdf_report["character_density"]["min"] < 180:
        findings.append(Finding("PAGE_RHYTHM_SPARSE_PAGE", f"sparsest pages {pdf_report['character_density']['sparsest_pages']} have very low text density", blocking=False, recommendation="review page breaks and final-page balance; do not add filler content"))

    blocking = [item for item in findings if item.blocking]
    status = "INVALID" if blocking or (strict and findings) else ("VALID_WITH_WARNINGS" if findings else "VALID")
    return {
        "status": status,
        "docx": str(docx_path),
        "profile": str(profile_path) if profile_path else None,
        "styles": {"Normal": body, **heading_styles, **semantic_styles},
        "font_availability": font_availability,
        "direct_formatting": formatting,
        "pdf_page_rhythm": pdf_report,
        "visual_review_required": True,
        "findings": [asdict(item) for item in findings],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--docx", required=True, type=Path)
    parser.add_argument("--profile", type=Path)
    parser.add_argument("--pdf", type=Path)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    report = validate(args.docx, args.profile, args.pdf, args.strict)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("Publication Visual Structure Report")
        for finding in report["findings"]:
            marker = "BLOCKING" if finding["blocking"] else "WARNING"
            print(f"[{marker}] {finding['code']}: {finding['message']}")
        print(f"Status: {report['status']}")
        print("Human visual review required: YES")
    return 1 if report["status"] == "INVALID" else 0


if __name__ == "__main__":
    raise SystemExit(main())
