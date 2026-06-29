import sys
import unittest
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from ocr.ocr_diagnostics import analyze_ocr_text_for_diagnostics, attach_parser_diagnostics, build_calibration_summary
from ocr_parsers.boc_ocr_pdf_converter import extract_accounts_from_text_with_diagnostics


FIXTURE_DIR = APP_ROOT / "tests" / "fixtures" / "ocr_boc"


def parse_fixture(name):
    text = (FIXTURE_DIR / name).read_text(encoding="utf-8")
    parser_result = extract_accounts_from_text_with_diagnostics(text)
    report = analyze_ocr_text_for_diagnostics(text)
    attach_parser_diagnostics(report, parser_result)
    return parser_result, build_calibration_summary(report)


class TestBocOcrParserCalibration(unittest.TestCase):
    def test_new_redacted_fixtures_are_readable(self):
        for name in [
            "boc_scanned_sample_03_redacted.txt",
            "boc_scanned_sample_04_redacted.txt",
            "boc_scanned_sample_05_redacted.txt",
        ]:
            with self.subTest(name=name):
                text = (FIXTURE_DIR / name).read_text(encoding="utf-8")
                self.assertIn("REDACTED", text)
                self.assertIn("ACCOUNT NO. XXXXXXXX", text)

    def test_parser_normalizes_spaced_amount_thousands_separator(self):
        parser_result, summary = parse_fixture("boc_scanned_sample_03_redacted.txt")
        rows = parser_result.accounts["BOC HKD Current Account"]

        self.assertEqual(rows[0]["Description"], "B/F BALANCE")
        self.assertEqual(rows[0]["Balance"], 1000.0)
        self.assertEqual(rows[1]["Deposit"], 100.0)
        self.assertEqual(rows[2]["Withdrawal"], 50.0)
        self.assertEqual(rows[-1]["Control"], 1025.0)
        self.assertEqual(summary["skipped_candidate_line_count"], 0)

    def test_parser_handles_amount_like_token_in_description(self):
        parser_result, summary = parse_fixture("boc_scanned_sample_04_redacted.txt")
        rows = parser_result.accounts["BOC HKD Current Account"]

        receipt_row = rows[1]
        self.assertIn("REDACTED MERCHANT", receipt_row["Description"])
        self.assertEqual(receipt_row["Deposit"], 300.0)
        self.assertEqual(receipt_row["Balance"], 2300.0)
        self.assertEqual(summary["skip_reason_counts"]["Could not classify deposit/withdrawal"], 1)
        self.assertGreater(summary["parse_success_ratio"], 0)
        self.assertLess(summary["parse_success_ratio"], 1)

    def test_parser_records_stable_skip_reasons_for_noisy_candidates(self):
        parser_result, summary = parse_fixture("boc_scanned_sample_05_redacted.txt")
        reasons = [item["reason"] for item in parser_result.skipped_lines]

        self.assertIn("Skipped dated line without amount", reasons)
        self.assertIn("Skipped transaction line without transaction amount", reasons)
        self.assertEqual(summary["skip_reason_counts"]["Skipped dated line without amount"], 1)
        self.assertEqual(summary["skip_reason_counts"]["Skipped transaction line without transaction amount"], 1)
        self.assertTrue(parser_result.warnings)
        self.assertGreater(summary["parse_success_ratio"], 0)


if __name__ == "__main__":
    unittest.main()
