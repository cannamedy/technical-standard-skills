#!/usr/bin/env python3
"""Validate mechanical invariants and quality signals for technical assessment items."""

from __future__ import annotations

import argparse
import json
import math
import re
import statistics
import sys
from pathlib import Path
from typing import Any

LABELS = ("A", "B", "C", "D")
ABSOLUTE_WORDS = re.compile(r"\b(always|never|only|all|none)\b", re.IGNORECASE)
NEGATIVE_STEM = re.compile(r"\b(not|except|least|false|cannot|incorrect)\b", re.IGNORECASE)
ALL_NONE_OPTION = re.compile(r"\b(all|none)\s+of\s+the\s+above\b", re.IGNORECASE)


def _normalized(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip()).lower()


def _text_length(value: str) -> int:
    return len(re.sub(r"\s+", "", value))


def _tokens(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.lower()))


def _add(issues: list[dict[str, str]], code: str, message: str, question_id: str | None = None) -> None:
    entry = {"code": code, "message": message}
    if question_id:
        entry["question_id"] = question_id
    issues.append(entry)


def _labels_for_count(count: int) -> tuple[str, ...]:
    return tuple(chr(ord("A") + index) for index in range(count))


def _answer_labels(raw: Any, allowed_labels: tuple[str, ...]) -> list[str] | None:
    values = raw if isinstance(raw, list) else [raw]
    answer_labels: list[str] = []
    for value in values:
        if isinstance(value, bool):
            return None
        if isinstance(value, int):
            if value not in range(len(allowed_labels)):
                return None
            value = allowed_labels[value]
        if not isinstance(value, str) or value.upper() not in allowed_labels:
            return None
        answer_labels.append(value.upper())
    return answer_labels


def _result(errors: list[dict[str, str]], warnings: list[dict[str, str]], summary: dict[str, Any]) -> dict[str, Any]:
    status = "INVALID" if errors else "VALID_WITH_WARNINGS" if warnings else "VALID"
    return {"status": status, "errors": errors, "warnings": warnings, "summary": summary}


