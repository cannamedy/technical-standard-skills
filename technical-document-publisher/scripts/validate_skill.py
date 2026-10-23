#!/usr/bin/env python3
from pathlib import Path
import json, re, sys

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
    "references/release-manifest.md",
    "references/human-readability-gate.md",
    "references/pais-profile-notes.md",
    "examples/activation-examples.md",
    "scripts/validate_publication_structure.py",
    "scripts/validate_publication_visual_structure.py",
    "scripts/validate_perceptual_publication.py",
    "scripts/validate_before_after_review.py",
    "scripts/validate_release_manifest.py",
    "tests/test_validator.py",
    "profiles/index.json",
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
        if 'version: "0.9.0"' not in front:
            errors.append("Wrong version")

for rel in required:
    if not (root / rel).exists():
        errors.append(f"Missing {rel}")

registry_path = root / "profiles/index.json"
if registry_path.exists():
    try:
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        profiles = registry["profiles"]
        numbers = [entry["number"] for entry in profiles]
        ids = [entry["id"] for entry in profiles]
        if numbers != [f"{i:02d}" for i in range(1, len(profiles) + 1)]:
            errors.append("Profiles must use consecutive two-digit numbers starting at 01")
        if len(ids) != len(set(ids)) or registry["default"] not in numbers:
            errors.append("Profile IDs must be unique and the default must be registered")
        for entry in profiles:
            for key, filename in (("definition", "profile.md"), ("config", "profile.yaml")):
                expected = f"{entry['number']}/{filename}"
                if entry[key] != expected or not (root / "profiles" / expected).is_file():
                    errors.append(f"Missing or invalid profile {key}: {expected}")
            config = root / "profiles" / entry["number"] / "profile.yaml"
            if config.is_file():
                config_text = config.read_text(encoding="utf-8")
                if not re.search(rf'^  number: [\"\']{re.escape(entry["number"])}[\"\']$', config_text, re.M):
                    errors.append(f"Profile number mismatch: {entry['number']}")
                if not re.search(rf'^  id: {re.escape(entry["id"])}$', config_text, re.M):
                    errors.append(f"Profile ID mismatch: {entry['id']}")
    except (ValueError, KeyError, TypeError) as exc:
        errors.append(f"Invalid profile registry: {exc}")

text = skill.read_text(encoding="utf-8") if skill.exists() else ""
for phrase in [
    "publication-orchestration skill",
    "Markdown is the content Source of Truth",
    "No content mutation during publication",
    "Installed `doc` skill is the DOCX engine",
    "Content fidelity",
    "Visual QA",
    "structural-fidelity",
    "TOC",
    "FINAL RELEASE MODE",
    "Source Readiness",
    "HUMAN READABILITY GATE",
    "Reader-first Architecture Writing",
    "Technical Whitepaper Profile",
    "Visual Hierarchy",
    "Page Rhythm",
    "Typography",
    "Font Fallback",
    "Style-first Publication Design",
    "technical-whitepaper",
    "Perceptual Hierarchy",
    "Visual Role Identity",
    "Blind Before/After Review",
    "VISUAL_MONOTONY_WARNING",
    "CROSS_RENDERER_NOT_VERIFIED",
    "PERCEPTUAL_HIERARCHY_AMBIGUOUS",
    "DIRECT_FORMATTING_EXCESSIVE",
    "assessment-question-designer",
    "publication-manifest.json",
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
