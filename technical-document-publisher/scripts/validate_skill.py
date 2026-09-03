#!/usr/bin/env python3
from pathlib import Path
import re, sys

root = Path(__file__).resolve().parents[1]
skill = root / "SKILL.md"
required = [
    "README.md",
    "references/source-of-truth.md",
    "references/content-fidelity.md",
    "references/publication-profile.md",
    "references/publication-workflow.md",
    "references/visual-qa.md",
    "references/structural-fidelity.md",
    "references/pais-profile-notes.md",
    "examples/activation-examples.md",
    "scripts/validate_publication_structure.py",
    "tests/test_validator.py",
]

errors = []
if not skill.exists():
    errors.append("Missing SKILL.md")
else:
    text = skill.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, flags=re.S)
    if not m:
        errors.append("Missing YAML frontmatter")
    else:
        front = m.group(1)
        if not re.search(r"^name:\s*technical-document-publisher\s*$", front, re.M):
            errors.append("Wrong skill name")
        if 'version: "0.4.0"' not in front:
            errors.append("Wrong version")

for rel in required:
    if not (root / rel).exists():
        errors.append(f"Missing {rel}")

text = skill.read_text(encoding="utf-8") if skill.exists() else ""
for phrase in [
    "thin publication-orchestration skill",
    "Markdown is the content Source of Truth",
    "No content mutation during publication",
    "Installed `doc` skill is the DOCX engine",
    "Content fidelity",
    "Visual QA",
    "structural-fidelity",
    "TOC",
]:
    if phrase.lower() not in text.lower():
        errors.append(f"Missing core rule: {phrase}")

if errors:
    print("INVALID")
    for e in errors:
        print("-", e)
    raise SystemExit(1)

print("VALID")
print(root)
