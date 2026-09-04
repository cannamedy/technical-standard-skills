#!/usr/bin/env python3
"""Validate a neutral A/B before/after publication review record."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED_PAGE_TYPES = {
    "mental_map", "concepts", "object_definitions", "runtime", "principles",
    "boundaries", "questions", "table_heavy", "code_ascii", "final_pages",
}
FORBIDDEN_LABELS = {"GOOD", "BAD", "BETTER", "WORSE"}


def _contains_forbidden(value: object) -> bool:
    if isinstance(value, str):
        return value.upper() in FORBIDDEN_LABELS
    if isinstance(value, dict):
        return any(_contains_forbidden(key) or _contains_forbidden(item) for key, item in value.items())
    if isinstance(value, list):
        return any(_contains_forbidden(item) for item in value)
    return False


def validate(data: object) -> dict:
    errors: list[str] = []
    if not isinstance(data, dict):
        return {"status": "INVALID", "errors": ["review must be an object"]}
    if _contains_forbidden(data):
        errors.append("review must use neutral A/B labels, not evaluative labels")
    if data.get("result") not in {"YES", "NO", "MIXED"}:
        errors.append("result must be YES, NO, or MIXED")
    comparisons = data.get("comparisons")
    if not isinstance(comparisons, list) or len(comparisons) < 10:
        errors.append("at least ten page-type comparisons are required")
        comparisons = []
    seen: set[str] = set()
    for index, item in enumerate(comparisons):
        if not isinstance(item, dict):
            errors.append(f"comparison {index} must be an object")
            continue
        page_type = item.get("page_type")
        if page_type in seen:
            errors.append(f"duplicate page type: {page_type}")
        if isinstance(page_type, str):
            seen.add(page_type)
        if page_type not in REQUIRED_PAGE_TYPES:
            errors.append(f"comparison {index} has unknown page type")
        if item.get("labels") != ["A", "B"]:
            errors.append(f"comparison {index} must expose labels exactly as A/B")
        if item.get("winner") not in {"A", "B", "MIXED"}:
            errors.append(f"comparison {index} winner must be A, B, or MIXED")
        if item.get("candidate_side") not in {"A", "B"}:
            errors.append(f"comparison {index} must record candidate_side as A or B")
        for key in ("a", "b"):
            if not isinstance(item.get(key), str) or not item[key]:
                errors.append(f"comparison {index} missing {key} artifact")
    missing = REQUIRED_PAGE_TYPES - seen
    if missing:
        errors.append("missing page types: " + ", ".join(sorted(missing)))
    if data.get("result") == "YES" and any(item.get("winner") == "MIXED" for item in comparisons if isinstance(item, dict)):
        errors.append("YES result cannot contain MIXED comparison winners")
    return {"status": "VALID" if not errors else "INVALID", "errors": errors}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review", type=Path, required=True)
    parser.add_argument("--json", action="store_true", help="emit JSON result")
    args = parser.parse_args(argv)
    try:
        data = json.loads(args.review.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        result = {"status": "INVALID", "errors": [str(exc)]}
    else:
        result = validate(data)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["status"])
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["status"] == "VALID" else 1


if __name__ == "__main__":
    raise SystemExit(main())
