---
name: technical-document-publisher
description: >
  Orchestrate publication of approved technical Markdown into professional DOCX/PDF using an installed
  DOCX-capability skill such as `doc`. This skill owns publication policy, source-of-truth protection,
  repository layout, publication profile, artifact naming, content-fidelity gates, and release workflow.
  It does not implement low-level DOCX manipulation itself and must not rewrite technical content.
metadata:
  version: "0.3.0"
  role: "thin-publication-orchestrator"
---

# Technical Document Publisher

This is a **thin publication-orchestration skill**.

It does not replace the installed `doc` skill.

Its job is to define **how an approved technical document is published**, not how DOCX internals are implemented.

Core relationship:

```text
technical-specification-guide / engineering-contract-spec
                ↓
         approved Markdown
                ↓
technical-document-publisher
                ↓
      publication policy
                ↓
              doc
                ↓
        DOCX / PDF output
```

---

# 1. Responsibility boundary

## This skill owns

- publication workflow;
- Markdown source-of-truth rules;
- repository publication layout;
- publication profile;
- output naming;
- version/status metadata;
- cover/front-matter policy;
- content-fidelity gates;
- source-integrity checks;
- invocation expectations for the installed `doc` skill;
- release-candidate criteria.

## This skill does not own

- python-docx implementation details;
- OOXML manipulation;
- DOCX rendering implementation;
- LibreOffice invocation internals;
- Poppler invocation internals;
- Word style manipulation algorithms;
- technical prose authoring;
- architecture decisions;
- normative contract authoring.

Those belong to:
- `doc` for DOCX engineering;
- `technical-specification-guide` for explanatory architecture content;
- `engineering-contract-spec` for normative implementation contracts.

---

# 2. Markdown is the content Source of Truth

Unless the user explicitly designates another authoritative source:

> The approved Markdown file is the authoritative content source.

DOCX and PDF are generated publication artifacts.

Do not treat the generated DOCX as the maintenance source.

If layout is wrong:
- fix publication profile;
- fix build script;
- fix template/reference DOCX;
- regenerate.

Do not edit technical content inside generated DOCX merely to improve layout.

Read `references/source-of-truth.md`.

---

# 3. No content mutation during publication

Publishing may change presentation.

Publishing must not silently change technical meaning.

Forbidden during publication:
- rewriting prose;
- shortening paragraphs;
- deleting examples;
- changing terminology;
- changing numbers or units;
- changing code;
- changing equations;
- changing architecture diagrams semantically;
- changing MUST / SHOULD / MAY strength;
- inventing content to fill layout gaps;
- reorganizing chapters merely for pagination.

If a source-content problem is found:
1. stop publication work on that issue;
2. report it;
3. return it to the appropriate authoring/review workflow.

Read `references/content-fidelity.md`.

## 3.1 Markdown semantic whitespace

Whitespace MUST NOT be normalized blindly during publication. In particular, trailing spaces at the
end of a Markdown line may encode a hard line break. `git diff --check` and other trailing-whitespace
scanners are warning signals, not authorization to delete those spaces.

When processing trailing spaces, indentation, blank lines, fenced code, ASCII diagrams, or YAML,
distinguish semantic whitespace from accidental whitespace. Preserve semantic whitespace in the frozen
source. If Word layout needs different spacing or wrapping, make the parser, builder, template, or
publication profile interpret the source correctly; do not mutate the source to satisfy layout or lint.

## 3.2 Source-semantic content vs publication-only content

Classify publication inputs and outputs as follows.

**Source-semantic content** includes:
- technical definitions;
- normative clauses;
- architecture decisions;
- examples;
- diagrams with technical meaning;
- tables with technical meaning;
- references;
- technical terminology.

The publisher MUST NOT add, delete, or rewrite source-semantic content.

**Publication-only content** may include:
- cover or title page;
- TOC;
- running header and footer;
- page numbers;
- section breaks;
- Word styles;
- automatic numbering metadata;
- bookmarks;
- repeated table headers;
- page-orientation changes;
- pagination controls.

Publication-only content MUST NOT change source semantics. The publisher MUST NOT add a new technical
explanation, normative clause, architecture concept, example used to justify architecture, taxonomy,
or content-bearing summary. Publication may add presentation structure, but MUST NOT add technical meaning.

---

# 4. Installed `doc` skill is the DOCX engine

When `doc` is available, use it for:
- DOCX creation;
- Word styles;
- tables;
- lists;
- spacing;
- margins;
- headers/footers;
- TOC;
- page numbering;
- captions;
- cross-reference behavior supported by that skill;
- render and visual QA;
- other DOCX engineering tasks supported by the installed version.

Do not duplicate those instructions here.

Before publication:
- confirm `doc` is installed;
- read its current `SKILL.md`;
- use its actual capabilities, not assumed capabilities.

If the installed `doc` version differs from a previously known version, trust the installed file.

---

# 5. Current preferred toolchain

For the current PAIS environment, the known ready toolchain is:

```text
/home/htc/.venvs/docx-tools/bin/python
    ↓
python-docx
    ↓
DOCX
    ↓
LibreOffice / soffice
    ↓
PDF
    ↓
pdf2image + Poppler / pdftoppm
    ↓
page images
    ↓
visual QA
```

Pandoc is optional, not required by the current core renderer.

Do not make Pandoc a hard requirement unless the chosen build path actually uses it.

Do not hard-code this environment into a publication artifact; it is execution context.

---

# 6. Preferred project layout

For repository-managed technical publications, prefer:

```text
project/
├── docs/
│   └── guide.md
├── publishing/
│   ├── publication-profile.yaml
│   ├── reference.docx
│   └── README.md
├── scripts/
│   └── build_docx.py
├── build/
│   └── publication/
└── dist/
    ├── guide.docx
    └── guide.pdf
```

