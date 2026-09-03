# Component Boundaries

Use this reference to define a proportional component and module architecture.

## Boundary record

```text
component_id
name
visibility
responsibilities
owned_data
public_inputs_outputs
internal_interfaces
dependencies
forbidden_dependencies
failure_boundary
evidence_hooks
source_refs
```

Review dependency direction, circular references, abstraction inversion, responsibility
leakage, hidden coupling, transport/domain coupling, persistence/domain coupling, and
test-only abstractions leaking into runtime. Make the boundary where ownership or
failure handling changes, not where a new folder would be convenient.

Internal interfaces should define relevant inputs, outputs, preconditions,
postconditions, idempotency, ordering, failure behavior, and visibility without
turning implementation details into public standards.
