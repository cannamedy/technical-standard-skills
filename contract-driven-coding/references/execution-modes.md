# Execution Modes

## Gated

`gated` is the default. Obtain human approval before each Task group or milestone. This preserves a
review point between approved planning and code changes.

## Autonomous

`autonomous` permits continuous execution after the Contract and overall Plan are approved. It does
not authorize new architecture decisions, Contract changes, destructive or irreversible actions,
security-sensitive actions, external side effects, merge, push, publish, or release.

In either mode, stop when the next action would require guessing. Record the stop reason and tracker
status so the work can resume without relying on Agent memory.
