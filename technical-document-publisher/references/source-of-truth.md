# Source of Truth

For Markdown-first technical projects:

- Markdown is authoritative content.
- DOCX/PDF are generated artifacts.
- publication fixes belong in templates, profiles, or build scripts.
- technical-content fixes belong in the authoring/review workflow.

Do not create a hidden second source of truth by manually editing generated DOCX files.

Before publication, record the Markdown SHA-256. After the build and after
rendering, recompute it and fail the source-integrity gate if it changed without
explicit authorization. Publication-layer fixes belong in the parser, builder,
template, profile, or validator. A source syntax defect is reported separately
and is not silently rewritten to make a DOCX pass.
