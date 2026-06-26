import argparse
from pathlib import Path

from ocr.ocr_diagnostics import analyze_ocr_file_for_diagnostics, format_diagnostic_report, write_diagnostic_report


def build_arg_parser():
    parser = argparse.ArgumentParser(description="Inspect OCR text/searchable PDF output for parser calibration.")
    parser.add_argument("input", type=Path, help="OCR .txt or searchable .pdf file")
    return parser


def main(argv=None):
    args = build_arg_parser().parse_args(argv)
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

