---
name: technical-specification-guide
description: >
  Create, extend, or review detailed human-readable technical architecture guides and white papers
  that preserve technical depth while helping first-time readers understand why a system is designed
  the way it is. Use for PAIS, Physical AI, robotics, distributed systems, runtimes, protocols,
  architecture principles, and similar systems when the user wants one coherent, detailed technical
  document with rationale, examples, counterexamples, diagrams, and architecture reasoning.
  When a user provides a golden/master document, preserve its information and narrative unless an
  explicit change is requested. Do not silently simplify, invent architecture, or insert writing-process
  language into the publication.
metadata:
  version: "0.6.0"
  role: "human-readable-detailed-technical-guide-with-source-readiness-audit"
---

# Technical Specification Guide

Create **detailed technical documents that humans can understand without reducing the technical content**.

The objective is not "make it simpler."

The objective is:

> Preserve the real architecture, constraints, edge cases, and implementation context, while making the reasoning easier to follow.

A first-time reader should finish the document with more understanding, not fewer facts.

---

# 1. Core philosophy

## 1.1 Detailed does not mean difficult to read

A detailed guide may contain:
- exact technical distinctions;
- lifecycle concepts;
- architecture boundaries;
- implementation context;
- examples;
- counterexamples;
- diagrams;
- reasoning questions;
- normative rules when they are important to understanding.

Do not remove useful technical material merely because the audience is new.

For a first-time reader, prefer:
- better sequencing;
- clearer cause-and-effect;
- concrete examples;
- explicit boundary explanations;
- local definitions at the moment of need.

Do **not** prefer:
- broad simplification;
- replacing technical paragraphs with summaries;
- creating many new teaching terms;
- turning the document into a training handout.

## 1.2 Reader value rule

Every sentence in the publication should earn its place for the target reader.

A sentence should normally add information about:
- the system;
- the architecture;
- the design decision;
- the engineering consequence;
- the example;
- the boundary;
- the implementation context;
- the future direction.

Default to removing publication prose whose primary purpose is to describe:
- how the document was written;
- which Skill created it;
- which draft was the "golden master";
- what happened in the current editing round;
- what an Agent or another model did;
- whether the document is "human-readable";
- what internal review workflow produced it;
- whether it is "Git Commit Ready."

Read `references/publication-cleanliness.md`.

## 1.3 Narrative continuity over local completeness

Human understanding is built through a continuous chain of engineering questions.

Prefer:

existing system
→ what it already solves
→ remaining problem
→ new abstraction
→ why that abstraction is needed
→ consequence of violating the boundary
→ next engineering problem

Do not break a coherent technical story into isolated knowledge cards merely because each card is locally clear.

A paragraph can be excellent while the document is still bad if the whole document feels fragmented.

Read `references/narrative-continuity.md`.

## 1.4 Conceptual expansion budget

Do not explain one concept by inventing several new concepts unless they are genuinely necessary.

Before adding a new term, ask:

> Does this term remove a real misunderstanding, or merely increase taxonomy?

If a concept can be explained using existing vocabulary, do that.

Avoid:
- creating parallel classification axes without need;
- introducing "helper" terms that then require their own chapter;
- turning a simple distinction into a taxonomy.

Read `references/concept-budget.md`.

---

# 2. Golden master preservation mode

When the user identifies an existing document as:
- golden master;
- preferred version;
- canonical draft;
- best version;
- source to evolve from;

enter **Golden Master Preservation Mode** by default.

In this mode:

1. Read the full relevant source before editing.
2. Preserve useful technical information.
3. Preserve the source's successful narrative rhythm.
4. Preserve examples that carry engineering meaning.
5. Preserve counterexamples that expose real failure modes.
6. Preserve important implementation context.
7. Prefer additive clarification over replacement.
8. Prefer local reordering over global restructuring.
9. Do not rewrite merely to make the document "cleaner."
10. Do not reduce length merely because the document is long.

The target document may become longer than the golden master if more explanation is needed.

## 2.1 Omission ledger

Any meaningful removal from a golden master must be justified.

For every removed technical block, verify:
- what information was removed;
- why removal improves the reader's understanding;
- whether the information is preserved elsewhere;
- whether the removal changes architecture meaning.

If the answer is unclear, keep the material.

