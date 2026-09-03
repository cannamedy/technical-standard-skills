#!/usr/bin/env python3
import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("manifest_validator", ROOT / "scripts" / "validate_release_manifest.py")
manifest = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = manifest
SPEC.loader.exec_module(manifest)


def candidate():
    return {
        "schema_version": "1.0", "mode": "FINAL_RELEASE",
        "status": "PUBLICATION CANDIDATE READY FOR HUMAN RELEASE REVIEW",
        "source": {"path": "docs/guide.md", "hash_before_repair": "a", "hash_frozen": "b", "modifications": [], "git_head": "x"},
        "skills": {"technical-document-publisher": "0.5.0"}, "inputs": {},
        "artifacts": {"docx_path": "a.docx", "docx_hash": "a", "pdf_path": "a.pdf", "pdf_hash": "b", "page_count": 4},
        "gates": {
            "source_readiness": {"status": "SOURCE_READY"},
            "content_fidelity": {"status": "PASS"}, "structural_fidelity": {"status": "PASS"},
            "visual_fidelity": {"status": "PASS", "page_level_qa": "qa.md"},
        },
        "normative_keyword_delta": {"MUST": 0, "SHOULD": 0, "MAY": 0}, "iterations": 2,
    }


class ReleaseManifestTests(unittest.TestCase):
    def test_candidate_requires_all_release_fields(self):
        self.assertEqual(manifest.validate(candidate())["status"], "VALID")

    def test_ready_with_failed_gate_is_invalid(self):
        data = candidate()
        data["gates"]["structural_fidelity"]["status"] = "FAIL"
        result = manifest.validate(data)
        self.assertEqual(result["status"], "INVALID")

    def test_blocked_manifest_is_allowed(self):
        data = candidate()
        data["status"] = "PUBLICATION BLOCKED"
        data["gates"]["structural_fidelity"]["status"] = "FAIL"
        self.assertEqual(manifest.validate(data)["status"], "VALID")


if __name__ == "__main__":
    unittest.main()
