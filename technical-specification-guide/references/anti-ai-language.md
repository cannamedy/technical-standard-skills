# Anti-AI Language Audit

The goal is natural engineer-to-engineer explanation, not a keyword purge. A phrase can be correct
once and still become artificial when its pattern repeats across adjacent sections.

## Patterns to review

- **Contrast formula**: repeated “不是 A，而是 B” or “真正的问题不是 A，而是 B”. Keep a contrast
  when the distinction matters; otherwise state the engineering fact directly.
- **Meta-explanation**: “本节将…”, “这里必须先让读者…”, or commentary about how the document is
  being written. Replace it with the technical statement unless it is useful navigation.
- **Abstract noun stacking**: boundary, surface, semantics, context, governance, capability,
  framework, and similar nouns packed into one sentence. Name who acts, what is observed, and what
  fails.
- **Rhetorical closure**: repeated endings such as “这意味着…”, “因此…”, or “真正的价值在于…”.
  Vary the sentence shape or stop after the evidence has done its work.
- **Artificial symmetry**: every subsection forced into the same number of bullets or the same three
  sentences. Let the engineering relationship determine the size.
- **Empty emphasis**: “非常重要”, “核心中的核心”, or “从根本上” without an immediate mechanism,
  object, and consequence.
- **Template rhythm**: repeated What/Example/Understanding/Why/Consumer/Failure blocks. Convert
  local labels to lead-ins, merge adjacent fragments, or retain only the transitions that answer a
  real engineering question.

## Review boundary

The audit reports frequency and adjacency as deterministic signals. It does not ban Chinese-English
technical prose, a contrast that prevents a real category error, or a short rhetorical sentence that
serves as a genuine memory anchor. A reviewer must inspect the surrounding paragraphs and preserve
technical precision.