A final publication does not need to contain the ledger; the editing/review process does.

Read `references/golden-master-preservation.md`.

`references/golden-style.md` is a PAIS-specific worked style benchmark. It is example material for
studying detailed exposition, not a generic architecture rule or a required table of contents.

---

# 3. No silent architecture invention

A human guide explains architecture. It must not quietly redesign architecture just to make the prose flow.

If the source does not decide an issue such as:
- Device-to-Node cardinality;
- Node-to-process cardinality;
- Node-to-runtime cardinality;
- exact Discovery lifecycle;
- exact handshake ordering;
- whether Authority must be globally unique;
- whether every Action must create an asynchronous Operation;
- where Available Capability is computed;
- whether a particular profile is normative or reference;

do not invent a single answer for narrative convenience.

Instead:
- keep the explanation at the level actually supported by the architecture;
- mark the point as unresolved if necessary;
- distinguish conceptual intuition from formal protocol semantics.

Never turn a teaching diagram into an accidental normative state machine.

Read `references/no-silent-invention.md`.

---

## 3.1 Canonical Standardization Root Object Rule

Before expanding an object model, Identity, Manifest/Descriptor, Lifecycle, Discovery, Permission,
State, or Capability, explicitly identify the **Canonical Standardization Root Object**: the entity
that the standard directly standardizes, addresses, describes, and governs.

Every technical standard SHOULD make its canonical root object explicit. Core objects must be able to
answer “who owns or contains this?” in the standard's model. An internal implementation element that
is not directly governed by the standard must not be promoted to a peer standard entity merely for
writing convenience.

Do not infer child objects, component objects, nested objects, internal graphs, or similar ontology
from the existence of a root object. “First clarify the standardized atom, then expand the object
model.” Changing the root object is an architecture decision, not a terminology-only substitution.

---

## 3.2 Deep Architecture Audit Method

When reviewing a standard, protocol, platform architecture, layered system, runtime, interface
standard, Agent or device architecture, Task / World / Capability model, or safety / permission
architecture, activate the **Deep Architecture Audit**. This is a reasoning method, not a fixed
publication template: apply the checks that fit the document and its declared scope.

The audit checks, as applicable, are:

- **Concept Closure**: whether a core concept forms a reader-usable loop from identity, purpose,
  neighbors, layer, responsibility, ownership, consumption, normal behavior, failure boundaries,
  and later use—not merely whether it has a definition;
- **Layer Responsibility**: whether responsibilities stay within their layer, with upward leakage,
  downward leakage, responsibility creep, and abstraction leakage named at the crossed boundary;
- **Orthogonal Taxonomy**: whether type, state, location, source, lifecycle, capability, profile,
  and implementation labels answer the same question before being made one taxonomy;
- **Responsibility & Guarantee Boundary**: whether names such as Safety, Security, Authority,
  Validation, Recovery, Supervisor, Controller, Compliance, or Trust imply guarantees or ownership
  that the architecture does not provide;
- **Cross-Section Concept Consistency**: whether a concept remains stable across Definition,
  Principle, Object Model, Runtime, Example, and Roadmap;
- **Architecture Independence**: whether claims such as independent, reusable, vendor-neutral,
  model-agnostic, or transport-agnostic survive replacement of the consumer, runtime, or lower
  implementation, while keeping normative semantics separate from reference implementation;
- **Reader Mental Model Integrity**: whether the explanation follows the engineering cause-and-effect
  chain and establishes boundaries without either flattening technical depth or multiplying terms;
- **Human Guide → Engineering Contract Handoff**: whether a gap is an architecture explanation
  problem or an Engineering Contract formalization problem, and whether the handoff is explicit.

For a detailed method and generic examples, read
`references/deep-architecture-audit.md`. When a document makes strong independence or reuse claims,
the reviewer MUST actively perform Independence and Boundary checks. Do not turn this method into a
requirement that every concept fill every audit dimension, every document use identical chapters, or
the Human Guide define a complete schema, API contract, retry protocol, state machine, or conformance
suite that belongs to `engineering-contract-spec`.

### Deep Audit Finding Format

Findings SHOULD be specific enough to be actionable. Use this structure when a concern is found:

