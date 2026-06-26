import json
import sys
import tempfile
import unittest
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from ocr.ocr_diagnostics import (
    analyze_ocr_text_for_diagnostics,
    attach_parser_diagnostics,
    candidate_transaction_lines,
    format_diagnostic_report,
    write_diagnostic_report,
)
from ocr_parsers.boc_ocr_pdf_converter import extract_accounts_from_text_with_diagnostics


class TestOcrDiagnostics(unittest.TestCase):
    def test_analyze_ocr_text_for_diagnostics(self):
        text = """
        BANK OF CHINA
        2025/04/01 B/F BALANCE 1,000.00
        2025/04/02 TRANSFER 100.00 1,100.00
        02-Apr-25 CHEQUE 50.00 1,050.00
        """
        report = analyze_ocr_text_for_diagnostics(text)
        self.assertEqual(report["detected_bank_code"], "BOC")
        self.assertGreaterEqual(report["date_count"], 2)
        self.assertGreaterEqual(report["amount_count"], 4)
        self.assertGreaterEqual(report["candidate_transaction_line_count"], 2)

    def test_candidate_transaction_lines(self):
        text = "noise\n2025/04/01 TRANSFER 100.00 1,100.00\nnot a tx\n"
        self.assertEqual(candidate_transaction_lines(text), ["2025/04/01 TRANSFER 100.00 1,100.00"])

    def test_write_diagnostic_report_text_and_json(self):
        report = analyze_ocr_text_for_diagnostics("BANK OF CHINA 2025/04/01 100.00 200.00")
        with tempfile.TemporaryDirectory() as tmp:
            txt_path = Path(tmp) / "sample.diagnostic.txt"
            json_path = Path(tmp) / "sample.diagnostic.json"
            write_diagnostic_report(report, txt_path)
            write_diagnostic_report(report, json_path)
            self.assertIn("Detected bank: BOC", txt_path.read_text(encoding="utf-8"))
            self.assertEqual(json.loads(json_path.read_text(encoding="utf-8"))["detected_bank_code"], "BOC")

    def test_attach_parser_diagnostics_keys_and_format(self):
        text = """
        BANK OF CHINA HKD CURRENT ACCOUNT
        2025/04/01 B/F BALANCE 1,000.00
        2025/04/02 BROKEN OCR 500.00 9,999.00
        """
        parser_result = extract_accounts_from_text_with_diagnostics(text)
        report = analyze_ocr_text_for_diagnostics(text)
        attach_parser_diagnostics(report, parser_result)

        self.assertEqual(report["parsed_transaction_row_count"], 1)
        self.assertEqual(report["skipped_candidate_line_count"], 1)
        self.assertTrue(report["parsed_rows"])
        self.assertTrue(report["skipped_lines"])
        self.assertTrue(report["warnings"])
        rendered = format_diagnostic_report(report)
        for label in ["Parsed transaction rows", "Skipped candidate lines", "Parsed rows", "Skipped lines", "reason", "Warnings"]:
            self.assertIn(label, rendered)


if __name__ == "__main__":
    unittest.main()
