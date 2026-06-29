import sys
import unittest
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

import calibrate_ocr_fixtures


FIXTURE_DIR = APP_ROOT / "tests" / "fixtures" / "ocr_boc"
MIN_OVERALL_PARSE_SUCCESS_RATIO = 0.5


class TestBocOcrCalibrationBaseline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.summary = calibrate_ocr_fixtures.build_aggregate_summary(FIXTURE_DIR)

    def test_aggregate_summary_totals_are_present(self):
        summary = self.summary

        self.assertGreaterEqual(summary["fixture_count"], 10)
        self.assertGreater(summary["total_candidate_transaction_line_count"], 0)
        self.assertGreater(summary["total_parsed_transaction_row_count"], 0)
        self.assertGreaterEqual(summary["total_skipped_candidate_line_count"], 0)
        self.assertGreater(summary["overall_parse_success_ratio"], 0)
        self.assertLessEqual(summary["overall_parse_success_ratio"], 1)
        self.assertGreater(summary["average_parse_success_ratio"], 0)
        self.assertLessEqual(summary["average_parse_success_ratio"], 1)

    def test_aggregate_summary_reason_and_merge_totals_are_typed(self):
        summary = self.summary

        self.assertIsInstance(summary["skip_reason_totals"], dict)
        self.assertIsInstance(summary["blocked_merge_reason_totals"], dict)
        self.assertIsInstance(summary["merged_line_total"], int)
        self.assertIsInstance(summary["blocked_merge_total"], int)
        self.assertGreaterEqual(summary["merged_line_total"], 0)
        self.assertGreaterEqual(summary["blocked_merge_total"], 0)

    def test_lowest_parse_success_fixture_is_recorded(self):
        summary = self.summary

        self.assertIsInstance(summary["lowest_parse_success_fixture"], str)
        self.assertTrue(summary["lowest_parse_success_fixture"].endswith("_redacted.txt"))
        self.assertGreaterEqual(summary["lowest_parse_success_ratio"], 0)
        self.assertLessEqual(summary["lowest_parse_success_ratio"], 1)

    def test_overall_parse_success_ratio_baseline(self):
        self.assertGreaterEqual(self.summary["overall_parse_success_ratio"], MIN_OVERALL_PARSE_SUCCESS_RATIO)


if __name__ == "__main__":
    unittest.main()
