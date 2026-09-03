# Publication Workflow v2

Publication acceptance is separate from technical acceptance. The Markdown
approved by the authoring/review workflow remains the only content source of
truth.

```text
Approved Markdown
      ↓
Source Integrity Gate
      ↓
DOCX Build via installed `doc` capability
      ↓
Content Fidelity Gate
      ↓
Structural Fidelity Gate
      ↓
TOC / Heading / List Fidelity
      ↓
DOCX → PDF → page images
      ↓
Page-level Visual QA
      ↓
PUBLICATION CANDIDATE READY FOR HUMAN RELEASE REVIEW
```

The structural gate is deterministic and is run with:

```text
python technical-document-publisher/scripts/validate_publication_structure.py \
  --source <approved.md> \
  --docx <generated.docx> \
  --profile <publication-profile.yaml> \
  --source-sha256 <hash-recorded-before-build>
```

It must compare the source and DOCX semantic models, not just extracted text.
The gate blocks heading-level/text mismatch, literal Markdown heading leakage,
unexpected numbering continuation, list-level mismatch, code indentation or
diagram whitespace loss, table loss, missing normative terms, and empty or
incomplete TOCs.

The build layer must create a distinct Word numbering instance for each
independent Markdown ordered-list block. A shared `List Number` style without
explicit `numId` is not sufficient. The layer must preserve source starts and
nested list levels.

The build layer may use heuristics to classify an indented, box-drawn, tree,
or arrow-heavy fenced block as `ASCII_DIAGRAM`. Classification changes only
presentation. Source lines, spaces, and line breaks remain unchanged.

Every page must be rendered and recorded in a page-level QA report. If visual
inspection is unavailable, report `automatic visual checks only` and keep the
artifact at human-release-review status; never claim visual approval by
sampling only first/middle/last pages.

Any blocking gate failure means `PUBLICATION BLOCKED`. Source defects are
reported separately and are not silently repaired in the publishing task.
