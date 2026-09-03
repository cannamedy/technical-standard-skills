# Invariant Modeling

Use an invariant when a requirement must remain true across values, messages,
transitions, time, or external state and a schema would either be incomplete or
misleading.

## Invariant record

Each invariant should carry:

```text
id
source_requirement
engineering_spec_anchor
statement
scope
evaluation_point
machine_checkable
validator_role
failure_semantics
```

The field names are a recommended evidence shape, not a universal artifact schema.
Keep the statement close to the source wording and preserve normative strength.

## Suitable cases

Use invariants for stable identity, uniqueness across a registry, monotonicity,
cross-message relationships, ownership, freshness, temporal ordering, and conditions
requiring external context. Link related state transitions and serialization rules
instead of duplicating their definitions.

If deterministic checking is impossible or unsafe, mark the disposition
`CONFORMANCE_ONLY` or `NON_MACHINE_ENFORCEABLE` and state the evidence needed. If the
source does not define the evaluation point or failure semantics for a load-bearing
rule, use `OPEN_SPEC_ISSUE`.

An invariant is not permission to invent a stronger implementation policy. “Must be
unique within a request” does not imply uniqueness across the system; “stable during
the lifetime” does not imply immutability before creation or after deletion.
