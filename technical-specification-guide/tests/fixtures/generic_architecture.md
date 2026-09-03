# Interoperable Runtime Guide

## Scope

### Concepts

#### Runtime Boundary

##### Authority

The implementation MUST preserve source evidence. A consumer SHOULD inspect freshness and MAY cache
descriptions.

**Why it matters:** a local label should not create another navigation level.

1. Discover the resource
2. Read the contract
3. Observe current state

1. Start an independent transaction
2. Reconcile the result

- contract
  - identity
  - authority
- runtime evidence

```python
def run():
    return "ok"
```

```text
Root
├── Node A -> State
└── Node B -> Action
```

> A quoted rationale.

| Field | Meaning |
| --- | --- |
| id | Stable identifier |

## Assessment

### Knowledge Check

The assessment section is routed to the question designer for source-grounded review.

## Runtime Example

### Observe

This intentionally long paragraph represents a technical-document tail that should be checked for
pagination density and orphan control rather than repaired by deleting source content. The renderer
may adjust style metrics, keep-with-next behavior, or page breaks while preserving the source.

The runtime also records the observation timestamp, the authority that owns the fact, the freshness
policy used by the consumer, and the boundary at which a stale observation can no longer support an
action. These details remain part of the guide's technical explanation.

The contract separates discovery from execution, declaration from current availability, and a
request from evidence that the physical side effect occurred. A reference implementation may use
one transport while another implementation uses a different transport.

The example is intentionally longer than a checklist so a renderer can exercise body spacing,
heading keep-with-next, list indentation, code preservation, diagram whitespace, and final-page
density. No source paragraph should be removed merely to make a page look fuller.
