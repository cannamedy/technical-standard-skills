#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
EXPECTED_NAME = "contract-driven-coding"
EXPECTED_VERSION = "0.1.1"
REQUIRED_FILES = [
    "references/execution-tracker.md",
    "references/pre-task-check.md",
    "references/tdd-workflow.md",
    "references/spec-compliance-review.md",
    "references/final-verification.md",
    "references/execution-modes.md",
]
REQUIRED_SECTIONS = [
    "Binding Authority",
    "Pre-task Re-read",
    "Bounded Implementation Context",
    "Persistent Execution Tracker",
    "Test and Verification Workflow",
    "Implementation Scope Discipline",
    "Contract Mutation Prohibition",
    "Completion Reviews",
    "Worktree and Execution Modes",
    "Final Verification",
    "Disposition Promotion Rule",
]
FORBIDDEN_CORE_TOKENS = (
    "Claude",
    "Codex",
    "Gemini",
    "TaskCreate",
    "EnterPlanMode",
    "ExitPlanMode",
)


def main() -> int:
    errors = []
    text = ""
    if not SKILL.exists():
        errors.append("Missing SKILL.md")
    else:
        text = SKILL.read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n", text, flags=re.S)
        if not match:
            errors.append("Missing YAML frontmatter")
        else:
            front = match.group(1)
            if not re.search(r"^name:\s*" + re.escape(EXPECTED_NAME) + r"\s*$", front, re.M):
                errors.append(f"Wrong skill name; expected {EXPECTED_NAME}")
            if not re.search(r'^  version:\s*["\']' + re.escape(EXPECTED_VERSION) + r'["\']\s*$', front, re.M):
                errors.append(f"Wrong version; expected {EXPECTED_VERSION}")
            if "description:" not in front:
                errors.append("Missing description")

    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            errors.append(f"Missing {rel}")

    for section in REQUIRED_SECTIONS:
        if f"## {section}" not in text:
            errors.append(f"Missing core section: {section}")

    for marker, label in [
        ("`IMPLEMENTED` from the Planning stage", "planning IMPLEMENTED meaning"),
        ("MUST NOT be promoted automatically to `VERIFIED`", "promotion prohibition"),
        ("reread the Requirement / Section Anchor", "authoritative reread before promotion"),
        ("inspect the conformance landing and evidence", "conformance evidence inspection"),
    ]:
        if marker not in text:
            errors.append(f"Missing promotion rule: {label}")

    for token in FORBIDDEN_CORE_TOKENS:
        if token.lower() in text.lower():
            errors.append(f"Core SKILL.md contains platform-specific token: {token}")

    for link in re.findall(r"\]\(([^)#]+)(?:#[^)]+)?\)", text):
        if not link.startswith(("http://", "https://", "#")) and not (ROOT / link).exists():
            errors.append(f"Broken relative reference: {link}")

    if errors:
        print("INVALID")
        for error in errors:
            print(f"- {error}")
        return 1

    print("VALID")
    print(ROOT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
