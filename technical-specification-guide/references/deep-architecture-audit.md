# Deep Architecture Audit

Use this reference when a Human Guide needs a deeper review than definition and prose correctness.
The audit is a method for discovering architectural and reader-model defects; it is not a mandatory
template and does not require every document to contain every listed subsection.

## Activation triggers

Strengthen the audit for standards, protocols, platform architectures, layered systems, runtimes,
interface standards, Agent or device architectures, Task / World / Capability models, and safety or
permission architectures. Strong claims such as independent, reusable, vendor-neutral,
model-agnostic, and transport-agnostic require explicit Independence and Boundary checks.

## Audit dimensions

### 1. Concept Closure

For each core architecture concept, ask whether a reader can explain:

- what it is and why it exists;
- the problem it solves and its nearest distinction;
- its layer, responsibility, and explicit non-responsibility;
- who produces or owns it and who reads, calls, or consumes it;
- its relationships to adjacent objects;
- its normal behavior and failure or boundary behavior;
- whether later sections use the same meaning.

If a concept is only named or defined but its role, relationships, or boundaries cannot be explained,
record a Concept Closure finding. This tests the architecture mental model, not field-level contract
completeness.

### 2. Layer Responsibility Consistency

For every important responsibility, ask whether it belongs to the current layer, whether the layer
uses information it should not know, and whether upper-layer logic or lower-level implementation
details have leaked across the boundary. Check whether the layer still stands apart from a particular
consumer, and whether replacing its lower implementation leaves upper logic stable.

Name the crossing explicitly: which responsibility crossed which boundary, in which direction, and
why that creates responsibility creep or abstraction leakage.

### 3. Orthogonal Taxonomy

For every classification table, identify the question each axis answers. Type, state, location,
source, lifecycle, capability scope, profile, and implementation strategy are not automatically one
taxonomy. Ask: “Do these two labels answer the same question?”

If an object can coherently carry values from both proposed categories, the dimensions are likely
orthogonal and should be represented separately. Do not replace two axes with a larger enum merely to
make the table look complete.

### 4. Responsibility and Guarantee Boundaries

Audit terms that imply strong operational, safety, security, authority, validation, recovery,
supervision, control, compliance, or trust responsibilities. For each, state what the component does,
what it does not guarantee, what it does not replace, and where final responsibility resides when a
reasonable reader could otherwise infer too much from the name.

Distinguish architecture responsibility, operational responsibility, and safety or security
responsibility. Misleading naming is a finding even when the described mechanism itself is valid.

### 5. Cross-Section Concept Consistency

Trace each core concept through:

```text
Definition → Principle → Object Model → Runtime → Example → Roadmap
```

Check scope, layer neutrality, implementation assumptions, terminology, examples, and responsibility
boundaries at every point. A concept that is correct in its definition but changes meaning in a later
example or runtime section is a cross-section finding.

### 6. Architecture Independence

Test each independence claim against its implied dependencies:

- private concepts from a particular consumer;
- vendor-specific fields or assumptions;
- a required runtime hidden in the prose;
- reference behavior presented as normative semantics;
- a recommended implementation presented as the only architecture.

Mentally replace the consumer and lower implementation. If the claimed standard no longer holds,
record the dependency and clarify the boundary or narrow the claim.

### 7. Reader Mental Model Integrity

Prefer the explanatory progression:

```text
problem → why existing approaches are insufficient → new concept → distinction
→ normal behavior → boundary or counterexample → normative rule
```

Check that concepts are introduced before use, causes precede rules, examples are sufficient but not
excessive, and the document is not merely a long list of terms or keywords. Preserve technical depth
while avoiding unnecessary taxonomy and repetition.

### 8. Human Guide to Engineering Contract Handoff

When a review finds missing idempotency, retry, schema fields, state transitions, compatibility
rules, API precision, or conformance profiles, first decide whether the Human Guide's architecture
concept is unclear or whether the concept is clear and needs Engineering Contract formalization.

For the latter, the Human Guide should provide the governing rationale, boundaries, and intended
semantics, then make the Engineering Contract handoff explicit. Do not force the Human Guide to
become a JSON Schema, coding-level API contract, complete protocol, or full conformance suite.

## Structured finding

Report a substantive finding with:

1. Finding;
2. Audit Principle;
3. Evidence;
4. Reasoning;
5. Risk;
6. Recommendation;
7. Ownership: Human Guide, Engineering Contract, Implementation, or no change needed.

“Unclear” or “should be improved” without evidence, reasoning, and ownership is not a complete
finding. Recommendations must repair the identified boundary without silently inventing architecture.
