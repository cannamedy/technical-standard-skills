---
name: contract-implementation-planner
description: >
  Transform an approved Engineering Contract into an implementation-ready plan, dependency-aware
  atomic tasks, and traceability artifacts without writing code or changing the Contract. Use when
  implementation work needs bounded tasks, file mapping, verification mapping, or a persistent plan.
  Do not use this skill to author architecture, revise normative requirements, or perform coding.
metadata:
  version: "0.2.1"
  role: "contract-to-implementation-planner"
  companion: "engineering-contract-spec"
---

# Contract Implementation Planner

Turn an approved Engineering Contract into durable execution artifacts that a coding Agent can use
without guessing. The Planner owns implementation decomposition; the Contract remains authoritative
for behavior.

## Responsibility Boundary

The Planner MUST:
- inspect the existing repository, schemas, tests, implementation, and project constraints;
- use the Engineering Contract as the behavior authority;
- create a plan, dependency graph, task files, verification mapping, and traceability;
- map requirements to repository files only after inspecting the repository;
- stop affected planning when a load-bearing `OPEN CONTRACT ISSUE` exists.

The Planner MUST NOT:
- rewrite architecture or normative Contract semantics;
- make code changes;
- let existing implementation override the Contract;
- impose a global directory convention when the project has an established one;
- turn a planning preference into a new mandatory Contract requirement.

Read [references/plan-gate.md](references/plan-gate.md) before planning. Read the other references
when their topic is in scope.

## Inputs

Accept, as applicable:
- the Engineering Contract;
- the architecture or design source it formalizes;
- the existing repository;
- schemas and other contract artifacts;
- tests and conformance checks;
- existing implementation;
- project constraints and authorized change scope.

Identify the authoritative Contract path and version before producing tasks.

## Outputs

Prefer project-compatible durable artifacts:

```text
implementation/
├── plan.md
├── tasks/
│   ├── TASK-001-*.md
│   └── TASK-002-*.md
└── traceability.md
```

Adapt this layout when the project already has a clear convention. Long-lived plan, task, and
traceability artifacts belong in Git. Temporary prompts, raw Agent logs, scratch reasoning, and
disposable review packages stay outside the repository or under ignored paths.

## Planning Pipeline

Execute this pipeline:

```text
Contract Readiness Check
        ↓
Requirement Inventory
        ↓
Dependency Graph
        ↓
Implementation Boundaries
        ↓
Vertical Slices
        ↓
Atomic Tasks
        ↓
Verification Mapping
        ↓
Plan Consistency Audit
```

### 1. Contract Readiness Check

Run the Contract readiness gate before decomposing affected requirements. If the result is
`CONTRACT NOT READY FOR IMPLEMENTATION PLANNING`, record the affected scope and stop that planning
path. Unaffected requirements MAY continue.

Before planning begins, apply the conditional Frozen Source Integrity Gate. If an authoritative
Architecture Guide, Engineering Contract, or other source declares a freeze commit, freeze tag,
checksum, SHA-256, or immutable revision, verify the current source against that declaration. A
mismatch MUST stop affected planning; do not repair, reinterpret, or silently replace the frozen
source. If no freeze metadata is declared, do not impose a new checksum or tag requirement.

Read [references/frozen-source-integrity.md](references/frozen-source-integrity.md).

### 2. Requirement Inventory

Inventory all requirements in the current scope and preserve their stable IDs or Section Anchors.
Planning labels MAY include:

- schema;
- core runtime;
- state/lifecycle;
- adapter;
- discovery;
- safety;
- permission;
- audit;
- integration;
- conformance.

These are planning labels, not a replacement for the Contract's canonical taxonomy.

Every current-scope Requirement MUST receive an explicit disposition. Use semantic equivalents when
the project already has them, but do not leave an `UNMAPPED` Requirement. At minimum distinguish
existing evidence from work still required, using statuses such as `IMPLEMENTED`, `PARTIAL`,
`PENDING`, `DRIFT`, `BLOCKED`, and `DEFERRED`.

`IMPLEMENTED` at planning time means only that an implementation landing point was found in the
current repository. It does not mean `VERIFIED`; promotion requires Contract-based verification in
the Coding / Verification stage.

Read [references/requirement-disposition.md](references/requirement-disposition.md).

### 2a. Repository Reality Classification

For each current-scope Requirement, classify repository evidence as at least:

- Already implemented;
- Partially implemented;
- Implementation drift;
- Missing;
- Deferred.

Existing code is evidence, not authority. If it runs or its tests pass but violates the authoritative
Contract, mark `IMPLEMENTATION DRIFT`; do not reuse its wrong semantics, promote it to verified, or
change the Contract to fit it.

### 2b. Declared Gap Reconciliation

Treat gap counts or TODO counts from Contracts, design documents, and old audit reports as planning
inputs, not current repository truth. Re-audit them against the current repository and classify each
as:

- confirmed gap;
- already resolved by the current repository;
- additional implementation drift;
- newly discovered gap.

The Contract is behavior authority, not a live repository inventory database.

### 3. Dependency Graph

Order tasks by real dependency, not Contract chapter order. For example:

```text
identity / schema
        ↓
lifecycle
        ↓
runtime dispatch
        ↓
higher behavior
        ↓
integration
        ↓
conformance
```

Check that the graph is acyclic. A discovered cycle involving architecture or behavior is a
Contract issue, not a reason to invent an ordering.

### 4. Implementation Boundaries

Only after repository inspection, record files and areas to add, change, or delete. For each
boundary, preserve the Contract's ownership, failure, authority, safety, and compatibility rules.
Do not add file paths to the Contract itself.

