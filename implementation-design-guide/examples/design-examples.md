# Implementation Design Examples

These examples are generic and illustrative. They do not define a universal module
layout, framework, persistence technology, or domain ontology.

## A. Schema obligation and validator ownership

Machine Contract: an input object must satisfy a structural schema.

```text
design_element: DESIGN-VALIDATION-001
component: boundary validator
responsibility: validate at every normative entry point
state_owner: none
failure_owner: boundary validator
evidence_hook: structured validation result
visibility: INTERNAL_STABLE
```

The design does not copy the schema or require a particular validation library.

## B. Lifecycle state owner

Machine Contract: an accepted cancellation transitions an item to `cancelled`.

```text
design_element: DESIGN-LIFECYCLE-001
state_owner: lifecycle coordinator
transition_authority: lifecycle coordinator
execution_point: after cancellation preconditions pass
invalid_transition: translated according to the approved error contract
evidence_hook: state trace + transition event
```

Internal worker states remain `INTERNAL_ONLY` and cannot become new public states.

## C. Conformance evidence hook

Conformance obligation: a consumer must not observe a lower revision after a higher
revision for the same resource.

```text
conformance_id: CONF-REVISION-001
observable_surface: ordered consumer observations
design_component: observation boundary
evidence_hook: append-only state trace
support: retain comparison context for the observation scope
```

No test framework or test implementation is selected.

## D. Internal versus normative state

Normative state: `active` and `stopped`. The implementation may use an internal
`draining` state.

```text
internal_state: draining
visibility: INTERNAL_PRIVATE
constraint: must map to the approved external semantics
forbidden: expose draining as a new normative state
```

## E. Error translation boundary

```text
origin: dependency timeout
category: infrastructure failure
translation_boundary: public adapter
public_exposure: only the error form defined by the approved interface contract
evidence: structured error plus dependency diagnostic
recovery_owner: retry coordinator, if retries are specified
```

The design does not invent a public status code.

## F. Existing code conflicts with specification

The repository currently accepts an input that the approved specification requires
to be rejected.

```text
finding: IMPLEMENTATION_SPEC_MISMATCH
design_action: preserve normative rejection and map the affected validation boundary
not_allowed: weaken the specification to match current code
```

## G. Two legitimate architecture choices

Both a local durable store and an external durable store satisfy the approved
requirements, but they create different ownership and recovery commitments. The
specification does not select one.

```text
verdict: ARCHITECTURE_DECISION_REQUIRED
decision_scope: persistence authority and recovery boundary
options: local durable store | external durable store
next_step: obtain the required architecture decision before Planner handoff
```

This verdict is not used for ordinary module defects.
