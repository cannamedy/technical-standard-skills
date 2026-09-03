# Lifecycle and Error Realization

Use this reference for externally normative state and error behavior.

## Lifecycle dimensions

Record, when applicable:

```text
state_owner
transition_authority
transition_execution_point
invalid_transition_handling
concurrency_semantics
recovery_owner
terminal_cleanup
persistence_reconstruction
```

Internal states may support execution, but mark them `INTERNAL_ONLY` and ensure they
do not alter the normative state machine.

## Error translation dimensions

For each important failure, record:

```text
origin
category
translation_boundary
public_exposure
logging_or_evidence
recovery_owner
```

Keep internal exceptions, domain errors, Machine Contract validation errors, public
interface errors, transport failures, and infrastructure failures distinct unless
the specification explicitly defines a translation. Do not collapse all failures
into a convenient generic error.
