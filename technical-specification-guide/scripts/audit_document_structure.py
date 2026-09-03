#!/usr/bin/env python3
"""Audit Markdown structure before a technical document is frozen for publication."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

HEADING_RE = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*$")
FENCE_RE = re.compile(r"^[ \t]*(`{3,}|~{3,})")
NORMATIVE = ("MUST", "SHOULD", "MAY")
PSEUDO_LABELS = {
    "发生了什么", "示例", "示例 contract / exchange", "为什么需要", "如何理解",
    "上层系统拿它做什么", "failure / boundary", "场景", "选项", "正确答案",
    "为什么正确", "为什么其他选项错误", "本题检验",
}
RUNTIME_STEP_RE = re.compile(r"^(?:runtime\s+step|step|步骤)\s*[a-z0-9一二三四五六七八九十]+", re.I)
VISIBLE_NUMBER_RE = re.compile(r"^(?:第\s*)?(\d{1,4})[.、:)：][ \t]+")


@dataclass
class Finding:
    code: str
    message: str
    severity: str = "blocking"
    requires_reasoning: bool = False
    line: int | None = None


def _canonical(value: str) -> str:
    value = re.sub(r"[`*_]", "", value)
    return re.sub(r"\s+", " ", value.strip()).lower()


def _source_lines(text: str) -> tuple[list[tuple[int, str]], int]:
    outside: list[tuple[int, str]] = []
    code_blocks = 0
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        fence = FENCE_RE.match(lines[index])
        if not fence:
            outside.append((index + 1, lines[index]))
            index += 1
            continue
        marker = fence.group(1)[0]
        code_blocks += 1
        index += 1
        while index < len(lines) and not re.match(rf"^[ \t]*{re.escape(marker)}{{3,}}", lines[index]):
            index += 1
        if index < len(lines):
            index += 1
    return outside, code_blocks


def audit_text(text: str, *, strict: bool = False) -> dict:
    outside, code_blocks = _source_lines(text)
    headings: list[dict] = []
    findings: list[Finding] = []
    for line_no, line in outside:
        match = HEADING_RE.match(line)
        if match:
            headings.append({"level": len(match.group(1)), "text": match.group(2).strip(), "line": line_no})

    for previous, current in zip(headings, headings[1:]):
        if current["level"] > previous["level"] + 1:
            findings.append(Finding(
                "HEADING_HIERARCHY_JUMP",
                f"H{previous['level']} at line {previous['line']} jumps to H{current['level']} at line {current['line']}",
                line=current["line"],
            ))

    previous_numbers: dict[int, int] = {}
    for heading in headings:
        number = VISIBLE_NUMBER_RE.match(heading["text"])
        if number:
            value = int(number.group(1))
            level = heading["level"]
            previous = previous_numbers.get(level)
            if previous is not None and value <= previous:
                findings.append(Finding(
                    "LEGACY_SECTION_NUMBERING_CONFLICT",
                    f"visible H{level} numbering moves from {previous} to {value}; use current-order numbering or stable internal IDs",
                    line=heading["line"],
                ))
            previous_numbers[level] = value
            if value > len(headings) * 2:
                findings.append(Finding(
                    "LEGACY_SECTION_NUMBERING_SUSPECT",
                    f"visible H{level} number {value} is inconsistent with this source outline; review legacy numbering",
                    severity="review", requires_reasoning=True, line=heading["line"],
                ))

        normalized = _canonical(heading["text"])
        if normalized in PSEUDO_LABELS:
            findings.append(Finding(
                "PSEUDO_HEADING_MISUSE",
                f"heading '{heading['text']}' looks like a local label rather than a navigation node",
                severity="review", requires_reasoning=True, line=heading["line"],
            ))

    runtime_steps = [heading for heading in headings if RUNTIME_STEP_RE.match(_canonical(heading["text"]))]
    if len(runtime_steps) >= 4:
        findings.append(Finding(
            "RUNTIME_MICROSTEP_OUTLINE_INFLATION",
            f"{len(runtime_steps)} runtime-step headings detected; review whether internal steps should be lead-ins or lists",
            severity="review", requires_reasoning=True, line=runtime_steps[0]["line"],
        ))

    paragraph_count = sum(1 for _, line in outside if line.strip() and not HEADING_RE.match(line))
    if headings and paragraph_count and len(headings) / paragraph_count > 0.35:
        findings.append(Finding(
            "OUTLINE_DENSITY_REVIEW",
            f"{len(headings)} headings for {paragraph_count} non-heading lines; inspect navigation value rather than applying a fixed threshold",
            severity="review", requires_reasoning=True,
        ))

    lower_text = text.lower()
    assessment_terms = (
        "questions", "quiz", "mcq", "assessment", "architecture questions", "knowledge check",
        "测试题", "选择题", "考题", "练习题",
    )
    normative = {token: len(re.findall(rf"\b{token}\b", text)) for token in NORMATIVE}
    assessment_detected = any(term in lower_text for term in assessment_terms)
    review = [item for item in findings if item.severity == "review"]
    blocking = [item for item in findings if item.severity == "blocking"]
    if strict:
        blocking.extend(review)
    status = "SOURCE_REPAIR_REQUIRED" if blocking or review else "SOURCE_READY"
    return {
        "status": status,
        "source_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "headings": headings,
        "summary": {
            "heading_count": len(headings),
            "heading_levels": {f"H{i}": sum(h["level"] == i for h in headings) for i in range(1, 7)},
            "fenced_code_blocks": code_blocks,
            "assessment_detected": assessment_detected,
            "normative_keywords": normative,
        },
        "findings": [asdict(item) for item in findings],
    }


def audit(path: Path, *, strict: bool = False) -> dict:
    return audit_text(path.read_text(encoding="utf-8"), strict=strict)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--strict", action="store_true", help="treat reasoning-review findings as blocking")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = audit(args.source, strict=args.strict)
    except OSError as exc:
        print(f"SOURCE_BLOCKED: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["status"])
        print(json.dumps(result["summary"], ensure_ascii=False, sort_keys=True))
        for finding in result["findings"]:
            marker = "BLOCKING" if finding["severity"] == "blocking" else "REVIEW"
            print(f"{marker} {finding['code']}: {finding['message']}")
    return 0 if result["status"] == "SOURCE_READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
