# Technical Whitepaper Fixture

This fixture exercises the reusable technical-whitepaper publication design system with Chinese
body text, stable English object names, lists, code, diagrams, tables, quotations, and long-form
pagination. A renderer test repeats the content across 15 or more pages without adding technical
meaning.

## Architecture Overview

The system exposes a Contract and keeps implementation details behind a named boundary.

### Reader Map

The reader follows discovery, description, observation, request, execution, and evidence.

#### Physical Node

The Node owns authoritative facts.

#### Adapter

The Adapter translates the Contract to a vendor interface.

### Design Rules

The guide preserves explicit semantics and a readable page rhythm.

1. Discover the resource.
2. Read the Contract.
3. Observe current State.

- semantic type
  - unit
  - frame
- authority

```python
def observe(node):
    return node.read_state()
```

```text
Consumer
  └── Contract
       ├── State
       └── Action
```

> A publication profile changes presentation, not the Contract meaning.

| Field | Meaning |
|---|---|
| state | authoritative current fact |
| action | typed request for change |

## Runtime Consequence

The same visual system remains readable when the document becomes long: headings identify level,
lists support scanning, code and diagrams remain distinct, and tables preserve their header.
