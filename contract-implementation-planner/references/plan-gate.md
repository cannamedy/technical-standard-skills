# Planner Gate

Planning starts only after the Contract readiness decision is recorded.

## Ready

Use:

`CONTRACT READY FOR IMPLEMENTATION PLANNING`

when canonical terms, anchors, boundaries, claimed state semantics, failures, authority, safety,
conformance landing points, and load-bearing issue status are sufficient for the requested scope.

## Not ready

Use:

`CONTRACT NOT READY FOR IMPLEMENTATION PLANNING`

when a missing or contradictory decision would force a planner or coding Agent to guess. Record the
affected requirements and issue IDs. Continue with unrelated scope only when its independence is
demonstrable.

## Plan approval

The plan should record its `execution_mode` as `gated` or `autonomous`, with `gated` as the default.
Approval of a plan does not approve Contract changes, destructive operations, external side effects,
or publication/release actions.

## Scope-aware working-tree audit

A non-clean working tree is not an unconditional failure. Classify the changes before planning or
compatibility auditing:

- Expected Target Artifacts (the declared plan, Task, traceability, or audit-report outputs) may be
  untracked or modified and do not block the audit by themselves.
- Frozen Authoritative Sources with a modification, conflict, checksum mismatch, or revision
  mismatch fail the Frozen Source Integrity Gate and block affected planning.
- Unexpected unrelated tracked, untracked, generated, source, or merge-conflict changes must be
  checked for contamination of repository reality, file mapping, dependencies, or verification.
  Continue only when the boundary is reliably isolatable and record it; otherwise stop.

Working-tree cleanliness is an audit-isolation signal, not an authority condition.

## Post-patch re-evaluation

Gate status is based on the Current State. After an authorized patch, reread the current artifact,
rerun affected validations, and recompute the Gate. Record the Historical Transition separately.
The historical defect may explain an earlier `REQUIRES MINIMAL PATCH` result, but cannot alone keep
the current Gate blocked. Only remaining defects in the current artifact do that.
