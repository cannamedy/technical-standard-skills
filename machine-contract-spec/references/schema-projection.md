# Schema Projection

Use this reference when a requirement can be represented as a structural or value
constraint. The companion `engineering-contract-spec` schema reference remains the
source for general schema-contract discipline; this document focuses on projection
decisions.

## Projection table

| Source semantic | Use schema when | Do not use schema alone when |
| --- | --- | --- |
| object/property presence | the source defines structure or requiredness | presence depends on lifecycle/history not represented in the object |
| type/cardinality/range | the source states the type or bound | the bound is only an operational recommendation |
| enum/const | the source explicitly closes the set | extensions or future values are allowed |
| cross-field rule | the relation is finite and faithfully expressible | it needs external state, ordering, or an action result |
| reference | ownership and target semantics are defined | resolution, freshness, or permissions are runtime facts |
| extension field | the source defines an extension policy | rejecting unknown fields would be an invented compatibility policy |

## Review points

For each schema object, verify `type`, `required`, `additionalProperties`, enums,
bounds, collection uniqueness, patterns, nullability, composition, and `$ref`
ownership against source anchors. An omitted keyword can be correct when the source
does not define the corresponding constraint. An added keyword is a semantic change,
not harmless precision.

Check forward compatibility explicitly: whether unknown fields, unknown enum values,
new versions, and extension namespaces are accepted or rejected must come from the
Engineering Specification. Do not turn a reference profile's stricter behavior into
a universal Machine Contract rule.

## Cross-field choice

Use conditional schema constructs only when they preserve the exact source meaning.
If the condition involves prior messages, resource ownership, time, registry state,
or authoritative execution outcome, model it as an invariant, state-machine
precondition, runtime validator, or conformance obligation instead.

## No over-constraint gate

Before approval, compare every restrictive keyword with a source clause. If no
normative basis exists, remove it or record `OPEN_SPEC_ISSUE`; do not retain it as a
“reasonable default.”
