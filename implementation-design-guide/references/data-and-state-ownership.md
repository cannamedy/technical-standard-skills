# Data and State Ownership

Use this reference for data whose authority, mutation, serialization, or lifecycle
must remain unambiguous.

## Ownership dimensions

For important data, identify:

```text
creator
owner
mutator
reader
persistence_owner
serialization_owner
validation_owner
lifecycle_owner
authority
derived_from
freshness
```

Separate authoritative state from cache, projection, and evidence. A serializer may
format state without owning its truth. A validator may reject an update without
becoming the lifecycle owner. If persistence exists, distinguish stored authority
from reconstructible derived data.

Do not infer a database, cache, immutability rule, or write-back path from the fact
that the current code happens to have one.
