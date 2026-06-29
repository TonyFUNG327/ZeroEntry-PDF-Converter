import sys
import unittest
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from ocr.ocr_diagnostics import analyze_ocr_text_for_diagnostics, attach_parser_diagnostics, build_calibration_summary
from ocr_parsers.boc_ocr_pdf_converter import extract_accounts_from_text_with_diagnostics, normalize_ocr_line, prepare_ocr_lines


FIXTURE_DIR = APP_ROOT / "tests" / "fixtures" / "ocr_boc"


def parse_fixture(name):
    text = (FIXTURE_DIR / name).read_text(encoding="utf-8")
    parser_result = extract_accounts_from_text_with_diagnostics(text)
    report = analyze_ocr_text_for_diagnostics(text)
    attach_parser_diagnostics(report, parser_result)
    return text, parser_result, build_calibration_summary(report)


class TestBocOcrLineMerge(unittest.TestCase):
    def test_new_line_merge_fixtures_are_redacted(self):
        for name in [
            "boc_scanned_sample_06_redacted.txt",
            "boc_scanned_sample_07_redacted.txt",
            "boc_scanned_sample_08_redacted.txt",
        ]:
            with self.subTest(name=name):
                text = (FIXTURE_DIR / name).read_text(encoding="utf-8")
                self.assertIn("REDACTED", text)
                self.assertIn("ACCOUNT NO. XXXXXXXX", text)

    def test_split_transaction_and_amount_lines_are_merged_and_parsed(self):
        text, parser_result, summary = parse_fixture("boc_scanned_sample_06_redacted.txt")
        logical_lines = prepare_ocr_lines(text)
        rows = parser_result.accounts["BOC HKD Current Account"]

        self.assertIn("2025/08/02 CUSTOMER RECEIPT 100.00 1,100.00", logical_lines)
        self.assertIn("2025/08/03 REDACTED MERCHANT PAYMENT 50.00 1,050.00", logical_lines)
        self.assertEqual(rows[0]["Balance"], 1000.0)
        self.assertEqual(rows[1]["Deposit"], 100.0)
        self.assertEqual(rows[2]["Withdrawal"], 50.0)
        self.assertGreater(summary["parse_success_ratio"], 0)

    def test_amount_like_description_token_does_not_hide_transaction_amount(self):
        text, parser_result, summary = parse_fixture("boc_scanned_sample_07_redacted.txt")
        rows = parser_result.accounts["BOC HKD Current Account"]

        self.assertIn("2025/08/04 REF 888.00 CUSTOMER RECEIPT 25.00 2,025.00", prepare_ocr_lines(text))
        self.assertIn("REF", rows[1]["Description"])
        self.assertEqual(rows[1]["Deposit"], 25.0)
        self.assertEqual(rows[1]["Balance"], 2025.0)
        self.assertNotIn("UNRELATED OCR NOISE LINE 999.00", [item["line"] for item in parser_result.parsed_rows])
        self.assertGreater(summary["parse_success_ratio"], 0)

    def test_amount_o_is_normalized_but_description_o_is_preserved(self):
        self.assertEqual(normalize_ocr_line("2025/08/01 B/F BALANCE 1,0O0.00"), "2025/08/01 B/F BALANCE 1,000.00")
        self.assertEqual(normalize_ocr_line("DESCRIPTION WITH LETTER O SHOULD STAY OPEN"), "DESCRIPTION WITH LETTER O SHOULD STAY OPEN")

        text, parser_result, summary = parse_fixture("boc_scanned_sample_08_redacted.txt")
        rows = parser_result.accounts["BOC HKD Current Account"]
        reasons = [item["reason"] for item in parser_result.skipped_lines]

        self.assertEqual(rows[0]["Balance"], 1000.0)
        self.assertEqual(rows[1]["Deposit"], 100.0)
        self.assertIn("LETTER O SHOULD STAY OPEN", rows[2]["Description"])
        self.assertIn("Skipped dated line without amount", reasons)
        self.assertGreater(summary["parse_success_ratio"], 0)
        self.assertLessEqual(summary["parse_success_ratio"], 1)


if __name__ == "__main__":
    unittest.main()
