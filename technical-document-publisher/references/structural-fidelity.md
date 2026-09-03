# Publication Structural Fidelity Gate

Structural fidelity answers a different question from content fidelity:

> Did the Markdown semantic structure become the corresponding Word semantic
> structure, rather than merely becoming the same visible text?

## Deterministic checks

`validate_publication_structure.py` extracts both models and compares:

- H1-H6 count, order, level, and heading text;
- illegal hierarchy jumps introduced by the DOCX;
- body paragraphs containing literal `#{1,6}` heading syntax, excluding
  classified code/diagram blocks;
- independent ordered-list block count, item text, source start, `numId`, and
  `ilvl` nesting;
- bullet-list nesting and item text;
- fenced code line breaks and indentation;
- ASCII diagram classification and whitespace-preserving lines;
- table count and cell rows;
- `MUST`, `SHOULD`, and `MAY` counts;
- TOC field presence, cached entries, page numbers, and leader dots up to the
  profile depth;
- style-first Word semantics, with direct formatting treated as an exception
  requiring review.

## Blocking error codes

`HEADING_LEVEL_MISMATCH`, `HEADING_TEXT_MISSING`,
`HEADING_HIERARCHY_INVALID`, `LITERAL_MARKDOWN_HEADING_LEAK`,
`LIST_RESTART_MISMATCH`, `LIST_START_OVERRIDE_MISSING`, `UNEXPECTED_LIST_CONTINUATION`,
`LIST_LEVEL_MISMATCH`, `LIST_ITEM_TEXT_MISSING`, `ASCII_DIAGRAM_CLASS_MISMATCH`,
`ASCII_DIAGRAM_WRAPPED`, `CODE_INDENTATION_CORRUPTED`, `TABLE_ROW_LOSS`,
`CONTENT_FIDELITY_MISMATCH`, `TOC_EMPTY`, `TOC_INCOMPLETE`,
`TOC_PAGE_NUMBERS_MISSING`, and `TOC_LEADER_DOTS_MISSING` block release.

Source-level heading jumps are reported as nonblocking
`SOURCE_HEADING_HIERARCHY_WARNING` when the DOCX preserves them exactly. The
publisher reports the source defect rather than changing the authoritative
Markdown.

## Statuses

- `VALID`: no findings;
- `VALID_WITH_WARNINGS`: no blocking publication finding, but a source or
  environment warning is recorded;
- `INVALID`: at least one blocking finding.

Only a result with no blocking findings may proceed to render QA, and the
complete pipeline still ends at human release review.
