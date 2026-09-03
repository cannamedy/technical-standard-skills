---
name: machine-contract-spec
description: Generate and independently review machine-verifiable contracts from approved Engineering Specifications by selecting schemas, state machines, invariants, serialization rules, and traceability without inventing normative semantics.
metadata:
  version: "0.1.0"
  role: "machine-contract-projection"
  companion: "engineering-contract-spec"
---

# Machine Contract Specification

## Role

Use this Skill when an approved Engineering Specification must be projected into a
machine-verifiable **Machine Contract**. The output may combine structured schemas,
state machines, invariants, canonical serialization rules, error contracts, and
validator metadata. It is not synonymous with JSON Schema and it is not an
implementation design.

The Engineering Specification is the normative input. Implementation code may be
used as evidence during review, but it must not be used to repair, weaken, or invent
the specification. If the specification leaves a load-bearing semantic undecided,
record `OPEN_SPEC_ISSUE` and identify the blocked scope.

This Skill is project-neutral. A field or object name in an example is illustrative,
not a rule for every project.

## Inputs and outputs

Accept the inputs relevant to the requested mode:

- approved Engineering Specification and its stable anchors;
- Requirement IDs and Contract anchors;
- Change Record or semantic delta;
- an accepted Machine Contract, when revising;
- previous review findings and validator evidence;
- target artifact path, format, schema conventions, and project extensions.

Produce an external or project-scoped candidate Machine Contract together with:

- a requirement-to-representation map;
- normative coverage and unmapped-requirement results;
- compatibility findings for incremental revisions;
- deterministic validation metadata and conformance obligations;
- an independent review verdict: `APPROVED`, `REQUIRES_PATCH`, or
  `OPEN_SPEC_ISSUE`.

The artifact envelope is project-defined. A useful projection can contain
`schemas`, `state_machines`, `invariants`, `serialization_rules`, `error_contracts`,
`traceability`, `coverage`, and `conformance_obligations`; do not treat that list as
an invented universal schema.

## Operating modes

### Generate

Read the complete approved specification, enumerate its normative requirements,
classify their machine representability, select the least-assumptive representation,
then emit the candidate and coverage report.

### Revise

Compare the accepted artifact and the Change Record before editing. Preserve stable
IDs and unaffected objects. Change only the affected closure, and re-run coverage,
compatibility, and traceability checks.

### Review

Use a fresh context where possible. Review semantic fidelity, coverage, representation
choice, schema/state/invariant closure, serialization consistency, compatibility, and
traceability. A defect in the projection is `REQUIRES_PATCH`; a missing or conflicting
normative decision is `OPEN_SPEC_ISSUE`.

## Source and separation rules

Use the companion [Engineering Contract rules](../engineering-contract-spec/SKILL.md)
for normative language, stable clause identity, contract boundaries, verifiable
behavior, open contract issues, safety, and the Human Guide-to-Contract handoff.
Read only the companion references needed by the current artifact, especially
[normative contracts](../engineering-contract-spec/references/normative-contract.md),
[schema contracts](../engineering-contract-spec/references/schema-contract.md),
[state machines](../engineering-contract-spec/references/state-machine.md),
[traceability](../engineering-contract-spec/references/traceability.md), and
[verifiable behavior](../engineering-contract-spec/references/verifiable-behavior.md).
For human-readable source interpretation, reuse the companion guide's
[no-silent-invention](../technical-specification-guide/references/no-silent-invention.md)
and [semantic-propagation](../technical-specification-guide/references/semantic-propagation.md)
rules rather than duplicating their publication methodology here.

The Machine Contract defines what can be structurally or deterministically enforced.
It must not prescribe Python names, module paths, database choices, internal managers,
or other incidental implementation structure. Use the companion
[Contract/Implementation separation](../engineering-contract-spec/references/contract-implementation-separation.md)
rule and leave such decisions to an Implementation Design.

Do not silently turn an unspecified property into `required`, a default, a closed
enum, a range, a lifecycle, or a rejection rule. Do not weaken a stated MUST. When
the source does not determine the choice, use `OPEN_SPEC_ISSUE` rather than a
plausible guess.

## Projection workflow

1. **Establish the source set.** Record the specification revision/hash, applicable
   requirements and anchors, change ID, accepted artifact hash, and target format.
2. **Build the semantic inventory.** For every normative requirement, retain its
   exact strength and classify it using the [representability taxonomy](references/machine-representability.md).
