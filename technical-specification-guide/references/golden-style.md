# Golden Style — PAIS First Detailed Edition

## Why this is the benchmark

The benchmark is the first detailed PAIS v0.1 document because it successfully combined:
- architecture explanation;
- design principles;
- technical examples;
- counterexamples;
- boundary diagrams;
- object-level concepts;
- reference implementation context;
- architecture reasoning questions;
- future evolution.

Its strongest feature is that it helps a reader build an architecture mental model.

## Structural pattern

The guide may contain these chapter families in one master document:

1. Purpose and problem
2. Why the existing architecture is not enough
3. Design principles
4. Core concepts and object relationships
5. Important semantic distinctions
6. Boundaries with adjacent systems
7. Runtime intuition
8. Discovery / lifecycle intuition
9. Safety philosophy
10. Integration examples
11. Reference implementation context
12. Design rationale
13. Architecture reasoning questions
14. Future evolution
15. Development/review checklist
16. Conclusion and mental model

Do not force this exact table of contents on every project.

## Key writing pattern

A strong PAIS section often does this:

- "Adapter already solves vendor protocol translation."
- "But it does not tell a new AI what the device means."
- "Therefore PAIS adds a machine-readable physical contract."
- "Vendor-specific details stop below the boundary."
- "Here is the architecture."
- "Here is a robot/balance/camera example."
- "Here is what goes wrong if the boundary leaks."

This is the preferred teaching pattern.

## Useful repetition

Human technical guides may restate a core principle in several chapters if each restatement serves a
different teaching context.

Example:
- introduce State vs Action in principles;
- revisit it in the object model;
- revisit it in an architecture question.

This is acceptable when:
- the wording remains consistent;
- there is one canonical definition;
- repetition reinforces rather than mutates the concept.

## Detailed but readable

Add detail for:
- conceptual boundaries;
- non-obvious failure modes;
- architecture decisions;
- important exceptions;
- examples of correct and incorrect use.

Do not add detail simply to make the document longer.