def validate_document(
    document: Any,
    *,
    strict: bool = False,
    source_grounded: bool | None = None,
    release: bool = False,
) -> dict[str, Any]:
    """Return a VALID, VALID_WITH_WARNINGS, or INVALID validation result."""

    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    if not isinstance(document, dict):
        _add(errors, "MALFORMED_SCHEMA", "Top-level document must be a JSON object")
        return _result(errors, warnings, {"questions": 0})
    items = document.get("questions")
    if not isinstance(items, list):
        _add(errors, "MALFORMED_SCHEMA", "Top-level questions must be a list")
        return _result(errors, warnings, {"questions": 0})
    if source_grounded is None:
        source_grounded = document.get("mode") == "source-grounded"
    expected_count = document.get("expected_option_count", 4)
    if not isinstance(expected_count, int) or isinstance(expected_count, bool) or expected_count not in range(2, 27):
        _add(errors, "MALFORMED_SCHEMA", "expected_option_count must be an integer from 2 to 26")
        expected_count = 4
    declared_question_count = document.get("expected_question_count")
    if declared_question_count is not None and (
        not isinstance(declared_question_count, int)
        or isinstance(declared_question_count, bool)
        or declared_question_count < 1
    ):
        _add(errors, "MALFORMED_SCHEMA", "expected_question_count must be a positive integer")

    ids: set[str] = set()
    answers: list[str] = []
    difficulty_distribution: dict[str, int] = {}
    lengths: list[tuple[str, int, int, int]] = []
    distractors_total = 0
    distractors_annotated = 0
    item_difficulties: list[tuple[str, int]] = []

    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            _add(errors, "MALFORMED_SCHEMA", f"Question {index} must be an object")
            continue
        question_id = item.get("id")
        if not isinstance(question_id, str) or not question_id.strip():
            _add(errors, "MALFORMED_SCHEMA", f"Question {index} is missing a non-empty id")
            question_id = f"<question-{index}>"
        elif question_id in ids:
            _add(errors, "DUPLICATE_QUESTION_ID", f"Duplicate question id: {question_id}", question_id)
        ids.add(question_id)

        stem = item.get("stem")
        if not isinstance(stem, str) or not stem.strip():
            _add(errors, "MALFORMED_SCHEMA", "Question stem must be a non-empty string", question_id)
            stem = ""
        if NEGATIVE_STEM.search(stem):
            _add(warnings, "NEGATIVE_STEM", "Stem contains a negative or exception construction; review readability", question_id)

        question_type = item.get("question_type", "MCQ4")
        item_expected_count = 4 if question_type == "MCQ4" else expected_count
        allowed_labels = _labels_for_count(item_expected_count)
        options = item.get("options")
        if not isinstance(options, list):
            _add(errors, "MALFORMED_SCHEMA", "Options must be a list", question_id)
            options = []
        if question_type == "MCQ4" and len(options) != 4:
            _add(errors, "OPTION_COUNT", f"MCQ4 requires exactly four options, found {len(options)}", question_id)
        elif len(options) != item_expected_count:
            _add(errors, "OPTION_COUNT", f"Expected {item_expected_count} options, found {len(options)}", question_id)

        option_map: dict[str, dict[str, Any]] = {}
        option_texts: list[str] = []
        correct_flags: list[str] = []
        for option in options:
            if not isinstance(option, dict):
                _add(errors, "MALFORMED_SCHEMA", "Each option must be an object", question_id)
                continue
            label = option.get("label")
            if not isinstance(label, str) or label.upper() not in allowed_labels:
                _add(errors, "MALFORMED_SCHEMA", f"Option labels must be {', '.join(allowed_labels)}", question_id)
                continue
            label = label.upper()
            if label in option_map:
                _add(errors, "MALFORMED_SCHEMA", f"Duplicate option label: {label}", question_id)
            option_map[label] = option
            option_text = option.get("text")
            if not isinstance(option_text, str) or not option_text.strip():
                _add(errors, "MALFORMED_SCHEMA", f"Option {label} must have non-empty text", question_id)
                option_text = ""
            option_texts.append(option_text)
            if option.get("is_correct") is True:
                correct_flags.append(label)

        normalized_options = [_normalized(text) for text in option_texts]
        if len(normalized_options) != len(set(normalized_options)):
            _add(errors, "DUPLICATE_OPTION", "Options contain duplicate text", question_id)

        raw_answer = item.get("correct_option")
        if raw_answer is None and correct_flags:
            answer_labels = correct_flags
        elif raw_answer is None:
            answer_labels = None
        else:
            answer_labels = _answer_labels(raw_answer, allowed_labels)
            if answer_labels is None:
                _add(errors, "INVALID_ANSWER_POSITION", "correct_option must be A-D or a zero-based option index", question_id)
        allow_multiple = bool(item.get("allow_multiple_correct", False))
        if answer_labels is not None:
            if not allow_multiple and len(answer_labels) != 1:
                _add(errors, "MULTIPLE_CORRECT", "MCQ4 must have exactly one correct option", question_id)
            if any(label not in option_map for label in answer_labels):
                _add(errors, "INVALID_ANSWER_POSITION", "Correct option does not exist in options", question_id)
            if correct_flags and set(correct_flags) != set(answer_labels):
                _add(errors, "CORRECTNESS_MISMATCH", "correct_option disagrees with is_correct metadata", question_id)
            if len(answer_labels) == 1 and not allow_multiple:
                answers.append(answer_labels[0])
        else:
            _add(errors, "MISSING_CORRECT_ANSWER", "Question has no internally declared correct answer", question_id)

        difficulty = item.get("difficulty_level")
        if difficulty is not None:
            if not isinstance(difficulty, int) or isinstance(difficulty, bool) or difficulty not in range(1, 6):
                _add(errors, "MALFORMED_SCHEMA", "difficulty_level must be an integer from 1 to 5", question_id)
            else:
                difficulty_distribution[str(difficulty)] = difficulty_distribution.get(str(difficulty), 0) + 1
                item_difficulties.append((question_id, difficulty))
        elif "difficulty_level" in document:
            _add(warnings, "MISSING_DIFFICULTY", "Item lacks difficulty_level metadata", question_id)

        if source_grounded and not isinstance(item.get("source_evidence"), str):
            _add(errors if strict else warnings, "SOURCE_EVIDENCE_MISSING", "Source-grounded item lacks source_evidence", question_id)
        if document.get("require_explanations") and not isinstance(item.get("rationale"), str):
            _add(warnings, "EXPLANATION_MISSING", "Explanation is required by the document but missing", question_id)
        if item.get("ambiguity_check") in (False, "fail", "FAIL") or item.get("one_best_answer") is False:
            _add(warnings, "AMBIGUOUS_ANSWER", "Metadata indicates that the item may not have one best answer", question_id)

        incorrect_labels = set(option_map) - set(answer_labels or [])
        distractors_total += len(incorrect_labels)
        for label in incorrect_labels:
            misconception = option_map[label].get("misconception")
            if isinstance(misconception, str) and misconception.strip():
                distractors_annotated += 1
            else:
                _add(warnings, "NON_DIAGNOSTIC_DISTRACTOR", f"Distractor {label} lacks misconception metadata", question_id)
            if option_map[label].get("distractor_quality") in {"weak", "silly", "obvious"}:
                _add(warnings, "WEAK_DISTRACTOR_SIGNAL", f"Distractor {label} is marked {option_map[label]['distractor_quality']}", question_id)

        if any(ALL_NONE_OPTION.search(text) for text in option_texts):
            _add(warnings, "ABSOLUTE_OPTION", "Option uses all/none-of-the-above wording", question_id)
        if answer_labels and len(answer_labels) == 1:
            correct_text = option_map.get(answer_labels[0], {}).get("text", "")
            distractor_text = " ".join(option_map[label].get("text", "") for label in incorrect_labels)
            if ABSOLUTE_WORDS.search(distractor_text) and not ABSOLUTE_WORDS.search(correct_text):
                _add(warnings, "ABSOLUTE_WORD_CUE", "Absolute wording appears in distractors but not the correct option", question_id)

        if option_texts and len(option_texts) == len(options):
            item_lengths = [_text_length(text) for text in option_texts]
            correct_length = _text_length(option_map.get(answer_labels[0], {}).get("text", "")) if answer_labels and len(answer_labels) == 1 else 0
            distractor_lengths = [_text_length(option_map[label].get("text", "")) for label in incorrect_labels]
            if min(item_lengths, default=0) and max(item_lengths) > 1.5 * min(item_lengths):
                _add(warnings, "OPTION_LENGTH_IMBALANCE", "Option lengths differ by more than the 1.5 heuristic ratio", question_id)
            if distractor_lengths and correct_length > 1.5 * statistics.median(distractor_lengths):
                _add(warnings, "OPTION_LENGTH_LEAK", "Correct option is much longer than the median distractor", question_id)
            if answer_labels and len(answer_labels) == 1:
                lengths.append((question_id, correct_length, max(item_lengths), min(item_lengths)))
            if len({bool(re.search(r"[.!?]$", text.strip())) for text in option_texts}) > 1:
                _add(warnings, "GRAMMAR_LEAK", "Options use inconsistent terminal punctuation", question_id)
            option_sets = [_tokens(text) for text in option_texts]
            for left in range(len(option_sets)):
                for right in range(left + 1, len(option_sets)):
                    shorter, longer = sorted((normalized_options[left], normalized_options[right]), key=len)
                    union = option_sets[left] | option_sets[right]
                    overlap = len(option_sets[left] & option_sets[right]) / len(union) if union else 0
                    if len(shorter) >= 12 and (shorter in longer or overlap >= 0.8):
                        _add(warnings, "OPTION_OVERLAP", "Options substantially overlap or one subsumes another", question_id)

    if answers:
        distribution_labels = _labels_for_count(expected_count)
        distribution = {label: answers.count(label) for label in distribution_labels}
        if max(distribution.values()) - min(distribution.values()) > 1:
            _add(warnings, "ANSWER_POSITION_BIAS", "Answer position distribution differs by more than one")
        longest_streak = 1
        current_streak = 1
        for previous, current in zip(answers, answers[1:]):
            current_streak = current_streak + 1 if current == previous else 1
            longest_streak = max(longest_streak, current_streak)
        if longest_streak > 2:
            _add(warnings, "ANSWER_STREAK", f"Same-answer streak is {longest_streak}; maximum recommended streak is two")
        if expected_count == 4 and len(answers) >= 8 and len(set(answers[:4])) == 4:
            repeated = (answers[:4] * math.ceil(len(answers) / 4))[: len(answers)]
            if answers == repeated:
                _add(warnings, "ANSWER_PATTERN", "Answer positions repeat a predictable four-position cycle")
        correct_longest = sum(correct_len == maximum for _, correct_len, maximum, _ in lengths)
        if lengths and correct_longest / len(lengths) >= 0.6:
            _add(warnings, "CORRECT_LONGEST_SYSTEMATIC", "Correct options are systematically the longest")
    else:
        distribution = {label: 0 for label in _labels_for_count(expected_count)}
        longest_streak = 0

    if len(item_difficulties) >= 8:
        tail_count = max(1, math.ceil(len(item_difficulties) * 0.25))
        head = [level for _, level in item_difficulties[:-tail_count]]
        tail = [level for _, level in item_difficulties[-tail_count:]]
        if head and statistics.mean(head) - statistics.mean(tail) > 1:
            _add(warnings, "TAIL_QUALITY_DEGRADATION", "Final 25% has materially lower difficulty than earlier items")

    summary = {
        "questions": len(items),
        "release_mode": release,
        "answer_distribution": distribution,
        "longest_streak": longest_streak,
        "option_length_warnings": sum(issue["code"] in {"OPTION_LENGTH_IMBALANCE", "OPTION_LENGTH_LEAK", "CORRECT_LONGEST_SYSTEMATIC"} for issue in warnings),
        "distractor_coverage": {
            "annotated": distractors_annotated,
            "total": distractors_total,
            "ratio": round(distractors_annotated / distractors_total, 3) if distractors_total else 1.0,
        },
        "difficulty_distribution": difficulty_distribution,
    }
    if declared_question_count is not None and declared_question_count != len(items):
        _add(errors, "QUESTION_COUNT", f"Expected {declared_question_count} questions, found {len(items)}")
    if release:
        release_blocking_codes = {
            "ANSWER_POSITION_BIAS", "ANSWER_STREAK", "ANSWER_PATTERN",
            "SOURCE_EVIDENCE_MISSING", "NON_DIAGNOSTIC_DISTRACTOR", "WEAK_DISTRACTOR_SIGNAL",
            "TAIL_QUALITY_DEGRADATION", "AMBIGUOUS_ANSWER",
        }
        promoted = [warning for warning in warnings if warning["code"] in release_blocking_codes]
        errors.extend(promoted)
        warnings = [warning for warning in warnings if warning["code"] not in release_blocking_codes]
    result = _result(errors, warnings, summary)
    result["summary"]["release_blocking_findings"] = len([issue for issue in errors if issue["code"] in {
        "ANSWER_POSITION_BIAS", "ANSWER_STREAK", "ANSWER_PATTERN", "SOURCE_EVIDENCE_MISSING",
        "NON_DIAGNOSTIC_DISTRACTOR", "WEAK_DISTRACTOR_SIGNAL", "TAIL_QUALITY_DEGRADATION",
        "OPTION_LENGTH_IMBALANCE", "OPTION_LENGTH_LEAK", "CORRECT_LONGEST_SYSTEMATIC", "AMBIGUOUS_ANSWER",
    }])
    return result


