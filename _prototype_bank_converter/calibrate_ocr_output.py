import argparse
import json
from pathlib import Path

from inspect_ocr_output import read_ocr_text
from ocr.ocr_diagnostics import (
    analyze_ocr_text_for_diagnostics,
    attach_parser_diagnostics,
    build_calibration_summary,
    format_diagnostic_report,
    write_diagnostic_report,
)
from ocr_parsers import boc_ocr_pdf_converter


def build_arg_parser():
    parser = argparse.ArgumentParser(description="Build an OCR parser calibration report from redacted OCR text or searchable PDF.")
    parser.add_argument("input", type=Path, help="Redacted OCR .txt or searchable .pdf file")
    parser.add_argument("--parser", choices=["BOC"], required=True, help="Parser diagnostics to run for calibration.")
    return parser


def build_boc_calibration_report(input_path):
    ocr_text, page_count = read_ocr_text(input_path)
    report = analyze_ocr_text_for_diagnostics(ocr_text)
    report["source_file"] = str(input_path)
    report["page_count"] = page_count
    parser_result = boc_ocr_pdf_converter.extract_accounts_from_text_with_diagnostics(ocr_text)
    attach_parser_diagnostics(report, parser_result)
    summary = build_calibration_summary(report)
    return report, summary


def write_calibration_outputs(input_path, report, summary):
    input_path = Path(input_path)
    txt_path = input_path.with_suffix(input_path.suffix + ".diagnostic.txt")
    json_path = input_path.with_suffix(input_path.suffix + ".diagnostic.json")
    summary_path = input_path.with_suffix(input_path.suffix + ".calibration_summary.json")
    write_diagnostic_report(report, txt_path)
    write_diagnostic_report(report, json_path)
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    return txt_path, json_path, summary_path


def main(argv=None):
    args = build_arg_parser().parse_args(argv)
    report, summary = build_boc_calibration_report(args.input)
    txt_path, json_path, summary_path = write_calibration_outputs(args.input, report, summary)

    print(format_diagnostic_report(report))
    print("Calibration summary:")
    for key, value in summary.items():
        print(f"  {key}: {value}")
    print(f"Diagnostic report saved: {txt_path}")
    print(f"Diagnostic JSON saved: {json_path}")
    print(f"Calibration summary JSON saved: {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
