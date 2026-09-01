
#!/usr/bin/env python3
from pathlib import Path
import re, sys

root = Path(__file__).resolve().parents[1]
skill_path = root / "SKILL.md"
expected = "engineering-contract-spec"
required = [
    'references/normative-contract.md',
    'references/schema-contract.md',
    'references/state-machine.md',
    'references/safety-contract.md',
    'references/traceability.md',
    'references/review-severity.md',
    'references/contract-implementation-separation.md',
    'references/boundary-contract.md',
    'references/verifiable-behavior.md',
    'references/open-contract-issue.md',
    'references/contract-readiness.md',
    'examples/activation-examples.md',
]

errors = []
if not skill_path.exists():
    errors.append("Missing SKILL.md")
else:
    text = skill_path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, flags=re.S)
    if not m:
        errors.append("Missing YAML frontmatter")
    else:
        front = m.group(1)
        nm = re.search(r"^name:\s*(.+)$", front, flags=re.M)
        if not nm or nm.group(1).strip() != expected:
            errors.append(f"Frontmatter name must be {expected}")
        if "description:" not in front:
            errors.append("Missing description")
        if not re.search(r'^  version:\s*["\']0\.3\.0["\']\s*$', front, flags=re.M):
            errors.append("Wrong version; expected 0.3.0")

for rel in required:
    if not (root / rel).exists():
        errors.append(f"Missing {rel}")

if skill_path.exists():
    text = skill_path.read_text(encoding="utf-8")
    for phrase in [
        "Contract vs Implementation Separation",
        "Concrete Boundary Contracts",
        "Verifiable Behavior and Requirement Classification",
        "Open Contract Issue Protocol",
        "Contract Readiness Gate",
        "Agent-Neutrality",
    ]:
        if phrase not in text:
            errors.append(f"Missing core section: {phrase}")

    for link in re.findall(r'\]\(([^)#]+)(?:#[^)]+)?\)', text):
        if not link.startswith(('http://', 'https://', '#')) and not (root / link).exists():
            errors.append(f"Broken relative reference: {link}")

if errors:
    print("INVALID")
    for e in errors:
        print("-", e)
    sys.exit(1)

print("VALID")
print(root)
