from __future__ import annotations

import argparse
from pathlib import Path

from classifier.review import (
    REVIEW_COLUMNS,
    add_manual_review_columns,
    apply_manual_review,
    read_review_rows,
    write_review_outputs,
)


def default_summary_json(output_path: Path) -> Path:
    return output_path.with_suffix(".summary.json")


def default_summary_text(output_path: Path) -> Path:
    return output_path.with_suffix(".summary.txt")


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Apply manual review decisions to classified bank transactions.")
    parser.add_argument("input", type=Path, help="Classified or manually reviewed workbook/CSV.")
    parser.add_argument("--output", type=Path, required=True, help="Reviewed workbook output path.")
    parser.add_argument("--summary-json", type=Path, default=None, help="Optional review summary JSON path.")
    parser.add_argument("--summary-txt", type=Path, default=None, help="Optional review summary text path.")
    parser.add_argument(
        "--add-template-columns",
        action="store_true",
        help="Append blank Manual_* columns for reviewer input without applying review.",
    )
    return parser


def run(args: argparse.Namespace) -> dict[str, Path | dict]:
    rows = read_review_rows(args.input)
    if args.add_template_columns:
        template_rows = add_manual_review_columns(rows)
        from classifier.io import write_workbook

        output = write_workbook(args.output, template_rows, REVIEW_COLUMNS)
        return {"output": output, "summary": {"transaction_count": len(template_rows)}}

    reviewed = apply_manual_review(rows)
    return write_review_outputs(
        args.output,
        reviewed,
        args.summary_json or default_summary_json(args.output),
        args.summary_txt or default_summary_text(args.output),
    )


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    result = run(args)
    print(f"Saved reviewed workbook: {result['output']}")
    if "summary_json" in result:
        print(f"Saved review summary JSON: {result['summary_json']}")
        print(f"Saved review summary text: {result['summary_txt']}")
    print(result["summary"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
