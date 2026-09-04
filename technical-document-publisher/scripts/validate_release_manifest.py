#!/usr/bin/env python3
"""Validate the required safety fields of a publication-manifest.json."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

READY = "PUBLICATION CANDIDATE READY FOR HUMAN RELEASE REVIEW"
BLOCKED = {"PUBLICATION BLOCKED", "BLOCKED_NEEDS_HUMAN_DECISION"}
READY_GATE_STATUSES = {"PASS", "SOURCE_READY", "HUMAN_READABILITY_PASS", "HUMAN_READABILITY_REVIEW", "NOT_APPLICABLE", "VALID_WITH_WARNINGS", "PASS_WITH_WARNINGS"}
REQUIRED = (
    ("schema_version",), ("mode",), ("status",),
    ("source", "path"), ("source", "hash_before_repair"), ("source", "hash_frozen"),
    ("source", "modifications"), ("skills",), ("inputs",), ("artifacts",),
    ("artifacts", "docx_path"), ("artifacts", "docx_hash"),
    ("artifacts", "pdf_path"), ("artifacts", "pdf_hash"), ("artifacts", "page_count"),
    ("gates", "source_readiness"), ("gates", "human_readability"), ("gates", "content_fidelity"),
    ("gates", "structural_fidelity"), ("gates", "visual_hierarchy"),
    ("gates", "typography"), ("gates", "page_rhythm"), ("gates", "visual_fidelity"),
    ("normative_keyword_delta",), ("iterations",),
)


def _get(data: dict, path: tuple[str, ...]):
    value = data
    for key in path:
        if not isinstance(value, dict) or key not in value:
            return None
        value = value[key]
    return value


def validate(data: object) -> dict:
    errors: list[str] = []
    if not isinstance(data, dict):
        return {"status": "INVALID", "errors": ["manifest must be an object"]}
    for path in REQUIRED:
        value = _get(data, path)
        if value is None or value == "":
            errors.append("missing " + ".".join(path))
    status = data.get("status")
    gates = data.get("gates", {})
    gate_statuses = [value.get("status") for value in gates.values() if isinstance(value, dict)]
    if status == READY and any(gate not in READY_GATE_STATUSES for gate in gate_statuses):
        errors.append("ready status cannot contain a non-passing gate")
    if status == READY and not isinstance(gates.get("visual_fidelity", {}).get("page_level_qa"), str):
        errors.append("ready status requires page-level visual QA record")
    if status not in {READY, *BLOCKED}:
        errors.append("status must be a release candidate or blocked state")
    return {"status": "VALID" if not errors else "INVALID", "errors": errors}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args(argv)
    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"INVALID: {exc}")
        return 1
    result = validate(data)
    print(result["status"])
    for error in result["errors"]:
        print(f"- {error}")
    return 0 if result["status"] == "VALID" else 1


if __name__ == "__main__":
    raise SystemExit(main())
