---
name: conformance-specification
description: Generate and independently review project-neutral Conformance Specifications from approved Engineering Specifications and Machine Contracts, defining observable obligations, evidence, and deterministic verdicts without inventing behavior.
metadata:
  version: "0.1.0"
  role: "conformance-specification"
  companions: "engineering-contract-spec, machine-contract-spec"
---

# Conformance Specification

## Role

Use this Skill when an approved Engineering Specification and its approved Machine
Contract must be turned into a proof-oriented Conformance Specification:

```text
Requirement
→ Conformance Obligation
→ Scenario / Assertion
→ Evidence Requirement
→ Deterministic Verdict
```

The Conformance Specification answers **how an implementation can be shown to
conform**. It is not a unit-test guide, pytest guide, implementation test plan,
generic QA checklist, or code-coverage optimizer. Its root is the normative
requirement, not an implementation branch.

This Skill is project-neutral. Names in examples are illustrative and do not define
any project's ontology.

## Authoritative inputs

Accept the inputs relevant to the requested mode:

- approved Engineering Specification, Requirement IDs, and stable anchors;
- approved Machine Contract, its requirement map, and conformance obligations;
- Change Record and affected requirement/artifact closure;
- accepted Conformance Specification and previous review findings;
- profile, feature, and applicability definitions;
- target artifact conventions and evidence constraints.

The Engineering Specification remains the semantic root. The Machine Contract is a
machine-oriented projection and cannot override it. If they conflict, emit
`SPEC_MACHINE_CONTRACT_CONFLICT`; do not select a side by implementation convenience.
If the specification is insufficient to define a sound proof obligation, emit
`OPEN_SPEC_ISSUE` rather than inventing a test condition.

## Outputs

Produce a candidate or reviewed Conformance Specification containing, as appropriate:

- stable conformance obligations and scenario IDs;
- Requirement and Engineering Specification anchor mappings;
- Machine Contract object references and disposition consumption;
- profile/applicability rules;
- scenario preconditions, stimulus, observation point, and expected/forbidden results;
- evidence type and minimum evidence requirements;
- deterministic verdict rules;
- coverage and change-impact maps;
- independent review verdict: `APPROVED`, `REQUIRES_PATCH`, or `OPEN_SPEC_ISSUE`.

The artifact envelope and file format remain project-defined. Do not turn the field
list in this Skill into a universal schema.

## Operating modes

### Generate

Read the complete approved sources, enumerate normative obligations, classify each
one, choose the minimum sufficient observable proof, and produce coverage and evidence
records.

### Revise

Compare the accepted artifact and Change Record. Preserve stable IDs and unaffected
scenarios, update only the affected closure, and classify scenarios as
`NEW_SCENARIO`, `UPDATED_SCENARIO`, `REMOVED_SCENARIO`, or `UNCHANGED_SCENARIO`.

### Review

Use an independent context where possible. Check source fidelity, Machine Contract
alignment, applicability, evidence sufficiency, verdict determinism, and traceability.
Ordinary scenario defects are `REQUIRES_PATCH`; a missing normative decision is
`OPEN_SPEC_ISSUE`.

## Obligation analysis

First inventory the normative source. Preserve `MUST`, `MUST NOT`, `SHOULD`,
`SHOULD NOT`, and `MAY` semantics using the companion
[normative contract rules](../engineering-contract-spec/references/normative-contract.md).
Then classify each obligation using the [obligation taxonomy](references/normative-obligations.md):

```text
STRUCTURAL_VALIDATION
VALUE_CONSTRAINT
CROSS_FIELD
STATE_TRANSITION
LIFECYCLE
TEMPORAL
IDENTITY
REFERENCE
SERIALIZATION
INTEGRITY
ERROR_BEHAVIOR
CAPABILITY_DECLARATION
NEGOTIATION
INTEROPERABILITY
OBSERVABLE_SIDE_EFFECT
SECURITY_BOUNDARY
PROFILE_REQUIREMENT
NON_OBSERVABLE
NON_TESTABLE_DIRECTLY
```

