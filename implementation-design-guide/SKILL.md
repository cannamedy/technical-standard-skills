---
name: implementation-design-guide
description: Generate and independently review project-neutral Implementation Designs that realize approved Engineering Specifications, Machine Contracts, and Conformance Specifications without changing normative semantics or replacing the Implementation Plan.
metadata:
  version: "0.1.0"
  role: "implementation-design"
  companions: "engineering-contract-spec, machine-contract-spec, conformance-specification, contract-implementation-planner, contract-driven-coding"
---

# Implementation Design Guide

## Role

Use this Skill when approved Engineering Specification, Machine Contract, and
Conformance Specification inputs need an implementation-ready internal design:

```text
Normative Engineering Inputs
→ responsibility decomposition
→ reference runtime architecture
→ internal design contracts
→ implementation-ready design
```

It answers **how the implementation realizes what the system must do**. It is not an
Engineering Specification, Machine Contract, Conformance Specification,
Implementation Plan, Atomic Task, or Coding guide.

This Skill is project-neutral. Names in examples are illustrative and do not define
any product ontology.

## Authoritative inputs

Accept the inputs relevant to the requested mode:

- approved Engineering Specification, Requirement IDs, and anchors;
- approved Machine Contract mappings, invariants, state machines, and validators;
- approved Conformance Specification, Conformance IDs, and evidence obligations;
- Change Record and affected closure;
- accepted Implementation Design and previous design findings;
- existing repository/module structure and implementation evidence;
- explicit project conventions and technology/runtime constraints.

The Engineering Specification owns external semantics, the Machine Contract owns its
machine-verifiable projection, and the Conformance Specification owns proof
obligations. Existing code is evidence about current structure, never an authority
that can rewrite those inputs. Conflicts become `IMPLEMENTATION_SPEC_MISMATCH`,
`OPEN_SPEC_ISSUE`, or `OPEN_DESIGN_ISSUE` as applicable; do not resolve them by
silently narrowing the public behavior.

## Outputs

Produce a candidate or reviewed Implementation Design containing, as appropriate:

- component/module map and dependency direction;
- responsibility and data/state ownership;
- public, project-public, internal, and test-only boundaries;
- control/data flows and internal interface contracts;
- Machine Contract realization map;
- Conformance realization and evidence-hook map;
- lifecycle, error, persistence, concurrency, extension, security, and recovery decisions;
- repository projection and incremental change impact;
- design decision records and unresolved issue records;
- closure audit and `PLANNER_READY` or `NOT_PLANNER_READY`.

The file format and envelope remain project-defined. A single `implementation/design.md`
is a useful default, not a mandatory directory layout.

## Operating modes

### Generate

Read all approved inputs, identify required external surfaces, decompose internal
responsibilities, make only necessary implementation decisions, and produce traceable
design elements with failure and evidence paths.

### Revise

Compare the accepted design and Change Record. Preserve unaffected decisions,
component identities, ownership, rationale, and evidence hooks. Update only the
affected closure and classify repository elements as `UNCHANGED`, `MODIFIED`, `NEW`,
`DEPRECATED`, or `SUPERSEDED`.

### Review

Use an independent context where possible. Check normative fidelity, ownership,
realizability, boundaries, closure, failure/recovery, planner readiness, and
unnecessary architecture. Ordinary design defects are `REQUIRES_PATCH`; unresolved
specification ambiguity is `OPEN_SPEC_ISSUE`; multiple legitimate architecture
choices requiring human selection are `ARCHITECTURE_DECISION_REQUIRED`.

## Boundary and no-invention rules

Keep these layers separate:

```text
Engineering Specification
= externally observable normative behavior

Machine Contract
= machine-verifiable normative representation

Conformance Specification
= proof obligations and evidence requirements

Implementation Design
= internal realization of those obligations
```

Every design statement must be recognizable as one of:

```text
NORMATIVE_REQUIREMENT
IMPLEMENTATION_DECISION
PROJECT_CONSTRAINT
DESIGN_ASSUMPTION
OPEN_DESIGN_ISSUE
OPEN_SPEC_ISSUE
```

An implementation choice may select among permitted behaviors, but must not silently
remove an allowed option, turn MAY into MUST, expose an internal choice as a public
contract, or add a normative persistence/error/compatibility requirement. If the
choice changes external semantics, it belongs in the normative authority layer and
must be reported rather than hidden in design.

## Design Decision model

Record a stable decision ID only for choices affecting ownership, architecture,
compatibility, lifecycle semantics, persistent data, public boundaries, or
cross-component coupling. A decision may carry:

