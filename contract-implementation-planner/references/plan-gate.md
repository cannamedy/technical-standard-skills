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
