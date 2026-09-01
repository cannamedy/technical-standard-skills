---
name: engineering-contract-spec
description: >
  Create, formalize, extend, or review machine-actionable engineering specifications used by AI coding
  agents and engineers to implement interoperable systems without architectural guesswork. Use for
  normative clauses, schemas, object contracts, state machines, authority rules, lifecycle semantics,
  discovery profiles, safety contracts, compatibility rules, and conformance traceability. Use when
  implementation correctness, deterministic behavior, testability, or AI coding constraints matter.
  Do not use this skill as the primary human-oriented architecture white paper.
compatibility: >
  Agent Skills-compatible clients. Best used alongside source code, schemas, tests,
  and a human-centered architecture guide when available.
metadata:
  version: "0.3.0"
  role: "ai-engineering-contract"
  companion: "technical-specification-guide"
---

# Engineering Contract Specification

Create engineering contracts that constrain implementation behavior.

Primary audience:
- AI coding agents;
- implementation engineers;
- test engineers;
- architecture reviewers;
- conformance reviewers.

The goal is:

> Two independent teams should be able to implement the same contract and produce compatible behavior
> without relying on undocumented assumptions.

## Role

This skill transforms stable architecture intent into an implementation-facing normative contract.

It answers:
- What exactly must be implemented?
- What object fields exist?
- Which fields are required?
- Who owns each fact?
- What states exist?
- Which transitions are legal?
- What is rejected?
- What happens on timeout, disconnect, restart, or cancellation?
- What is normative vs reference implementation?
- How is conformance proven?
- What is the AI explicitly forbidden to invent?

## Relationship to technical-specification-guide

When a human-centered Guide exists:
- read the relevant guide principles first;
- preserve the intended architecture;
- formalize, do not redesign silently;
- if a principle is ambiguous, report the ambiguity before choosing a contract;
- the Guide explains "why";
- this Contract defines "exactly what".

Preferred flow:

Human Guide principle
→ Normative Clause
→ Schema / Contract Element
→ Runtime Semantics
→ Conformance Requirement
→ Executable Test
→ Reference Implementation / Example

Example:

Guide:
"Action changes reality; State describes reality."

Contract:
`STATE-001`: Authoritative physical State MUST NOT be externally writable through the control interface.

Schema:
`access = read_only`

Conformance:
attempted external write → deterministic rejection.

## Source-of-truth discipline

The Engineering Contract is authoritative for:
- exact normative clauses;
- object fields and constraints;
- lifecycle/state transitions;
- schema semantics;
- safety validation behavior;
- compatibility/versioning rules;
- conformance criteria.

It MUST NOT silently override stable architecture principles from the Guide.

If the Guide and Contract conflict:
1. stop;
2. identify the conflict;
3. classify whether the Guide or Contract is stale;
4. propose reconciliation;
5. do not let code decide the architecture.

## Modes

### A. Formalization mode

Use when converting architecture into an implementable contract.

Workflow:
1. Read the human-centered guide or architecture source.
2. Extract stable principles.
3. Identify normative objects and responsibilities.
4. Create a terminology/identity model.
5. Define clause IDs.
6. Define schemas and field constraints.
7. Define authority and mutability.
8. Define lifecycle/state machines.
9. Define errors and failure behavior.
10. Define discovery/registration/lease behavior when applicable.
11. Define safety validation and veto order.
12. Define compatibility/versioning/extension behavior.
13. Create Clause → Schema → Test traceability.
14. Identify intentionally deferred items.
15. Review for ambiguity before implementation starts.

### B. Extension mode

Use when extending an existing Engineering Contract.

Workflow:
1. Read the current contract, schemas, tests, and relevant code.
2. Preserve existing IDs and semantics unless change is intentional.
3. Identify all clauses affected by the change.
4. Update schemas, state machines, examples, and tests consistently.
5. Check backward compatibility.
6. Check whether the change affects authority, safety, lifecycle, discovery, or versioning.
7. Produce a change-impact summary.

### C. Review mode

Use when reviewing contract quality or implementation alignment.

