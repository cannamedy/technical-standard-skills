# Machine Contract Realization

Use this reference to map approved Machine Contract objects into implementation
responsibilities without duplicating their normative definitions.

## Realization record

```text
machine_contract_ref
implementing_component
validation_point
state_or_data_owner
failure_propagation
bypass_prevention
evidence_hook
source_refs
```

Cover Schemas, Invariants, State Machines, Serialization Rules, Runtime Validators,
and Error Contracts as applicable. For each, answer which component enforces it,
when enforcement occurs, what state it reads, how failure travels, and how alternate
entry points cannot bypass it.

The design may choose an implementation mechanism, but it must not weaken the
Machine Contract, copy its definitions into a second authority, or add constraints
not supported by the approved inputs.
