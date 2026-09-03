# conformance-specification

`conformance-specification` v0.1.0 converts normative Engineering Specification
obligations and approved Machine Contract projections into observable evidence and
deterministic conformance verdicts.

It is deliberately distinct from unit-test authoring, implementation test planning,
QA checklists, and code coverage. The source of every obligation remains normative
specification semantics.

## Layout

- `SKILL.md`: role, workflow, boundaries, and routing.
- `references/`: conformance-specific methods.
- `examples/`: generic examples across structure, lifecycle, profiles, and interoperability.
- `scripts/validate_skill.py`: package, reference, version, and manifest validation.
- `MANIFEST.sha256.json`: tracked file integrity manifest.

## Validation

```bash
python3 scripts/validate_skill.py conformance-specification
python3 /home/htc/.codex/skills/.system/skill-creator/scripts/quick_validate.py conformance-specification
```

The validator checks the Skill package, not the semantic correctness of a project's
generated Conformance Specification.
