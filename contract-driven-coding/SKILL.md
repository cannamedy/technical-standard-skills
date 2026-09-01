---
name: contract-driven-coding
description: >
  Implement approved Engineering Contract work from an approved Implementation Plan and bounded
  Atomic Task, with requirement-level verification and explicit stop conditions. Use when code must
  be constrained by durable specifications and traceability. Do not use this skill to invent
  architecture, modify the Contract, or silently expand implementation scope.
metadata:
  version: "0.1.1"
  role: "contract-bound-coding-executor"
  companion: "engineering-contract-spec"
---

# Contract-Driven Coding

Implement only what an approved Engineering Contract, Implementation Plan, and Atomic Task authorize.
The workflow is Agent-neutral and works whether one Agent performs all roles or separate review
contexts are available.

## Binding Authority

Use this precedence:

```text
Engineering Contract
        >
Approved Implementation Plan
        >
Atomic Task
        >
Existing Implementation
```

The Contract wins when a Task or existing code conflicts with it. Do not edit the Contract or Task
to make code pass. Report:

- `PLAN / TASK DEFECT` when the approved downstream artifact conflicts with the Contract;
- `OPEN CONTRACT ISSUE` when the Contract itself leaves a load-bearing decision unresolved.

Code must not become a hidden source of new standard behavior.

## Pre-task Re-read

At the start of every Task, MUST:

1. read the Task MD;
2. collect its Implements Requirement IDs or Section Anchors;
3. reopen the authoritative Engineering Contract;
4. read the referenced Requirement / Section text;
5. inspect the current repository and Git state;
6. confirm allowed files, dependencies, and verification method;
7. only then begin implementation.

Do not code from remembered requirements. Read [references/pre-task-check.md](references/pre-task-check.md).

## Bounded Implementation Context

Load only what the current Task needs:
- the Task;
- referenced Contract sections;
- dependency outputs;
- relevant source files;
- relevant tests and configuration;
- project constraints needed for the change.

Do not assume that the whole Contract or repository must be loaded for every Task. If the bounded
context is insufficient to implement or verify the requirement, stop and report the missing input.

## Persistent Execution Tracker

Use `implementation/traceability.md`, or the project's designated durable tracker, as the recovery
source of truth. At minimum track:

| Requirement | Task | Status | Implementation | Test | Verification |
|---|---|---|---|---|---|
| REQ-... | TASK-... | PENDING | path / commit | test id / path | result / evidence |

Recommended statuses are `PENDING`, `IN_PROGRESS`, `IMPLEMENTED`, `VERIFIED`, `BLOCKED`, and
`CONTRACT_ISSUE`. Resume from the tracker and Git state, not Agent memory. Durable tracker updates
belong in Git; scratch notes and raw logs do not.

Read [references/execution-tracker.md](references/execution-tracker.md).

## Disposition Promotion Rule

`IMPLEMENTED` from the Planning stage means only that repository evidence identified an
implementation landing point. It MUST NOT be promoted automatically to `VERIFIED`.

Promotion to `VERIFIED` requires all applicable evidence to be completed against the authoritative
Contract:

- reread the Requirement / Section Anchor;
- inspect the implementation and its diff;
- run the required tests or deterministic checks;
- inspect the conformance landing and evidence.

If the implementation conflicts with the Contract, do not promote it. Use an appropriate
`DRIFT`, `BLOCKED`, `CONTRACT_ISSUE`, or `PLAN / TASK DEFECT` disposition and stop the affected
workflow as required.

Read [references/final-verification.md](references/final-verification.md).

## Test and Verification Workflow

For behavior that can be tested, default to:

```text
re-read Contract
    → write failing test
    → verify expected failure
    → minimal implementation
    → test passes
    → refactor if needed
    → rerun relevant tests
```

This is a TDD default, not a ritual. Static schemas, generated configuration, documentation-only
changes, and environment-only changes MAY use deterministic verification suited to their type; the
method must be recorded.

Read [references/tdd-workflow.md](references/tdd-workflow.md).

## Implementation Scope Discipline

Modify only the Task's allowed or expected surface. If correctness requires an important area
outside the Task, stop and report:

`PLAN EXPANSION REQUIRED`

Do not silently re-plan the system, widen the Task, add mandatory behavior with no Contract basis,
or use an incidental existing implementation as authority.

The following always require a stop and explicit direction when not already authorized:
- architecture changes;
- Contract mutation;
- destructive or irreversible operations;
- security-sensitive actions;
- external side effects beyond the authorized repository or worktree;
- merge, push, publish, or release.

## Contract Mutation Prohibition

The Coding Agent MUST NOT:
- change the Engineering Contract to satisfy an implementation;
- lower a normative requirement to match existing code;
- add mandatory behavior without Contract basis;
- turn a reference implementation detail into a standard rule.

When a Contract gap is found:

```text
OPEN CONTRACT ISSUE
    → stop affected Task
    → return to Contract workflow
    → revise, review, freeze, and approve Contract
    → update Plan / Task if authorized
    → resume coding
```

## Completion Reviews

Every completed Task has two ordered reviews.

### 1. Specification Compliance Review

Re-read the Contract and diff. Check that the Requirement is actually implemented, failure behavior
is present, no extra behavior was invented, scope was respected, and authority, safety, lifecycle,
and compatibility rules hold.

### 2. Code Quality Review

Only after compliance passes, review maintainability, duplication, clarity, typing, error handling,
test quality, performance, and repository conventions.

Read [references/spec-compliance-review.md](references/spec-compliance-review.md).

If review contexts or subagents are available, a fresh context SHOULD perform the review. Otherwise
the same Agent MUST logically separate `IMPLEMENTER`, `SPEC REVIEWER`, and `CODE REVIEWER` roles;
the reviewer must reread the Contract and inspect the diff rather than trusting the implementer's
summary.

## Worktree and Execution Modes

For complex or multi-Task work, use an isolated branch or worktree when the repository workflow
supports it. Do not bind this rule to a particular tool.

The default execution mode is:

`gated`

In gated mode, approval is required before each Task group or milestone. In `autonomous` mode,
approved Contract and Plan permit continuous eligible Task execution, but hard stops remain binding.

Read [references/execution-modes.md](references/execution-modes.md).

Hard stops include:
- `OPEN CONTRACT ISSUE`;
- `PLAN / TASK DEFECT`;
- `PLAN EXPANSION REQUIRED`;
- destructive or irreversible operation;
- security-sensitive action;
- unauthorized external side effect;
- merge, push, publish, or release;
- any continuation that would require guessing.

Autonomous mode does not grant new authority for these actions.

## Final Verification

After all eligible Tasks, perform a requirement-level gap analysis:

```text
Contract
    → Task
    → Implementation
    → Test
    → Verification
```

Classify every current-scope Requirement as `implemented`, `verified`, `unimplemented`, `partially
implemented`, `blocked`, or `contract issue`. “Tests passed” is not evidence that every Contract
Requirement was implemented.

Output exactly one final status:

`CONTRACT IMPLEMENTATION VERIFIED`

or

`CONTRACT IMPLEMENTATION HAS GAPS`

Read [references/final-verification.md](references/final-verification.md).