Review:
- clause clarity;
- testability;
- schema completeness;
- lifecycle completeness;
- authority;
- safety;
- compatibility;
- normative/reference separation;
- implementation drift;
- undocumented behavior;
- missing tests;
- vendor/implementation leakage;
- AI-created assumptions not present in the contract.

Use verdicts:
- Incorrect
- Ambiguous
- Incomplete for current scope
- Intentionally deferred
- Optional improvement

Then assign severity if useful:
- Critical
- High
- Medium
- Low

Read `references/review-severity.md`.

## Normative language

Use:
- MUST
- MUST NOT
- SHOULD
- SHOULD NOT
- MAY

A MUST should normally be deterministically verifiable.

Do not use MUST for:
- rhetorical emphasis;
- subjective quality;
- implementation preference that is not required for interoperability/safety.

Do not hide mandatory behavior in examples.

Define Chinese equivalents when the contract is bilingual.

When an edit is described as terminology cleanup, semantic propagation, or another semantic-only
change, perform a normative keyword delta audit for MUST, MUST NOT, SHOULD, and MAY. A delta is not
automatically forbidden, but an unexplained change in normative strength is a contract review failure.
Report its location, reason, and whether it introduces a new architecture decision.

Read `references/normative-contract.md`.

## Clause IDs

Important conformance-affecting rules SHOULD have stable IDs.

Examples:
- `STATE-001`
- `OP-004`
- `DISC-007`
- `SAFE-003`

Rules:
- IDs identify rules, not paragraphs.
- Do not assign IDs to every explanatory sentence.
- Preserve IDs across editorial rewrites.
- Breaking semantic changes require explicit version/change handling.

## Terminology and identity

Formalize:
- canonical term;
- definition;
- identity scope;
- owner;
- lifecycle;
- relation to neighboring identities.

Check ambiguous pairs such as:
- Device vs Node;
- Runtime vs Process;
- Registry vs Capability Registry;
- Action vs Operation;
- Source vs Producer vs Authority;
- Capability Declaration vs Availability.

Do not invent these distinctions when the architecture does not need them.

## Schema contract

For each core object, define as applicable:
- object name;
- namespace/version;
- required fields;
- optional fields;
- field type;
- allowed values;
- unit/frame/timestamp semantics;
- mutability;
- authority/producer;
- lifecycle;
- errors;
- extension mechanism;
- compatibility behavior.

Read `references/schema-contract.md`.

## State machines

For every lifecycle-bearing object, define:
- initial state;
- all legal states;
- terminal states;
- legal transitions;
- transition trigger;
- guards/preconditions;
- side effects;
- emitted events;
- timeout;
- cancellation;
- invalid transition behavior;
- duplicate/idempotent request behavior;
- disconnect/restart behavior;
- reconciliation/recovery behavior.

Read `references/state-machine.md`.

## Authority, cache, and derived state

When state truth matters, formalize:
- authority;
- producer/source;
- cache;
- derived_from;
- freshness;
- expiry;
- conflict handling;
- update permission;
- write-back prohibition.

An AI, cache, or fused world model MUST NOT become the authority for a physical fact merely because it
has a copy.

## Discovery and registration profiles

When registry/heartbeat discovery is in scope, define:
- registration request/response;
- identity validation;
- endpoint;
- manifest/hash;
- lease duration;
- heartbeat cadence;
- degraded/offline thresholds;
- duplicate identity behavior;
- re-registration;
- registry restart;
- node restart;
- version negotiation;
- disconnect vs lease expiry;
- availability invalidation/recovery.

Do not confuse abstract discovery semantics with one reference discovery profile.

## Safety contract

When safety-critical execution is in scope, formalize:
- native/lower-level safety authority;
- software validation authority;
- orchestration safety;
- veto ordering;
- default-deny/fail-safe behavior;
- stale-state handling;
- unknown/missing constraint handling;
- validation order;
- TOCTOU risk;
- revalidation before dispatch when required;
- cancel vs stop vs emergency stop;
- validator failure behavior;
- audit linkage.

