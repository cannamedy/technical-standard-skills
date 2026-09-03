# Machine Contract Projection Examples

These examples are deliberately small and generic. The field names and fragments
are illustrative; they become normative only when an input Engineering Specification
supports them.

## A. Type and range

Source: “`revision` MUST be a non-negative integer.”

```text
classes: TYPE + RANGE
representation: JSON Schema
object: schema.resource.properties.revision
projection: {"type": "integer", "minimum": 0}
disposition: MACHINE_ENFORCED
```

No default, maximum, or requiredness is added unless separately specified.

## B. Stable identity

Source: “`resource_id` MUST remain stable for the lifetime of a resource.”

```text
classes: IDENTITY + TEMPORAL
representation: invariant
object: INV-RESOURCE-IDENTITY-001
scope: one resource lifetime
evaluation_point: create, update, reload, and observe
disposition: PARTIALLY_MACHINE_ENFORCED
```

A string type alone cannot prove stability across observations. The remaining proof
is a conformance/runtime obligation.

## C. Cross-field constraint

Source: “If `status` is `completed`, `completed_at` MUST be present.”

```text
classes: CROSS_FIELD
representation: conditional schema
object: schema.job.completed-status-requirement
projection: if status == completed, then required(completed_at)
disposition: MACHINE_ENFORCED
```

Do not infer the reverse rule, timestamp format, or allowed status values.

## D. Runtime invariant

Source: “A consumer MUST NOT observe a lower revision after observing a higher
revision for the same resource.”

```text
classes: TEMPORAL + BEHAVIORAL
representation: runtime invariant
object: INV-RESOURCE-REVISION-MONOTONIC-001
evaluation_point: ordered consumer observations
validator_role: consumer_observation_validator
disposition: CONFORMANCE_ONLY
```

The Machine Contract can describe the invariant and its evidence obligation; a
single object schema cannot validate an observation history.

## E. Normative ambiguity

Source: “A request SHOULD expire promptly.” No duration, clock, owner, or observable
failure is defined.

```text
classes: TEMPORAL + BEHAVIORAL
representation: OPEN_SPEC_ISSUE
issue: define expiration bound, authority, and observable expiry behavior
disposition: OPEN_SPEC_ISSUE
```

Do not choose a timeout merely because one is common in an implementation.
