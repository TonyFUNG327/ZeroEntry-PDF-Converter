import sys
import unittest
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from ocr_parsers.boc_ocr_pdf_converter import extract_accounts_from_text_with_diagnostics


class TestBocOcrAccountDetection(unittest.TestCase):
    def test_current_heading_sets_current_account(self):
        result = extract_accounts_from_text_with_diagnostics("""
        BANK OF CHINA HKD CURRENT ACCOUNT
        2025/04/01 B/F BALANCE 1,000.00
        """)
        self.assertIn("BOC HKD Current Account", result.accounts)

    def test_savings_heading_sets_savings_account(self):
        result = extract_accounts_from_text_with_diagnostics("""
        BANK OF CHINA HKD SAVINGS
        2025/04/01 B/F BALANCE 1,000.00
        """)
        self.assertIn("BOC HKD Savings Account", result.accounts)

    def test_default_account_adds_warning(self):
        result = extract_accounts_from_text_with_diagnostics("""
        BANK OF CHINA
        2025/04/01 B/F BALANCE 1,000.00
        """)
        self.assertIn("BOC HKD Current Account", result.accounts)
        self.assertTrue(any("defaulted to BOC HKD Current Account" in warning for warning in result.warnings))


if __name__ == "__main__":
    unittest.main()
