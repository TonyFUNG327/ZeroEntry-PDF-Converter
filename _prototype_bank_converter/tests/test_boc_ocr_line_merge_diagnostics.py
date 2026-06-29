import json
import sys
import tempfile
import unittest
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from ocr.ocr_diagnostics import analyze_ocr_text_for_diagnostics, attach_parser_diagnostics, build_calibration_summary, format_diagnostic_report, write_diagnostic_report
from ocr_parsers.boc_ocr_pdf_converter import extract_accounts_from_text_with_diagnostics, prepare_ocr_lines_with_diagnostics


FIXTURE_DIR = APP_ROOT / "tests" / "fixtures" / "ocr_boc"


def load_fixture(name):
    return (FIXTURE_DIR / name).read_text(encoding="utf-8")


def report_for_text(text):
    parser_result = extract_accounts_from_text_with_diagnostics(text)
    report = analyze_ocr_text_for_diagnostics(text)
    attach_parser_diagnostics(report, parser_result)
    return parser_result, report, build_calibration_summary(report)


class TestBocOcrLineMergeDiagnostics(unittest.TestCase):
    def test_three_line_split_transaction_is_merged_and_parsed(self):
        text = load_fixture("boc_scanned_sample_09_redacted.txt")
        prepared = prepare_ocr_lines_with_diagnostics(text)
        parser_result, report, summary = report_for_text(text)
        rows = parser_result.accounts["BOC HKD Current Account"]

        self.assertIn(
            "2025/09/02 CUSTOMER RECEIPT REDACTED MERCHANT 100.00 1,100.00",
            prepared.lines,
        )
        self.assertIn(
            "2025/09/03 REDACTED MERCHANT PAYMENT REFERENCE REDACTED 50.00 1,050.00",
            prepared.lines,
        )
        self.assertEqual(rows[1]["Deposit"], 100.0)
        self.assertEqual(rows[2]["Withdrawal"], 50.0)
        self.assertEqual(report["line_merge_diagnostics"]["merged_line_count"], 2)
        self.assertGreater(summary["parse_success_ratio"], 0)
        self.assertLessEqual(summary["parse_success_ratio"], 1)

    def test_metadata_line_blocks_merge_and_preserves_skip_reason(self):
        text = load_fixture("boc_scanned_sample_10_redacted.txt")
        prepared = prepare_ocr_lines_with_diagnostics(text)
        parser_result, report, summary = report_for_text(text)
        reasons = [item["reason"] for item in parser_result.skipped_lines]

        self.assertNotIn("2025/09/02 CUSTOMER RECEIPT ACCOUNT NO. XXXXXXXX5678 100.00 2,100.00", prepared.lines)
        self.assertIn("Skipped dated line without amount", reasons)
        self.assertEqual(report["line_merge_diagnostics"]["merged_line_count"], 1)
        self.assertGreater(summary["parse_success_ratio"], 0)
        self.assertLessEqual(summary["parse_success_ratio"], 1)

    def test_line_merge_diagnostics_are_rendered_and_written_to_json(self):
        text = load_fixture("boc_scanned_sample_09_redacted.txt")
        _parser_result, report, _summary = report_for_text(text)
        rendered = format_diagnostic_report(report)

        self.assertIn("Line merge diagnostics:", rendered)
        self.assertIn("Merged lines: 2", rendered)
        self.assertIn("Merged line samples:", rendered)

        with tempfile.TemporaryDirectory() as tmp:
            json_path = Path(tmp) / "diagnostic.json"
            write_diagnostic_report(report, json_path)
            payload = json.loads(json_path.read_text(encoding="utf-8"))

        self.assertIn("line_merge_diagnostics", payload)
        self.assertEqual(payload["line_merge_diagnostics"]["merged_line_count"], 2)
        self.assertTrue(payload["line_merge_diagnostics"]["merged_lines"])


if __name__ == "__main__":
    unittest.main()
