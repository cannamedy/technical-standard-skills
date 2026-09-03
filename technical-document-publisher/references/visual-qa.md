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

Blocking page issues are `BROKEN`, `CLIPPED`, `OVERLAPPED`, `EMPTY_TOC`,
`MARKDOWN_LEAK`, and `LIST_NUMBERING_BROKEN`. A document with any blocking
page issue is `PUBLICATION BLOCKED`.

If the environment supports visual inspection, inspect every rendered page at
100% zoom. If it supports only automated checks, label the report `automatic
visual checks only`; the output may proceed only to human release review and
must not be described as visually approved.
