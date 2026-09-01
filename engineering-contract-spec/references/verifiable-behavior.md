# Verifiable Behavior

An observable behavior should connect four things:

```text
Condition / Trigger
        ↓
Expected Behavior
        ↓
Failure / Rejection Behavior
        ↓
Verification Method
```

`Given / When / Then` can express this connection, but it is not mandatory for every requirement.

## Verification classes

- **Runtime-testable**: exercise a live behavior and observe the result.
- **Schema-testable**: validate structure, type, enum, or invariant constraints.
- **Static-conformance-testable**: inspect a deterministic artifact or rule without running the full system.
- **Integration-testable**: verify behavior across a defined boundary or component set.
- **Safety-testable**: verify veto, fail-safe, stale-state, or revalidation behavior.
- **Review-only**: human judgment is required; document why automation is not sufficient.

Do not create a scenario merely to satisfy a checklist. A schema invariant can be verified by schema
validation, and a static namespace rule can be verified by a conformance check.