Rules:

- `docs/*.md` contains authoritative content.
- `publishing/` contains publication configuration/template material.
- `scripts/` contains reproducible build logic.
- `build/` contains temporary generated files and render pages.
- `dist/` contains release artifacts.

Do not place temporary rendered PNG pages in `docs/` or `dist/`.

---

# 7. Publication profile

Keep presentation decisions separate from content.

A publication profile may define:
- title;
- subtitle if useful;
- version;
- status;
- page size;
- margins;
- font families;
- base font size;
- line spacing;
- heading hierarchy;
- code/ASCII styling;
- table style;
- caption style;
- cover behavior;
- TOC depth;
- page header;
- page footer;
- page numbering;
- section-break policy.

A publication profile must not contain rewritten technical body content.

Read `references/publication-profile.md`.

---

# 8. Cover and front matter policy

Include only publication-useful metadata.

Typical useful content:
- document title;
- project/standard name;
- version;
- status;
- organization/maintainer when appropriate;
- date when appropriate.

Avoid meta-document language such as:
- "human-readable edition";
- "golden master";
- "generated by AI";
- "for human understanding";
- internal review-process commentary.

Publication should look like a technical document, not an editing log.

---

# 9. Publication workflow

Preferred workflow:

```text
Approved Markdown
      ↓
Source integrity check
      ↓
Publication profile
      ↓
Invoke doc skill / build pipeline
      ↓
DOCX
      ↓
Content fidelity audit
      ↓
Render all pages
      ↓
Visual QA of every page
      ↓
Fix publication layer only
      ↓
Rebuild
      ↓
Re-render
      ↓
Publication candidate
```

Read `references/publication-workflow.md`.

---

# 10. Source integrity

Before publication:
- record source path;
- record SHA-256;
- record Git branch and HEAD when relevant;
- record working-tree state when relevant.

After publication:
- recompute source SHA-256;
- verify publishing did not modify authoritative source unexpectedly.

If source changed without explicit authorization:
- publication gate fails.

---

# 11. Content fidelity

After DOCX generation, verify that publication preserved:
- heading text/order;
- body paragraphs;
- lists;
- tables;
- code blocks;
- equations;
- captions;
- diagrams;
- normative keywords;
- units;
- identifiers.

Expected differences may include:
- generated TOC;
- page numbers;
- headers/footers;
- generated figure numbering when semantically equivalent;
- typography/layout.

Blocking differences include:
- omitted text;
- changed technical term;
- changed value/unit;
- lost table row;
- corrupted code;
- missing diagram;
- changed MUST/SHOULD/MAY;
- changed architecture meaning.

If a suspicious difference appears, do not auto-correct technical content in DOCX.

---

# 12. Visual QA

Use the installed `doc` skill's render workflow.

The publication is not ready merely because:
- DOCX opens successfully;
- DOCX XML is valid;
- build script exits with code 0.

Every rendered page must be inspected.

Check for:
- clipping;
- overlaps;
- unexpected blank pages;
- broken tables;
- broken code blocks;
- ASCII diagram wrapping;
- missing glyphs;
- isolated headings;
- isolated captions;
- header/footer collisions;
- bad page numbering;
- TOC overflow.

If a publishing defect is found:
- fix template/profile/build logic;
- rebuild;
- re-render;
- inspect again.

Do not sample only the first/last pages for a long document.

---

# 13. Publication defects vs source defects

## Publication defect

Examples:
- bad page break;
- incorrect font size;
- table overflow;
- code wrapping;
- caption placement;
- header spacing.

Fix in publication layer.

## Source defect

Examples:
- wrong technical term;
- contradictory content;
- incorrect architecture diagram;
- malformed source table;
- wrong normative keyword.

Do not silently fix during publication.

Return it to:
- `technical-specification-guide`,
- `engineering-contract-spec`,
- or human author/reviewer.

---

# 14. Build reproducibility

Prefer a rebuildable publication pipeline.

Where practical, preserve:
- source hash;
- publication-profile hash;
- template hash;
- output hash;
- toolchain versions;
- render page count;
- QA result.

This may be stored in a build manifest.

Build metadata belongs in the build/release workflow, not inside the technical publication unless explicitly requested.

---

# 15. PAIS-like publication defaults

For PAIS-style technical white papers, default visual intent:

- A4;
- restrained engineering/standards-document appearance;
- clear heading hierarchy;
- professional Chinese/English mixed typography;
- monospaced code and ASCII diagrams;
- compact technical tables;
- page numbers;
- simple running header;
- generated TOC;
- no decorative dependence;
- no government-document aesthetic unless requested;
- no academic-journal aesthetic unless requested.

These are defaults, not content rules.

---

# 16. Final publication gate

Before calling an artifact publication-ready, confirm:

1. authoritative source identified;
2. source hash recorded;
3. source unchanged after build;
4. `doc` skill used according to its installed instructions;
5. DOCX successfully generated;
6. content fidelity passed;
7. every page rendered;
8. every page visually inspected;
9. publication defects resolved through the publication layer;
10. no technical content silently changed;
11. final artifact path recorded.

Before human release approval, use:

`PUBLICATION CANDIDATE READY FOR HUMAN RELEASE REVIEW`

Do not self-declare a major technical publication final solely because tooling passed.

---

# 17. Relationship to the other skills

```text
technical-specification-guide
        ↓
detailed explanatory technical content

engineering-contract-spec
        ↓
normative implementation contract

technical-document-publisher
        ↓
publication policy and orchestration

doc
        ↓
DOCX implementation and render QA
```

Keep these roles separate.
