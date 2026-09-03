# Compatibility Audit

Use this reference for an incremental Machine Contract revision. Compatibility
policy remains owned by the Engineering Specification; this audit reports the
shape of the change.

## Compare at semantic level

Check whether the candidate:

- adds a required field;
- removes a field or object;
- narrows a type, range, enum, pattern, or cardinality;
- changes unknown-field or extension behavior;
- removes a state or transition;
- changes error, ordering, freshness, or lifecycle semantics;
- changes canonical serialization, encoding, hash domain, or content identity.

Also inspect reference ownership, invariant scope, validator failure behavior, and
stable IDs. A textual diff alone is insufficient.

## Result vocabulary

Report `NON_BREAKING`, `POTENTIALLY_BREAKING`, or `BREAKING` for each material
change, with the affected requirement and compatibility source. “Potentially” means
the effect depends on an explicitly unresolved version or extension policy; it is
not permission to choose one. If compatibility authority is missing, create an
`OPEN_SPEC_ISSUE` rather than silently accepting the change.

Preserve unaffected objects and their IDs. A semantic no-op may still change a
serialization hash; record that as provenance without labeling it a behavioral
change.
