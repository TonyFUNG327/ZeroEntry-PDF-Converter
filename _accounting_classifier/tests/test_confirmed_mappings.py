import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from classifier.engine import classify_transactions, summarize_classification
from classifier.io import read_transactions
from classifier.mappings import (
    MAPPING_FIELDS,
    extract_confirmed_mappings,
    load_mappings,
    write_mappings,
)
from classifier.review import apply_manual_review, read_review_rows
from classifier.rules import load_rules
from classify_bank_transactions import build_arg_parser as build_classify_arg_parser
from classify_bank_transactions import run as run_classify
from extract_confirmed_mappings import build_arg_parser as build_extract_arg_parser
from extract_confirmed_mappings import run as run_extract


FIXTURES = APP_ROOT / "tests" / "fixtures"
DEFAULT_RULES = APP_ROOT / "rules" / "classification_rules.csv"


def write_mapping_csv(path, rows, fieldnames=None):
    with path.open("w", newline="", encoding="utf-8") as handle:
        fields = fieldnames or MAPPING_FIELDS
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def mapping_row(mapping_id="MAP_TEST", **overrides):
    row = {
        "mapping_id": mapping_id,
        "enabled": "Yes",
        "priority": "10",
        "match_type": "exact_description",
        "description_pattern": "Synthetic mapping charge",
        "direction": "Withdrawal",
        "amount_min": "",
        "amount_max": "",
        "category": "Mapped Charges",
        "account_code": "7300",
        "account_name": "Mapped Charges",
        "tax_type": "Review",
        "counterparty": "Synthetic Vendor",
        "confidence": "1.0",
        "source_review_status": "Corrected",
        "source_rule_id": "",
        "source_classification_source": "manual_corrected",
        "use_count": "1",
        "last_used_date": "2025-03-01",
        "notes": "Synthetic mapping note",
    }
    row.update(overrides)
    return row


