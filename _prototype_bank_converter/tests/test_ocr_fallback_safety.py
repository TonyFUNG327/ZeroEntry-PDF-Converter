import sys
import unittest
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from convert_bank_pdf import is_no_account_rows_error
from core.bank_registry import ParserExecutionError


class TestOcrFallbackSafety(unittest.TestCase):
    def test_detects_no_account_rows_errors(self):
        self.assertTrue(is_no_account_rows_error(ParserExecutionError("BOC parser returned no account rows.")))
        self.assertTrue(is_no_account_rows_error(ParserExecutionError("returned no account rows after OCR")))

    def test_rejects_non_no_rows_parser_errors(self):
        self.assertFalse(is_no_account_rows_error(ParserExecutionError("BOC parser failed: write_workbook failed")))
        self.assertFalse(is_no_account_rows_error(ParserExecutionError("BOC parser failed: unexpected layout")))


if __name__ == "__main__":
    unittest.main()
