#!/usr/bin/env python3
import copy
import json
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
from validate_assessment_questions import validate_document  # noqa: E402


FIXTURE = Path(__file__).parent / "fixtures" / "valid_20.json"


def load_fixture():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def codes(result):
    return {issue["code"] for issue in result["errors"] + result["warnings"]}


class AssessmentValidatorTests(unittest.TestCase):
    def test_perfect_20_question_distribution_passes(self):
        result = validate_document(load_fixture())
        self.assertEqual(result["status"], "VALID")
        self.assertEqual(result["summary"]["answer_distribution"], {"A": 5, "B": 5, "C": 5, "D": 5})

    def test_all_answer_b_warns_for_bias_and_streak(self):
        data = load_fixture()
        for item in data["questions"]:
            item["correct_option"] = "B"
            for option in item["options"]:
                option["is_correct"] = option["label"] == "B"
                option.setdefault("misconception", "wrong position inference")
        result = validate_document(data)
        self.assertEqual(result["status"], "VALID_WITH_WARNINGS")
        self.assertIn("ANSWER_POSITION_BIAS", codes(result))
        self.assertIn("ANSWER_STREAK", codes(result))

    def test_three_answer_streak_is_detected(self):
        data = load_fixture()
        for index in range(3):
            data["questions"][index]["correct_option"] = "B"
            for option in data["questions"][index]["options"]:
                option["is_correct"] = option["label"] == "B"
        result = validate_document(data)
        self.assertIn("ANSWER_STREAK", codes(result))

    def test_correct_option_much_longer_is_detected(self):
        data = load_fixture()
        item = data["questions"][0]
        item["correct_option"] = "A"
        item["options"][0]["is_correct"] = True
        item["options"][0]["text"] = "A very long proposition that adds needless explanation and detail"
        result = validate_document(data)
        self.assertTrue({"OPTION_LENGTH_IMBALANCE", "OPTION_LENGTH_LEAK"} & codes(result))

    def test_duplicate_options_are_invalid(self):
        data = load_fixture()
        data["questions"][0]["options"][1]["text"] = data["questions"][0]["options"][0]["text"]
        result = validate_document(data)
        self.assertEqual(result["status"], "INVALID")
        self.assertIn("DUPLICATE_OPTION", codes(result))

    def test_only_three_options_are_invalid(self):
        data = load_fixture()
        data["questions"][0]["options"].pop()
        result = validate_document(data)
        self.assertEqual(result["status"], "INVALID")
        self.assertIn("OPTION_COUNT", codes(result))

    def test_missing_misconception_is_a_warning(self):
        data = load_fixture()
        data["questions"][0]["options"][1].pop("misconception")
        result = validate_document(data)
        self.assertIn("NON_DIAGNOSTIC_DISTRACTOR", codes(result))

    def test_negative_stem_and_all_above_are_warned(self):
        data = load_fixture()
        data["questions"][0]["stem"] = "Which choice is not all of the above?"
        data["questions"][0]["options"][3]["text"] = "All of the above"
        result = validate_document(data)
        self.assertIn("NEGATIVE_STEM", codes(result))
        self.assertIn("ABSOLUTE_OPTION", codes(result))

    def test_malformed_answer_index_is_invalid(self):
        data = load_fixture()
        data["questions"][0]["correct_option"] = 9
        result = validate_document(data)
        self.assertEqual(result["status"], "INVALID")
        self.assertIn("INVALID_ANSWER_POSITION", codes(result))

    def test_source_grounded_missing_evidence_warns_or_fails_strictly(self):
        data = load_fixture()
        data["questions"][0].pop("source_evidence")
        warning_result = validate_document(data)
        strict_result = validate_document(data, strict=True)
        self.assertEqual(warning_result["status"], "VALID_WITH_WARNINGS")
        self.assertEqual(strict_result["status"], "INVALID")
        self.assertIn("SOURCE_EVIDENCE_MISSING", codes(strict_result))

    def test_valid_level_five_scenario_passes(self):
        data = load_fixture()
        item = data["questions"][0]
        item["difficulty_level"] = 5
        item["cognitive_level"] = "architecture reasoning"
        result = validate_document({"questions": [item]})
        self.assertEqual(result["status"], "VALID")

    def test_repeated_abcd_pattern_is_detected(self):
        data = load_fixture()
        sequence = ["A", "B", "C", "D"] * 5
        for item, answer in zip(data["questions"], sequence):
            item["correct_option"] = answer
            for option in item["options"]:
                option["is_correct"] = option["label"] == answer
        result = validate_document(data)
        self.assertIn("ANSWER_PATTERN", codes(result))

    def test_balanced_non_obvious_order_passes(self):
        result = validate_document(load_fixture())
        self.assertNotIn("ANSWER_PATTERN", codes(result))
        self.assertNotIn("ANSWER_STREAK", codes(result))

    def test_tail_difficulty_degradation_is_detected(self):
        data = load_fixture()
        for item in data["questions"][:15]:
            item["difficulty_level"] = 5
        for item in data["questions"][15:]:
            item["difficulty_level"] = 1
        result = validate_document(data)
        self.assertIn("TAIL_QUALITY_DEGRADATION", codes(result))

    def test_multiple_correct_answers_are_invalid(self):
        data = load_fixture()
        data["questions"][0]["correct_option"] = ["A", "B"]
        result = validate_document(data)
        self.assertEqual(result["status"], "INVALID")
        self.assertIn("MULTIPLE_CORRECT", codes(result))

    def test_explicit_non_mcq4_option_count_is_supported(self):
        item = {
            "id": "Q5OPT",
            "question_type": "MCQ5",
            "stem": "Which statement is supported by the source?",
            "correct_option": "E",
            "options": [
                {"label": "A", "text": "A plausible boundary error", "misconception": "wrong layer"},
                {"label": "B", "text": "A plausible timing error", "misconception": "wrong timing"},
                {"label": "C", "text": "A plausible authority error", "misconception": "wrong authority"},
                {"label": "D", "text": "A plausible scope error", "misconception": "wrong scope"},
                {"label": "E", "text": "Supported proposition", "is_correct": True},
            ],
        }
        result = validate_document({"expected_option_count": 5, "questions": [item]})
        self.assertEqual(result["status"], "VALID")
        self.assertEqual(result["summary"]["answer_distribution"]["E"], 1)


if __name__ == "__main__":
    unittest.main()
