#!/usr/bin/env python3
"""Regression tests for the neutral A/B blind-review gate."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("before_after", ROOT / "scripts" / "validate_before_after_review.py")
before_after = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = before_after
SPEC.loader.exec_module(before_after)


PAGE_TYPES = sorted(before_after.REQUIRED_PAGE_TYPES)


def review(result: str = "YES") -> dict:
    return {
        "result": result,
        "comparisons": [
            {"page_type": page_type, "labels": ["A", "B"], "a": f"{page_type}-a.png", "b": f"{page_type}-b.png", "winner": "A", "candidate_side": "A"}
            for page_type in PAGE_TYPES
        ],
    }


class BeforeAfterReviewTests(unittest.TestCase):
    def test_ten_neutral_comparisons_pass(self):
        self.assertEqual(before_after.validate(review())["status"], "VALID")

    def test_mixed_review_does_not_pass_as_yes(self):
        data = review("YES")
        data["comparisons"][0]["winner"] = "MIXED"
        self.assertEqual(before_after.validate(data)["status"], "INVALID")

    def test_evaluative_labels_are_rejected(self):
        data = review()
        data["comparisons"][0]["a"] = "GOOD"
        self.assertEqual(before_after.validate(data)["status"], "INVALID")


if __name__ == "__main__":
    unittest.main()