Classification selects proof shape; it does not encode a test framework.

## Conformance obligation model

Each obligation should carry, at minimum:

```text
conformance_id
source_requirement_id
engineering_spec_anchor
machine_contract_refs
normative_strength
profile
obligation_statement
observable_surface
preconditions
stimulus
expected_observation
forbidden_observation
evidence_type
verdict_rule
applicability
notes
```

Keep IDs stable across editorial changes and incremental revisions. The exact ID
format is project-defined; do not bind a reusable naming rule to a domain object.

## Scenario semantics

Use structured semantics for:

```text
precondition
stimulus / action
observation point
expected result
forbidden result
normative timeout or ordering window, when defined
cleanup / isolation requirement
```

`Given / When / Then` is a useful rendering, not a mandatory syntax. A scenario must
state what evidence is observed and what exact condition determines its verdict.
Do not add an error code, timeout, payload, fixture, or cleanup behavior absent from
the normative inputs.

## Positive, negative, and minimum sufficient scenarios

Choose only scenario classes justified by the obligation:

```text
POSITIVE
NEGATIVE
BOUNDARY
TRANSITION
INTEROP
```

Valid-input success does not prove rejection of invalid input. `MUST NOT`, forbidden
states, invalid transitions, and rejection obligations normally require negative
evidence. Do not mechanically require all five classes for every Requirement.

Use the smallest scenario set that proves the stated obligation. Redundant scenarios
that test the same normative fact without adding boundary, profile, failure, or
interoperability evidence are review findings, not coverage improvements.

## Machine Contract integration

Consume the Machine Contract's dispositions:

- `MACHINE_ENFORCED`: reuse its validator evidence where it proves the implementation
  surface, and add implementation-level evidence only if the requirement demands it;
- `PARTIALLY_MACHINE_ENFORCED`: add scenarios for the uncovered behavior;
- `CONFORMANCE_ONLY`: create an explicit conformance obligation;
- `NON_MACHINE_ENFORCEABLE`: retain the obligation with manual, review, or external
  evidence, or explain why it is outside executable conformance;
- `OPEN_SPEC_ISSUE`: do not invent scenarios.

Do not duplicate schema, state-machine, invariant, or serialization definitions. Link
to approved Machine Contract objects and define only the proof and evidence needed
to demonstrate them.

## Evidence and deterministic verdicts

Select evidence using the [evidence and verdict guidance](references/evidence-and-verdicts.md):

```text
SCHEMA_VALIDATION
RUNTIME_ASSERTION
PROTOCOL_TRACE
STATE_TRACE
API_RESPONSE
EVENT_SEQUENCE
SERIALIZED_BYTES
HASH_RESULT
ERROR_RESULT
INTEROP_RESULT
MANUAL_AUDIT
STATIC_ANALYSIS
TEST_EXECUTION
```

Every executable scenario defines `PASS`, `FAIL`, `INAPPLICABLE`, and, when needed,
`BLOCKED`/`UNTESTABLE` conditions. Final verdicts must be deterministic. If the
source cannot support a deterministic rule, record `NON_DETERMINISTIC_CONFORMANCE`
and classify the needed human or specification action; do not use “looks compliant.”

## Profiles, applicability, and capability claims

Use the [profile applicability rules](references/profile-applicability.md). Each
obligation must state whether it is:

```text
MANDATORY_FOR_PROFILE
CONDITIONAL_IF_CAPABILITY_DECLARED
OPTIONAL_FEATURE
NOT_APPLICABLE
```

An optional feature does not fail merely because it is absent. Once an implementation
declares the feature, the linked obligations become applicable and its claim must be
checked against observed behavior. Capability declaration is not evidence of capability.

Preserve SHOULD/SHOULD NOT as defeasible recommendations with deviation rationale
when they form an obligation. MAY is not a failure for non-use, but an offered MAY
feature can activate its own requirements.

