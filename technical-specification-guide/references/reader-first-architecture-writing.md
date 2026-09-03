# Reader-first Architecture Writing

Reader-first writing is a method for preserving technical depth while giving a first-time engineer
an architecture they can reconstruct. It is not a simplified edition, a tutorial template, or a
request to add more headings.

## Reader outcome

After reading, an engineer should be able to explain in their own words:

- why the system exists and what the previous mechanism already solved;
- the central standardized object and its neighbors;
- the small set of ideas that constrain the architecture;
- one complete runtime flow, including a failure or uncertainty branch;
- where responsibility stops and which adjacent layer owns the next decision;
- why representative incorrect designs fail.

## Review sequence

### 1. Early Reader Mental Model Gate

Read only the first 10–15% and answer: What is this system? What problem does it solve? Why is the
common approach insufficient? What is the central object? What does a consumer gain? What is outside
the boundary? If the answers arrive only much later, record `READER_ENTRY_FAILURE` with evidence.
Do not force these answers into fixed headings.

### 2. One-page Mental Map

Before the large object model, provide one compact map: a diagram, before/after, short table, or
paragraph. It should show relationships such as who discovers whom, what a Node can tell a consumer,
and where a request crosses a deterministic boundary. It is a cognitive scaffold, not a compressed
glossary and not a normative protocol sequence.

### 3. Design Spine

Select roughly 3–7 reader-facing ideas from the complete architecture constitution. Each idea should
explain why a family of objects exists. Keep the full formal principles elsewhere. A good spine is
remembered without becoming a slogan list.

### 4. Principle Propagation

For each spine idea, find at least one concrete consequence in the problem statement, concept model,
runtime story, boundary discussion, example, or counterexample. Use the chain:

```text
principle → problem it prevents → object or rule → runtime consequence → failure if violated
```

The evidence may be distributed; repetition of the principle's name is not required. A late list of
principles with no earlier consequences is `PRINCIPLE_PROPAGATION_GAP`.

### 5. Concept introduction

Introduce the minimum term needed by the current engineering question. Prefer:

```text
concrete situation → intuitive meaning → formal concept → boundary and exact semantics
```

The formal term, fields, normative strength, and Engineering Contract handoff remain intact. Do not
replace a concept with a metaphor or create a new taxonomy just to explain it.

### 6. Runtime continuity

An end-to-end example should feel like one engineer following one system through time. Each stage
answers the previous stage's remaining question and creates the next one. Use paragraphs, diagrams,
tables, and short lead-ins where appropriate. Repeating a fixed What/Example/Why/How/Boundary block
is a signal to merge or vary the exposition.

### 7. Prose and language

Audit pattern overuse rather than banning words. Prefer direct technical statements over contrast
formulas, document-meta narration, stacked abstract nouns, artificial symmetry, and repeated rhetorical
closures. In Chinese-first documents, preserve canonical English object names but translate ordinary
relationships into natural Chinese.

### 8. Tail quality

Read the final 15% independently. Appendices, questions, future work, checklists, and handoff notes
must still explain responsibility and consequence. A long bullet list may be correct, but it should
have a clear purpose and transitions; do not delete technical detail merely to improve visual density.

## Finding boundary

Deterministic signals may count headings, repeated labels, lexical patterns, paragraph density, and
early-answer coverage. They cannot prove that a reader understands the architecture or that a
principle genuinely propagates. Record reasoning findings with evidence, risk, recommendation, and
ownership. The release gate may accept review warnings only when every blocking reader failure has a
documented source-aware disposition.
