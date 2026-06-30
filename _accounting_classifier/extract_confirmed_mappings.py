from __future__ import annotations

import argparse
from pathlib import Path

from classifier.mappings import extract_confirmed_mappings, write_mappings
from classifier.review import apply_manual_review, read_review_rows
from classifier.simple_manual import read_simple_manual_rows, simple_manual_rows_to_reviewed_rows


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Extract confirmed/corrected mapping candidates from reviewed transactions.")
    parser.add_argument("input", type=Path, help="A.2.1 reviewed workbook or CSV.")
    parser.add_argument("--output", type=Path, required=True, help="confirmed_mappings.csv output path.")
    parser.add_argument("--simple-template", action="store_true", help="Read the simplified manual classification template.")
    return parser


def run(args: argparse.Namespace) -> dict[str, Path | int]:
    if args.simple_template:
        rows = simple_manual_rows_to_reviewed_rows(read_simple_manual_rows(args.input))
    else:
        rows = apply_manual_review(read_review_rows(args.input))
    mapping_rows = extract_confirmed_mappings(rows)
    output = write_mappings(args.output, mapping_rows)
    return {"output": output, "mapping_count": len(mapping_rows)}


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    result = run(args)
    print(f"Saved confirmed mappings: {result['output']}")
    print(f"Mapping count: {result['mapping_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