AI reasoning MUST NOT be treated as the final safety authority unless the architecture explicitly and
safely defines that responsibility.

Read `references/safety-contract.md`.

## Reference implementation discipline

Separate:
- Normative Standard
- Reference Runtime
- Reference Profile
- Mock / Example
- Vendor Adapter Validation

Reference implementation behavior MUST NOT become normative merely because the current code happens to
work that way.

Current implementation limitations MUST NOT silently weaken the contract.

When code conflicts with the Contract:
- report the conflict;
- do not rewrite the Contract merely to make tests pass.

## Contract traceability chain

Maintain the following chain at the granularity appropriate to the contract:

```text
Human Guide Principle
        ↓
Normative Clause
        ↓
Schema / Contract Element
        ↓
Runtime Semantics / State Machine
        ↓
Conformance Requirement
        ↓
Executable Test
        ↓
Reference Implementation / Example
```

Every important MUST or MUST NOT clause SHOULD be traceable to an implementation contract. Every mandatory
schema field or runtime behavior in the current release MUST have an upstream normative basis. Every
mandatory conformance test MUST trace to a normative clause; a test for behavior the standard never
requires is a consistency defect.

Do not allow a requirement with no runtime semantics or testable landing point. Do not allow a
mandatory conformance check with no supporting requirement. Deferred or future capabilities MUST NOT
enter current-version mandatory conformance.

Important rules SHOULD use stable Requirement IDs or an equivalent stable reference mechanism, but
this skill does not require a particular ID format.

An **unmapped mandatory requirement** or an **unsupported mandatory conformance check** is a contract
consistency defect.

An optional review matrix may use columns such as:

| Principle | Normative Clause | Schema | Runtime | Conformance | Test |
|---|---|---|---|---|---|

The matrix is a useful representation, not a mandatory project format.

For critical rules, define as applicable:
- positive test;
- negative test;
- lifecycle test;
- failure test;
- boundary test;
- safety test where relevant.

Read `references/traceability.md`.

## Contract vs Implementation Separation

The Engineering Contract defines:
- what MUST be true;
- what is allowed or forbidden;
- what fails and how rejection is observed;
- who owns each fact;
- required runtime semantics;
- how conformance can be determined.

It MUST NOT prescribe incidental implementation structure by default, including:
- source-code file paths;
- class or function names;
- internal module layout;
- a particular third-party library;
- implementation tasks.

Those details belong in `contract-implementation-planner` unless they are themselves an external
compatibility contract. The contract constrains implementation behavior; it does not prescribe
incidental implementation structure.

Read `references/contract-implementation-separation.md`.

## Concrete Boundary Contracts

For each important external, module, or protocol boundary, specify the applicable parts of:
- contract name;
- owner or authority;
- input and output;
- preconditions and postconditions;
- expected failures and rejection behavior;
- mutability and idempotency;
- timeout, cancellation, and ordering;
- freshness;
- permission or safety gate;
- observability or audit;
- extension behavior.

Not every dimension applies to every boundary. Omitted dimensions MUST NOT leave a load-bearing
behavior to implementation guesswork.

Read `references/boundary-contract.md`.

## Verifiable Behavior and Requirement Classification

An observable runtime requirement SHOULD identify a condition or trigger, expected behavior,
failure or rejection behavior, and a verification method. `Given / When / Then` is an allowed
expression, not a mandatory format.

Classify important requirements as applicable:
- Runtime-testable;
- Schema-testable;
- Static-conformance-testable;
- Integration-testable;
- Safety-testable;
- Review-only / not automatically testable.

Review-only requirements MUST explain why deterministic automation is not suitable. Schema
invariants, static constraints, namespace rules, and immutable identity rules MAY be verified by
schema validation, static validation, contract inspection, or conformance checks. Do not require a
scenario for every requirement mechanically.

Read `references/verifiable-behavior.md`.

## Open Contract Issue Protocol

