import argparse
import json
from pathlib import Path

from calibrate_ocr_output import build_boc_calibration_report


SUMMARY_FILENAME = "boc_ocr_fixture_calibration_summary.json"


def build_arg_parser():
    parser = argparse.ArgumentParser(description="Build aggregate OCR parser calibration metrics for redacted fixture text files.")
    parser.add_argument("fixture_dir", type=Path, help="Folder containing *_redacted.txt OCR fixtures")
    parser.add_argument("--parser", choices=["BOC"], required=True, help="Parser diagnostics to run for calibration.")
    parser.add_argument("--output-dir", type=Path, required=True, help="Folder for generated aggregate calibration report.")
    return parser


def collect_redacted_fixtures(fixture_dir):
    fixture_dir = Path(fixture_dir)
    return sorted(path for path in fixture_dir.glob("*_redacted.txt") if path.is_file())


def _line_merge_metric(report, key, default=0):
    return (report.get("line_merge_diagnostics") or {}).get(key, default)


def _sample_lines(report, key):
    return (report.get("line_merge_diagnostics") or {}).get(key, [])


def build_fixture_metric(fixture_path):
    report, summary = build_boc_calibration_report(fixture_path)
    return {
        "fixture_name": Path(fixture_path).name,
        "candidate_transaction_line_count": summary["candidate_transaction_line_count"],
        "parsed_transaction_row_count": summary["parsed_transaction_row_count"],
        "skipped_candidate_line_count": summary["skipped_candidate_line_count"],
        "parse_success_ratio": summary["parse_success_ratio"],
        "warning_count": summary["warning_count"],
        "skip_reason_counts": summary["skip_reason_counts"],
        "merged_line_count": _line_merge_metric(report, "merged_line_count"),
        "blocked_merge_count": _line_merge_metric(report, "blocked_merge_count"),
        "merged_line_samples": _sample_lines(report, "merged_lines")[:5],
        "blocked_merge_reasons": _blocked_merge_reason_counts(report),
    }


def _blocked_merge_reason_counts(report):
    counts = {}
    for item in _sample_lines(report, "blocked_merges"):
        reason = item.get("reason") or "Unknown"
        counts[reason] = counts.get(reason, 0) + 1
    return counts


def _add_counts(target, source):
    for key, value in (source or {}).items():
        target[key] = target.get(key, 0) + value


def _ratio(numerator, denominator):
    return round(numerator / denominator, 4) if denominator else 0


def build_aggregate_totals(fixture_metrics):
    total_candidates = sum(item["candidate_transaction_line_count"] for item in fixture_metrics)
    total_parsed = sum(item["parsed_transaction_row_count"] for item in fixture_metrics)
    total_skipped = sum(item["skipped_candidate_line_count"] for item in fixture_metrics)
    total_warnings = sum(item["warning_count"] for item in fixture_metrics)
    merged_total = sum(item["merged_line_count"] for item in fixture_metrics)
    blocked_total = sum(item["blocked_merge_count"] for item in fixture_metrics)
    skip_reason_totals = {}
    blocked_merge_reason_totals = {}

    for item in fixture_metrics:
        _add_counts(skip_reason_totals, item["skip_reason_counts"])
        _add_counts(blocked_merge_reason_totals, item["blocked_merge_reasons"])

    ratios = [item["parse_success_ratio"] for item in fixture_metrics]
    lowest_item = min(fixture_metrics, key=lambda item: item["parse_success_ratio"]) if fixture_metrics else None
    return {
        "total_candidate_transaction_line_count": total_candidates,
        "total_parsed_transaction_row_count": total_parsed,
        "total_skipped_candidate_line_count": total_skipped,
        "overall_parse_success_ratio": _ratio(total_parsed, total_candidates),
        "average_parse_success_ratio": round(sum(ratios) / len(ratios), 4) if ratios else 0,
        "lowest_parse_success_ratio": lowest_item["parse_success_ratio"] if lowest_item else 0,
        "lowest_parse_success_fixture": lowest_item["fixture_name"] if lowest_item else None,
        "total_warning_count": total_warnings,
        "skip_reason_totals": skip_reason_totals,
        "merged_line_total": merged_total,
        "blocked_merge_total": blocked_total,
        "blocked_merge_reason_totals": blocked_merge_reason_totals,
    }


def build_aggregate_summary(fixture_dir):
    fixtures = collect_redacted_fixtures(fixture_dir)
    fixture_metrics = [build_fixture_metric(path) for path in fixtures]
    return {
        "fixture_dir": str(Path(fixture_dir)),
        "fixture_count": len(fixtures),
        **build_aggregate_totals(fixture_metrics),
        "fixtures": fixture_metrics,
    }


def write_aggregate_summary(summary, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / SUMMARY_FILENAME
    output_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    return output_path


def main(argv=None):
    args = build_arg_parser().parse_args(argv)
    summary = build_aggregate_summary(args.fixture_dir)
    output_path = write_aggregate_summary(summary, args.output_dir)
    print(f"Fixture count: {summary['fixture_count']}")
    print(f"Overall parse success ratio: {summary['overall_parse_success_ratio']}")
    print(f"Merged line total: {summary['merged_line_total']}")
    print(f"Blocked merge total: {summary['blocked_merge_total']}")
    print(f"Aggregate calibration summary saved: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
