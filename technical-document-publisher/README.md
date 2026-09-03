# technical-document-publisher v0.4.0

A thin publication-orchestration skill with separate content, structural, and visual fidelity gates.

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

Responsibilities:
- protect Markdown as source of truth;
- prevent content mutation during publication;
- define publication profile and repository layout;
- require source-integrity and content-fidelity checks;
- compare Markdown headings, lists, code/ASCII blocks, tables, normative terms, and TOC cache against DOCX semantics;
- require full-page render QA through `doc`;
- keep technical authoring separate from publication.

Structural validation can be run independently:

```text
python technical-document-publisher/scripts/validate_publication_structure.py \
  --source docs/guide.md \
  --docx dist/guide.docx \
  --profile publishing/publication-profile.yaml
```

Version 0.4 adds the Publication Structural Fidelity Gate while retaining the
thin publication-orchestration boundary.  The publisher owns policy and
validation; the installed `doc` skill owns low-level DOCX and rendering.