```text
decision_id
title
source_requirements
machine_contract_refs
conformance_refs
decision
rationale
alternatives
tradeoffs
affected_components
compatibility_effect
failure_modes
status
```

Do not turn every helper or local implementation detail into an ADR. For important
choices, name a credible alternative and why it is insufficient for the stated
constraints; avoid empty claims such as “more flexible” without a causal reason.

## Responsibility ownership

For every required responsibility, define:

```text
component/module
responsibility
owned state
owned invariants
inputs
outputs
dependencies
forbidden responsibilities
failure ownership
```

Use a single responsibility owner even when several components participate. Explicitly
assign creator, mutator, reader, persistence owner, serialization owner, validation
owner, and lifecycle owner for important data. A component may delegate work, but
delegation must not create ambiguous authority or a second state owner.

Read [responsibility ownership](references/responsibility-ownership.md) and
[data/state ownership](references/data-and-state-ownership.md).

## Component and module architecture

Produce a component map, module map, dependency direction, and boundary contracts.
Review circular dependencies, responsibility leakage, abstraction inversion,
duplicated ownership, hidden coupling, transport/domain coupling,
persistence/domain coupling, and test-only architecture leaking into runtime.

Do not add layers, managers, adapters, plugins, or repositories unless a stated
responsibility, boundary, constraint, or failure mode needs them. Internal class and
module names are design details, not standard objects.

Read [component boundaries](references/component-boundaries.md).

## Data, control flow, and internal interfaces

For critical operations, describe:

```text
entry point
→ validation
→ dispatch
→ state transition
→ side effect
→ result/error propagation
→ evidence generation
```

Use sequence descriptions, flow tables, transition mappings, or diagrams as useful;
no diagram format is mandatory. Internal interfaces should state inputs, outputs,
preconditions, postconditions, ownership, failure behavior, idempotency, ordering,
and visibility where relevant.

## Machine Contract realization

For each approved Schema, Invariant, State Machine, Serialization Rule, Runtime
Validator, or Error Contract, map:

```text
Machine Contract object
→ implementing component
→ validation point
→ state/data owner
→ failure propagation
→ bypass prevention
```

Do not copy the Machine Contract definition into the design. The closure condition is:

```text
UNOWNED MACHINE CONTRACT OBLIGATION = 0
```

Read [Machine Contract realization](references/machine-contract-realization.md).

## Conformance realization

For each executable Conformance obligation, map:

```text
Conformance ID
→ observable runtime surface
→ design component
→ evidence hook
→ implementation support
```

Evidence hooks may expose state traces, protocol traces, structured errors, event
sequences, serialized bytes, or hash evidence without changing normative behavior.
Do not write test code or prescribe its framework. If an executable obligation
cannot be exposed or evidenced, emit `DESIGN_CONFORMANCE_GAP` rather than deferring
the architecture question to the Planner. The closure condition is:

```text
UNREALIZABLE EXECUTABLE CONFORMANCE = 0
```

Read [Conformance realization](references/conformance-realization.md).

## Public and internal boundaries

Label each element as applicable:

```text
PUBLIC_NORMATIVE
PROJECT_PUBLIC
INTERNAL_STABLE
INTERNAL_PRIVATE
TEST_ONLY
```

Do not let an internal class name become a standard object, and do not implement a
normative public interface as an inaccessible helper. A project-public contract may
be stable for local consumers without becoming an external standard.

## Lifecycle, errors, persistence, and concurrency

For a normative lifecycle, assign state owner, transition authority, execution point,
invalid-transition handling, concurrency semantics, recovery owner, terminal cleanup,
and persistence/reconstruction when applicable. Internal implementation states are
allowed only when marked `INTERNAL_ONLY` and when they do not change observable
semantics.

Distinguish internal exceptions, domain errors, Machine Contract validation errors,
normative interface errors, transport errors, and infrastructure failures. Record
origin, translation boundary, public exposure, logging/evidence, and recovery owner;
do not collapse all exceptions into one public error.

Add persistence only when required by the project or a necessary implementation
guarantee. If used, define authority, derived/cache status, persistence owner,
transaction boundary, reconstruction, version/migration, and failure behavior.

If the specification requires ordering, monotonicity, cancellation, atomicity, or
race-sensitive lifecycle behavior, state how the design provides it. Label guarantees
as `SPEC_REQUIRED`, `IMPLEMENTATION_GUARANTEE`, `BEST_EFFORT`, or `NOT_GUARANTEED`.
Do not invent complex concurrency when no such requirement exists.

Read [lifecycle and errors](references/lifecycle-and-errors.md) and
[failure and recovery](references/failure-recovery.md).

## Extensions, security, and evidence hooks

