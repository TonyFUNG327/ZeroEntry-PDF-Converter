from __future__ import annotations

import argparse
from pathlib import Path

from classifier.engine import classify_transactions, summarize_classification, unclassified_rows
from classifier.io import read_transactions, write_json, write_summary_text, write_workbook
from classifier.mappings import load_mappings
from classifier.rules import load_rules


DEFAULT_RULES = Path(__file__).resolve().parent / "rules" / "classification_rules.csv"


def default_summary_json(output_path: Path) -> Path:
    return output_path.with_suffix(".summary.json")


def default_summary_text(output_path: Path) -> Path:
    return output_path.with_suffix(".summary.txt")


def default_review_output(output_path: Path) -> Path:
    return output_path.with_name(output_path.stem + "_unclassified.xlsx")


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Classify merged bank transactions using CSV rules.")
    parser.add_argument("input", type=Path, help="Merged bank .xlsx or .csv with ZeroEntry bank columns.")
    parser.add_argument("--rules", type=Path, default=DEFAULT_RULES, help="Rules CSV path.")
    parser.add_argument("--output", type=Path, required=True, help="Classified Excel output path.")
    parser.add_argument("--summary-json", type=Path, default=None, help="Optional summary JSON path.")
    parser.add_argument("--summary-txt", type=Path, default=None, help="Optional summary text path.")
    parser.add_argument("--review-output", type=Path, default=None, help="Optional unclassified review workbook path.")
    parser.add_argument("--mappings", type=Path, default=None, help="Optional confirmed mappings CSV path.")
    return parser


def run(args: argparse.Namespace) -> dict[str, Path | dict]:
    rules = load_rules(args.rules)
    mappings = load_mappings(args.mappings) if args.mappings else None
    rows = read_transactions(args.input)
    classified = classify_transactions(rows, rules, mappings)
    summary = summarize_classification(classified)

    output_path = write_workbook(args.output, classified)
    summary_json = write_json(args.summary_json or default_summary_json(output_path), summary)
    summary_txt = write_summary_text(args.summary_txt or default_summary_text(output_path), summary)
    review_path = write_workbook(args.review_output or default_review_output(output_path), unclassified_rows(classified))

    return {
        "output": output_path,
        "summary_json": summary_json,
        "summary_txt": summary_txt,
        "review_output": review_path,
        "summary": summary,
    }


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    result = run(args)
    print(f"Saved classified workbook: {result['output']}")
    print(f"Saved unclassified review workbook: {result['review_output']}")
    print(f"Saved summary JSON: {result['summary_json']}")
    print(f"Saved summary text: {result['summary_txt']}")
    print(result["summary"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
