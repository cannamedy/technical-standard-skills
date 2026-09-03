# Machine Representability

Use this reference after collecting normative requirements and before drafting
Machine Contract objects. Classify the semantic first; representation follows.

## Taxonomy

| Class | Typical question | Candidate representation |
| --- | --- | --- |
| `STRUCTURAL` | What objects, properties, or nesting exist? | Schema/object model |
| `TYPE` | What value type is allowed? | Schema type or typed contract |
| `CARDINALITY` | How many values/items are allowed? | Schema cardinality |
| `RANGE` | What numeric or ordered bounds are stated? | Schema bounds or validator |
| `ENUMERATION` | Is the value a specified set? | Enum/const only when source closes it |
| `PATTERN` | Is a lexical form explicitly required? | Pattern/format validator |
| `IDENTITY` | What makes an entity stable or unique? | Identity rule/invariant |
| `REFERENCE` | How does one object refer to another? | `$ref`, reference rule, or validator |
| `CROSS_FIELD` | Do fields constrain one another? | Conditional schema or invariant |
| `STATE_TRANSITION` | Which lifecycle moves are legal? | State machine |
| `TEMPORAL` | What ordering, freshness, or duration is required? | Temporal invariant/validator |
| `SERIALIZATION` | What bytes or canonical form are authoritative? | Serialization rule |
| `INTEGRITY` | How is content checked or identified? | Integrity/hash rule |
| `ERROR` | What failure is observable and how? | Error contract |
| `BEHAVIORAL` | What observable action must occur? | Runtime validator/conformance obligation |
| `NON_MACHINE_ENFORCEABLE` | Is deterministic checking not suitable? | Conformance/review disposition |

One requirement may have multiple classes. For example, “a value MUST be a
non-negative integer” is `TYPE + RANGE`; “an identifier MUST remain stable for an
entity lifetime” is an `IDENTITY`/`TEMPORAL` invariant, not merely a string schema.

## Decision boundary

Use a representation when the source explicitly defines its subject, strength,
scope, and failure meaning. Use a validator or conformance assertion when the
constraint needs runtime context, history, external state, or an observable action.
Use `OPEN_SPEC_ISSUE` when more than one representation would change behavior and
the source does not select one.

Never infer requiredness, defaults, closed-world enums, bounds, lifecycle states,
or failure behavior from naming conventions or implementation convenience.
