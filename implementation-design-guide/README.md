# implementation-design-guide

`implementation-design-guide` v0.1.0 turns approved normative artifacts into an
internal Reference Implementation Design. It makes component responsibility,
data/state ownership, lifecycle realization, evidence hooks, failure behavior, and
Planner readiness explicit without changing the external specification.

It is deliberately distinct from Engineering Specification, Machine Contract,
Conformance Specification, Implementation Plan, and Coding.

## Layout

- `SKILL.md`: role, workflow, boundaries, and handoff gate.
- `references/`: implementation-design-specific methods.
- `examples/`: generic design examples.
- `scripts/validate_skill.py`: package, reference, version, and manifest validation.
- `MANIFEST.sha256.json`: tracked file integrity manifest.

## Validation

```bash
python3 scripts/validate_skill.py implementation-design-guide
python3 /home/htc/.codex/skills/.system/skill-creator/scripts/quick_validate.py implementation-design-guide
```

The validator checks the Skill package, not the correctness of a project's generated
Implementation Design.