When the source architecture does not determine a load-bearing engineering behavior, do not guess.
Record an `OPEN CONTRACT ISSUE` with at least:
- Issue ID;
- source principle or section;
- affected requirements;
- missing decision;
- why implementation cannot safely infer it;
- downstream tasks blocked;
- proposed options when useful;
- resolution status.

A load-bearing open issue MUST block downstream planning and coding for the affected behavior.
Unrelated requirements MAY continue through the workflow.

Read `references/open-contract-issue.md`.

## Contract Readiness Gate

Before implementation planning, check:
- canonical terms are stable;
- the architecture source is identified;
- important requirements have stable IDs or section anchors;
- major boundaries are defined;
- state machines are sufficient for the claimed scope;
- expected failures and authority are defined;
- safety responsibility is defined where applicable;
- conformance has a landing point;
- load-bearing open contract issues are resolved;
- deferred items are separate from current mandatory scope.

Output exactly one status:

`CONTRACT READY FOR IMPLEMENTATION PLANNING`

or

`CONTRACT NOT READY FOR IMPLEMENTATION PLANNING`

The second status does not prevent work on unaffected requirements.

Read `references/contract-readiness.md`.

## Downstream Execution Anchors

Planner and Coding workflows MUST use a stable Requirement ID or Section Anchor as the execution
anchor. The contract does not generate a file map, atomic task list, or coding sequence; those are
downstream planning artifacts.

The traceability chain remains:

```text
Human Guide Principle
        ↓
Normative Clause
        ↓
Schema / Contract Element
        ↓
Runtime Semantics / State Machine
        ↓
Conformance Requirement
        ↓
Executable Test
        ↓
Reference Implementation / Example
```

## Agent-Neutrality

The core Contract workflow is tool- and Agent-neutral. It MUST NOT require a named coding product,
vendor command, task API, permission API, or subagent API. Platform-specific integration MAY exist
only as an optional adapter or example and MUST NOT alter the Contract / Plan / Task semantics.

## AI coding guardrails

When this contract will guide a coding agent, explicitly state:
- what the AI may change;
- what it must not reinterpret;
- source-of-truth documents;
- stable clause IDs;
- required tests;
- forbidden architecture shortcuts;
- vendor leakage rules;
- when to stop and report ambiguity instead of guessing;
- whether spec changes require human review.

The AI SHOULD stop and report when:
- two normative clauses conflict;
- the Guide and Contract conflict;
- a required schema field is undefined;
- a state transition is missing;
- safety behavior is ambiguous;
- implementation would require inventing a new architecture decision.

## Working-draft maturity

A Working Draft may be incomplete.

Classify gaps before severity:
- Incorrect
- Ambiguous
- Incomplete for current scope
- Intentionally deferred
- Optional improvement

Do not demand production-grade federation, certification, or recovery mechanisms if they are outside
the declared release scope.

However, if the release claims an implementable contract for a feature, the semantics necessary for
independent implementation must be present.

## Output patterns

A mature engineering contract commonly contains:
1. status/scope;
2. terminology;
3. architecture boundaries;
4. object model;
5. normative clauses;
6. schemas;
7. state machines;
8. authority rules;
9. errors;
10. discovery/lifecycle;
11. safety;
12. versioning/extensions;
13. reference profile;
14. conformance;
15. traceability;
16. intentionally deferred items.

Do not force this exact table of contents when not needed.

## Final quality gate

Before finishing, ask:

1. Can two independent teams implement compatible behavior?
2. Are architecture decisions inherited rather than silently reinvented?
3. Are important MUST clauses testable?
4. Do important clauses have stable IDs?
5. Are schemas sufficiently precise?
6. Are ownership and authority explicit?
7. Are state machines complete for the claimed scope?
8. Are failure, timeout, cancel, disconnect, and restart semantics defined where needed?
9. Are safety veto order and fail-safe behavior explicit?
10. Are normative and reference implementation behavior separated?
11. Are deferred items clearly marked?
12. Can clauses be traced to tests?
13. Can tests be traced to implementation?
14. Did the AI have to guess anything important?
15. Is vendor/implementation detail contained in the correct layer?
16. Does the Contract remain aligned with the human-centered Guide?
