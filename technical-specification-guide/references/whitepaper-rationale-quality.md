# Whitepaper & Rationale Quality

Use this reference to audit whether a human-facing architecture document actually proves its
important design conclusions. It applies to architecture whitepapers, technical architecture guides,
interface or protocol rationale documents, standard design guides, and similar documents that may
also contain normative requirements.

This is an argument-quality method, not a fixed article template. It defines reasoning obligations,
not identical section structures. Apply the checks that fit the document, its audience, and its
declared scope.

## Reasoning spine

For a significant design choice, prefer the causal progression:

```text
existing reality → remaining problem → consequence → root cause
→ responsible layer → design choice → normative consequence
```

Depending on context, a complete rationale may also show what the current system already solves, when
the problem appears, what non-adoption would cause, and how the choice removes or limits the problem.
Do not accept “X is important, therefore the system adopts X” as a complete rationale without the
missing causal evidence.

## Rationale Target Selection

Prioritize the full WP-01..12 audit for a design that satisfies any of these conditions:

1. introduces a new core abstraction;
2. changes a system or standard boundary;
3. leads to a MUST, MUST NOT, or key SHOULD;
4. involves Safety, Authority, Trust, Permission, or another strong responsibility or guarantee;
5. assigns a responsibility to a particular layer;
6. supports a strong claim of independence, reuse, vendor neutrality, model agnosticism, or
   transport agnosticism;
7. decides current-version or deferred scope;
8. introduces a mechanism because an existing mechanism is said to be insufficient; or
9. has system-wide impact on interoperability, compatibility, conformance, or implementation.

Ordinary field descriptions, local examples, small implementation hints, and already-supported
repetition do not need a mechanical full WP-01..12 pass. Select depth where it matters and remain
concise where it does not. This is a selection heuristic, not a new taxonomy.

## WP review checks

### WP-01 Problem Justification

Before accepting a core design choice, identify the existing reality, the remaining problem, the
conditions that expose it, and the concrete engineering consequence. The problem need not be new,
but it must be real within the document's scope.

### WP-02 Causal Closure

Trace the choice from current behavior through problem, consequence, root cause, responsible layer,
design response, non-adoption consequence, and resulting requirement. Stop at the depth needed for a
technical reader to understand the decision; do not mechanically fill every step in every section.

### WP-03 Importance / Necessity / Urgency

For a major decision, Importance and Necessity normally need explanation. Urgency needs explanation
only when a real time factor exists, such as:

- **Importance** — why the problem is worth solving;
- **Necessity** — why omitting the decision breaks or materially weakens the target architecture;
- **Urgency** — when applicable, why this version, deployment stage, or technical context calls for
  solving it now;
- **Non-adoption consequence** — what remains wrong if it is not solved;
- **Layer ownership** — why this layer, rather than a neighboring layer, should address it.

Relevant time factors may include a version window, deployment stage, scale transition, safety or risk
window, ecosystem transition, compatibility deadline, or a technical paradigm change that makes the
old mechanism start to fail. Do not manufacture urgency. Without real evidence, do not add phrases
such as “rapidly evolving,” “critical period,” “increasingly urgent,” or “now more than ever.”

These are questions, not mandatory headings. Do not accept adjectives such as better, safer, smarter,
or more extensible as their own evidence.

### WP-04 Information Density

Apply the Delete Test to publication prose: “If this sentence were removed, what information would
the reader lose?” Retain sentences that contribute a fact, distinction, causal relationship, design
rationale, boundary, engineering consequence, constraint, example, counterexample, or implementation
implication. Delete or rewrite prose whose only contribution is rhetorical completeness.

### WP-05 Empty Claim Detection

Challenge claims such as “significant value,” “solid foundation,” “more flexible,” “more reliable,”
or “AI-native.” An unsupported claim must have enough context-specific evidence to be understandable,
traceable, and technically defensible. Comparison, change, mechanism, affected object, and scenario
are common substantiation dimensions, not a five-field template that every sentence must display. If
the surrounding context already makes some dimensions clear, do not repeat them. The audit targets
unsupported usage, not particular words as an absolute blacklist.

### WP-06 Failure-driven Rationale

When an abstract rule depends on a hidden assumption, prefer a realistic failure or counterexample:

```text
failure / counterexample → violated assumption → engineering risk → architecture rule
```

Explain why the mistake is tempting and which boundary it violates. Do not require every concept to
have a counterexample when the risk is already clear by another explanation.

### WP-07 Normative / Informative Separation

Keep “why the design exists” distinct from “what an implementation must do.” Explanatory prose must
not silently create a new requirement, and a normative rule must retain enough rationale and scope
for a reader to understand its purpose. A document need not add literal Normative and Informative
headings if its structure and wording make the distinction clear.

### WP-08 Normative Strength Justification

For a newly proposed requirement, ask:

- why it is MUST rather than SHOULD;
- whether violation means the implementation is non-conforming;
- which reasonable exceptions a SHOULD permits;
- whether MAY is genuinely optional;
- whether reference-profile behavior was accidentally raised to a universal MUST.

If the author cannot justify the strength, record an architecture or Engineering Contract decision
instead of inventing a level. Never alter frozen or source-of-truth normative wording through prose
polish.

### WP-09 Alternative Sufficiency

When a new abstraction relies on “the existing mechanism is not enough,” name the existing mechanism
and show the precise insufficiency: missing semantics, authority, boundary, failure handling, or other
relevant property. Do not demand an artificial A/B/C comparison for small changes.

### WP-10 Responsibility Ownership

Reuse the Deep Architecture Audit for layer responsibility, guarantee boundaries, and independence.
The rationale must explain why the problem belongs to this layer without moving orchestration into an
interface, vendor details into a core standard, or implementation profile behavior into architecture
law. Do not duplicate the full layer audit here.

### Finding format reuse

Whitepaper & Rationale Quality findings SHOULD reuse the existing Deep Architecture Audit Finding
Format: Finding, Audit Principle, Evidence, Reasoning, Risk, Recommendation, and Ownership. The Audit
Principle may be a WP check such as WP-01 Problem Justification, WP-05 Empty Claim Detection, or
WP-11 Reader-derived Conclusion. If one issue triggers both audits, list the applicable principles
under one finding rather than emitting two findings with identical evidence and reasoning.

### WP-11 Reader-derived Conclusion

Remove the final design sentence mentally. Can a technical reader substantially infer the conclusion
from the preceding facts, constraints, failures, and alternatives? If not, strengthen the rationale
or mark the unresolved architecture decision. This is an argument-quality test, not a demand for
literary prose.

### WP-12 Specification Dump Detection

Detect documents that have become object lists, schema lists, API catalogs, MUST lists, or principle
lists without explaining why the elements exist, how they relate, where their boundaries are, or what
engineering consequence follows. Restore causal explanation without deleting technical depth or
formal requirements.

## Anti-patterns and boundaries

Do not force every section into Problem / Why / Failure / Solution / Alternative / Normative headings.
Do not require every concept to use every WP check, every document to share the same table of
contents, or every claim to become a formal contract clause. Use examples and counterexamples where
they reduce uncertainty, and use the smallest structure that lets a reader follow the reasoning.

When a gap is field-level schema, API behavior, retry or idempotency, state-machine, compatibility,
or conformance detail, use the Human Guide → Engineering Contract handoff. The Whitepaper audit may
identify that handoff, but it must not silently turn the guide into a coding-level contract.
