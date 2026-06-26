import sys
import unittest
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from ocr.ocr_errors import OcrQualityError
from ocr.ocr_quality import analyze_ocr_text, validate_ocr_quality


class TestOcrQuality(unittest.TestCase):
    def test_short_text_fails_quality_gate(self):
        with self.assertRaises(OcrQualityError):
            validate_ocr_quality("HSBC", min_text_length=20)

    def test_supported_bank_dates_and_amounts_pass(self):
        text = """
        HSBC Business Direct
        Statement Date 2025/01/31
        2025/01/01 B/F BALANCE 1,000.00
        2025/01/02 TRANSFER 100.00 1,100.00
        """
        report = validate_ocr_quality(text, min_text_length=20, min_date_count=2, min_amount_count=2)
        self.assertEqual(report.bank_code, "HSBC")
        self.assertGreaterEqual(report.date_count, 2)
        self.assertGreaterEqual(report.amount_count, 2)

    def test_unknown_bank_fails_quality_gate(self):
        text = "2025/01/01 Something 100.00 200.00 " * 5
        with self.assertRaises(OcrQualityError):
            validate_ocr_quality(text, min_text_length=20, min_date_count=1, min_amount_count=1)

    def test_analyze_ocr_text_reports_bank_code(self):
        report = analyze_ocr_text("DBS Bank (Hong Kong) Limited 2025/01/01 100.00 200.00")
        self.assertEqual(report.bank_code, "DBS")


if __name__ == "__main__":
    unittest.main()

