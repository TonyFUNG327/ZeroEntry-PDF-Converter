import sys
import unittest
from datetime import datetime
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from ocr_parsers.boc_ocr_pdf_converter import extract_accounts_from_text, validate_accounts


class TestBocOcrParser(unittest.TestCase):
    def test_extract_accounts_from_sample_text(self):
        text = """
        BANK OF CHINA HKD CURRENT ACCOUNT
        2025/04/01 B/F BALANCE 1,000.00
        2025/04/02 CUSTOMER RECEIPT 500.00 1,500.00
        2025/04/03 CHEQUE PAYMENT 200.00 1,300.00
        2025/04/30 BALANCE CARRIED FORWARD 1,300.00
        """
        accounts, warnings = extract_accounts_from_text(text)
        self.assertIn("BOC HKD Current Account", accounts)
        rows = accounts["BOC HKD Current Account"]
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[1]["Deposit"], 500.0)
        self.assertEqual(rows[2]["Withdrawal"], 200.0)
        self.assertEqual(rows[-1]["Control"], 1300.0)
        self.assertEqual(validate_accounts(accounts)[0]["balance_mismatches"], [])
        self.assertEqual(warnings, [])

    def test_unclassifiable_line_is_skipped_with_warning(self):
        text = """
        BANK OF CHINA HKD CURRENT ACCOUNT
        2025/04/01 B/F BALANCE 1,000.00
        2025/04/02 BROKEN OCR 500.00 9,999.00
        """
        accounts, warnings = extract_accounts_from_text(text)
        self.assertEqual(len(accounts["BOC HKD Current Account"]), 1)
        self.assertTrue(any("Could not classify" in warning for warning in warnings))

    def test_supported_date_formats_parse_to_rows(self):
        cases = [
            "2025/04/02",
            "2025-04-02",
            "02-Apr-25",
            "02-Apr-2025",
            "02 Apr 25",
            "02 Apr 2025",
        ]
        for date_text in cases:
            with self.subTest(date_text=date_text):
                text = f"""
                BANK OF CHINA HKD CURRENT ACCOUNT
                2025/04/01 B/F BALANCE 1,000.00
                {date_text} CUSTOMER RECEIPT 100.00 1,100.00
                """
                accounts, warnings = extract_accounts_from_text(text)
                self.assertIn("BOC HKD Current Account", accounts)
                rows = accounts["BOC HKD Current Account"]
                self.assertGreaterEqual(len(rows), 2)
                transaction = rows[1]
                self.assertEqual(transaction["Date"], datetime(2025, 4, 2))
                self.assertEqual(transaction["Deposit"], 100.0)
                self.assertEqual(transaction["Balance"], 1100.0)
                self.assertFalse(any("date format" in warning.lower() for warning in warnings))


if __name__ == "__main__":
    unittest.main()
