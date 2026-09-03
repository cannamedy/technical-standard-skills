# machine-contract-spec

`machine-contract-spec` v0.1.0 projects an approved Engineering Specification into
a machine-verifiable Machine Contract. It supports mixed representations—schemas,
state machines, invariants, serialization rules, error contracts, and traceability—
without treating JSON Schema or current implementation behavior as the whole
contract.

The Skill is intentionally project-neutral. Its general normative and contract
discipline is reused from `engineering-contract-spec`; its own references cover
machine representability, projection choices, coverage closure, compatibility, and
review.

## Layout

- `SKILL.md`: routing, boundaries, and operating workflow.
- `references/`: projection-specific guidance.
- `examples/`: small generic projection examples.
- `scripts/validate_skill.py`: repository-style structure and cross-reference checks.
- `MANIFEST.sha256.json`: tracked file integrity manifest.

## Validation

```bash
python3 scripts/validate_skill.py machine-contract-spec
python3 /home/htc/.codex/skills/.system/skill-creator/scripts/quick_validate.py machine-contract-spec
```

The validator checks the Skill contract and its references; it does not validate a
project's generated Machine Contract content.
