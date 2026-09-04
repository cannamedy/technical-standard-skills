# Publication Profile v3

The publication profile is a presentation contract. It may configure the
publication artifact, but it must not contain rewritten technical content.
The concrete format may be YAML or an equivalent profile supported by the
project build layer.

## Technical Whitepaper Profile

`technical-whitepaper` is the default family for architecture guides, standard
design guides, protocol rationale, engineering whitepapers, reference
architectures, and interface standards. Its visual intent is professional,
restrained, readable, engineering-oriented, long-form friendly, print-friendly,
and safe for Chinese-English typography. It does not use brochure, slide-deck,
government-form, dense academic-journal, or colorful marketing conventions
unless the user explicitly selects them.

The profile is a design system, not a fixed set of numbers. Implementations may
adjust values for a font family or page size, but MUST preserve minimum visual
contrast: `H1 > H2 > H3 > Body`, H1/H2 bold, meaningful heading spacing, and a
visibly separate treatment for code, diagrams, tables, and TOC levels.

Recommended default ranges:

| role | default range / rule |
|---|---|
| Cover title | 24–28 pt |
| H1 | 18–20 pt, bold |
| H2 | 15–16 pt, bold |
| H3 | 12.5–14 pt, bold |
| H4 | 11–12 pt, bold or semibold |
| Body | 10.5–11 pt |
| Lead-in | body size, bold/semibold |
| Code / ASCII Diagram | 8.5–9.5 pt monospace |
| Table body | 9–10 pt |
| Body rhythm | line spacing about 1.25–1.4, paragraph after about 4–6 pt |

The profile SHOULD define semantic classes where the renderer supports them:
`Title`, `Subtitle`, `Body`, `Heading 1`–`Heading 6`, `Lead-in`, `Runtime
Label`, `Question Label`, `Code`, `ASCII Diagram`, `Quote`, `Caption`, `Table
Header`, `Table Body`, `Bullet 1`–`Bullet 3`, `Numbered 1`–`Numbered 3`, `TOC 1`–
`TOC 3`, `Header`, and `Footer`. Repeated presentation decisions belong in
named styles; direct run or paragraph formatting is an exception and is
measured by the visual validator.

## Layout and quality policy

- A4 or the selected page size uses moderate margins; page count is subordinate to reading efficiency.
- Heading styles combine size, weight, spacing, `keep_with_next`, and page-break policy.
- H1/top-level chapter starts MAY begin a new page; H2/H3 MUST NOT mechanically force page breaks.
- Lists use hanging indents, clear nested levels, restrained item spacing, and independent ordered-list restarts.
- Tables use bold headers, readable contrast, cell padding, repeated headers, semantic widths, light borders, and no decorative heavy grid.
- Code and ASCII diagrams use monospace, preserved whitespace, block separation, keep-together for short blocks, and safe non-wrapping behavior.
- TOC 1/2/3 use descending visual weight, increasing indentation, aligned page numbers, and consistent leader dots.
- Header/footer remain smaller and quieter than body text; the cover MAY use a different first-page treatment.
- Pagination and Page Rhythm QA review orphan headings, isolated captions, short diagram splits, sparse pages, text walls, heading walls, and the final page.
- Font fallback validation checks CJK, Latin, monospace, and box-drawing glyph availability plus PDF replacement-glyph signals.

## Profile families

The first complete family is `technical-whitepaper`. Future families such as
`compact-specification`, `engineering-contract`, `report`, or `minimal` MAY be
added, but a publisher MUST NOT silently switch family. Architecture guides
default to `technical-whitepaper` unless the user selects another style.

```yaml
document:
  title: "..."
  subtitle: "..."
  version: "..."
  status: "..."
  date: "YYYY-MM-DD"

page:
  size: A4
  margins_cm: 2.0

body:
  font: "..."
  cjk_font: "..."
  latin_font: "..."
  size_pt: 10.5
  line_spacing: 1.15
  paragraph_spacing_pt: 5

headings:
  h1: {size_pt: 16, keep_with_next: true}
  h2: {size_pt: 13, keep_with_next: true}
  h3: {size_pt: 11.5, keep_with_next: true}
  h4: {size_pt: 10.5, keep_with_next: true}
  h5: {size_pt: 10, keep_with_next: true}
  h6: {size_pt: 9.5, keep_with_next: true}
  numbering: false
  numbering_policy: source-level-only
  page_break_before: false

fonts:
  cjk: "..."
  latin: "..."
  monospace: "... Mono"

lists:
  ordered_restart_policy: per-markdown-block
  nesting: preserve-source-indent
  hanging_indent_cm: 0.25
  paragraph_spacing_pt: 1

code:
  font: "... Mono"
  size_pt: 8.2
  background: "F3F5F7"
  preserve_whitespace: true
  keep_together: short-blocks
  wrapping: preserve-lines

ascii_diagram:
  font: "... Mono"
  size_pt: 8.0
  background: "EEF4F8"
  preserve_whitespace: true
  keep_together: true
  fit_to_width: reduce-safe-font
  allow_landscape: false

tables:
  style: "Table Grid"
  repeat_header: true
  split_rows: true
  autofit: true
  font_size_pt: 8.5

toc:
  enabled: true
  depth: 3
  title: "Contents"
  update_fields: true
  verify_entries: true
  require_page_numbers: true
  leader: "dots"

labels:
  lead_in: "Lead-in"
  runtime_label: "Runtime Label"
  question_label: "Question Label"

header:
  enabled: true
  content: "..."

footer:
  page_numbers: true
  format: "— PAGE —"

pagination:
  orphan_control: true
  heading_keep_with_next: true
  avoid_isolated_heading: true
  avoid_single_line_page_tail: true
  avoid_short_final_page: true
  keep_question_block: true
  keep_short_diagram: true
  minimum_tail_fill_policy: "warn; style-only remediation"

visual:
  profile_family: technical-whitepaper
  minimum_h1_body_ratio: 1.4
  minimum_h2_body_ratio: 1.2
  minimum_h3_body_ratio: 1.08
  direct_formatting_warning_ratio: 0.35
  direct_formatting_fail_ratio: 0.75
  hierarchy_gate: true
  page_rhythm_gate: true
  density_gate: true
```

The minimum semantic requirements are independent of visual choices:

- Markdown H1-H6 map to Word Heading 1-6, unless an explicit documented
  offset is part of the profile.
- Every independent ordered list receives a distinct Word numbering instance;
  nested levels remain explicit.
- Code and layout-sensitive ASCII diagrams are classified separately.
- A TOC field is accompanied by verifiable cached or rendered entries when
  TOC is enabled; each visible entry has a page number and the configured
  leader pattern.
- Word structure is style-first: heading, list, code, diagram, quote, table,
  and TOC semantics are represented by named styles or numbering XML before
  paragraph-level direct formatting is considered.
