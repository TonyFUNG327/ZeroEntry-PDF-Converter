import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from classifier.engine import OUTPUT_COLUMNS, classify_transactions, summarize_classification
from classifier.mappings import (
    CONFLICT_FIELDS,
    MAPPING_FIELDS,
    extract_confirmed_mappings,
    load_mappings,
    merge_confirmed_mappings,
    write_mappings,
)
from classifier.review import MANUAL_REVIEW_COLUMNS, apply_manual_review, read_review_rows
from classifier.rules import load_rules
from merge_confirmed_mappings import build_arg_parser, run


FIXTURES = APP_ROOT / "tests" / "fixtures"
EXPERIENCE_DB = APP_ROOT / "experience_db"
DEFAULT_RULES = APP_ROOT / "rules" / "classification_rules.csv"


def read_header(path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return next(csv.reader(handle))


def write_csv(path, fields, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def mapping_row(mapping_id="MAP_0001", **overrides):
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
        "notes": "Existing synthetic mapping",
    }
    row.update(overrides)
    return row


def candidates():
    rows = apply_manual_review(read_review_rows(FIXTURES / "mapping_reviewed_input.csv"))
    return extract_confirmed_mappings(rows)


class TestMappingMergeA31(unittest.TestCase):
    def test_experience_db_template_files_exist(self):
        for name in [
            "README.md",
            "manual_classification_template.csv",
            "reviewed_transactions.csv",
            "mapping_conflicts.csv",
            "mapping_merge_summary.json",
        ]:
            self.assertTrue((EXPERIENCE_DB / name).exists())

    def test_manual_classification_template_headers_correct(self):
        self.assertEqual(read_header(EXPERIENCE_DB / "manual_classification_template.csv"), OUTPUT_COLUMNS + MANUAL_REVIEW_COLUMNS)

    def test_reviewed_transactions_headers_correct(self):
        self.assertEqual(read_header(EXPERIENCE_DB / "reviewed_transactions.csv"), OUTPUT_COLUMNS + MANUAL_REVIEW_COLUMNS)

    def test_mapping_conflicts_headers_correct(self):
        self.assertEqual(read_header(EXPERIENCE_DB / "mapping_conflicts.csv"), CONFLICT_FIELDS)

    def test_mapping_merge_summary_template_valid_json(self):
        payload = json.loads((EXPERIENCE_DB / "mapping_merge_summary.json").read_text(encoding="utf-8"))
        self.assertEqual(payload["input_reviewed_rows"], 0)
        self.assertEqual(payload["source_status_counts"], {})

    def test_merge_new_mapping_into_empty_existing_mappings(self):
        merged, conflicts, summary = merge_confirmed_mappings([], candidates(), input_reviewed_rows=7)
        self.assertEqual(len(merged), 2)
        self.assertEqual(conflicts, [])
        self.assertEqual(summary["new_mappings"], 2)
        self.assertEqual(merged[0]["mapping_id"], "MAP_0001")

    def test_preserve_existing_mapping_id_on_same_description_direction_category(self):
        merged, conflicts, summary = merge_confirmed_mappings([mapping_row("MAP_0099")], candidates())
        existing = [row for row in merged if row["description_pattern"] == "Synthetic mapping charge"][0]
        self.assertEqual(existing["mapping_id"], "MAP_0099")
        self.assertEqual(conflicts, [])
        self.assertEqual(summary["updated_mappings"], 1)

    def test_update_use_count_on_duplicate_mapping(self):
        merged, _, _ = merge_confirmed_mappings([mapping_row(use_count="3")], candidates())
        existing = [row for row in merged if row["description_pattern"] == "Synthetic mapping charge"][0]
        self.assertEqual(existing["use_count"], "5")

    def test_update_last_used_date_to_newer_date(self):
        merged, _, _ = merge_confirmed_mappings([mapping_row(last_used_date="2025-01-01")], candidates())
        existing = [row for row in merged if row["description_pattern"] == "Synthetic mapping charge"][0]
        self.assertEqual(existing["last_used_date"], "2025-03-01")

    def test_conflict_when_same_description_direction_but_different_category(self):
        existing = mapping_row(category="Different Category")
        merged, conflicts, summary = merge_confirmed_mappings([existing], candidates())
        self.assertEqual(len(conflicts), 1)
        self.assertEqual(conflicts[0]["existing_category"], "Different Category")
        self.assertEqual(summary["conflicts"], 1)
        self.assertEqual(len(merged), 2)

    def test_conflict_when_same_description_direction_but_different_account_code(self):
        existing = mapping_row(account_code="9999")
        merged, conflicts, _ = merge_confirmed_mappings([existing], candidates())
        self.assertEqual(len(conflicts), 1)
        self.assertEqual(conflicts[0]["existing_account_code"], "9999")
        self.assertEqual(len(merged), 2)

    def test_disabled_existing_mapping_is_not_overwritten(self):
        existing = mapping_row(enabled="No")
        merged, conflicts, summary = merge_confirmed_mappings([existing], candidates())
        same = [row for row in merged if row["description_pattern"] == "Synthetic mapping charge"]
        self.assertEqual(len(same), 1)
        self.assertEqual(same[0]["enabled"], "No")
        self.assertEqual(summary["disabled_conflicts"], 1)
        self.assertEqual(len(conflicts), 1)

    def test_new_mapping_id_starts_after_existing_max_map_number(self):
        merged, _, _ = merge_confirmed_mappings([mapping_row("MAP_0042", description_pattern="Other synthetic")], candidates())
        ids = {row["mapping_id"] for row in merged}
        self.assertIn("MAP_0043", ids)

    def test_pending_ignore_need_advice_blank_not_merged(self):
        descriptions = {row["description_pattern"] for row in candidates()}
        self.assertNotIn("Pending synthetic", descriptions)
        self.assertNotIn("Ignored synthetic", descriptions)
        self.assertNotIn("Needs advice synthetic", descriptions)
        self.assertNotIn("Blank synthetic", descriptions)

    def test_mapping_conflicts_csv_output_contains_expected_conflict_row(self):
        with tempfile.TemporaryDirectory() as tmp:
            _, conflicts, _ = merge_confirmed_mappings([mapping_row(category="Different Category")], candidates())
            path = Path(tmp) / "conflicts.csv"
            write_csv(path, CONFLICT_FIELDS, conflicts)
            with path.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(rows[0]["description_pattern"], "Synthetic mapping charge")
            self.assertEqual(rows[0]["resolution_status"], "Pending")

    def test_mapping_merge_summary_counts_correct(self):
        merged, conflicts, summary = merge_confirmed_mappings([mapping_row()], candidates(), input_reviewed_rows=7, source_status_counts={"Corrected": 2})
        self.assertEqual(summary["input_reviewed_rows"], 7)
        self.assertEqual(summary["candidate_mappings"], 2)
        self.assertEqual(summary["existing_mappings"], 1)
        self.assertEqual(summary["new_mappings"], 1)
        self.assertEqual(summary["updated_mappings"], 1)
        self.assertEqual(summary["conflicts"], 0)
        self.assertEqual(summary["output_mappings"], 2)
        self.assertEqual(summary["source_status_counts"], {"Corrected": 2})
        self.assertEqual(conflicts, [])
        self.assertEqual(len(merged), 2)

    def test_cli_merge_confirmed_mappings_works(self):
        with tempfile.TemporaryDirectory() as tmp:
            existing = Path(tmp) / "existing.csv"
            write_mappings(existing, [mapping_row()])
            args = build_arg_parser().parse_args([
                str(FIXTURES / "mapping_reviewed_input.csv"),
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
            self.assertTrue(result["output"].exists())
            self.assertTrue(result["conflicts"].exists())
            self.assertTrue(result["summary_json"].exists())
            self.assertEqual(result["summary"]["updated_mappings"], 1)

    def test_classification_summary_includes_rule_mapping_total_counts(self):
        mappings = load_mappings(FIXTURES / "confirmed_mappings_sample.csv")
        rules = load_rules(DEFAULT_RULES)
        rows = [
            {"Description": "Synthetic mapping charge", "Deposit": "", "Withdrawal": 25},
            {"Description": "Bank charge", "Deposit": "", "Withdrawal": 25},
            {"Description": "Mystery", "Deposit": "", "Withdrawal": 25},
        ]
        summary = summarize_classification(classify_transactions(rows, rules, mappings))
        self.assertEqual(summary["rule_classified_count"], 1)
        self.assertEqual(summary["mapping_classified_count"], 1)
        self.assertEqual(summary["total_classified_count"], 2)


if __name__ == "__main__":
    unittest.main()
