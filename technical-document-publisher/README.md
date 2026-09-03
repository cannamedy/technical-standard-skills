# technical-document-publisher v0.5.0

A publication-orchestration skill with source-readiness, assessment, content, structural, and visual
release gates.

It intentionally does **not** reimplement DOCX engineering.

Use with an installed `doc` skill:

```text
Approved Markdown
    ↓
technical-document-publisher
    ↓
doc
    ↓
DOCX / PDF
```

One-call final release:

> 使用 technical-document-publisher，把 docs/architecture-guide.md 生成最终可发布 DOCX 和 PDF。

This enters FINAL RELEASE MODE: source structure is audited, assessment sections are routed to
`assessment-question-designer`, minimal responsible repairs are applied before freezing, and the
document is built through `doc`, checked for content/structure/TOC/lists/code/diagrams, rendered to
PDF and all page images, and iterated until a release candidate or explicit human-decision block.

Strict frozen-source publication:

> 严格按冻结 Markdown 发布，不修改源文档，只生成 DOCX/PDF 并执行发布门禁。

Responsibilities:
- protect Markdown as source of truth;
- prevent content mutation during publication;
- define publication profile and repository layout;
- require source-integrity and content-fidelity checks;
- compare Markdown headings, lists, code/ASCII blocks, tables, normative terms, and TOC cache against DOCX semantics;
- require full-page render QA through `doc`;
- orchestrate FINAL RELEASE MODE and record `publication-manifest.json`;
- keep technical authoring separate from publication.

Structural validation can be run independently:

```text
python technical-document-publisher/scripts/validate_publication_structure.py \
  --source docs/guide.md \
  --docx dist/guide.docx \
  --profile publishing/publication-profile.yaml
```

Version 0.5 adds FINAL RELEASE MODE, Source Readiness and Assessment routing,
three distinct fidelity gates, an explicit repair/rebuild loop, and a release
manifest while retaining the separation between publisher policy and low-level
DOCX/rendering implementation owned by the installed `doc` skill.