1. **Finding** — the precise problem;
2. **Audit Principle** — the triggered deep-audit rule;
3. **Evidence** — the relevant prose, diagram, table, example, or cross-section comparison;
4. **Reasoning** — why the evidence violates or weakens the principle;
5. **Risk** — architecture, interoperability, responsibility, or reader-understanding risk;
6. **Recommendation** — the smallest direction that resolves the issue without inventing design;
7. **Ownership** — Human Guide, Engineering Contract, Implementation, or no change needed.

Do not use vague findings such as “unclear” without evidence and ownership. Do not encode a
project-specific answer as a generic audit rule.

## 3.3 Whitepaper & Rationale Quality Method

For an architecture whitepaper, technical architecture guide, interface or protocol rationale,
standard design guide, or other human-facing technical document that also contains normative
requirements, activate **Whitepaper & Rationale Quality**. This is an argument-quality audit, not a
fixed article template. It requires reasoning obligations, not identical section structures.

The method checks whether important design conclusions are earned by the document's evidence:

- **Problem-first Reasoning** and **Causal Closure**: establish existing reality, remaining problem,
  consequence, root cause, responsible layer, design choice, and normative consequence as far as the
  scope requires;
- **Importance / Necessity / Urgency**: test why a problem matters, why non-adoption harms the target
  architecture, why the current stage calls for action, and why the current layer owns it;
- **Information Density** and **Empty Claim Detection**: apply the Delete Test and require claims
  such as “more flexible” or “more reliable” to name a comparison, mechanism, object, and scenario;
- **Failure-driven Rationale** and **Alternative Sufficiency**: use plausible failure or
  counterexample chains and explain why an existing mechanism is insufficient when a new abstraction
  depends on that premise;
- **Normative / Informative Separation** and **Normative Strength Justification**: keep rationale
  distinct from requirements and justify new MUST / SHOULD / MAY strength without changing frozen
  source-of-truth wording;
- **Responsibility Test**: reuse Deep Architecture Audit's layer and guarantee-boundary checks to
  explain why the issue belongs to this layer;
- **Reader-derived Conclusion**: test whether the preceding facts, constraints, and failure modes
  let a technical reader substantially derive the conclusion rather than merely receive an assertion;
- **Whitepaper ≠ Specification Dump**: preserve technical depth while explaining relationships,
  causes, boundaries, and consequences instead of presenting only object, schema, API, or MUST lists.

Read `references/whitepaper-rationale-quality.md` for the WP-01..12 checks. Reuse
`references/deep-architecture-audit.md` for layer responsibility, responsibility / guarantee
boundaries, and architecture independence; do not duplicate those audits here. The method does not
require every section to expose Importance, Necessity, Urgency, Failure, Alternative, or Normative
labels, and it does not force the Human Guide to become a complete Engineering Contract.

## 3.4 Source Readiness Audit

Before a document enters a final publication workflow, run the **Source Readiness Audit** against
the actual Markdown source. The audit is a pre-publication review, not a replacement for reading the
technical content.

Use `scripts/audit_document_structure.py` for deterministic findings, then apply the reasoning
checks in `references/document-structure-ontology.md`. The audit MUST cover, as applicable:

- heading ontology and hierarchy, including unexplained H2→H4 or deeper jumps;
- visible legacy numbering after information-architecture reorganization;
- legacy visible numbering MUST be resolved or explicitly reviewed;
- pseudo-headings that are local labels, lead-ins, callouts, or question metadata;
- outline explosion and runtime microstep inflation;
- lists, fenced code, ASCII diagrams, tables, and normative keyword counts;
- assessment-section discovery and handoff to `assessment-question-designer`;
- source hash and before/after normative keyword delta when a repair is proposed.

The deterministic result uses these statuses:

- `SOURCE_READY`: no blocking source-structure finding remains;
- `SOURCE_REPAIR_REQUIRED`: a deterministic or explicitly review-required finding must be repaired
  by the responsible authoring Skill before freeze;
- `SOURCE_BLOCKED`: the source cannot be safely repaired without a human architecture decision or
  missing information.

The script reports heuristics as findings requiring reasoning review. It MUST NOT claim that a
regular expression has established architectural meaning. A source repair MUST preserve technical
meaning, architecture decisions, normative strength, and source-grounded assessment evidence.
After any repair, rerun the complete audit and record a normative keyword delta.

