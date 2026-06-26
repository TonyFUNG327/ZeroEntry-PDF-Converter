import sys
import unittest
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from ocr_parsers.boc_ocr_pdf_converter import extract_accounts_from_text


class TestBocOcrDateFormats(unittest.TestCase):
    def test_supported_date_formats_parse(self):
        for date_text in ["2025/04/02", "2025-04-02", "02-Apr-25", "02-Apr-2025", "02 Apr 25", "02 Apr 2025"]:
            with self.subTest(date_text=date_text):
                text = f"""
                BANK OF CHINA HKD CURRENT ACCOUNT
                {date_text} B/F BALANCE 1,000.00
                """
                accounts, warnings = extract_accounts_from_text(text)
                self.assertEqual(len(accounts["BOC HKD Current Account"]), 1)
                self.assertFalse(any("Unrecognized date format" in warning for warning in warnings))


if __name__ == "__main__":
    unittest.main()
