# Publication Profile v2

The publication profile is a presentation contract. It may configure the
publication artifact, but it must not contain rewritten technical content.
The concrete format may be YAML or an equivalent profile supported by the
project build layer.

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
