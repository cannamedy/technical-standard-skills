# Failure and Recovery

Use this reference for failure-driven design of critical components. Apply only the
dimensions relevant to the stated scope.

For each selected failure mode, answer:

```text
what fails?
who detects it?
who owns recovery?
what state remains?
what observable behavior results?
```

Consider validation failure, dependency failure, interrupted lifecycle, partial side
effect, stale state, restart/recovery, and corrupted persisted state when applicable.
Define transaction or compensation boundaries only when required by the behavior or
project constraints. Do not invent a recovery promise merely because a component has
an error path.

If recovery cannot preserve the approved external semantics, mark the design issue
and identify the affected Requirement or Conformance obligation.
