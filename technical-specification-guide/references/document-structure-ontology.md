# Document Structure Ontology

This reference defines the generic source-structure rules used by the Source Readiness Audit. It is
not a required table of contents and it does not decide architecture content.

## Headings are semantic structure

Markdown headings are navigation and hierarchy semantics, not a convenient way to enlarge or bold a
local phrase. `#` through `######` represent real document levels. A heading should answer:

> Will this location be useful in the reader's navigation pane and in the document's outline?

If the answer is no, use a named paragraph style, bold lead-in, definition-list label, callout, or
question metadata instead.

An H2→H4 (or deeper) jump is a source-structure finding unless the document explicitly explains the
intermediate-level omission. A publication renderer preserves the frozen hierarchy; it does not
invent missing sections to make a malformed source look regular.

## Pseudo-heading heuristic

The following kinds of text are often local labels rather than navigation nodes:

- `发生了什么`, `示例`, `为什么需要`, `如何理解`, `上层系统拿它做什么`, `Failure / Boundary`;
- `场景`, `选项`, `正确答案`, `为什么正确`, `为什么其他选项错误`, `本题检验`;
- short labels such as `上层`, `PAIS`, `Native Device`, `State`, `Parameter`, or `Action` when
  they introduce one paragraph inside a larger section.

This is a review heuristic, not a universal ban. A label may be a real subsection when it has
independent scope, sustained content, and navigation value. The audit therefore emits an actionable
review finding; `technical-specification-guide` decides the smallest source-layer repair.

## Outline density and runtime hierarchy

Do not use a fixed heading-count threshold to fail a document. A long architecture guide can
legitimately contain many headings. Instead review heading density against paragraph count and the
reader's navigation needs.

Runtime explanations should prefer a small number of semantic stages with rich internal explanation.
Repeated `Runtime step 1` through `Runtime step N` headings are a review signal, not a mandatory
six-stage template. Internal actions can be numbered, bolded, or presented as a definition list
without becoming peer navigation nodes.

## Legacy numbering and traceability

When the information architecture is reorganized, visible section numbers MUST reflect the current
reading order. A sequence such as `64 → 28 → 39 → 79` is a reader-facing structural defect.
Preserve traceability with stable anchors, legacy IDs, metadata, or cross-reference IDs; do not keep
obsolete visible numbering merely because technical content was preserved.

## Review boundary

Deterministic checks can identify syntax, order, counts, and suspicious patterns. They cannot decide:

- whether a label deserves independent navigation;
- whether a runtime microstep is conceptually independent;
- whether a structural repair preserves architecture meaning;
- whether a heading change alters a normative or contractual interpretation.

Those decisions require source-aware reasoning and must be recorded with evidence, ownership, and a
minimal repair direction.
