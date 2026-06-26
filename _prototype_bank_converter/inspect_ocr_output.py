import argparse
from pathlib import Path

from ocr.ocr_diagnostics import (
    analyze_ocr_file_for_diagnostics,
    analyze_ocr_text_for_diagnostics,
    attach_parser_diagnostics,
    extract_text_from_pdf,
    format_diagnostic_report,
    write_diagnostic_report,
)
from ocr_parsers import boc_ocr_pdf_converter


def build_arg_parser():
    parser = argparse.ArgumentParser(description="Inspect OCR text/searchable PDF output for parser calibration.")
    parser.add_argument("input", type=Path, help="OCR .txt or searchable .pdf file")
    parser.add_argument("--parser", choices=["BOC"], help="Optional parser-level diagnostics to run against OCR output.")
    return parser


def read_ocr_text(input_path):
    input_path = Path(input_path)
    if input_path.suffix.lower() == ".pdf":
        text, page_count = extract_text_from_pdf(input_path)
        return text, page_count
    return input_path.read_text(encoding="utf-8", errors="replace"), None


def main(argv=None):
    args = build_arg_parser().parse_args(argv)
    if args.parser == "BOC":
        ocr_text, page_count = read_ocr_text(args.input)
        report = analyze_ocr_text_for_diagnostics(ocr_text)
        report["source_file"] = str(args.input)
        report["page_count"] = page_count
        parser_result = boc_ocr_pdf_converter.extract_accounts_from_text_with_diagnostics(ocr_text)
        attach_parser_diagnostics(report, parser_result)
    else:
        report = analyze_ocr_file_for_diagnostics(args.input)
    txt_path = args.input.with_suffix(args.input.suffix + ".diagnostic.txt")
    json_path = args.input.with_suffix(args.input.suffix + ".diagnostic.json")
    write_diagnostic_report(report, txt_path)
    write_diagnostic_report(report, json_path)
    print(format_diagnostic_report(report))
    print(f"Diagnostic report saved: {txt_path}")
    print(f"Diagnostic JSON saved: {json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
