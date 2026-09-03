# Incremental Design Revision

Use this reference when a Change Record affects an accepted Implementation Design.

## Revision inputs

Compare:

```text
Change Record
affected Engineering Specification requirements
affected Machine Contract objects
affected Conformance obligations
accepted design decisions/components
existing implementation evidence
```

Compute the minimum design closure. Preserve unaffected decisions, component
identity, ownership, rationale, evidence hooks, and valid implementation choices.

Classify repository/design elements as:

```text
UNCHANGED
MODIFIED
NEW
DEPRECATED
SUPERSEDED
```

Do not renumber stable decisions or rewrite unaffected sections merely to improve
style. If an ownership migration is needed, record old owner, new owner, transition
boundary, compatibility effect, and migration/recovery evidence.
