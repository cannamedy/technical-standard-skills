#!/usr/bin/env python3
"""Validate perceptual role separation for technical-whitepaper DOCX/PDF outputs.

The checks are deterministic signals for human review. They do not claim that
style metrics alone prove one-second comprehension or technical taste.
"""

from __future__ import annotations

import argparse
import json
import math
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


def _value(text: str, key: str, default: Any) -> Any:
    match = re.search(rf"^\s+{re.escape(key)}:\s*[\"']?([^\"'\n#]+?)[\"']?\s*$", text, re.MULTILINE)
    if not match:
        return default
    value = match.group(1).strip()
    try:
        return float(value) if "." in value else int(value)
    except ValueError:
        return value


def _pt(value) -> float:
    return round(value.pt, 3) if value is not None else 0.0


def _font(style, east_asia: bool = False) -> str | None:
    rpr = style._element.rPr
    if rpr is None:
        return style.font.name
    fonts = rpr.find(qn("w:rFonts"))
    if fonts is None:
        return style.font.name
    return fonts.get(qn("w:eastAsia" if east_asia else "w:ascii")) or style.font.name


def _record(document: Document, name: str) -> dict[str, Any] | None:
    try:
        style = document.styles[name]
    except KeyError:
        return None
    pf = style.paragraph_format
    ppr = style._element.pPr
    tags = {child.tag for child in ppr} if ppr is not None else set()
    return {
        "name": name,
        "font": _font(style),
        "cjk_font": _font(style, east_asia=True),
        "size_pt": _pt(style.font.size),
        "bold": style.font.bold is True,
        "before_pt": _pt(pf.space_before),
        "after_pt": _pt(pf.space_after),
        "indent_cm": round(pf.left_indent.cm, 3) if pf.left_indent else 0.0,
        "border": qn("w:pBdr") in tags,
        "shading": qn("w:shd") in tags,
        "page_break_before": pf.page_break_before is True,
    }


def _distance(left: dict[str, Any], right: dict[str, Any]) -> float:
    """Return a bounded heuristic distance in [0, 1]."""
    if not left or not right:
        return 0.0
    score = 0.0
    if left["size_pt"] and right["size_pt"]:
        score += min(abs(math.log(left["size_pt"] / right["size_pt"])), 0.35)
    if left["bold"] != right["bold"]:
        score += 0.30
    score += min((abs(left["before_pt"] - right["before_pt"]) + abs(left["after_pt"] - right["after_pt"])) / 30.0, 0.25)
    score += min(abs(left["indent_cm"] - right["indent_cm"]) / 1.5, 0.15)
    if left["border"] != right["border"]:
        score += 0.22
    if left["shading"] != right["shading"]:
        score += 0.10
    if left["page_break_before"] != right["page_break_before"]:
        score += 0.18
    return round(min(score, 1.0), 4)


def _pdf_signal(path: Path | None) -> dict[str, Any] | None:
    if not path or not path.exists() or not shutil.which("pdfinfo") or not shutil.which("pdftotext"):
        return None
    info = subprocess.run(["pdfinfo", str(path)], capture_output=True, text=True, check=False).stdout
    match = re.search(r"^Pages:\s+(\d+)", info, re.MULTILINE)
    pages = int(match.group(1)) if match else 0
    densities: list[int] = []
    for page in range(1, pages + 1):
        text = subprocess.run(["pdftotext", "-f", str(page), "-l", str(page), "-layout", str(path), "-"], capture_output=True, text=True, check=False).stdout
        densities.append(len(re.sub(r"\s+", "", text)))
    longest_run = 0
    current = 0
    for left, right in zip(densities, densities[1:]):
        current = current + 1 if left and abs(left - right) / max(left, right) <= 0.08 else 0
        longest_run = max(longest_run, current + 1)
    return {"page_count": pages, "densities": densities, "longest_similar_density_run": longest_run}


