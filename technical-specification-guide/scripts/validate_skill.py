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
    "references/deep-architecture-audit.md",
    "references/whitepaper-rationale-quality.md",
    "references/review-checklist.md",
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
        if not re.search(r'^  version:\s*["\']0\.5\.0["\']\s*$', front, re.M):
            errors.append("Wrong version")
        if "description:" not in front:
            errors.append("Missing description")

for rel in required:
    if not (root / rel).exists():
        errors.append(f"Missing {rel}")

text = skill.read_text(encoding="utf-8") if skill.exists() else ""
normalized_text = re.sub(r"\s+", " ", text).lower()
for phrase in [
    "Reader value rule",
    "Golden master preservation mode",
    "No silent architecture invention",
    "Semantic propagation",
    "Preserve normative strength",
    "Publication cleanliness",
    "Conceptual expansion budget",
    "Acceptance review mode",
    "Deep Architecture Audit",
    "Concept Closure",
    "Layer Responsibility",
    "Orthogonal Taxonomy",
    "Responsibility & Guarantee Boundary",
    "Cross-Section Concept Consistency",
    "Architecture Independence",
    "Reader Mental Model Integrity",
    "Human Guide → Engineering Contract Handoff",
    "Finding",
    "Audit Principle",
    "Evidence",
    "Reasoning",
    "Risk",
    "Recommendation",
    "Ownership",
    "as applicable",
    "not a fixed publication template",
    "MUST actively perform Independence and Boundary checks",
    "complete schema",
    "Whitepaper & Rationale Quality",
    "Problem-first Reasoning",
    "Causal Closure",
    "Importance / Necessity / Urgency",
    "Information Density",
    "Empty Claim Detection",
    "Failure-driven Rationale",
    "Normative / Informative Separation",
    "Normative Strength Justification",
    "Alternative Sufficiency",
    "Responsibility Test",
    "Reader-derived Conclusion",
    "Whitepaper ≠ Specification Dump",
    "reasoning obligations, not identical section structures",
    "WP-01..12",
    "not a fixed article template",
]:
    if phrase.lower() not in normalized_text:
        errors.append(f"Missing core rule: {phrase}")

deep_audit = root / "references/deep-architecture-audit.md"
if deep_audit.exists():
    deep_text = deep_audit.read_text(encoding="utf-8")
    for token in ("PAIS", "NodeIdentity", "ESTUN"):
        if token.lower() in deep_text.lower():
            errors.append(f"Deep audit reference contains project-specific token: {token}")

checklist = root / "references/review-checklist.md"
if checklist.exists() and "WP-01..12" not in checklist.read_text(encoding="utf-8"):
    errors.append("Review checklist does not link the WP-01..12 gate")

if errors:
    print("INVALID")
    for e in errors:
        print("-", e)
    sys.exit(1)

print("VALID")
print(root)