def read_csv_rows(path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


class TestConfirmedMappingsA30(unittest.TestCase):
    def test_load_confirmed_mappings_csv(self):
        mappings = load_mappings(FIXTURES / "confirmed_mappings_sample.csv")
        self.assertEqual(len(mappings), 3)
        self.assertEqual(mappings[0].mapping_id, "MAP_0003")

    def test_missing_mapping_columns_raises_value_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.csv"
            fields = [field for field in MAPPING_FIELDS if field != "notes"]
            write_mapping_csv(path, [mapping_row()], fields)
            with self.assertRaisesRegex(ValueError, "notes"):
                load_mappings(path)

    def test_duplicate_mapping_id_raises_value_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.csv"
            write_mapping_csv(path, [mapping_row("MAP_DUP"), mapping_row("MAP_DUP")])
            with self.assertRaisesRegex(ValueError, "Duplicate mapping_id"):
                load_mappings(path)

    def test_invalid_match_type_raises_value_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.csv"
            write_mapping_csv(path, [mapping_row(match_type="fuzzy")])
            with self.assertRaisesRegex(ValueError, "invalid match_type"):
                load_mappings(path)

    def test_invalid_direction_raises_value_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.csv"
            write_mapping_csv(path, [mapping_row(direction="Unknown")])
            with self.assertRaisesRegex(ValueError, "invalid direction"):
                load_mappings(path)

    def test_exact_description_matching(self):
        mapping = load_mappings(FIXTURES / "confirmed_mappings_sample.csv")[1]
        self.assertTrue(mapping.matches("Synthetic mapping charge", "Withdrawal", 25))
        self.assertFalse(mapping.matches("Synthetic mapping charge extra", "Withdrawal", 25))

    def test_contains_matching(self):
        mapping = load_mappings(FIXTURES / "confirmed_mappings_sample.csv")[2]
        self.assertTrue(mapping.matches("Monthly subscription service", "Withdrawal", 50))

    def test_enabled_no_does_not_match(self):
        mapping = load_mappings(FIXTURES / "confirmed_mappings_sample.csv")[0]
        self.assertFalse(mapping.matches("disabled mapping", "Withdrawal", 1))

    def test_priority_lower_number_wins(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "mappings.csv"
            write_mapping_csv(
                path,
                [
                    mapping_row("MAP_LOW", priority="50", category="Low"),
                    mapping_row("MAP_HIGH", priority="1", category="High"),
                ],
            )
            classified = classify_transactions(
                [{"Description": "Synthetic mapping charge", "Deposit": "", "Withdrawal": 25}],
                load_rules(DEFAULT_RULES),
                load_mappings(path),
            )
            self.assertEqual(classified[0]["Category"], "High")

    def test_amount_min_and_max_filtering(self):
        mappings = load_mappings(FIXTURES / "confirmed_mappings_sample.csv")
        rules = load_rules(DEFAULT_RULES)
        classified = classify_transactions(
            [
                {"Description": "Monthly subscription service", "Deposit": "", "Withdrawal": 50},
                {"Description": "Monthly subscription service", "Deposit": "", "Withdrawal": 250},
            ],
            rules,
            mappings,
        )
        self.assertEqual(classified[0]["Classification_Source"], "confirmed_mapping")
        self.assertEqual(classified[1]["Classification_Source"], "unclassified")

    def test_unknown_direction_does_not_match_mapping(self):
        classified = classify_transactions(
            [{"Description": "Synthetic mapping charge", "Deposit": "", "Withdrawal": ""}],
            load_rules(DEFAULT_RULES),
            load_mappings(FIXTURES / "confirmed_mappings_sample.csv"),
        )
        self.assertEqual(classified[0]["Classification_Source"], "unclassified")

    def test_mapping_matches_before_rule(self):
        classified = classify_transactions(
            [{"Description": "Synthetic mapping charge", "Deposit": "", "Withdrawal": 25}],
            load_rules(DEFAULT_RULES),
            load_mappings(FIXTURES / "confirmed_mappings_sample.csv"),
        )
        self.assertEqual(classified[0]["Classification_Source"], "confirmed_mapping")
        self.assertEqual(classified[0]["Category"], "Mapped Charges")

    def test_mapping_miss_falls_back_to_rule(self):
        classified = classify_transactions(
            [{"Description": "Bank charge", "Deposit": "", "Withdrawal": 25}],
            load_rules(DEFAULT_RULES),
            load_mappings(FIXTURES / "confirmed_mappings_sample.csv"),
        )
        self.assertEqual(classified[0]["Classification_Source"], "rule")
        self.assertEqual(classified[0]["Rule_ID"], "BANK_CHARGE")

    def test_mapping_miss_and_rule_miss_becomes_unclassified(self):
        classified = classify_transactions(
            [{"Description": "Mystery item", "Deposit": "", "Withdrawal": 25}],
            load_rules(DEFAULT_RULES),
            load_mappings(FIXTURES / "confirmed_mappings_sample.csv"),
        )
        self.assertEqual(classified[0]["Classification_Source"], "unclassified")

    def test_classification_source_and_notes_for_mapping(self):
        classified = classify_transactions(
            [{"Description": "Synthetic mapping charge", "Deposit": "", "Withdrawal": 25}],
            load_rules(DEFAULT_RULES),
            load_mappings(FIXTURES / "confirmed_mappings_sample.csv"),
        )
        self.assertEqual(classified[0]["Classification_Source"], "confirmed_mapping")
        self.assertIn("MAP_0001", classified[0]["Notes"])

    def test_summary_mapping_fields(self):
        classified = classify_transactions(
            [{"Description": "Synthetic mapping charge", "Deposit": "", "Withdrawal": 25}],
            load_rules(DEFAULT_RULES),
            load_mappings(FIXTURES / "confirmed_mappings_sample.csv"),
        )
        summary = summarize_classification(classified)
        self.assertEqual(summary["mapping_classified_count"], 1)
        self.assertEqual(summary["mapping_hit_counts"], {"MAP_0001": 1})

    def test_extract_mappings_from_confirmed_and_corrected_rows(self):
        rows = apply_manual_review(read_review_rows(FIXTURES / "mapping_reviewed_input.csv"))
        mappings = extract_confirmed_mappings(rows)
        expected = read_csv_rows(FIXTURES / "expected_confirmed_mappings.csv")
        actual = [
            {
                "mapping_id": row["mapping_id"],
                "description_pattern": row["description_pattern"],
                "direction": row["direction"],
                "category": row["category"],
                "account_code": row["account_code"],
                "account_name": row["account_name"],
                "tax_type": row["tax_type"],
                "counterparty": row["counterparty"],
                "source_review_status": row["source_review_status"],
                "source_rule_id": row["source_rule_id"],
                "source_classification_source": row["source_classification_source"],
                "use_count": row["use_count"],
            }
            for row in mappings
        ]
        self.assertEqual(actual, expected)

    def test_do_not_extract_other_statuses(self):
        rows = apply_manual_review(read_review_rows(FIXTURES / "mapping_reviewed_input.csv"))
        mappings = extract_confirmed_mappings(rows)
        descriptions = {row["description_pattern"] for row in mappings}
        self.assertNotIn("Pending synthetic", descriptions)
        self.assertNotIn("Ignored synthetic", descriptions)
        self.assertNotIn("Needs advice synthetic", descriptions)
        self.assertNotIn("Blank synthetic", descriptions)

    def test_duplicate_reviewed_rows_merge_with_use_count(self):
        rows = apply_manual_review(read_review_rows(FIXTURES / "mapping_reviewed_input.csv"))
        mappings = extract_confirmed_mappings(rows)
        duplicate = [row for row in mappings if row["description_pattern"] == "Synthetic mapping charge"][0]
        self.assertEqual(duplicate["use_count"], "2")

    def test_cli_extract_confirmed_mappings(self):
        with tempfile.TemporaryDirectory() as tmp:
            args = build_extract_arg_parser().parse_args([
                str(FIXTURES / "mapping_reviewed_input.csv"),
                "--output",
                str(Path(tmp) / "confirmed_mappings.csv"),
            ])
            result = run_extract(args)
            self.assertTrue(result["output"].exists())
            self.assertEqual(result["mapping_count"], 2)

    def test_cli_classify_with_mappings(self):
        with tempfile.TemporaryDirectory() as tmp:
            input_path = Path(tmp) / "input.csv"
            input_path.write_text(
                "Bank_Account,Date,Description,Deposit,Withdrawal,Balance,Control\n"
                "Synthetic Bank,2025-03-01,Synthetic mapping charge,,25,975,975\n",
                encoding="utf-8",
            )
            args = build_classify_arg_parser().parse_args([
                str(input_path),
                "--output",
                str(Path(tmp) / "classified.xlsx"),
                "--mappings",
                str(FIXTURES / "confirmed_mappings_sample.csv"),
            ])
            result = run_classify(args)
            self.assertEqual(result["summary"]["mapping_classified_count"], 1)
            self.assertEqual(result["summary"]["mapping_hit_counts"], {"MAP_0001": 1})


if __name__ == "__main__":
    unittest.main()
