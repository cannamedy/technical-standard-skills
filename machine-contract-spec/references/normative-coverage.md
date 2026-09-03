# Normative Coverage

Use this reference to make omission visible. Coverage is an audit of the source
requirements, not a count of generated objects.

## Coverage record

For each normative requirement retain:

```text
requirement_id
engineering_spec_anchor
normative_strength
semantic_classes
machine_contract_objects
disposition
validator_or_conformance_evidence
open_issue_id (when applicable)
```

Allowed dispositions are:

- `MACHINE_ENFORCED`: deterministic contract validation is sufficient for the claimed part;
- `PARTIALLY_MACHINE_ENFORCED`: the contract covers only a stated portion and downstream evidence is required;
- `CONFORMANCE_ONLY`: proof needs an implementation scenario or integration evidence;
- `NON_MACHINE_ENFORCEABLE`: deterministic automation is not suitable, with rationale;
- `OPEN_SPEC_ISSUE`: the source is insufficient or contradictory, with blocked scope.

## Closure rules

Every MUST and MUST NOT must have a disposition and traceable landing point. A
`MACHINE_ENFORCED` disposition must point to an actual object and validator. A
`PARTIALLY_MACHINE_ENFORCED` disposition must state what remains. A conformance or
review-only disposition must explain why schema/runtime validation cannot prove it.

The audit succeeds only when `UNMAPPED MUST = 0`; an explicit open issue is not a
silent omission. Include SHOULD and MAY requirements when they constrain observable
interoperability, while preserving their normative strength.

Do not count an implementation test as coverage when the specification does not
require the tested behavior. Unsupported mandatory checks are also traceability
defects.
