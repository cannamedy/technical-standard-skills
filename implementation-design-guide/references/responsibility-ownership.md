# Responsibility Ownership

Use this reference to turn required behavior into explicit internal ownership.

## Responsibility record

```text
responsibility_id
component_or_module
responsibility
owned_state
owned_invariants
inputs
outputs
dependencies
forbidden_responsibilities
failure_owner
visibility
source_refs
```

Assign one final owner for each required fact or responsibility. Participants may
validate, call, or observe it, but a second component must not silently become an
alternate authority. Mark delegated work and the boundary at which ownership returns.

## Ownership audit

Look for duplicated state, multiple Manifest/schema validators, competing lifecycle
managers, ambiguous mutation rights, and recovery without an owner. A component may
have several related duties when that is the smallest coherent boundary; do not add
layers merely to make the table look symmetrical.
