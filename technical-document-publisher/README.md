# technical-document-publisher v0.2

A thin publication-orchestration skill.

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
- require full-page render QA through `doc`;
- keep technical authoring separate from publication.

Version 0.2 replaces the earlier heavier prototype.
