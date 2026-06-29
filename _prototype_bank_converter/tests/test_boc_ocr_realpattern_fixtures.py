import sys
import unittest
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

import calibrate_ocr_fixtures
from ocr_parsers import boc_ocr_pdf_converter


FIXTURE_DIR = APP_ROOT / "tests" / "fixtures" / "ocr_boc"
REALPATTERN_FIXTURES = (
    "boc_realpattern_sample_01_redacted.txt",
    "boc_realpattern_sample_02_redacted.txt",
)
MIN_BASELINE_RATIO = 0.5


class TestBocOcrRealPatternFixtures(unittest.TestCase):
    def test_realpattern_fixtures_exist_and_are_redacted(self):
        for fixture_name in REALPATTERN_FIXTURES:
            with self.subTest(fixture=fixture_name):
                fixture_path = FIXTURE_DIR / fixture_name
                self.assertTrue(fixture_path.exists())
                text = fixture_path.read_text(encoding="utf-8")

                self.assertIn("REDACTED", text)
                self.assertIn("ACCOUNT NO. XXXXXXXX", text)
                self.assertIn("CUSTOMER NAME: REDACTED CUSTOMER", text)
                self.assertIn("ADDRESS: REDACTED ADDRESS", text)
                self.assertNotIn("TOP CHOICE", text)
                self.assertNotIn("CASTLE PEAK", text)

    def test_realpattern_fixtures_parse_with_diagnostics(self):
        expected_accounts = {
            "boc_realpattern_sample_01_redacted.txt": "BOC HKD Current Account",
            "boc_realpattern_sample_02_redacted.txt": "BOC HKD Savings Account",
        }
        for fixture_name, expected_account in expected_accounts.items():
            with self.subTest(fixture=fixture_name):
                fixture_path = FIXTURE_DIR / fixture_name
                text = fixture_path.read_text(encoding="utf-8")
                result = boc_ocr_pdf_converter.extract_accounts_from_text_with_diagnostics(text)
                rows = result.accounts.get(expected_account, [])

                self.assertGreaterEqual(len(rows), 4)
                self.assertFalse(result.warnings)
                self.assertGreater(result.line_merge_diagnostics["merged_line_count"], 0)
                self.assertEqual(result.line_merge_diagnostics["blocked_merge_count"], 0)

    def test_realpattern_fixture_metrics_are_in_batch_summary(self):
        summary = calibrate_ocr_fixtures.build_aggregate_summary(FIXTURE_DIR)
        metrics_by_name = {item["fixture_name"]: item for item in summary["fixtures"]}

        for fixture_name in REALPATTERN_FIXTURES:
            with self.subTest(fixture=fixture_name):
                self.assertIn(fixture_name, metrics_by_name)
                metric = metrics_by_name[fixture_name]
                self.assertGreater(metric["parsed_transaction_row_count"], 0)
                self.assertGreater(metric["parse_success_ratio"], 0)
                self.assertLessEqual(metric["parse_success_ratio"], 1)
                self.assertGreater(metric["merged_line_count"], 0)
                self.assertEqual(metric["blocked_merge_count"], 0)

    def test_v20_9_batch_baseline_still_passes_with_realpattern_fixtures(self):
        summary = calibrate_ocr_fixtures.build_aggregate_summary(FIXTURE_DIR)

        self.assertGreaterEqual(summary["fixture_count"], 14)
        self.assertGreaterEqual(summary["overall_parse_success_ratio"], MIN_BASELINE_RATIO)
        self.assertGreater(summary["merged_line_total"], 0)
        self.assertGreaterEqual(summary["blocked_merge_total"], 0)

    def test_realpattern_fixtures_remain_text_only_ocr_inputs(self):
        for fixture_name in REALPATTERN_FIXTURES:
            with self.subTest(fixture=fixture_name):
                fixture_path = FIXTURE_DIR / fixture_name
                self.assertEqual(fixture_path.suffix, ".txt")
                self.assertNotIn("Desktop", str(fixture_path))
                self.assertNotIn("OCR_WORK", str(fixture_path))


if __name__ == "__main__":
    unittest.main()
