# Normative Contract Language

## Keywords
- MUST: mandatory for conformance.
- MUST NOT: prohibited.
- SHOULD: recommended; justified exceptions allowed.
- SHOULD NOT: generally discouraged; justified exceptions allowed.
- MAY: optional.

## Testability

Bad:
- "The implementation MUST be robust."
- "The device MUST operate safely."

Better:
- "Every dynamic State MUST include a timestamp."
- "Requests outside a declared hard limit MUST be rejected before adapter dispatch."

## Clause design

A strong clause usually states:
- subject;
- condition;
- required behavior;
- observable result.

Example:
`OP-014`: If cancellation is accepted while an Operation is RUNNING, the Runtime MUST eventually
transition the Operation to CANCELLED or FAILED and MUST expose the terminal reason.

## Bilingual documents

If Chinese is used, define one authoritative equivalence table:
- 必须 = MUST
- 禁止/不得 = MUST NOT
- 应该 = SHOULD
- 不应 = SHOULD NOT
- 可以 = MAY

Avoid mixing casual "建议/推荐/最好" with conformance keywords unless their non-normative meaning is explicit.
