import json
import sys
import tempfile
import unittest
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from ocr.ocr_diagnostics import analyze_ocr_text_for_diagnostics, attach_parser_diagnostics, build_calibration_summary, write_diagnostic_report
from ocr_parsers.boc_ocr_pdf_converter import extract_accounts_from_text_with_diagnostics, prepare_ocr_lines_with_diagnostics


FIXTURE_DIR = APP_ROOT / "tests" / "fixtures" / "ocr_boc"


def load_fixture(name):
    return (FIXTURE_DIR / name).read_text(encoding="utf-8")


def parse_fixture(name):
    text = load_fixture(name)
    parser_result = extract_accounts_from_text_with_diagnostics(text)
    report = analyze_ocr_text_for_diagnostics(text)
    attach_parser_diagnostics(report, parser_result)
    return text, parser_result, report, build_calibration_summary(report)


class TestBocOcrLineMergeGuards(unittest.TestCase):
    def test_guard_fixtures_are_redacted(self):
        for name in ["boc_scanned_sample_11_redacted.txt", "boc_scanned_sample_12_redacted.txt"]:
            with self.subTest(name=name):
                text = load_fixture(name)
                self.assertIn("REDACTED", text)
                self.assertIn("ACCOUNT NO. XXXXXXXX", text)

    def test_random_noise_between_date_and_amount_is_not_merged(self):
        text, parser_result, report, summary = parse_fixture("boc_scanned_sample_11_redacted.txt")
        prepared = prepare_ocr_lines_with_diagnostics(text)
        logical_lines = prepared.lines
        blocked_reasons = [item["reason"] for item in report["line_merge_diagnostics"]["blocked_merges"]]
        rows = parser_result.accounts["BOC HKD Current Account"]

        self.assertNotIn("2025/10/02 CUSTOMER RECEIPT RANDOM OCR NOISE WITHOUT AMOUNT 100.00 1,100.00", logical_lines)
        self.assertIn("description_continuation_not_recognized", blocked_reasons)
        self.assertEqual(rows[1]["Date"].strftime("%Y/%m/%d"), "2025/10/03")
        self.assertEqual(rows[1]["Deposit"], 100.0)
        self.assertGreater(summary["parse_success_ratio"], 0)
        self.assertLessEqual(summary["parse_success_ratio"], 1)

    def test_legitimate_continuation_is_still_merged_and_parsed(self):
        text, _parser_result, report, _summary = parse_fixture("boc_scanned_sample_11_redacted.txt")
        prepared = prepare_ocr_lines_with_diagnostics(text)

        self.assertIn("2025/10/03 CUSTOMER RECEIPT TRANSACTION PARTY REDACTED MERCHANT 100.00 1,100.00", prepared.lines)
        merge_types = [item["merge_type"] for item in report["line_merge_diagnostics"]["merged_lines"]]
        self.assertIn("two_line_continuation", merge_types)

    def test_metadata_line_blocks_merge(self):
        text, parser_result, report, _summary = parse_fixture("boc_scanned_sample_11_redacted.txt")
        prepared = prepare_ocr_lines_with_diagnostics(text)
        blocked_reasons = [item["reason"] for item in report["line_merge_diagnostics"]["blocked_merges"]]

        self.assertNotIn("2025/10/04 CUSTOMER RECEIPT ACCOUNT NO. XXXXXXXX1234 100.00 1,200.00", prepared.lines)
        self.assertIn("metadata_line_blocked", blocked_reasons)
        self.assertNotIn("2025/10/04", [item["row"]["Date"].strftime("%Y/%m/%d") for item in parser_result.parsed_rows])

    def test_next_date_and_missing_amount_blocks_are_reported(self):
        _text, _parser_result, report, summary = parse_fixture("boc_scanned_sample_12_redacted.txt")
        blocked_reasons = [item["reason"] for item in report["line_merge_diagnostics"]["blocked_merges"]]

        self.assertIn("next_line_is_new_date", blocked_reasons)
        self.assertIn("description_continuation_not_recognized", blocked_reasons)
        self.assertGreater(summary["parse_success_ratio"], 0)
        self.assertLessEqual(summary["parse_success_ratio"], 1)

    def test_diagnostic_json_contains_merge_type_and_blocked_reasons(self):
        _text, _parser_result, report, _summary = parse_fixture("boc_scanned_sample_11_redacted.txt")
        with tempfile.TemporaryDirectory() as tmp:
            json_path = Path(tmp) / "diagnostic.json"
            write_diagnostic_report(report, json_path)
            payload = json.loads(json_path.read_text(encoding="utf-8"))

        diagnostics = payload["line_merge_diagnostics"]
        self.assertTrue(diagnostics["merged_lines"])
        self.assertIn("merge_type", diagnostics["merged_lines"][0])
        self.assertTrue(diagnostics["blocked_merges"])
        self.assertIn("reason", diagnostics["blocked_merges"][0])


if __name__ == "__main__":
    unittest.main()