# 4. Semantic propagation

Changing a core concept creates obligations across the whole document.

If you change or clarify a term such as:
- Device;
- Node;
- Identity;
- Manifest;
- State;
- Authority;
- Capability;
- Operation;
- Discovery;
- Safety;

perform a **Semantic Propagation Audit**.

Check every affected:
- definition;
- heading;
- diagram;
- table;
- example;
- field name;
- reference implementation;
- architecture question;
- conclusion;
- registration and lifecycle;
- state authority and ownership;
- parameter/action ownership;
- capability ownership;
- event subject;
- permission, safety, and audit scope;
- runtime and reference runtime;
- conformance;
- future sections where the old model may still leak.

Example:

If "Physical Node" is no longer identical to "Device", then review:
- Device Identity;
- device_id;
- Device Manifest;
- Node Manifest;
- examples containing multi-device nodes;
- capability ownership language.

Do not solve one conceptual problem at the front of the document while creating contradictions later.

A canonical architecture change is not complete until all semantic dependents have been audited.
Semantic propagation is not blind global search-and-replace: distinguish standard-object terms from
real-world hardware terms, implementation terms, and examples whose wording is intentionally local.

Read `references/semantic-propagation.md`.

---

# 5. Preserve normative strength

A human guide may quote or explain MUST / SHOULD / MAY rules.

Do not silently strengthen or weaken them.

Examples of invalid transformations:
- SHOULD → MUST because it sounds safer;
- MAY → SHOULD because it is a useful pattern;
- "long-running actions should expose Operation semantics" → "all actions must be asynchronous";
- reference profile behavior → standard requirement.

When paraphrasing normative rules:
- preserve their strength;
- preserve their scope;
- preserve explicit exceptions;
- keep "reference implementation" distinct from "required standard behavior."

If a new normative rule appears necessary, flag it as an architecture decision instead of inserting it.

## 5.1 Normative keyword delta audit

For terminology cleanup, semantic propagation, structural cleanup, publication preparation, and tiny
patches, compare the before/after use of **MUST**, **MUST NOT**, **SHOULD**, and **MAY**. The counts do
not have to remain unchanged, but any unexplained normative keyword delta is a review failure when
the task did not intend to change normative strength.

If a change such as SHOULD → MUST, MAY → SHOULD, or MUST → SHOULD occurs, report its location, reason,
and whether it represents a new architecture decision. Do not hide such a change as polishing.

---

# 6. Publication cleanliness

The final publication should read like a document about the technical subject, not a report about document production.

Normally exclude phrases like:
- "this is a human-understanding guide";
- "this document uses the golden master";
- "this round adds...";
- "the Skill requires...";
- "the next Engineering Contract will...";
- "the acceptance review found...";
- "Git Commit Ready";
- "the model preserved...".

Document-system information may appear once, when genuinely relevant, for example:
- document status;
- intended scope;
- relationship between a design guide and a normative specification.

Do not repeat the writing workflow throughout the technical body.

---

# 7. Modes

## 7.1 Authoring mode

Use when no strong prior document exists.

Workflow:
1. Identify the engineering problem.
2. Establish the existing architecture.
3. Explain what it already solves.
4. Show the remaining gap.
5. Introduce the minimum necessary new abstraction.
6. Explain the new abstraction in context.
7. Preserve technical depth.
8. Use realistic examples and counterexamples.
9. Add diagrams only when they reduce cognitive load.
10. Review the whole narrative, not only individual sections.

## 7.2 Extension mode

Use when evolving an existing document.

Workflow:
1. Read the complete relevant source.
2. Identify what is already good.
3. Preserve it.
4. Identify real reader confusion.
5. Make the smallest change that fixes that confusion.
6. Run semantic propagation if a core definition changes.
7. Check that no useful information was removed.
8. Check that no new taxonomy was created unnecessarily.
9. Re-read adjacent chapters for narrative continuity.
10. Compare the final result against the source, not only against the task checklist.

If the source is a golden master, apply Golden Master Preservation Mode.

## 7.3 Review mode

Review the actual publication text.

Do not accept:
- a prior AI review report;
- a revision report;
- a checklist;
- a self-declared quality gate;

