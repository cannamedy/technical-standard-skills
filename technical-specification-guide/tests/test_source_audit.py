#!/usr/bin/env python3
import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("source_audit", ROOT / "scripts" / "audit_document_structure.py")
audit = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = audit
SPEC.loader.exec_module(audit)


class SourceAuditTests(unittest.TestCase):
    def test_generic_fixture_is_ready(self):
        fixture = (ROOT / "tests" / "fixtures" / "generic_architecture.md").read_text(encoding="utf-8")
        result = audit.audit_text(fixture)
        self.assertEqual(result["status"], "SOURCE_READY")
        self.assertTrue(result["summary"]["assessment_detected"])

    def test_heading_jump_requires_repair(self):
        result = audit.audit_text("# A\n\n## B\n\n#### D\n")
        self.assertEqual(result["status"], "SOURCE_REPAIR_REQUIRED")
        self.assertIn("HEADING_HIERARCHY_JUMP", {f["code"] for f in result["findings"]})

    def test_pseudo_heading_is_review_not_regex_truth(self):
        result = audit.audit_text("# A\n\n## B\n\n##### 场景\ntext\n")
        finding = next(f for f in result["findings"] if f["code"] == "PSEUDO_HEADING_MISUSE")
        self.assertTrue(finding["requires_reasoning"])
        self.assertEqual(finding["severity"], "review")

    def test_legacy_numbering_and_runtime_inflation_are_detected(self):
        source = "# A\n\n## 64. A\n\n### Runtime step 1\n\n### Runtime step 2\n\n### Runtime step 3\n\n### Runtime step 4\n\n## 28. B\n"
        result = audit.audit_text(source)
        codes = {f["code"] for f in result["findings"]}
        self.assertIn("LEGACY_SECTION_NUMBERING_CONFLICT", codes)
        self.assertIn("RUNTIME_MICROSTEP_OUTLINE_INFLATION", codes)


if __name__ == "__main__":
    unittest.main()
