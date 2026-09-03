# Conformance Specification Examples

These examples are project-neutral and illustrative. They do not define universal
objects, status codes, timing values, or test-framework conventions.

## A. Structural range

Source: “`revision` MUST be a non-negative integer.”

```text
conformance_id: CONF-REVISION-001
class: VALUE_CONSTRAINT
scenario_kind: POSITIVE + NEGATIVE
stimulus: validate revision = 0 and revision = -1
expected: 0 is accepted; -1 is rejected
evidence_type: SCHEMA_VALIDATION
verdict: exact schema result matches the two expected outcomes
```

No default, maximum, or requiredness is added unless separately specified.

## B. MUST NOT / negative behavior

Source: “A consumer MUST NOT accept an unsigned message.”

```text
conformance_id: CONF-AUTH-001
scenario_kind: NEGATIVE
stimulus: submit an otherwise valid message without the required signature
expected: the message is rejected before the protected operation
forbidden: protected operation is performed
evidence_type: ERROR_RESULT + EVENT_SEQUENCE
```

No transport status or error code is invented.

## C. Lifecycle transition

Source: “After cancellation is accepted, the job MUST transition to `cancelled`.”

```text
conformance_id: CONF-JOB-CANCEL-001
scenario_kind: TRANSITION
precondition: job is cancellable and running
stimulus: request cancellation
expected: cancellation accepted, then observable state is cancelled
evidence_type: STATE_TRACE + EVENT_SEQUENCE
```

No timeout is added unless the source defines one.

## D. Optional capability claim

Source: “The implementation MAY declare feature X. A declaration MUST expose the X
operation and satisfy its response contract.”

```text
conformance_id: CONF-FEATURE-X-001
applicability: CONDITIONAL_IF_CAPABILITY_DECLARED
scenario_kind: POSITIVE + CLAIM_CONFORMANCE
stimulus: inspect declaration, then invoke X
expected: undeclared is NOT_APPLICABLE; declared requires the response contract
evidence_type: API_RESPONSE + STATIC_ANALYSIS
```

Absence of the optional declaration is not a failure.

## E. Interoperability

Source: “A producer and consumer MUST negotiate a mutually supported encoding.”

```text
conformance_id: CONF-NEGOTIATION-001
scenario_kind: INTEROP + NEGATIVE
stimulus: exchange overlapping and non-overlapping offers
expected: overlap selects a supported encoding; no overlap is rejected as specified
evidence_type: INTEROP_RESULT + PROTOCOL_TRACE
```

A producer-only unit test is insufficient for this obligation.

## F. Machine Contract partial coverage

Source: Machine Contract validates object shape, while the specification also
requires the value to remain stable across a resource lifetime.

```text
machine_contract: PARTIALLY_MACHINE_ENFORCED
scenario_kind: POSITIVE + LIFECYCLE
stimulus: observe the same resource before and after update/reload
expected: identity is unchanged
evidence_type: STATE_TRACE + RUNTIME_ASSERTION
```

The Conformance Specification references the approved invariant; it does not copy it.

## G. Normative ambiguity

Source: “The operation MUST complete promptly,” with no bound, clock, terminal
condition, or observer defined.

```text
conformance_id: CONF-OPEN-001
disposition: OPEN_SPEC_ISSUE
reason: no deterministic completion criterion can be selected safely
```

Do not choose a timeout to make the scenario executable.
