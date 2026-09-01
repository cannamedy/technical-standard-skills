---
name: contract-implementation-planner
description: >
  Transform an approved Engineering Contract into an implementation-ready plan, dependency-aware
  atomic tasks, and traceability artifacts without writing code or changing the Contract. Use when
  implementation work needs bounded tasks, file mapping, verification mapping, or a persistent plan.
  Do not use this skill to author architecture, revise normative requirements, or perform coding.
metadata:
  version: "0.1.0"
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

Task size should fit one bounded implementation context. Do not enforce an arbitrary file-count
limit; split when the change surface makes behavior, review, or verification unclear.

Read [references/task-template.md](references/task-template.md).

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

## Traceability and Final Gate

Maintain a durable mapping at requirement level:

```text
Requirement
    → Task
    → Implementation Boundary
    → Test
    → Verification
```

Audit that every current mandatory requirement has a task and verification landing point, every task
has an upstream Contract anchor, dependencies are consistent, blocked issues are visible, and
deferred scope is not accidentally mandatory.

Output exactly one final status:

`IMPLEMENTATION PLAN READY FOR EXECUTION`

or

`IMPLEMENTATION PLAN BLOCKED BY CONTRACT ISSUES`

Read [references/dependency-planning.md](references/dependency-planning.md) for the consistency
audit.
