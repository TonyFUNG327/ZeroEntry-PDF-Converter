import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

import calibrate_ocr_fixtures


FIXTURE_DIR = APP_ROOT / "tests" / "fixtures" / "ocr_boc"


class TestCalibrateOcrFixtures(unittest.TestCase):
    def test_collect_redacted_fixtures_finds_multiple_files(self):
        fixtures = calibrate_ocr_fixtures.collect_redacted_fixtures(FIXTURE_DIR)

        self.assertGreaterEqual(len(fixtures), 10)
        self.assertTrue(all(path.name.endswith("_redacted.txt") for path in fixtures))

    def test_build_aggregate_summary_contains_required_metrics(self):
        summary = calibrate_ocr_fixtures.build_aggregate_summary(FIXTURE_DIR)

        self.assertGreaterEqual(summary["fixture_count"], 10)
        self.assertEqual(summary["fixture_count"], len(summary["fixtures"]))
        required_keys = {
            "fixture_name",
            "candidate_transaction_line_count",
            "parsed_transaction_row_count",
            "skipped_candidate_line_count",
            "parse_success_ratio",
            "warning_count",
            "skip_reason_counts",
            "merged_line_count",
            "blocked_merge_count",
        }
        for item in summary["fixtures"]:
            with self.subTest(fixture=item["fixture_name"]):
                self.assertTrue(required_keys.issubset(item))
                self.assertGreaterEqual(item["parse_success_ratio"], 0)
                self.assertLessEqual(item["parse_success_ratio"], 1)
                self.assertIsInstance(item["skip_reason_counts"], dict)
                self.assertIsInstance(item["merged_line_count"], int)
                self.assertIsInstance(item["blocked_merge_count"], int)

    def test_cli_writes_aggregate_summary_to_temp_output_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "calibration"
            with patch("builtins.print"):
                exit_code = calibrate_ocr_fixtures.main([str(FIXTURE_DIR), "--parser", "BOC", "--output-dir", str(output_dir)])

            self.assertEqual(exit_code, 0)
            output_path = output_dir / calibrate_ocr_fixtures.SUMMARY_FILENAME
            self.assertTrue(output_path.exists())
            payload = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertGreaterEqual(payload["fixture_count"], 10)
            self.assertTrue(payload["fixtures"])


if __name__ == "__main__":
    unittest.main()