as a substitute for reading the actual document.

A proper review must examine:
- real prose;
- real examples;
- real headings;
- real diagrams;
- real tables;
- real questions.

Read `references/review-method.md`.

## 7.4 Acceptance review mode

Acceptance is stricter than author self-review.

Acceptance must:
1. read the candidate itself;
2. read the source/golden master when relevant;
3. compare them directly;
4. identify what improved;
5. identify what became weaker;
6. inspect publication cleanliness;
7. inspect terminology propagation;
8. inspect numbering and cross-references;
9. inspect narrative continuity;
10. explicitly ask whether the candidate is actually better.

The authoring agent's own "Final Quality Gate: PASS" is not independent evidence.

## 7.5 Tiny Patch Mode and Freeze Gate

Use **Tiny Patch Mode** when the architecture is stable and only a short, explicitly bounded defect
list is in scope. In this mode:

- modify only the listed defects;
- keep the diff small and concentrated;
- run targeted grep and semantic scans;
- run the normative keyword delta audit.

Do not use a tiny patch as an occasion to polish the whole document, restructure chapters, expand
explanations, add taxonomy or architecture concepts, reinterpret frozen decisions, or turn a local
repair into a rewrite.

A useful lifecycle is:

```text
Draft → Architecture Review → Semantic Propagation
      → Canonical Terminology Cleanup → Human Acceptance
      → FREEZE → Publication
```

After the Freeze Gate, treat the source content as immutable for publication purposes. Fix fonts,
page breaks, TOC, headers/footers, table width, code wrapping, and page numbers in the publication
layer; do not modify the frozen content source to solve those layout problems. A project may use a
status such as `MARKDOWN READY FOR FREEZE`, but the status name is not a universal industry token.

---

# 8. Explanation strategy

For a difficult principle, use only as much structure as needed.

Possible elements:
- current engineering reality;
- problem;
- design principle;
- why it exists;
- failure mode;
- example;
- counterexample;
- boundary with adjacent layers.

Do not force all elements into every section.

Avoid repetitive micro-structure such as:

Definition
→ Why
→ Example
→ Counterexample
→ Mental model

for every concept.

The reader should feel one continuous technical story.

---

# 9. Examples and counterexamples

Examples should:
- use the same canonical terminology as the main text;
- be realistic;
- connect directly to the current concept;
- avoid introducing new unresolved architecture.

Counterexamples should explain:
- why the mistake is tempting;
- what assumption is wrong;
- how the system fails;
- what boundary is violated.

Do not use obviously absurd distractors.

---

# 10. Architecture questions

Reasoning questions are useful when they test boundaries, authority, semantics, or failure handling.

Keep them when they strengthen understanding.

Do not preserve them merely because a template says every guide needs questions.

Questions should:
- test reasoning rather than keyword recall;
- use plausible distractors;
- not introduce architecture decisions absent from the main text;
- use the same canonical terms as the main text.

Read `references/reasoning-questions.md`.

---

# 11. Diagrams

A diagram must reduce cognitive load.

Before adding a diagram, ask:
- what question does it answer?
- does it show structure, flow, responsibility, or contrast better than prose?
- does it accidentally imply an ordering or lifecycle that is not actually normative?

Do not create a linear arrow chain merely because a concept is easier to visualize that way.

After editing diagrams, perform publication QA:
- numbering order;
- references;
- captions;
- terminology;
- consistency with prose.

Read `references/publication-qa.md`.

---

# 12. Terminology discipline

Maintain a canonical terminology ledger for important terms.

For physical quantities, do not casually substitute semantically different terms.

Examples:
- mass is not automatically weight;
- pose is not automatically position;
- source is not automatically authority;
- observed state is not authoritative state;
- declared is not native;
- native is not available;
- available is not composite.

If examples use different names for the same canonical concept, either:
- normalize them;
- or explain why the names differ.

## 12.1 Orthogonal classification dimensions audit

When multiple classification terms appear, determine whether they are one taxonomy or independent
dimensions. For each dimension, state:

1. what question it answers;
2. its possible values;
3. whether an object can also carry a value from another proposed dimension;
4. whether combinations across the dimensions naturally exist.

