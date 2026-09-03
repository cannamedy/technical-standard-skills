# Machine Contract Review Checklist

Use an independent review context where possible. Review the candidate against the
Engineering Specification, not against the generator's explanation.

## Verdict gates

### Semantic fidelity

- every normative requirement has a disposition;
- no MUST is weakened or silently omitted;
- no required/default/enum/range/lifecycle/error behavior was invented;
- source authority and affected anchors are correct.

### Representation quality

- each semantic class uses an appropriate representation;
- schemas are valid and not stricter than the source;
- state machines are closed for the claimed scope;
- invariants include evaluation and failure semantics;
- serialization and integrity domains are precise and non-conflicting;
- error contracts preserve observable rejection behavior.

### Traceability and compatibility

- object IDs are stable where unaffected;
- Requirement → anchor → object → validator/conformance evidence is complete;
- unaffected accepted objects are preserved;
- incremental compatibility findings are explicit;
- duplicated definitions do not drift.

## Verdict semantics

`APPROVED` means semantic review and deterministic validators pass. `REQUIRES_PATCH`
means the source is sufficient but the projection is defective; patch and review
again. `OPEN_SPEC_ISSUE` means a genuine source ambiguity, conflict, or missing
load-bearing decision prevents safe projection. Do not use it for ordinary schema or
traceability defects.

Record findings with evidence, affected object/requirement, severity, and disposition.
Do not include hidden reasoning or chain-of-thought in the artifact.
