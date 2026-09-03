# Content Fidelity Gate

Content fidelity and structural fidelity are different gates.

## Content Fidelity

The publisher must preserve technical meaning and verify:

- heading text and order;
- body paragraphs and identifiers;
- list item text;
- tables and rows;
- code, equations, and diagrams;
- captions and references;
- units and numeric values;
- normative keywords such as `MUST`, `SHOULD`, and `MAY`.

Expected publication-only additions include a cover, TOC, headers, footers,
page numbers, bookmarks, repeated table headers, and Word numbering metadata.

Blocking content defects include omitted text, changed terminology, changed
values or units, lost table rows, corrupted code, missing diagrams, or changed
normative strength. Do not repair suspicious content in the generated DOCX;
return it to the appropriate authoring or review workflow.

## Structural Fidelity

Text being present is not proof that Markdown semantics survived conversion.
The structural gate separately checks heading styles and levels, heading order,
explicit list numbering instances, list nesting, code/diagram classification,
whitespace preservation, table presence, Markdown syntax leakage, and TOC
entries. Use `scripts/validate_publication_structure.py` and retain its report
with the build metadata.

## Source integrity

Record the source path and SHA-256 before build and recompute it afterward. A
source hash change without explicit authorization is a blocking failure. Do not
normalize trailing spaces or indentation blindly: Markdown whitespace can be
semantic, especially in fenced code and ASCII diagrams.
