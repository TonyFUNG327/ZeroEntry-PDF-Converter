import csv
import sys
import tempfile
import unittest
from pathlib import Path

from openpyxl import Workbook, load_workbook


APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from classifier.engine import classify_transactions, detect_direction, summarize_classification
from classifier.io import read_transactions, write_workbook
from classifier.rules import RULE_FIELDS, load_rules
from classify_bank_transactions import build_arg_parser, run


def write_rules(path, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=RULE_FIELDS)
        writer.writeheader()
        for row in rows:
            base = {field: "" for field in RULE_FIELDS}
            base.update(row)
            writer.writerow(base)


def make_rule(rule_id, keyword, **overrides):
    row = {
        "rule_id": rule_id,
        "priority": "10",
        "enabled": "Yes",
        "match_type": "contains",
        "keyword": keyword,
        "direction": "Any",
        "category": rule_id,
        "account_code": "1000",
        "account_name": rule_id.title(),
        "tax_type": "Review",
        "counterparty": "",
        "confidence": "0.8",
        "review_needed": "No",
        "notes": "",
    }
    row.update(overrides)
    return row


class TestRuleClassifier(unittest.TestCase):
    def test_load_rules_orders_by_priority_and_skips_disabled_at_match_time(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "rules.csv"
            write_rules(
                path,
                [
                    make_rule("LOW", "fee", priority="50"),
                    make_rule("HIGH_DISABLED", "fee", priority="1", enabled="No"),
                    make_rule("HIGH", "fee", priority="2"),
                ],
            )
            rules = load_rules(path)
            rows = [{"Description": "Monthly fee", "Deposit": "", "Withdrawal": 10}]
            classified = classify_transactions(rows, rules)
            self.assertEqual(classified[0]["Rule_ID"], "HIGH")

    def test_contains_keyword_and_direction_filter(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "rules.csv"
            write_rules(path, [make_rule("RECEIPT", "customer", direction="Deposit")])
            rules = load_rules(path)
            classified = classify_transactions(
                [{"Description": "Customer payment", "Deposit": 100, "Withdrawal": ""}],
                rules,
            )
            self.assertEqual(classified[0]["Category"], "RECEIPT")
            self.assertEqual(classified[0]["Direction"], "Deposit")

    def test_direction_mismatch_goes_unclassified(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "rules.csv"
            write_rules(path, [make_rule("RECEIPT", "customer", direction="Deposit")])
            rules = load_rules(path)
            classified = classify_transactions(
                [{"Description": "Customer refund", "Deposit": "", "Withdrawal": 100}],
                rules,
            )
            self.assertEqual(classified[0]["Category"], "Unclassified")
            self.assertEqual(classified[0]["Review_Needed"], "Yes")

    def test_amount_min_and_max_filter(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "rules.csv"
            write_rules(path, [make_rule("SMALL_FEE", "fee", amount_min="1", amount_max="20")])
            rules = load_rules(path)
            classified = classify_transactions(
                [
                    {"Description": "Service fee", "Deposit": "", "Withdrawal": 10},
                    {"Description": "Service fee", "Deposit": "", "Withdrawal": 30},
                ],
                rules,
            )
            self.assertEqual(classified[0]["Rule_ID"], "SMALL_FEE")
            self.assertEqual(classified[1]["Classification_Source"], "unclassified")

    def test_detect_direction_unknown_when_both_amounts_present_or_missing(self):
        self.assertEqual(detect_direction({"Deposit": 5, "Withdrawal": 6}), "Unknown")
        self.assertEqual(detect_direction({"Deposit": "", "Withdrawal": ""}), "Unknown")

    def test_summary_counts_and_amounts(self):
        rows = [
            {"Description": "Bank charge", "Deposit": "", "Withdrawal": 25},
            {"Description": "Mystery", "Deposit": 50, "Withdrawal": ""},
        ]
        rules = [
            load_rules(APP_ROOT / "rules" / "classification_rules.csv")[0],
        ]
        classified = classify_transactions(rows, rules)
        summary = summarize_classification(classified)
        self.assertEqual(summary["transaction_count"], 2)
        self.assertEqual(summary["classified_count"], 1)
        self.assertEqual(summary["unclassified_count"], 1)
        self.assertEqual(summary["direction_amounts"]["Deposit"], 50)
        self.assertEqual(summary["direction_amounts"]["Withdrawal"], 25)

    def test_xlsx_input_and_output_columns(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_path = tmp_path / "input.xlsx"
            workbook = Workbook()
            sheet = workbook.active
            sheet.append(["Bank_Account", "Date", "Description", "Deposit", "Withdrawal", "Balance", "Control"])
            sheet.append(["HSBC", "2025-01-01", "Bank charge", "", 25, 975, 975])
            workbook.save(input_path)

            rows = read_transactions(input_path)
            rules = load_rules(APP_ROOT / "rules" / "classification_rules.csv")
            classified = classify_transactions(rows, rules)
            output_path = write_workbook(tmp_path / "classified.xlsx", classified)

            output = load_workbook(output_path)
            try:
                headers = [output.active.cell(1, col).value for col in range(1, output.active.max_column + 1)]
                self.assertIn("Rule_ID", headers)
                self.assertIn("Classification_Source", headers)
                self.assertEqual(output.active.cell(2, headers.index("Rule_ID") + 1).value, "BANK_CHARGE")
            finally:
                output.close()

    def test_cli_run_writes_all_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_path = tmp_path / "input.xlsx"
            output_path = tmp_path / "classified.xlsx"
            workbook = Workbook()
            sheet = workbook.active
            sheet.append(["Bank_Account", "Date", "Description", "Deposit", "Withdrawal", "Balance", "Control"])
            sheet.append(["HSBC", "2025-01-01", "Customer receipt", 1000, "", 2000, 2000])
            sheet.append(["HSBC", "2025-01-02", "Unknown item", "", 50, 1950, 1950])
            workbook.save(input_path)

            args = build_arg_parser().parse_args(
                [
                    str(input_path),
                    "--rules",
                    str(APP_ROOT / "rules" / "classification_rules.csv"),
                    "--output",
                    str(output_path),
                ]
            )
            result = run(args)

            self.assertTrue(result["output"].exists())
            self.assertTrue(result["review_output"].exists())
            self.assertTrue(result["summary_json"].exists())
            self.assertTrue(result["summary_txt"].exists())
            self.assertEqual(result["summary"]["transaction_count"], 2)
            self.assertEqual(result["summary"]["unclassified_count"], 1)


if __name__ == "__main__":
    unittest.main()
