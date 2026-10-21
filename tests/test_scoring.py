from decimal import Decimal
import unittest
from evaluations.scoring import average_rating, weighted_score, category_average
from evaluations.criteria import get_catalog, WEIGHTS


class TestScoring(unittest.TestCase):
    def test_na_is_ignored_zero_is_valid(self):
        self.assertEqual(average_rating({"a": "5", "b": "0", "c": "NA"}), Decimal("2.50"))

    def test_form_weights_match_supplied_guideline(self):
        self.assertEqual(WEIGHTS, {"student": 40, "department_head": 35, "peer": 15, "self": 10})
        self.assertEqual(weighted_score("student", {"a": "5"}), Decimal("40.00"))
        self.assertEqual(weighted_score("department_head", {"a": "5"}), Decimal("35.00"))
        self.assertEqual(weighted_score("peer", {"a": "5"}), Decimal("15.00"))
        self.assertEqual(weighted_score("self", {"a": "5"}), Decimal("10.00"))

    def test_no_numeric_responses_returns_zero(self):
        self.assertEqual(average_rating({"a": "NA", "b": "N/A"}), Decimal("0.00"))

    def test_category_average_only_counts_its_items(self):
        cat = {"items": [{"key": "a"}, {"key": "b"}]}
        self.assertEqual(category_average(cat, {"a": "4", "b": "2", "other": "5"}), Decimal("3.00"))

    def test_catalog_contains_all_four_academic_forms(self):
        self.assertGreater(len(get_catalog("student")), 0)
        self.assertGreater(len(get_catalog("department_head")), 0)
        self.assertGreater(len(get_catalog("peer")), 0)
        self.assertGreater(len(get_catalog("self")), 0)

if __name__ == "__main__":
    unittest.main()
