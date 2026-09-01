# Vertical Slicing

A vertical slice carries one behavior from its Contract anchor through the implementation boundary
to a deterministic verification point.

```text
Requirement → Schema / Runtime → Test → Verification
```

Prefer slices that can be reviewed and verified independently. Combine slices only when they share a
real invariant or cannot be tested separately. Infrastructure tasks are valid prerequisites when
the plan identifies the dependent behavior and its eventual verification.

Avoid a purely horizontal sequence that postpones all tests until after every schema or runtime
change. That shape hides missing semantics and makes failure ownership difficult to review.
