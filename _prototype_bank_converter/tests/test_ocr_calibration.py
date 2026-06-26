import sys
import unittest
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from ocr.ocr_diagnostics import analyze_ocr_text_for_diagnostics, attach_parser_diagnostics, build_calibration_summary
from ocr_parsers.boc_ocr_pdf_converter import extract_accounts_from_text_with_diagnostics


FIXTURE_DIR = APP_ROOT / "tests" / "fixtures" / "ocr_boc"


class TestOcrCalibration(unittest.TestCase):
    def test_redacted_boc_fixture_builds_parser_diagnostics_and_summary(self):
        text = (FIXTURE_DIR / "boc_scanned_sample_02_redacted.txt").read_text(encoding="utf-8")
        parser_result = extract_accounts_from_text_with_diagnostics(text)
        report = analyze_ocr_text_for_diagnostics(text)
        attach_parser_diagnostics(report, parser_result)
        summary = build_calibration_summary(report)

        self.assertTrue(parser_result.parsed_rows)
        self.assertTrue(parser_result.skipped_lines)
        self.assertTrue(parser_result.warnings)
        self.assertGreater(summary["candidate_transaction_line_count"], 0)
        self.assertEqual(summary["parsed_transaction_row_count"], len(parser_result.parsed_rows))
        self.assertEqual(summary["skipped_candidate_line_count"], len(parser_result.skipped_lines))
        self.assertEqual(summary["skip_reason_counts"]["Could not classify deposit/withdrawal"], 1)
        self.assertGreater(summary["parse_success_ratio"], 0)
        self.assertLess(summary["parse_success_ratio"], 1)

    def test_calibration_summary_handles_zero_candidate_count(self):
        report = {
            "candidate_transaction_line_count": 0,
            "parsed_transaction_row_count": 0,
            "skipped_candidate_line_count": 0,
            "warnings": [],
            "skipped_lines": [],
        }
        summary = build_calibration_summary(report)

        self.assertEqual(summary["parse_success_ratio"], 0)
        self.assertEqual(summary["skip_reason_counts"], {})


if __name__ == "__main__":
    unittest.main()
