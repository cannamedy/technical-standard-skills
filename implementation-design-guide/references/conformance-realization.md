# Conformance Realization

Use this reference to ensure approved Conformance obligations have an observable
implementation landing point.

## Realization record

```text
conformance_id
observable_runtime_surface
design_component
evidence_hook
implementation_support
evidence_boundary
source_refs
```

Map the obligation to a public response, state trace, event sequence, protocol
trace, serialized bytes, hash result, structured error, or other approved evidence
surface. Do not write test code or select a test framework here.

If an executable obligation cannot be observed or its evidence cannot be captured
without changing semantics, report `DESIGN_CONFORMANCE_GAP`. Do not defer the missing
architecture to the Planner. Label manual or external assurance requirements rather
than pretending they are runtime evidence.
