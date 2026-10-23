# Publication Profile v4

排版配置与正文分离。`technical-document-publisher` 保持技能名称不变，
每一种排版方式保存在 `profiles/` 下独立的两位数字目录中。

## 已登记的排版方式

| 编号 | 名称 | 标识 | 定义 | 配置 |
|---|---|---|---|---|
| 01 | 技术白皮书 | `technical-whitepaper` | [profile.md](../profiles/01/profile.md) | [profile.yaml](../profiles/01/profile.yaml) |
| 02 | 中文技术报告横线表版 | `zh-cn-technical-report` | [profile.md](../profiles/02/profile.md) | [profile.yaml](../profiles/02/profile.yaml) |

`profiles/index.json` 是编号、标识、路径及别名的登记表。
后续实际增加排版方式时依次使用 `03`、`04` 等目录，不预建没有配置的空目录。
已发布编号不可改用于另一种版式，配置更新应增加对应的配置版本。
`compact-specification`、`engineering-contract`、`report` 和 `minimal` 仍只是可能的未来名称。

## 选择与应用

1. 用户指定编号、名称或标识时，按登记表选择；未知编号应报告未登记，不能静默使用默认版式。
2. 用户没有指定时，沿用该项目已记录的配置。没有既有配置时，架构指南和白皮书采用 `01`；
   设备选型、技术调研、方案比较等中文报告采用 `02`，在开始生成前说明所选版式。
3. 直接读取所选目录的 `profile.md` 和 `profile.yaml`。不能只读本索引，也不能将两种版式混合。
4. 将所选配置复制到项目 `publishing/publication-profile.yaml`，补齐必要元数据和字体，
   再交给已安装的 `doc` 技能构建。YAML 是发布配置合同，不是本技能自带的 DOCX 渲染器。
5. 在发布记录中保存编号、标识、配置版本、最终字体和项目配置哈希。通用的内容、结构、
   目录及逐页检查继续执行；配置编号不改变 FINAL RELEASE / STRICT PUBLISH 工作模式。

用户选定编号后，该配置的具体视觉要求优先于 `doc`／`documents` 能力的通用视觉默认。
例如 `02` 的黑色横线、无竖线和无底色表格不得套回通用灰色全边框样式。
DOCX 能力仍负责实现、渲染和检查，内容与结构保真要求不变。

## 通用配置字段示例

下列 YAML 只说明字段，不能当作第三种版式。具体数值和字体以所选编号目录为准。

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
  perceptual_hierarchy_gate: true
  black_and_white_gate: true
  visual_monotony_gate: true
  blind_before_after_required: true
  minimum_topic_body_distance: 0.18
  minimum_local_label_body_distance: 0.10
  cross_renderer_policy: report-if-not-verified
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
