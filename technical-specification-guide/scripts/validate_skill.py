#!/usr/bin/env python3
from pathlib import Path
import re, sys

root = Path(__file__).resolve().parents[1]
skill = root / "SKILL.md"
required = [
    "README.md",
    "references/publication-cleanliness.md",
    "references/narrative-continuity.md",
    "references/concept-budget.md",
    "references/golden-master-preservation.md",
    "references/no-silent-invention.md",
    "references/semantic-propagation.md",
    "references/review-method.md",
    "references/publication-qa.md",
    "references/reasoning-questions.md",
    "references/failure-modes-v0.1.md",
    "examples/activation-examples.md",
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
        if not re.search(r"^name:\s*technical-specification-guide\s*$", front, re.M):
            errors.append("Wrong skill name")
        if 'version: "0.3.0"' not in front:
            errors.append("Wrong version")
        if "description:" not in front:
            errors.append("Missing description")

for rel in required:
    if not (root / rel).exists():
        errors.append(f"Missing {rel}")

text = skill.read_text(encoding="utf-8") if skill.exists() else ""
for phrase in [
    "Reader value rule",
    "Golden master preservation mode",
    "No silent architecture invention",
    "Semantic propagation",
    "Preserve normative strength",
    "Publication cleanliness",
    "Conceptual expansion budget",
    "Acceptance review mode",
]:
    if phrase.lower() not in text.lower():
        errors.append(f"Missing core rule: {phrase}")

if errors:
    print("INVALID")
    for e in errors:
        print("-", e)
    sys.exit(1)

print("VALID")
print(root)
