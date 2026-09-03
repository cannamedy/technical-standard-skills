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
READER_SPEC = importlib.util.spec_from_file_location("reader_first_audit", ROOT / "scripts" / "audit_reader_first.py")
reader_audit = importlib.util.module_from_spec(READER_SPEC)
assert READER_SPEC.loader is not None
sys.modules[READER_SPEC.name] = reader_audit
READER_SPEC.loader.exec_module(reader_audit)


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

    def test_reader_first_fixture_signals_are_explicitly_classified(self):
        cases = ROOT / "tests" / "fixtures" / "reader_first_cases"
        self.assertIn("CONCEPT_GLOSSARY_WALL", {f["code"] for f in reader_audit.audit_text((cases / "01_glossary_heavy.md").read_text(encoding="utf-8"))["findings"]})
        self.assertIn("DESIGN_SPINE_MISSING", {f["code"] for f in reader_audit.audit_text((cases / "02_principles_isolated.md").read_text(encoding="utf-8"))["findings"]})
        self.assertEqual(reader_audit.audit_text((cases / "03_reader_entry_pass.md").read_text(encoding="utf-8"))["status"], "HUMAN_READABILITY_PASS")
        self.assertIn("TEMPLATE_RHYTHM_OVERUSE", {f["code"] for f in reader_audit.audit_text((cases / "04_template_rhythm.md").read_text(encoding="utf-8"))["findings"]})
        self.assertIn("ABSTRACT_NOUN_STACKING", {f["code"] for f in reader_audit.audit_text((cases / "05_abstract_nouns.md").read_text(encoding="utf-8"))["findings"]})
        self.assertIn("CHINESE_ENGLISH_FRAGMENTATION", {f["code"] for f in reader_audit.audit_text((cases / "06_mixed_language.md").read_text(encoding="utf-8"))["findings"]})
        self.assertEqual(reader_audit.audit_text((cases / "07_good_mixed_language.md").read_text(encoding="utf-8"))["status"], "HUMAN_READABILITY_PASS")
        self.assertEqual(reader_audit.audit_text((cases / "08_concrete_before_abstract.md").read_text(encoding="utf-8"))["status"], "HUMAN_READABILITY_PASS")
        self.assertEqual(reader_audit.audit_text((cases / "09_propagated_principle.md").read_text(encoding="utf-8"))["status"], "HUMAN_READABILITY_PASS")
        self.assertEqual(reader_audit.audit_text((cases / "10_deep_without_simplification.md").read_text(encoding="utf-8"))["status"], "HUMAN_READABILITY_PASS")


if __name__ == "__main__":
    unittest.main()
