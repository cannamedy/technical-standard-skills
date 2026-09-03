#!/usr/bin/env python3
"""Audit reader-first architecture signals without pretending to judge prose by regex alone."""

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
ABSTRACT_NOUNS = re.compile(
    r"\b(boundary|surface|semantics|context|governance|capability|framework|contract|profile|runtime)\b",
    re.I,
)
CONTRAST = re.compile(r"不是[^\n。]{0,100}而是|真正的问题不是|本质上不是")
META_EXPLANATION = re.compile(r"这一节|本节|接下来我们|让读者|固定读者|本文将|下面将")
CLOSURE = re.compile(r"这意味着|真正的价值在于|这就是为什么|因此，")
RUNTIME_LABEL = re.compile(r"^(?:发生了什么|示例(?: contract / exchange)?|如何理解(?:这次交换)?|为什么 physical ai 需要它|上层系统拿它做什么|failure / boundary)$", re.I | re.M)


@dataclass
class Finding:
    code: str
    message: str
    severity: str = "review"
    requires_reasoning: bool = True
    line: int | None = None
    evidence: str = ""
    recommendation: str = ""


def _strip_fences(text: str) -> tuple[str, int]:
    output: list[str] = []
    blocks = 0
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        fence = FENCE_RE.match(lines[index])
        if not fence:
            output.append(lines[index])
            index += 1
            continue
        blocks += 1
        marker = fence.group(1)[0]
        output.append("")
        index += 1
        while index < len(lines) and not re.match(rf"^[ \t]*{re.escape(marker)}{{3,}}", lines[index]):
            output.append("")
            index += 1
        if index < len(lines):
            output.append("")
            index += 1
    return "\n".join(output), blocks


def _sentence_lines(text: str) -> list[tuple[int, str]]:
    result: list[tuple[int, str]] = []
    for line_no, line in enumerate(text.splitlines(), 1):
        value = line.strip()
        if value and not value.startswith(("#", "- ", "* ", ">", "```", "|")):
            result.append((line_no, value))
    return result


def _finding(code: str, message: str, *, severity: str = "review", line: int | None = None, evidence: str = "", recommendation: str = "") -> Finding:
    return Finding(code, message, severity=severity, line=line, evidence=evidence, recommendation=recommendation)


