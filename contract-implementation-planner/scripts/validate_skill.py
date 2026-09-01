#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
EXPECTED_NAME = "contract-implementation-planner"
EXPECTED_VERSION = "0.2.0"
REQUIRED_FILES = [
    "references/task-template.md",
    "references/dependency-planning.md",
    "references/vertical-slicing.md",
    "references/plan-gate.md",
    "references/frozen-source-integrity.md",
    "references/requirement-disposition.md",
    "references/task-context-boundary.md",
]
REQUIRED_RULES = [
    ("Responsibility Boundary", "Responsibility boundary"),
    ("Inputs", "Inputs"),
    ("Outputs", "Outputs"),
    ("Planning Pipeline", "Planning pipeline"),
    ("Atomic Task Contract", "Atomic task contract"),
    ("Execution Modes", "Execution modes"),
    ("Planner Guardrails", "Planner guardrails"),
    ("Traceability and Final Gate", "Traceability and final gate"),
    ("Frozen Source Integrity Gate", "Frozen source integrity"),
    ("explicit disposition", "Requirement disposition completeness"),
    ("Repository Reality Classification", "Repository reality classification"),
    ("Declared Gap Reconciliation", "Declared gap reconciliation"),
    ("Architecture Constraints", "Task architecture constraints"),
    ("Conformance Landing", "Task conformance landing"),
    ("Task Context Boundary Rule", "bounded Task context"),
    ("Deferred Scope Containment", "Deferred scope guard"),
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

    for marker, label in REQUIRED_RULES:
        if marker not in text:
            errors.append(f"Missing core rule: {label}")

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
