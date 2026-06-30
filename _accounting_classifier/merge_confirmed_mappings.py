from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from classifier.mappings import (
    extract_confirmed_mappings,
    load_mappings,
    mapping_to_row,
    merge_confirmed_mappings,
    write_conflicts,
    write_mappings,
)
from classifier.review import apply_manual_review, read_review_rows
from classifier.rules import text
from classifier.simple_manual import read_simple_manual_rows, simple_manual_rows_to_reviewed_rows


def default_summary_txt(path: Path) -> Path:
    return path.with_suffix(".txt")


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Merge reviewed confirmed/corrected rows into confirmed mappings.")
    parser.add_argument("input", type=Path, help="A.2.1 reviewed workbook or CSV.")
    parser.add_argument("--existing", type=Path, required=True, help="Existing confirmed_mappings.csv.")
    parser.add_argument("--output", type=Path, required=True, help="Merged confirmed_mappings.csv output.")
    parser.add_argument("--conflicts", type=Path, required=True, help="Mapping conflicts CSV output.")
    parser.add_argument("--summary-json", type=Path, required=True, help="Mapping merge summary JSON output.")
    parser.add_argument("--summary-txt", type=Path, default=None, help="Optional mapping merge summary text output.")
    parser.add_argument("--simple-template", action="store_true", help="Read the simplified manual classification template.")
    return parser


def write_summary_json(path: Path, summary: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def write_summary_text(path: Path, summary: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"input_reviewed_rows: {summary['input_reviewed_rows']}",
        f"candidate_mappings: {summary['candidate_mappings']}",
        f"existing_mappings: {summary['existing_mappings']}",
        f"new_mappings: {summary['new_mappings']}",
        f"updated_mappings: {summary['updated_mappings']}",
        f"conflicts: {summary['conflicts']}",
        f"skipped: {summary['skipped']}",
        f"disabled_conflicts: {summary['disabled_conflicts']}",
        f"output_mappings: {summary['output_mappings']}",
        "",
        "source_status_counts:",
    ]
    lines.extend(f"- {key}: {value}" for key, value in sorted(summary["source_status_counts"].items()))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def run(args: argparse.Namespace) -> dict[str, Path | dict]:
    if args.simple_template:
        reviewed_rows = simple_manual_rows_to_reviewed_rows(read_simple_manual_rows(args.input))
    else:
        reviewed_rows = apply_manual_review(read_review_rows(args.input))
    status_counts = Counter(text(row.get("Manual_Review_Status")) for row in reviewed_rows)
    candidates = extract_confirmed_mappings(reviewed_rows)
    existing = [mapping_to_row(mapping) for mapping in load_mappings(args.existing)]
    merged, conflicts, summary = merge_confirmed_mappings(
        existing,
        candidates,
        input_reviewed_rows=len(reviewed_rows),
        source_status_counts=dict(sorted(status_counts.items())),
    )
    output = write_mappings(args.output, merged)
    conflicts_path = write_conflicts(args.conflicts, conflicts)
    summary_json = write_summary_json(args.summary_json, summary)
    summary_txt = write_summary_text(args.summary_txt or default_summary_txt(args.summary_json), summary)
    return {
        "output": output,
        "conflicts": conflicts_path,
        "summary_json": summary_json,
        "summary_txt": summary_txt,
        "summary": summary,
    }


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    result = run(args)
    print(f"Saved merged mappings: {result['output']}")
    print(f"Saved mapping conflicts: {result['conflicts']}")
    print(f"Saved merge summary JSON: {result['summary_json']}")
    print(f"Saved merge summary text: {result['summary_txt']}")
    print(result["summary"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