def _print_result(result: dict[str, Any], as_json: bool = False) -> None:
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    print(result["status"])
    print(json.dumps(result["summary"], ensure_ascii=False, sort_keys=True))
    for issue in result["errors"]:
        suffix = f" [{issue['question_id']}]" if "question_id" in issue else ""
        print(f"ERROR {issue['code']}{suffix}: {issue['message']}")
    for issue in result["warnings"]:
        suffix = f" [{issue['question_id']}]" if "question_id" in issue else ""
        print(f"WARNING {issue['code']}{suffix}: {issue['message']}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate assessment question JSON")
    parser.add_argument("path", type=Path)
    parser.add_argument("--strict", action="store_true", help="Promote missing source evidence to an error")
    parser.add_argument("--source-grounded", action="store_true", help="Treat input as source-grounded")
    parser.add_argument("--release", action="store_true", help="Apply blocking final-release batch gates")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Emit machine-readable JSON")
    args = parser.parse_args(argv)
    try:
        document = json.loads(args.path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        result = _result([{"code": "MALFORMED_INPUT", "message": str(exc)}], [], {"questions": 0})
        _print_result(result, args.as_json)
        return 1
    result = validate_document(document, strict=args.strict, source_grounded=True if args.source_grounded else None, release=args.release)
    _print_result(result, args.as_json)
    return 1 if result["status"] == "INVALID" else 0


if __name__ == "__main__":
    sys.exit(main())
