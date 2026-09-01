# Concrete Boundary Contract

For an important boundary, record the dimensions that actually govern interoperability or safe
implementation:

| Dimension | Required question |
|---|---|
| Contract name | What boundary is being specified? |
| Owner / authority | Who owns each asserted fact and decision? |
| Input / output | What crosses the boundary, in what form? |
| Preconditions | What must already be true? |
| Postconditions | What is guaranteed after success? |
| Failures | Which failure classes are observable? |
| Rejection | How is invalid input rejected? |
| Mutability | What may be changed, and by whom? |
| Idempotency | What happens when the request is repeated? |
| Timing | What are timeout, cancellation, and ordering rules? |
| Freshness | How are timestamps, revisions, or expiry handled? |
| Safety / permission | Which gates can veto the operation? |
| Observability | What must be recorded or emitted? |
| Extension | How can compatible extensions be introduced? |

The table is a review aid, not a requirement to fill irrelevant cells. The selected dimensions must
be precise enough that an implementer does not need to guess a load-bearing behavior.