3. **Select representations.** Apply the [projection guidance](references/schema-projection.md)
   and choose JSON Schema, a state machine, an invariant, a serialization rule, an
   error contract, a runtime validator, a conformance-only assertion, or an explicit
   open issue. One requirement may map to more than one complementary object.
4. **Generate minimally.** Preserve unaffected accepted objects and stable IDs. For
   revisions, keep a before/after map and record every changed object.
5. **Close coverage.** Run the [normative coverage audit](references/normative-coverage.md).
   Every MUST must have a disposition; `UNMAPPED MUST = 0` unless the requirement is
   explicitly represented as `OPEN_SPEC_ISSUE` with a reason and blocked scope.
6. **Audit compatibility.** Use the [compatibility audit](references/compatibility-audit.md)
   to detect narrowing, removal, serialization changes, and state/transition changes.
   Do not decide compatibility policy that the Engineering Specification does not
   define.
7. **Review independently.** Apply the [review checklist](references/review-checklist.md),
   run declared deterministic validators, and emit the verdict plus evidence.

## Representation and validation boundary

The projection must expose, for each requirement:

```text
Requirement ID
→ Engineering Specification anchor
→ semantic class
→ representation
→ Machine Contract object/path
→ enforcement disposition
→ validator or conformance obligation
```

Use `MACHINE_ENFORCED`, `PARTIALLY_MACHINE_ENFORCED`, `CONFORMANCE_ONLY`,
`NON_MACHINE_ENFORCEABLE`, or `OPEN_SPEC_ISSUE` as the disposition vocabulary unless
the project has an explicitly compatible vocabulary. Deterministic validation checks
the artifact's declared structure and references; semantic review checks fidelity to
the source. Neither replaces the other.

For JSON Schema, constrain only what the specification supports. Review requiredness,
unknown fields and extension points, enum closure, numeric and collection bounds,
patterns, references, nullability, composition, and version compatibility. Put
cross-field, lifecycle, temporal, ownership, or identity guarantees in a more
appropriate representation when JSON Schema cannot express them faithfully.

For a state machine, include only source-defined or source-deterministically-derived
states and transitions. Capture initial and terminal states, preconditions, effects,
invalid transitions, observable events, and requirement references. For an invariant,
record a stable ID, statement, scope, evaluation point, machine-checkability,
validator role, failure semantics, and source requirement. For canonical
serialization, record the algorithm, normalization, included/excluded fields,
encoding, canonical bytes, and hash domain when the source defines them. Keep logical
revision, content identity, and authorization semantics separate when the source does.

## Conformance and implementation boundaries

The Machine Contract may emit `conformance_obligations` and machine-checkable
metadata, but it does not author the full scenario suite. A Conformance Specification
proves that an implementation conforms; it consumes the approved Machine Contract
and its traceability. An Implementation Design explains runtime structure and
ownership; it consumes the approved contract and must not be smuggled into this
artifact. See [boundary guidance](references/machine-representability.md) for the
decision boundary.

## CWO artifact adapter

When invoked as `artifact_kind=MACHINE_CONTRACT`, return structured artifact metadata
without embedding project content in this Skill:

- `kind=MACHINE_CONTRACT`;
- source revision/hash and `derived_from` references;
- affected requirements and Contract anchors;
- candidate path/hash and validator role;
- coverage, compatibility, review, and open-issue results.

The caller may use these results for candidate isolation, promotion, and downstream
impact scheduling. This Skill does not rewrite Contracts or Plans, create a second
Human Gate, or decide promotion authority.

## Reused rules and non-duplication

The companion `engineering-contract-spec` remains authoritative for MUST/SHOULD/MAY
handling, requirement identity, contract readiness, boundary contracts, state-machine
discipline, safety, traceability, review severity, and open contract issues. This
Skill adds only the projection-specific taxonomy, representation selection, coverage
closure, compatibility audit, and Machine Contract review concerns. It intentionally
does not restate those general methodologies.

## References

- [Machine representability](references/machine-representability.md) — classify a
  requirement before choosing a representation.
- [Schema projection](references/schema-projection.md) — select and audit JSON Schema
  without over-constraint.
- [State-machine contracts](references/state-machine-contracts.md) — project source
  lifecycle semantics.
- [Invariant modeling](references/invariant-modeling.md) — represent constraints that
  are not faithful schema fields.
- [Normative coverage](references/normative-coverage.md) — close requirement mappings.
- [Compatibility audit](references/compatibility-audit.md) — assess incremental change.
- [Review checklist](references/review-checklist.md) — conduct independent review.
- [Projection examples](examples/projection-examples.md) — generic examples,
  including ambiguity handling.