When the project defines extension points, record registration/discovery, stable
contract, ownership, failure isolation, and version compatibility. Do not introduce
a plugin architecture merely because one is familiar.

For security obligations, identify trust boundary, authorization decision point,
credential handling owner, sensitive state owner, and forbidden bypass path. Consume
security assurance obligations from the Conformance Specification without becoming a
full security architecture or penetration-testing Skill.

Prefer non-invasive evidence hooks and preserve public behavior. An observability
mechanism must not weaken authorization, expose sensitive state, or alter lifecycle
semantics.

## Repository projection and existing code

For an existing repository, map design elements to current surfaces and classify them:

```text
UNCHANGED
MODIFIED
NEW
DEPRECATED
SUPERSEDED
```

Prefer preserving sound structure and describe migrations where ownership changes.
Existing code may reveal technical debt, current ownership, and feasibility, but code
conflicting with the normative sources is `IMPLEMENTATION_SPEC_MISMATCH`, not a reason
to rewrite the sources.

## Incremental revision and failure-driven design

Use Change Record, affected Engineering Specification, Machine Contract, and
Conformance closure to compute the minimum design revision. Preserve unaffected
decisions, component identity, ownership, rationale, and evidence hooks.

For critical components, answer:

```text
what fails?
who detects it?
who owns recovery?
what state remains?
what observable behavior results?
```

Cover applicable validation failure, dependency failure, interrupted lifecycle,
partial side effect, stale state, restart/recovery, and corrupted persisted state.
Do not force irrelevant failure modes into a design.

Read [incremental design](references/incremental-design.md).

## Design closure and Planner readiness

Audit the following chain:

```text
Requirement → Design responsibility
Machine Contract → Owner
Conformance → Observable surface / evidence hook
State → Owner
Error → Translation boundary
Persistent data → Owner
Public interface → Implementing component
```

Before handing off to the Planner, verify:

- all required responsibilities are owned;
- component boundaries and dependency direction are defined;
- Machine Contract obligations are mapped;
- executable Conformance obligations are realizable;
- critical design decisions are resolved;
- affected repository surfaces are identified;
- no blocking design issue remains.

Output exactly one gate status:

```text
PLANNER_READY
```

or

```text
NOT_PLANNER_READY
```

The Planner decomposes approved design into work order and tasks; it must not silently
invent the remaining architecture.

## Independent review

Apply the [review checklist](references/review-checklist.md) in a fresh invocation.
Review normative fidelity, responsibility ownership, Machine Contract realization,
Conformance realizability, public/internal boundaries, lifecycle, error propagation,
dependency direction, persistence, concurrency, security, evidence hooks,
failure/recovery, incremental preservation, architecture proportionality, and
planner readiness.

Verdicts:

```text
APPROVED
REQUIRES_PATCH
OPEN_SPEC_ISSUE
ARCHITECTURE_DECISION_REQUIRED
```

## CWO artifact adapter

When invoked as `artifact_kind=IMPLEMENTATION_DESIGN`, return structured metadata
including:

- source revisions/hashes and Change Record;
- design decision, component, ownership, and repository projections;
- Machine Contract and Conformance mappings;
- evidence hooks and closure results;
- review verdict and Planner readiness.

Candidate isolation, promotion, HumanDecision, and scheduling remain caller concerns.
This Skill does not create a second approval system or modify implementation files.

## Reused rules and references

Reuse [engineering-contract-spec](../engineering-contract-spec/SKILL.md) for normative
boundaries, stable Requirement identity, state-machine discipline, traceability, and
open issues; [machine-contract-spec](../machine-contract-spec/SKILL.md) for contract
object ownership and representation; [conformance-specification](../conformance-specification/SKILL.md)
for evidence, applicability, and deterministic verdicts; and
[contract-implementation-planner](../contract-implementation-planner/SKILL.md) plus
[contract-driven-coding](../contract-driven-coding/SKILL.md) for downstream separation.
Reuse [technical-specification-guide](../technical-specification-guide/SKILL.md) for
architecture reasoning, concept closure, and failure-driven rationale. The references
below add only Implementation Design-specific guidance.

- [Responsibility ownership](references/responsibility-ownership.md)
- [Component boundaries](references/component-boundaries.md)
- [Data and state ownership](references/data-and-state-ownership.md)
- [Machine Contract realization](references/machine-contract-realization.md)
- [Conformance realization](references/conformance-realization.md)
- [Lifecycle and errors](references/lifecycle-and-errors.md)
- [Failure and recovery](references/failure-recovery.md)
- [Incremental design](references/incremental-design.md)
- [Review checklist](references/review-checklist.md)
- [Design examples](examples/design-examples.md)
