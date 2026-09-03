# Lifecycle and Temporal Proof

Use this reference for state, ordering, freshness, cancellation, timeout, retry,
eventuality, monotonicity, and lifetime requirements. The companion Contract and
Machine Contract Skills define state semantics; this reference defines evidence
choices.

## Proof dimensions

Record only source-defined dimensions:

```text
state before
trigger
guard/precondition
state after
observable event/effect
ordering relation
time window, if specified
cancel/retry/recovery behavior
```

“Eventually” without a bound may be proven as an allowed eventual relation, but must
not be changed into an invented number of seconds. If a bounded window is required
but not defined, use `OPEN_SPEC_ISSUE`.

Stable-over-lifetime and monotonicity normally need ordered or historical evidence;
a single snapshot schema cannot prove them. Test restart, duplicate, cancellation,
or recovery only when the source makes those behaviors normative.
