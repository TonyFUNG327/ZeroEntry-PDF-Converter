import sys
import unittest
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from core.bank_registry import (
    SCANNED_IMAGE_ONLY,
    ScannedPdfError,
    UnsupportedBankError,
    detect_bank_from_text,
    get_adapter,
)


class TestRegistrySafety(unittest.TestCase):
    def test_scanned_image_only_adapter_raises_scanned_pdf_error(self):
        with self.assertRaises(ScannedPdfError):
            get_adapter(SCANNED_IMAGE_ONLY)

    def test_unknown_or_missing_bank_code_raises_unsupported_bank_error(self):
        for bank_code in [None, "UNKNOWN_BANK"]:
            with self.subTest(bank_code=bank_code):
                with self.assertRaises(UnsupportedBankError):
                    get_adapter(bank_code)

    def test_empty_text_with_image_pages_detects_scanned_image_only(self):
        self.assertEqual(detect_bank_from_text("", page_checks=[(0, 1), (0, 2)]), SCANNED_IMAGE_ONLY)

    def test_supported_sample_texts_detect_existing_bank_codes(self):
        samples = {
            "HSBC": "HSBC Business Direct monthly statement",
            "HSB": "Hang Seng Bank HKD Statement Savings",
            "BOC": "BANK OF CHINA (HONG KONG) LIMITED monthly statement",
            "DBS": "DBS Bank (Hong Kong) Limited Current Account",
            "ICBC_ASIA": "INDUSTRIAL AND COMMERCIAL BANK OF CHINA (ASIA) LIMITED",
            "COMM": "Bank of Communications consolidated statement",
            "OCBC": "OCBC Bank BANK REFERENCE PORTFOLIO SUMMARY",
            "NCB": "Nanyang Commercial Bank Account Transaction Details",
        }
        for expected, text in samples.items():
            with self.subTest(expected=expected):
                self.assertEqual(detect_bank_from_text(text), expected)


if __name__ == "__main__":
    unittest.main()
