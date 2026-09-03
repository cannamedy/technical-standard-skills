#!/usr/bin/env python3
"""Validate the repository contract for conformance-specification."""

import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md",
    "MANIFEST.sha256.json",
    "agents/openai.yaml",
    "references/normative-obligations.md",
    "references/scenario-modeling.md",
    "references/evidence-and-verdicts.md",
    "references/profile-applicability.md",
    "references/coverage-closure.md",
    "references/interop-conformance.md",
    "references/lifecycle-temporal.md",
    "references/review-checklist.md",
    "examples/conformance-examples.md",
]


def main() -> int:
    errors = []
    skill_path = ROOT / "SKILL.md"
    text = skill_path.read_text(encoding="utf-8") if skill_path.exists() else ""
    if not skill_path.exists():
        errors.append("Missing SKILL.md")
    else:
        match = re.match(r"^---\n(.*?)\n---\n", text, flags=re.S)
        if not match:
            errors.append("Missing YAML frontmatter")
        else:
            front = match.group(1)
            if not re.search(r"^name:\s*conformance-specification\s*$", front, re.M):
                errors.append("Wrong skill name")
            if not re.search(r'^  version:\s*["\']0\.1\.0["\']\s*$', front, re.M):
                errors.append("Wrong version; expected 0.1.0")
            if "description:" not in front:
                errors.append("Missing description")

    for rel in REQUIRED:
        if not (ROOT / rel).exists():
            errors.append(f"Missing {rel}")

    for link in re.findall(r"\]\(([^)#]+)(?:#[^)]+)?\)", text):
        if not link.startswith(("http://", "https://", "#")) and not (ROOT / link).resolve().exists():
            errors.append(f"Broken relative reference: {link}")

    normalized = re.sub(r"\s+", " ", text).lower()
    for phrase in (
        "authoritative inputs",
        "obligation analysis",
        "conformance obligation model",
        "scenario semantics",
        "machine contract integration",
        "evidence and deterministic verdicts",
        "profiles, applicability, and capability claims",
        "coverage and change impact",
        "independent review",
        "cwo artifact adapter",
        "open_spec_issue",
        "unmapped must = 0",
    ):
        if phrase not in normalized:
            errors.append(f"Missing core rule: {phrase}")

    readme = ROOT / "README.md"
    if readme.exists() and "v0.1.0" not in readme.read_text(encoding="utf-8"):
        errors.append("README does not declare version 0.1.0")

    manifest_path = ROOT / "MANIFEST.sha256.json"
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid manifest JSON: {exc}")
            manifest = {}
        if not isinstance(manifest, dict):
            errors.append("Manifest must be a JSON object")
            manifest = {}
        actual_files = {
            path.relative_to(ROOT).as_posix()
            for path in ROOT.rglob("*")
            if path.is_file()
            and path.name != "MANIFEST.sha256.json"
            and "__pycache__" not in path.parts
        }
        if set(manifest) != actual_files:
            errors.append("Manifest file set does not match Skill files")
        for rel, expected_hash in manifest.items():
            path = ROOT / rel
            if path.exists() and path.is_file():
                actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
                if actual_hash != expected_hash:
                    errors.append(f"Manifest hash mismatch: {rel}")

    if errors:
        print("INVALID")
        for error in errors:
            print(f"- {error}")
        return 1
    print("VALID")
    print(ROOT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
