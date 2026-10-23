# 01 技术白皮书

编号：`01`。标识：`technical-whitepaper`。配置版本：`1.0.0`。

适用于架构指南、标准设计指南、协议原理、工程白皮书和接口标准。
本目录承接原 `references/publication-profile.md` 的技术白皮书设计规则，
没有更改正文、标题的语义映射或发布流程。

阅读本文件及同目录 `profile.yaml`。发布前将配置复制到项目的 `publishing/`，
补齐具体字体及文档元数据；保留配置编号、标识和版本，并记录配置哈希。
字体角色原本没有固定品牌，必须从实际可用字体中明确选择并记录，不能将空值当作字体名称。
通用内容保真、结构保真、目录核对及逐页检查仍遵循 Publisher 的共同规则。

以下保留现有设计约定；新增版式放入 `02`、`03` 等独立目录。

## Technical Whitepaper Profile


`technical-whitepaper` is the default family for architecture guides, standard
design guides, protocol rationale, engineering whitepapers, reference
architectures, and interface standards. Its visual intent is professional,
restrained, readable, engineering-oriented, long-form friendly, print-friendly,
and safe for Chinese-English typography. It does not use brochure, slide-deck,
government-form, dense academic-journal, or colorful marketing conventions
unless the user explicitly selects them.

The profile is a design system, not a fixed set of numbers. Implementations may
adjust values for a font family or page size, but MUST preserve perceptual role
identity: `Chapter > Major Section > Technical Topic > Local Label > Body`,
`H1 > H2 > H3 > Body`, H1/H2 bold, meaningful heading spacing, and a visibly
separate treatment for code, diagrams, tables, and TOC levels. A role that
differs only by a barely visible font-size delta is not a valid hierarchy.

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

Perceptual roles:

| role | default identity |
|---|---|
| Chapter | major heading weight, generous but bounded whitespace, optional chapter-start break |
| Major Section | bold heading with clear size and spacing contrast from topics |
| Technical Topic | bold topic heading with stable marker/rule or indentation plus visible size/spacing contrast |
| Local Label | non-navigational anchor with bold/semibold treatment, modest spacing, and optional subtle marker |
| Body | regular reading text with the baseline body rhythm |

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
- H1/top-level chapter starts MAY begin a new page; H2/H3 MUST NOT mechanically force page breaks unless the profile maps them to chapter/major-section roles explicitly.
- Lists use hanging indents, clear nested levels, restrained item spacing, and independent ordered-list restarts.
- Tables use bold headers, readable contrast, cell padding, repeated headers, semantic widths, light borders, and no decorative heavy grid.
- Code and ASCII diagrams use monospace, preserved whitespace, block separation, keep-together for short blocks, and safe non-wrapping behavior.
- TOC 1/2/3 use descending visual weight, increasing indentation, aligned page numbers, and consistent leader dots.
- Header/footer remain smaller and quieter than body text; the cover MAY use a different first-page treatment.
- Pagination and Page Rhythm QA review orphan headings, isolated captions, short diagram splits, sparse pages, text walls, heading walls, and the final page.
- Font fallback validation checks CJK, Latin, monospace, and box-drawing glyph availability plus PDF replacement-glyph signals.
- Black-and-white review MUST confirm that hierarchy remains legible without color; color is auxiliary only.
- Perceptual-distance, role-collapse, topic/body, local-label/body, chapter/section, and section/topic signals are deterministic aids, not substitutes for visual review.
- A design-system upgrade MUST include neutral A/B Before/After review and record `YES`, `NO`, or `MIXED`.
- Page-rhythm review SHOULD report long near-identical runs as `VISUAL_MONOTONY_WARNING`.

