# Dependency Planning

Build task order from prerequisites and observable behavior. A dependency means the downstream task
cannot be implemented or verified correctly without the upstream result; mere topic similarity is
not a dependency.

For each edge, record:

- upstream task;
- downstream task;
- required artifact or behavior;
- why the edge exists;
- how the downstream task verifies the prerequisite.

Reject circular dependencies. If the cycle represents an unresolved architecture decision, open a
Contract issue instead of breaking the cycle arbitrarily.

The final audit checks that every task is reachable from an approved Contract requirement and that
every current mandatory requirement maps to existing implementation evidence, an implementation
Task, or an explicit `BLOCKED` disposition. A Requirement already supported by evidence does not
need a duplicate Task, but it still needs a verification status later in the workflow.
