import sys
import unittest
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from core.bank_registry import SCANNED_IMAGE_ONLY, detect_bank_from_text, get_adapter


class TestBankRegistry(unittest.TestCase):
    def test_detect_supported_banks_from_sample_text(self):
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
                self.assertEqual(get_adapter(expected).code, expected)

    def test_detect_scanned_image_only(self):
        self.assertEqual(detect_bank_from_text("", page_checks=[(0, 1), (0, 2)]), SCANNED_IMAGE_ONLY)

    def test_detect_unknown(self):
        self.assertIsNone(detect_bank_from_text("Some unsupported statement"))


if __name__ == "__main__":
    unittest.main()
