# Human Readability Gate

The Human Readability Gate protects the reader's mental model during FINAL RELEASE MODE. It sits
after source integrity and before DOCX publication. It is an orchestration gate: the
`technical-specification-guide` owns the architecture-writing review, while the publisher records
the result and routes defects.

## Required upstream checks

- first 10–15% answers the six reader-entry questions;
- one compact mental map appears before the large object model;
- a 3–7 idea reader-facing Design Spine explains why later objects exist;
- important principles propagate through problems, concepts, runtime, boundaries, examples, and
  counterexamples;
- concepts appear when an engineering problem requires them, with concrete explanation before
  abstraction where useful;
- the runtime reads as a continuous story rather than repeated What/Why/How/Boundary blocks;
- anti-AI language patterns, abstract-noun stacking, mixed-language fragmentation, and tail quality
  receive source-aware review;
- the review preserves technical depth, normative strength, and Engineering Contract boundaries.

## Status and repair loop

```text
source → reader-first audit → HUMAN_READABILITY_FAIL?
                       ├─ yes → technical-specification-guide repair → re-audit
                       └─ no  → assessment → freeze → DOCX/PDF publication
```

Deterministic counts are evidence, not a prose judge. A `HUMAN_READABILITY_REVIEW` result can be
accepted only with a recorded disposition explaining why the signal does not block comprehension.
An unresolved reader-entry failure, concept overload, broken runtime story, or isolated principle
constitution is blocking.
