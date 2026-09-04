# Visual QA Checklist

Visual QA is a release gate after DOCX → PDF → page-image rendering. Long
technical documents MUST have every page inspected and a page-level record;
first/middle/last-page sampling is not sufficient.

For each page record `page`, `status`, and `issues`. Check:

- clipping, overlap, and missing glyphs;
- unexpected blank pages or pages containing only a tiny fragment;
- broken tables, row splits, and TOC overflow;
- code indentation, ASCII diagram spacing, wrapping, and page breaks;
- heading at the bottom without body text;
- visible heading hierarchy;
- ordered-list numbering and bullet indentation;
- header/footer collision and page-number presence;
- excessive blank space and extreme line density;
- font fallback or glyph corruption.

## Page Rhythm QA

Record character density and visual notes for every rendered page. Flag
`TEXT_WALL_PAGE` for an unusually dense page, `HEADING_WALL_PAGE` when
headings dominate without explanatory body text, `SPARSE_PAGE` for an
unexpectedly empty interior page, `BROKEN_RHYTHM_PAGE` for abrupt whitespace
or block-size discontinuity, and `SPARSE_FINAL_PAGE` when the final page is
unjustifiably short. These are layout findings, not permission to rewrite the
technical source; remediate with style, keep, spacing, or pagination rules.

The page-level record MUST identify the densest and sparsest pages and state
whether each outlier was reviewed. A technical whitepaper should make its
title, H1, H2, H3, body, list, table, code, and ASCII roles distinguishable at
a glance and should retain a steady body-text rhythm across the document.

## Visual Hierarchy QA

The deterministic visual-structure validator checks heading size order,
heading/body contrast, heading weight and spacing, TOC indentation and size
hierarchy, code/ASCII monospace separation, font availability, and direct
formatting ratio. Page images remain authoritative for clipping, one-second
heading recognition, table/code wrapping, and heading-at-page-bottom review.

Blocking page issues are `BROKEN`, `CLIPPED`, `OVERLAPPED`, `EMPTY_TOC`,
`MARKDOWN_LEAK`, `LIST_NUMBERING_BROKEN`, `ORPHAN_PAGE`, and
`SPARSE_FINAL_PAGE`. A document with any blocking page issue is
`PUBLICATION BLOCKED`. A short final page is repaired through style/layout
parameters only; technical source content must not be rewritten to fill it.

If the environment supports visual inspection, inspect every rendered page at
100% zoom. If it supports only automated checks, label the report `automatic
visual checks only`; the output may proceed only to human release review and
must not be described as visually approved.