If combinations such as A1+B1, A1+B2, A2+B1, and A2+B2 are all coherent, the dimensions MUST NOT be
collapsed into one taxonomy. Do not generate a large classification tree merely because separate
axes look more complete when combined.

---

# 13. Independent-standard discipline

If a standard is intended to be independent and reusable, do not let the primary narrative make one consumer appear to define the standard.

Prefer:
- generic upper-layer system first;
- named project as a reference consumer or worked example.

Example:

PAIS
→ upper-layer Physical AI systems
  → Labor-FSD
  → standalone robot agent
  → third-party automation system

Use the user's main project heavily as an example when useful, but do not accidentally redefine the standard as that project's private API.

---

# 14. Final quality gate

A document is not good because it contains:
- a "Why" section;
- examples;
- five diagrams;
- twenty-five questions;
- a reading path.

Those are only tools.

## 14.1 Scope → Runtime → Conformance traceability

For the declared release scope, perform a basic traceability check:

```text
Normative Scope
      ↓
Reference Runtime / Executable Semantics
      ↓
Conformance
      ↓
Reference Example / Validation
```

If a capability is MUST in the target scope, the reference runtime or explicit executable semantics
must provide a corresponding landing point. If conformance forcibly checks a capability, the scope
must contain the requirement or an explicit basis for it. Do not require A in scope while implementing
neither A nor its semantics, or test B/C without a normative basis. Future or deferred material must
not leak into current-version mandatory conformance.

The Human Guide need not contain a complete contract matrix, but it must check that this chain closes.
Detailed implementation-level traceability belongs to `engineering-contract-spec`.

If Whitepaper & Rationale Quality is active, the final review MUST include the applicable WP-01..12
checks. Not every WP check must produce a finding; the requirement is to inspect the applicable checks
and record any resulting evidence.

Before finishing, verify:

## Reader value
1. Does each section add technical understanding?
2. Is writing-process language absent from the publication?
3. Does the document talk primarily about the system, not about the document?

## Information fidelity
4. Was useful golden-master information preserved?
5. Were removals justified?
6. Did the revision accidentally simplify away technical depth?

## Narrative
7. Does the document read as one continuous technical explanation?
8. Are transitions driven by engineering problems rather than editorial structure?
9. Did local explanation fragments damage the whole?

## Concept budget
10. Did any explanation introduce unnecessary terms?
11. Did a simple idea turn into an unnecessary taxonomy?
12. Are new terms solving real reader confusion?

## Architecture fidelity
13. Did the guide silently invent an architecture decision?
14. Did any diagram imply a protocol/state machine that is not decided?
15. Did reference implementation behavior become normative?

## Semantic consistency
16. Were core-term changes propagated through the whole document?
17. Are Identity, Manifest, examples, diagrams, and questions aligned?
18. Are physical quantities semantically consistent?

## Normative fidelity
19. Were MUST / SHOULD / MAY strengths preserved?
20. Were reference profiles kept separate from normative rules?

## Publication QA
21. Are section numbers coherent?
22. Are figure/table numbers ordered and referenced correctly?
23. Are headings consistent?
24. Are examples and questions using canonical terminology?

## Comparative acceptance
25. If there was a golden master, is the candidate actually better?
26. What became weaker?
27. Would a human reader choose the candidate over the source?

If the candidate is not clearly better, do not call it final.

---

# 15. Relationship to engineering-contract-spec

The two skills serve different purposes.

This skill:
- preserves detailed architecture explanation;
- explains why;
- builds technical understanding;
- protects narrative and design intent.

`engineering-contract-spec`:
- formalizes exact implementation behavior;
- defines clauses, schemas, state machines, and conformance.

The existence of a future engineering contract is not itself publication content.

Mention the document relationship only when it gives the reader useful scope information.

---

# 16. Default behavior for PAIS-like work

When working on a PAIS-like architecture guide:

1. Treat a user-designated detailed version as the golden master.
2. Preserve technical depth.
3. Do not create a simplified "human version."
4. Improve readability by sequencing and explanation.
5. Keep examples, counterexamples, design rationale, and reasoning questions when they help.
6. Avoid process language.
7. Avoid taxonomy inflation.
8. Avoid silent architecture invention.
9. Run semantic propagation after changing core concepts.
10. Compare the finished candidate directly against the golden master.
