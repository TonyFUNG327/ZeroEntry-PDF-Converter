import sys
import unittest
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from ocr.ocr_diagnostics import analyze_ocr_text_for_diagnostics, attach_parser_diagnostics, format_diagnostic_report
from ocr_parsers.boc_ocr_pdf_converter import extract_accounts_from_text_with_diagnostics


class TestBocOcrParserDiagnostics(unittest.TestCase):
    def test_parser_result_preserves_warnings_and_skipped_lines(self):
        text = """
        BANK OF CHINA HKD CURRENT ACCOUNT
        2025/04/01 B/F BALANCE 1,000.00
        2025/04/02 BROKEN OCR 500.00 9,999.00
        """
        result = extract_accounts_from_text_with_diagnostics(text)

        self.assertEqual(len(result.parsed_rows), 1)
        self.assertEqual(len(result.skipped_lines), 1)
        self.assertEqual(result.skipped_lines[0]["reason"], "Could not classify deposit/withdrawal")
        self.assertTrue(result.warnings)

    def test_diagnostic_report_includes_parsed_and_skipped_sections(self):
        text = """
        BANK OF CHINA HKD CURRENT ACCOUNT
        2025/04/01 B/F BALANCE 1,000.00
        2025/04/02 BROKEN OCR 500.00 9,999.00
        """
        parser_result = extract_accounts_from_text_with_diagnostics(text)
        report = analyze_ocr_text_for_diagnostics(text)
        attach_parser_diagnostics(report, parser_result)
        rendered = format_diagnostic_report(report)

        self.assertIn("Parsed transaction rows: 1", rendered)
        self.assertIn("Skipped candidate lines: 1", rendered)
        self.assertIn("reason: Could not classify deposit/withdrawal", rendered)


if __name__ == "__main__":
    unittest.main()
