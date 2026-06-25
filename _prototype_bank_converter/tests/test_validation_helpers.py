import sys
import unittest
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from core.validation import format_report_item, summarize_account, summarize_accounts


class TestValidationHelpers(unittest.TestCase):
    def test_summarize_empty_account(self):
        summary = summarize_account("Empty", [])
        self.assertEqual(summary["rows"], 0)
        self.assertEqual(summary["deposit_total"], 0)
        self.assertEqual(summary["withdrawal_total"], 0)
        self.assertIsNone(summary["final_balance"])
        self.assertEqual(summary["balance_mismatches"], [])
        self.assertIn("rows=0", format_report_item(summary))

    def test_summarize_mismatch_account(self):
        rows = [
            {"Deposit": None, "Withdrawal": None, "Balance": 100.0, "Control": 100.0},
            {"Deposit": 10.0, "Withdrawal": None, "Balance": 120.0, "Control": 110.0},
        ]
        summary = summarize_account("Mismatch", rows)
        self.assertEqual(summary["rows"], 2)
        self.assertEqual(summary["deposit_total"], 10.0)
        self.assertEqual(summary["balance_mismatches"], [3])
        self.assertIn("balance_mismatches=1", format_report_item(summary))

    def test_summarize_accounts_collection(self):
        summaries = summarize_accounts({"A": []})
        self.assertEqual(len(summaries), 1)
        self.assertEqual(summaries[0]["account"], "A")


if __name__ == "__main__":
    unittest.main()