def audit_text(text: str) -> dict:
    readable_text, fenced_blocks = _strip_fences(text)
    lines = text.splitlines()
    headings = [(i + 1, len(m.group(1)), m.group(2).strip()) for i, line in enumerate(lines) if (m := HEADING_RE.match(line))]
    findings: list[Finding] = []
    total_lines = max(len(lines), 1)
    entry_limit = min(total_lines, max(10, int(total_lines * 0.15)))
    reader_entry_applicable = total_lines >= 40
    early = "\n".join(lines[:entry_limit])

    entry_checks = {
        "what_is_system": (r"PAIS.{0,80}(标准|接口|契约|standard|contract|system)", "系统身份"),
        "problem": (r"Adapter.{0,80}(不够|不足|问题|gap|missing)|耦合关系|gap left", "既有机制的缺口"),
        "central_object": (r"Physical Node.{0,80}(标准化|根|root|对象|contract)", "中心标准化对象"),
        "consumer_gain": (r"上层.{0,80}(读取|获得|发现|理解|使用)|Consumer.{0,80}(读取|获得|discover)", "消费者获得的变化"),
        "outside_boundary": (r"不负责|不拥有|不承担|MUST NOT.{0,80}(依赖|替代)|outside the boundary|remains outside", "明确的责任边界"),
        "design_spine": (r"Design Spine|阅读骨架|核心设计思想|五条|几件事", "可记忆的设计主线"),
    }
    reader_entry_answers: dict[str, bool] = {}
    for key, (pattern, label) in entry_checks.items():
        present = bool(re.search(pattern, early, re.I | re.S))
        reader_entry_answers[key] = present
        if not present and reader_entry_applicable:
            findings.append(_finding(
                "READER_ENTRY_FAILURE",
                f"first 15% does not make {label} recoverable",
                severity="blocking",
                line=entry_limit,
                evidence=f"searched first {entry_limit} of {total_lines} lines",
                recommendation="state the minimum reader mental model before the large concept model",
            ))

    lower = readable_text.lower()
    has_map = bool(re.search(r"一页理解|one-page mental map|mental map", lower, re.I))
    if not has_map and reader_entry_applicable:
        findings.append(_finding("ONE_PAGE_MENTAL_MAP_MISSING", "no compact mental map is visible before the object model", severity="blocking", recommendation="add one small relationship map or before/after explanation"))
    has_spine = bool(re.search(r"design spine|reader-facing|阅读骨架|核心设计思想", lower, re.I))
    if not has_spine and reader_entry_applicable:
        findings.append(_finding("DESIGN_SPINE_MISSING", "no reader-facing design spine is declared", severity="blocking", recommendation="distill 3–7 ideas without deleting the complete principles"))

    principle_headings = [item for item in headings if re.search(r"principle|原则", item[2], re.I)]
    readable_lines = readable_text.splitlines()
    first_principle_line = next((item[0] for item in principle_headings), total_lines + 1)
    before_principles = "\n".join(readable_lines[: max(first_principle_line - 1, 0)])
    after_principles = "\n".join(readable_lines[max(first_principle_line - 1, 0):])
    spine_terms = ("Discovery", "Manifest", "State", "Parameter", "Action", "Operation", "Capability", "Safety", "Adapter")
    propagated = [term for term in spine_terms if re.search(term, before_principles, re.I) and re.search(term, after_principles, re.I)]
    if principle_headings and len(propagated) < 3 and reader_entry_applicable:
        findings.append(_finding("PRINCIPLE_PROPAGATION_GAP", "principles are concentrated at the end without enough earlier consequences", severity="blocking", evidence=f"shared terms found across sections: {propagated}", recommendation="show each spine idea through a problem, object, runtime consequence, or boundary"))

    concept_start = next((item[0] for item in headings if re.search(r"concept|对象", item[2], re.I)), None)
    if concept_start:
        concept_slice = lines[concept_start - 1 : min(total_lines, concept_start + 160)]
        concept_heading_count = sum(
            1 for line in concept_slice
            if (m := HEADING_RE.match(line)) and len(m.group(2).strip()) <= 45
        )
        if concept_heading_count >= 8 and not re.search(r"问题链|下一个问题|先.*然后|因此.*需要", "\n".join(concept_slice), re.I):
            findings.append(_finding("CONCEPT_GLOSSARY_WALL", "the concept opening reads as a glossary wall", severity="blocking", line=concept_start, recommendation="introduce terms through the engineering question that requires each one"))

    runtime_steps = [item for item in headings if re.search(r"runtime\s+step|步骤\s*[一二三四五六七八九十0-9]", item[2], re.I)]
    repeated_labels = len(RUNTIME_LABEL.findall(readable_text))
    if runtime_steps and not re.search(r"连续.*故事|同一个.*robot|下一个问题|remaining question", lower, re.I):
        findings.append(_finding("RUNTIME_STORY_GAP", "runtime stages are present without a continuous question-to-consequence narrative", severity="blocking", recommendation="connect each stage to the previous unresolved engineering question"))
    if repeated_labels >= 6 or len(runtime_steps) >= 4 and repeated_labels >= 3:
        findings.append(_finding("TEMPLATE_RHYTHM_OVERUSE", f"repeated local runtime labels detected ({repeated_labels})", severity="blocking", recommendation="merge repeated blocks into story prose and retain only labels with navigation value"))

    pattern_counts = {
        "contrast_formula": len(CONTRAST.findall(readable_text)),
        "meta_explanation": len(META_EXPLANATION.findall(readable_text)),
        "rhetorical_closure": len(CLOSURE.findall(readable_text)),
        "abstract_noun_sentences": sum(1 for _, sentence in _sentence_lines(readable_text) if len(ABSTRACT_NOUNS.findall(sentence)) >= 4),
        "empty_emphasis": len(re.findall(r"非常重要|至关重要|核心中的核心|真正意义上|从根本上", readable_text)),
    }
    if pattern_counts["contrast_formula"] > 10:
        findings.append(_finding("ANTI_AI_CONTRAST_OVERUSE", f"contrast formula appears {pattern_counts['contrast_formula']} times", recommendation="retain only contrasts that prevent a real category error"))
    if pattern_counts["meta_explanation"] > 8:
        findings.append(_finding("ANTI_AI_META_EXPLANATION_OVERUSE", f"meta-explanation patterns appear {pattern_counts['meta_explanation']} times", recommendation="replace editing commentary with direct technical statements"))
    if pattern_counts["abstract_noun_sentences"] >= 5:
        findings.append(_finding("ABSTRACT_NOUN_STACKING", f"{pattern_counts['abstract_noun_sentences']} sentences stack four or more abstract nouns", recommendation="name the actor, observed fact, decision, and consequence"))
    if pattern_counts["rhetorical_closure"] > 12:
        findings.append(_finding("REPEATED_RHETORICAL_CLOSURE", f"rhetorical closure appears {pattern_counts['rhetorical_closure']} times", recommendation="stop after evidence or vary the sentence shape"))
    if pattern_counts["empty_emphasis"] > 3:
        findings.append(_finding("EMPTY_EMPHASIS", f"empty emphasis appears {pattern_counts['empty_emphasis']} times", recommendation="attach a mechanism and engineering consequence or remove the emphasis"))

    mixed_lines = [line for line_no, line in _sentence_lines(readable_text) if re.search(r"[\u4e00-\u9fff]", line) and len(re.findall(r"[A-Za-z]{3,}", line)) >= 4]
    if len(mixed_lines) >= 8:
        findings.append(_finding("CHINESE_ENGLISH_FRAGMENTATION", f"{len(mixed_lines)} prose lines mix dense Chinese and English terminology", recommendation="retain canonical object names but translate ordinary relationships into natural Chinese"))

    tail_start = int(total_lines * 0.85)
    tail = lines[tail_start:]
    tail_bullets = sum(1 for line in tail if re.match(r"^\s*(?:[-*+] |\d+[.)] )", line))
    if tail and tail_bullets / max(sum(bool(line.strip()) for line in tail), 1) > 0.55:
        findings.append(_finding("TAIL_QUALITY_REVIEW", "the final 15% is dominated by list material", line=tail_start + 1, recommendation="add transitions and responsibility/consequence prose; retain useful checklists"))

    blocking = [item for item in findings if item.severity == "blocking"]
    review = [item for item in findings if item.severity != "blocking"]
    return {
        "status": "HUMAN_READABILITY_FAIL" if blocking else ("HUMAN_READABILITY_REVIEW" if review else "HUMAN_READABILITY_PASS"),
        "source_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "summary": {
            "lines": total_lines,
            "fenced_code_blocks": fenced_blocks,
            "heading_count": len(headings),
            "reader_entry_limit_line": entry_limit,
            "reader_entry_answers": reader_entry_answers,
            "reader_entry_answered": sum(reader_entry_answers.values()),
            "reader_entry_total": len(reader_entry_answers),
            "principle_heading_count": len(principle_headings),
            "propagated_terms": propagated,
            "pattern_counts": pattern_counts,
            "runtime_stage_count": len(runtime_steps),
            "repeated_template_labels": repeated_labels,
        },
        "findings": [asdict(item) for item in findings],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = audit_text(args.source.read_text(encoding="utf-8"))
    except OSError as exc:
        print(f"HUMAN_READABILITY_FAIL: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["status"])
        print(json.dumps(result["summary"], ensure_ascii=False, sort_keys=True))
        for item in result["findings"]:
            print(f"{item['severity'].upper()} {item['code']}: {item['message']}")
    return 0 if result["status"] != "HUMAN_READABILITY_FAIL" else 1


if __name__ == "__main__":
    raise SystemExit(main())
