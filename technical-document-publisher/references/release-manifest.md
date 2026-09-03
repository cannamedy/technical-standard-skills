# Publication Manifest

`publication-manifest.json` is a build artifact, not technical-document content. It is the audit
record for one FINAL RELEASE MODE attempt and must be regenerated after any source or publication
repair.

```json
{
  "schema_version": "1.0",
  "mode": "FINAL_RELEASE",
  "status": "PUBLICATION CANDIDATE READY FOR HUMAN RELEASE REVIEW",
  "source": {
    "path": "docs/guide.md",
    "hash_before_repair": "sha256",
    "hash_frozen": "sha256",
    "git_head": "commit-or-null",
    "modifications": []
  },
  "skills": {
    "technical-specification-guide": "0.0.0",
    "assessment-question-designer": "0.0.0",
    "technical-document-publisher": "0.0.0",
    "doc": "installed-version-or-toolchain"
  },
  "inputs": {
    "publication_profile_hash": "sha256-or-null",
    "template_hash": "sha256-or-null",
    "build_script_hash": "sha256-or-null"
  },
  "artifacts": {
    "docx_path": "dist/guide.docx",
    "docx_hash": "sha256",
    "pdf_path": "dist/guide.pdf",
    "pdf_hash": "sha256",
    "page_count": 0
  },
  "gates": {
    "source_readiness": {"status": "SOURCE_READY", "report": "..."},
    "human_readability": {"status": "HUMAN_READABILITY_PASS", "report": "..."},
    "assessment": {"status": "NOT_APPLICABLE", "report": null},
    "content_fidelity": {"status": "PASS", "report": "..."},
    "structural_fidelity": {"status": "PASS", "report": "..."},
    "toc_heading_list_code_diagram": {"status": "PASS", "report": "..."},
    "visual_fidelity": {"status": "PASS", "report": "...", "page_level_qa": "..."}
  },
  "normative_keyword_delta": {"MUST": 0, "SHOULD": 0, "MAY": 0},
  "iterations": 1
}
```

`status` MUST not be the human-release candidate state when any gate is blocking, when the frozen
source hash cannot be verified, or when page-level visual QA is missing. A source change starts a new
freeze cycle and updates both source hashes and the normative delta.
