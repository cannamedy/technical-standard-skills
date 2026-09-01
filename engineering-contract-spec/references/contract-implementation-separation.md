# Contract / Implementation Separation

The contract is authoritative for externally observable behavior, ownership, constraints, failure
semantics, and conformance. It is not a default prescription for internal source layout.

## Belongs in the Contract

- externally visible objects and fields;
- required and forbidden behavior;
- authority and mutability;
- state transitions and failure semantics;
- compatibility and extension rules;
- conformance obligations.

## Belongs in the Planner

- repository file mapping;
- implementation boundaries;
- dependency order;
- vertical slices;
- atomic tasks;
- task-level verification commands.

File paths or implementation names belong in the Contract only when a path or name is itself part of
an external compatibility contract.