### 5. Vertical Slices

Prefer a verifiable slice:

```text
Requirement
    → Contract anchor
    → Schema / Runtime
    → Test
    → Verification
```

Infrastructure prerequisites are allowed when their necessity and dependent slices are explicit.
Avoid a plan that implements every schema, then every runtime, and only later adds all tests.

Read [references/vertical-slicing.md](references/vertical-slicing.md).

## Atomic Task Contract

Every task file MUST identify:

- a unique `TASK-xxx` identifier;
- objective;
- Requirement IDs or Section Anchors implemented;
- authoritative Contract anchors;
- dependencies;
- current repository state;
- required behavior;
- inputs, outputs, and failures when applicable;
- expected or allowed files and change surface;
- forbidden files or areas when applicable;
- tests and verification;
- acceptance criteria;
- definition of done;
- open Contract issues.

### Task Context Boundary Rule

Each Task MUST also express:

- **Architecture Constraints**: only the upstream principles needed by this Task, recorded as
  stable anchors rather than copied documents;
- **Conformance Landing**: the test, schema validation, runtime probe, fixture, conformance check,
  or review evidence that will prove the mapped Requirement has a downstream landing;
- **Forbidden Changes**: authoritative sources, unrelated architecture, and Task-specific areas
  that must not be modified.

The Task MUST fit a bounded implementation context. It should let a Coding Agent read the Task,
re-read its exact Contract anchors, load the relevant repository files, and implement without
loading the entire upstream document set into context.

Task size should fit one bounded implementation context. Do not enforce an arbitrary file-count
limit; split when the change surface makes behavior, review, or verification unclear.

Read [references/task-template.md](references/task-template.md) and
[references/task-context-boundary.md](references/task-context-boundary.md).

## Execution Modes

Plan metadata MUST support:

```yaml
execution_mode: gated | autonomous
```

Default to `gated`. In `gated` mode, each Task group or milestone requires approval before coding.
In `autonomous` mode, approval of the Contract and overall Plan permits continuous downstream
execution, but does not authorize architecture changes, Contract mutation, destructive actions, or
external side effects.

Read [references/plan-gate.md](references/plan-gate.md).

## Scope-Aware Working Tree Gate

A non-clean working tree is not by itself a planning blocker. Classify changes by scope before
deciding whether the requested planning or audit can proceed.

- **Expected Target Artifacts**: Plan, Task, traceability, and audit-report artifacts within the
  declared target scope MAY be untracked or modified. Do not stop solely because those artifacts
  are not committed.
- **Frozen Authoritative Sources**: A modified, conflicting, or checksum/revision-mismatched
  authoritative Guide, Contract, or other frozen source triggers the Frozen Source Integrity Gate
  and MUST stop affected planning.
- **Unexpected Unrelated Changes**: Assess unrelated tracked, untracked, generated, source, or
  merge-conflict changes for contamination of repository reality, file mapping, dependencies, or
  verification. Continue only when the affected scope can be reliably isolated, and record the
  contamination boundary; otherwise STOP.

Working-tree cleanliness is evidence about audit isolation, not an authority condition. It MUST NOT
be used as an unconditional planner prerequisite.

## Post-Patch Gate Re-evaluation

A Gate result describes the Current State of the artifact, not a historical defect state. After an
authorized planning-artifact patch, the Planner MUST reread the current artifact, rerun affected
validations, and recompute the Gate. Record the Historical Transition separately from the current
state.

`REQUIRES MINIMAL PATCH` may remain in the audit trail as a historical transition, but a historical
defect alone MUST NOT keep the current Gate blocked. If the Current State has no remaining defects,
report the current compatible or ready state; do not preserve a sticky failure state.

## Planner Guardrails

When the Contract is ambiguous, contradictory, or missing a load-bearing decision:

```text
OPEN CONTRACT ISSUE
    → block affected planning
    → return to engineering-contract-spec
    → revise and review Contract
    → freeze / approve
    → resume planning
```

Do not solve a Contract gap by selecting a file, API, class, or task behavior as if it were a
standard decision. Do not produce a plan that requires the coding Agent to guess.

### Deferred Scope Containment

Requirements or capabilities explicitly marked `DEFERRED`, `FUTURE`, `OUT OF CURRENT SCOPE`, or
`PROFILE-LEVEL FUTURE` MUST NOT produce a current mandatory implementation Task. A Task is allowed
only when the current Contract explicitly requires a compatibility placeholder, extension seam,
reserved field, interface stub, or other forward-compatibility behavior. That Task may implement
the seam only; it MUST NOT implement the deferred capability itself.

## Traceability and Final Gate

Maintain a durable mapping at requirement level:

```text
Requirement
    → Task
    → Implementation Boundary
    → Test
    → Verification
```

Audit that every current-scope Requirement has a disposition and is mapped to one of:

- existing implementation evidence;
- an implementation Task;
- an explicit `BLOCKED` disposition.

Do not mechanically create a duplicate Task for a Requirement that is already implemented. Confirm
that `IMPLEMENTED` is evidence classification only, not verification. Every mandatory Requirement
must have a clear downstream landing or an explicit blocker, and every Task must have an upstream
Contract anchor, consistent dependencies, and a conformance landing. Check that deferred scope has
not accidentally become mandatory work.

Output exactly one final status:

`IMPLEMENTATION PLAN READY FOR EXECUTION`

or

`IMPLEMENTATION PLAN BLOCKED BY CONTRACT ISSUES`

Read [references/dependency-planning.md](references/dependency-planning.md) for the consistency
audit.
