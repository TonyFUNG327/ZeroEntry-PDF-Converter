from __future__ import annotations

import argparse
from pathlib import Path

from classifier.mappings import extract_confirmed_mappings, write_mappings
from classifier.review import apply_manual_review, read_review_rows


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Extract confirmed/corrected mapping candidates from reviewed transactions.")
    parser.add_argument("input", type=Path, help="A.2.1 reviewed workbook or CSV.")
    parser.add_argument("--output", type=Path, required=True, help="confirmed_mappings.csv output path.")
    return parser


def run(args: argparse.Namespace) -> dict[str, Path | int]:
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
