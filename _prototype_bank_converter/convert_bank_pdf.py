import argparse
from pathlib import Path

from core.bank_registry import (
    ParserExecutionError,
    ScannedPdfError,
    UnsupportedBankError,
    convert_with_adapter,
)
from core.paths import BB2_DIR, BB_DIR, collect_pdf_paths, ensure_output_dir
from core.validation import format_report_item


DEFAULT_INPUT_PATH = BB_DIR
DEFAULT_OUTPUT_DIR = BB2_DIR


def convert_one(pdf_path, output_dir):
    return convert_with_adapter(Path(pdf_path), Path(output_dir))


def build_arg_parser():
    parser = argparse.ArgumentParser(description="Convert supported Hong Kong bank statement PDFs to Excel.")
    parser.add_argument(
        "input",
        type=Path,
        nargs="?",
        default=DEFAULT_INPUT_PATH,
        help=f"PDF file or folder of PDFs. Default: {DEFAULT_INPUT_PATH}",
    )
    parser.add_argument("-o", "--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help=f"Output directory. Default: {DEFAULT_OUTPUT_DIR}")
    return parser


def print_failure(pdf_path, exc):
    if isinstance(exc, ScannedPdfError):
        print(f"Failed [SCANNED_IMAGE_ONLY]: {pdf_path}")
        print(f"  {exc}")
    elif isinstance(exc, UnsupportedBankError):
        print(f"Failed [UNRECOGNIZED]: {pdf_path}")
        print(f"  {exc}")
    elif isinstance(exc, ParserExecutionError):
        print(f"Failed [PARSER_FAILED]: {pdf_path}")
        print(f"  {exc}")
    else:
        print(f"Failed [ERROR]: {pdf_path}")
        print(f"  {exc}")


def main(argv=None):
    args = build_arg_parser().parse_args(argv)
    output_dir = ensure_output_dir(args.output_dir)

    pdf_paths = collect_pdf_paths(args.input)
    if not pdf_paths:
        print(f"No PDF files found in: {args.input}")
        return 1

    exit_code = 0
    for pdf_path in pdf_paths:
        try:
            bank, output_path, report = convert_one(pdf_path, output_dir)
        except Exception as exc:
            exit_code = 1
            print_failure(pdf_path, exc)
            continue

        print(f"Saved [{bank}]: {output_path}")
        for item in report:
            print(format_report_item(item))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