def validate(docx_path: Path, profile_path: Path | None = None, pdf_path: Path | None = None, second_pdf_path: Path | None = None) -> dict[str, Any]:
    document = Document(str(docx_path))
    profile = _profile_text(profile_path)
    role_styles = {
        "Body": "Normal",
        "Chapter": str(_value(profile, "chapter_style", "Heading 2")),
        "Major Section": str(_value(profile, "major_section_style", "Heading 3")),
        "Technical Topic": str(_value(profile, "technical_topic_style", "Heading 4")),
        "Local Label": "Lead-in",
        "Runtime Label": "Runtime Label",
        "Question Label": "Question Label",
    }
    roles = {role: _record(document, name) for role, name in role_styles.items()}
    findings: list[Finding] = []
    for role in ("Chapter", "Major Section", "Technical Topic"):
        if roles[role] is None:
            findings.append(Finding("ROLE_STYLE_MISSING", f"{role} style {role_styles[role]!r} is missing", recommendation="define the selected profile's named heading style"))
    body = roles["Body"] or {}
    topic = roles["Technical Topic"] or {}
    section = roles["Major Section"] or {}
    chapter = roles["Chapter"] or {}
    label = roles["Local Label"] or {}

    thresholds = {
        "topic": float(_value(profile, "minimum_topic_body_distance", 0.45)),
        "label": float(_value(profile, "minimum_local_label_body_distance", 0.38)),
        "chapter_section": float(_value(profile, "minimum_chapter_section_distance", 0.35)),
        "section_topic": float(_value(profile, "minimum_section_topic_distance", 0.32)),
    }
    distances = {
        "chapter_section": _distance(chapter, section),
        "section_topic": _distance(section, topic),
        "topic_body": _distance(topic, body),
        "local_label_body": _distance(label, body),
    }
    if topic and body and distances["topic_body"] < thresholds["topic"]:
        findings.append(Finding("TOPIC_BODY_CONTRAST_TOO_LOW", f"Technical Topic/Body perceptual distance is {distances['topic_body']:.3f}", evidence=str({"topic": topic, "body": body}), recommendation="add stable topic size, spacing, indentation, rule, or shading signals"))
    if label and body and distances["local_label_body"] < thresholds["label"]:
        findings.append(Finding("LOCAL_LABEL_BODY_CONTRAST_TOO_LOW", f"Local Label/Body perceptual distance is {distances['local_label_body']:.3f}", evidence=str({"label": label, "body": body}), recommendation="give local anchors a semantic marker or spacing identity without promoting them to navigation headings"))
    if chapter and section and distances["chapter_section"] < thresholds["chapter_section"]:
        findings.append(Finding("CHAPTER_SECTION_CONTRAST_TOO_LOW", f"Chapter/Major Section perceptual distance is {distances['chapter_section']:.3f}", recommendation="separate chapter opening with bounded whitespace, weight, or page-start policy"))
    if section and topic and distances["section_topic"] < thresholds["section_topic"]:
        findings.append(Finding("SECTION_TOPIC_CONTRAST_TOO_LOW", f"Major Section/Technical Topic perceptual distance is {distances['section_topic']:.3f}", recommendation="make major sections and technical topics distinct in size and rhythm"))

    for left_name, right_name in (("Chapter", "Major Section"), ("Major Section", "Technical Topic"), ("Technical Topic", "Body")):
        left, right = roles[left_name], roles[right_name]
        if left and right and left["size_pt"] == right["size_pt"] and left["bold"] == right["bold"] and left["before_pt"] == right["before_pt"] and left["after_pt"] == right["after_pt"] and left["indent_cm"] == right["indent_cm"] and left["border"] == right["border"] and left["shading"] == right["shading"]:
            findings.append(Finding("HEADING_ROLE_COLLAPSE", f"{left_name} and {right_name} share the same perceptual signature", recommendation="define a stable non-color identity for each role"))
    if any(item.code in {"TOPIC_BODY_CONTRAST_TOO_LOW", "LOCAL_LABEL_BODY_CONTRAST_TOO_LOW", "CHAPTER_SECTION_CONTRAST_TOO_LOW", "SECTION_TOPIC_CONTRAST_TOO_LOW", "HEADING_ROLE_COLLAPSE"} for item in findings):
        findings.append(Finding("PERCEPTUAL_HIERARCHY_AMBIGUOUS", "at least one reading role is too close to its neighboring role", blocking=True, evidence=json.dumps(distances), recommendation="iterate the publication design and repeat blind Before/After review"))

    # Color is intentionally not part of the distance score. If all non-color
    # signals collapse, a color-only hierarchy is a deterministic failure.
    if topic and body and distances["topic_body"] == 0:
        findings.append(Finding("BLACK_WHITE_HIERARCHY_FAIL", "Technical Topic has no non-color distinction from Body", recommendation="use size, weight, spacing, indentation, rule, or shading in addition to color"))

    pdf = _pdf_signal(pdf_path)
    if pdf and pdf["longest_similar_density_run"] >= 10:
        findings.append(Finding("VISUAL_MONOTONY_WARNING", f"near-identical density persists for {pdf['longest_similar_density_run']} consecutive pages", blocking=False, recommendation="review block variety and hierarchy; do not add decorative filler"))
    second = _pdf_signal(second_pdf_path)
    cross_renderer = "PASS" if second else "CROSS_RENDERER_NOT_VERIFIED"
    if not second:
        findings.append(Finding("CROSS_RENDERER_NOT_VERIFIED", "only one renderer was supplied for this publication attempt", blocking=False, recommendation="run a second independent renderer when the environment provides one"))
    elif pdf and second["page_count"] != pdf["page_count"]:
        findings.append(Finding("CROSS_RENDERER_LAYOUT_WARNING", f"renderer page counts differ: {pdf['page_count']} vs {second['page_count']}", blocking=False, recommendation="record the variance and review representative pages"))

    blocking = [item for item in findings if item.blocking]
    status = "INVALID" if blocking else ("VALID_WITH_WARNINGS" if findings else "VALID")
    return {"status": status, "docx": str(docx_path), "profile": str(profile_path) if profile_path else None, "roles": roles, "perceptual_distances": distances, "pdf": pdf, "second_renderer": second, "cross_renderer": cross_renderer, "findings": [asdict(item) for item in findings], "human_review_required": True}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--docx", required=True, type=Path)
    parser.add_argument("--profile", type=Path)
    parser.add_argument("--pdf", type=Path)
    parser.add_argument("--second-pdf", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    report = validate(args.docx, args.profile, args.pdf, args.second_pdf)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for finding in report["findings"]:
            print(f"[{('BLOCKING' if finding['blocking'] else 'WARNING')}] {finding['code']}: {finding['message']}")
        print(f"Status: {report['status']}")
        print("Human perceptual review required: YES")
    return 1 if report["status"] == "INVALID" else 0


if __name__ == "__main__":
    raise SystemExit(main())