## Interoperability, lifecycle, errors, and security

Distinguish single-implementation proof from producer/consumer or client/server
interoperability proof; see [interop conformance](references/interop-conformance.md).
Use real boundary evidence when the requirement is about interaction, and label mock
evidence as such.

For ordering, lifetime, cancellation, timeout, retry, monotonicity, and eventuality,
use the [lifecycle and temporal guidance](references/lifecycle-temporal.md). Do not
invent a duration to make a scenario executable.

For errors, distinguish occurrence, category, code, payload, and recovery. If the
source requires only rejection, prove rejection without inventing a transport code.

Security obligations may cover observable authorization boundaries, forbidden
operations, and disclosure behavior. When proof requires broader assurance, emit
`SECURITY_ASSURANCE_REQUIRED`; this Skill is not a penetration-testing methodology.

## Coverage and change impact

Build the coverage chain:

```text
Requirement
→ Conformance Obligation
→ Scenario / Assertion
→ Evidence Requirement
→ Verdict
```

Every MUST and MUST NOT receives a disposition from
`EXECUTABLE_CONFORMANCE`, `MACHINE_CONTRACT_SUFFICIENT`, `MANUAL_AUDIT`,
`NON_OBSERVABLE`, `NOT_APPLICABLE`, or `OPEN_SPEC_ISSUE`. The audit succeeds only
when `UNMAPPED MUST = 0` or every exception is explicit and scoped.

On revision, also report implementation-test, interoperability-test, and manual-audit
impact. This Skill does not edit test code or implementation files.

## Independent review

Apply the [review checklist](references/review-checklist.md) in a fresh invocation.
Review semantic fidelity, MUST coverage, no invented behavior, applicability,
positive/negative sufficiency, evidence, verdict determinism, profile/capability
logic, lifecycle/temporal correctness, error semantics, interoperability, Machine
Contract alignment, traceability, and redundancy.

## Boundaries

Machine Contract answers:

```text
What can machines enforce structurally or deterministically?
```

Conformance Specification answers:

```text
What evidence proves an implementation conforms?
```

Implementation Design, `contract-implementation-planner`, and
`contract-driven-coding` decide how fixtures, modules, runners, and CI are organized.
This Skill does not prescribe a test framework, fixture layout, class/module owner,
mock library, or CI pipeline.

## CWO artifact adapter

When invoked as `artifact_kind=CONFORMANCE_SPEC`, return structured metadata including:

- artifact kind and source revisions/hashes;
- derived Machine Contract references;
- affected Requirements and anchors;
- candidate path/hash and validator role;
- obligations, coverage, applicability, evidence, and review results;
- scenario change-impact classification.

Candidate isolation, promotion, HumanDecision, and scheduling remain caller concerns.
This Skill does not create a second Human Gate.

## Reused rules and references

Reuse [engineering-contract-spec](../engineering-contract-spec/SKILL.md) for normative
strength, stable Requirement identity, traceability, state-machine discipline,
verifiable behavior, review severity, and open contract issues. Reuse
[machine-contract-spec](../machine-contract-spec/SKILL.md) for representation
dispositions and Machine Contract object references. Reuse
[technical-specification-guide](../technical-specification-guide/SKILL.md) for
no-silent-invention and semantic propagation. The references below contain only
conformance-specific guidance and do not duplicate those general methods.

- [Normative obligations](references/normative-obligations.md)
- [Scenario modeling](references/scenario-modeling.md)
- [Evidence and verdicts](references/evidence-and-verdicts.md)
- [Profile applicability](references/profile-applicability.md)
- [Coverage closure](references/coverage-closure.md)
- [Interoperability conformance](references/interop-conformance.md)
- [Lifecycle and temporal proof](references/lifecycle-temporal.md)
- [Review checklist](references/review-checklist.md)
- [Generic examples](examples/conformance-examples.md)
