# Conformance Specification Review Checklist

Review the candidate against the Engineering Specification and approved Machine
Contract, not against the implementation's current behavior.

## Fidelity and coverage

- every MUST/MUST NOT has a disposition;
- no SHOULD became MUST and no MAY became mandatory support;
- no behavior, timeout, error code, fixture, or profile condition was invented;
- every obligation has source anchors and stable IDs;
- Machine Contract conflicts are reported, not resolved silently.

## Proof quality

- scenarios observe the required external surface;
- negative, boundary, transition, and interop evidence is present where needed;
- evidence is sufficient and correctly labeled;
- PASS/FAIL/INAPPLICABLE/BLOCKED rules are deterministic;
- temporal and lifecycle proof preserves source ordering and windows;
- capability claims activate the correct obligations;
- unsupported or redundant scenarios are removed or justified.

## Separation and review verdict

- no implementation framework or CI layout is prescribed;
- no Schema/FSM/invariant is duplicated from the Machine Contract;
- no unit-test result is mislabeled as conformance evidence;
- security assurance limits are explicit;
- change impact preserves unaffected scenario IDs and evidence contracts.

`APPROVED` requires semantic review and declared deterministic checks to pass.
`REQUIRES_PATCH` is for a projection defect when the source is sufficient.
`OPEN_SPEC_ISSUE` is for a genuine normative ambiguity or conflict.
