import csv
import re
import sys
import tempfile
import unittest
from pathlib import Path

from openpyxl import Workbook


APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from classifier.engine import OUTPUT_COLUMNS
from classifier.mappings import write_mappings
from classifier.review import MANUAL_REVIEW_COLUMNS
from classifier.simple_manual import (
    SIMPLE_MANUAL_COLUMNS,
    extract_mappings_from_simple_manual_rows,
    infer_amount,
    infer_direction,
    read_simple_manual_rows,
    simple_manual_rows_to_reviewed_rows,
)
from merge_confirmed_mappings import build_arg_parser, run


EXPERIENCE_DB = APP_ROOT / "experience_db"


def read_csv_rows(path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def read_header(path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return next(csv.reader(handle))


class TestSimpleManualTemplateA32(unittest.TestCase):
    def test_manual_classification_template_is_header_only(self):
        rows = read_csv_rows(EXPERIENCE_DB / "manual_classification_template.csv")
        self.assertEqual(rows, [])

    def test_manual_classification_template_headers_exactly_match_full_reviewed_columns(self):
        self.assertEqual(read_header(EXPERIENCE_DB / "manual_classification_template.csv"), OUTPUT_COLUMNS + MANUAL_REVIEW_COLUMNS)

    def test_simple_manual_classification_template_exists(self):
        self.assertTrue((EXPERIENCE_DB / "simple_manual_classification_template.csv").exists())

    def test_simple_template_headers_exactly_match_expected_simplified_columns(self):
        self.assertEqual(read_header(EXPERIENCE_DB / "simple_manual_classification_template.csv"), SIMPLE_MANUAL_COLUMNS)

    def test_simple_template_contains_exactly_two_synthetic_example_rows(self):
        rows = read_csv_rows(EXPERIENCE_DB / "simple_manual_classification_template.csv")
        self.assertEqual(len(rows), 2)
        self.assertTrue(all("Synthetic" in row["Bank_Account"] for row in rows))

    def test_simple_template_does_not_contain_sensitive_sample_data(self):
        content = (EXPERIENCE_DB / "simple_manual_classification_template.csv").read_text(encoding="utf-8")
        self.assertNotRegex(content, r"HSBC|DBS|OCBC|ICBC|Hang Seng|Account No|[0-9]{8,}")

    def test_read_simple_csv_rows(self):
        rows = read_simple_manual_rows(EXPERIENCE_DB / "simple_manual_classification_template.csv")
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["Description"], "Synthetic customer receipt")

    def test_infer_deposit_direction(self):
        self.assertEqual(infer_direction({"Deposit": "100", "Withdrawal": ""}), "Deposit")

    def test_infer_withdrawal_direction(self):
        self.assertEqual(infer_direction({"Deposit": "", "Withdrawal": "100"}), "Withdrawal")

    def test_infer_unknown_direction_when_both_blank(self):
        self.assertEqual(infer_direction({"Deposit": "", "Withdrawal": ""}), "Unknown")

    def test_infer_unknown_direction_when_both_have_values(self):
        self.assertEqual(infer_direction({"Deposit": "100", "Withdrawal": "50"}), "Unknown")

    def test_calculate_amount_from_deposit(self):
        row = {"Deposit": "1200.00", "Withdrawal": ""}
        self.assertEqual(infer_amount(row, infer_direction(row)), 1200.0)

    def test_calculate_amount_from_withdrawal(self):
        row = {"Deposit": "", "Withdrawal": "5000.00"}
        self.assertEqual(infer_amount(row, infer_direction(row)), 5000.0)

    def test_convert_simple_rows_to_reviewed_rows(self):
        rows = simple_manual_rows_to_reviewed_rows(read_simple_manual_rows(EXPERIENCE_DB / "simple_manual_classification_template.csv"))
        self.assertEqual(rows[0]["Direction"], "Deposit")
        self.assertEqual(rows[0]["Classification_Source"], "manual_simple")
        self.assertEqual(rows[1]["Direction"], "Withdrawal")

    def test_confirmed_row_becomes_mapping_candidate(self):
        rows = read_simple_manual_rows(EXPERIENCE_DB / "simple_manual_classification_template.csv")
        mappings = extract_mappings_from_simple_manual_rows([rows[0]])
        self.assertEqual(len(mappings), 1)
        self.assertEqual(mappings[0]["source_review_status"], "Confirmed")

    def test_corrected_row_becomes_mapping_candidate(self):
        rows = read_simple_manual_rows(EXPERIENCE_DB / "simple_manual_classification_template.csv")
        mappings = extract_mappings_from_simple_manual_rows([rows[1]])
        self.assertEqual(len(mappings), 1)
        self.assertEqual(mappings[0]["source_review_status"], "Corrected")

    def test_pending_ignore_need_advice_blank_do_not_become_mapping_candidates(self):
        base = read_simple_manual_rows(EXPERIENCE_DB / "simple_manual_classification_template.csv")[0]
        rows = []
        for status in ["Pending", "Ignore", "Need_Advice", ""]:
            row = dict(base)
            row["Manual_Review_Status"] = status
            rows.append(row)
        self.assertEqual(extract_mappings_from_simple_manual_rows(rows), [])

    def test_lowercase_and_uppercase_status_normalization_works(self):
        rows = read_simple_manual_rows(EXPERIENCE_DB / "simple_manual_classification_template.csv")
        rows[0]["Manual_Review_Status"] = "confirmed"
        rows[1]["Manual_Review_Status"] = "CORRECTED"
        reviewed = simple_manual_rows_to_reviewed_rows(rows)
        self.assertEqual(reviewed[0]["Manual_Review_Status"], "Confirmed")
        self.assertEqual(reviewed[1]["Manual_Review_Status"], "Corrected")

    def test_invalid_header_with_leading_trailing_spaces_raises_value_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.csv"
            path.write_text(
                "Bank_Account,Date,Description, Deposit ,Withdrawal,Manual_Category,Manual_Account_Code,Manual_Account_Name,Manual_Tax_Type,Manual_Counterparty,Manual_Review_Status,Manual_Notes\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "Invalid simple manual template header"):
                read_simple_manual_rows(path)

    def test_simple_xlsx_rows_can_be_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "simple.xlsx"
            workbook = Workbook()
            sheet = workbook.active
            sheet.append(SIMPLE_MANUAL_COLUMNS)
            sheet.append([
                "Synthetic Bank",
                "2025-01-01",
                "Synthetic receipt",
                "100",
                "",
                "Sales",
                "4000",
                "Sales Revenue",
                "Review",
                "Synthetic Customer",
                "CONFIRMED",
                "Synthetic note",
            ])
            workbook.save(path)
            rows = read_simple_manual_rows(path)
            self.assertEqual(rows[0]["Description"], "Synthetic receipt")

    def test_merge_confirmed_mappings_simple_template_works(self):
        with tempfile.TemporaryDirectory() as tmp:
            existing = Path(tmp) / "existing.csv"
            write_mappings(existing, [])
            args = build_arg_parser().parse_args([
                str(EXPERIENCE_DB / "simple_manual_classification_template.csv"),
                "--simple-template",
                "--existing",
                str(existing),
                "--output",
                str(Path(tmp) / "merged.csv"),
                "--conflicts",
                str(Path(tmp) / "conflicts.csv"),
                "--summary-json",
                str(Path(tmp) / "summary.json"),
            ])
            result = run(args)
            self.assertEqual(result["summary"]["new_mappings"], 2)
            self.assertTrue(result["output"].exists())


if __name__ == "__main__":
    unittest.main()
