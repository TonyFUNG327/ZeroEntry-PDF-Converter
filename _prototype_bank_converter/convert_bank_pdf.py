import argparse
from pathlib import Path

from core.bank_registry import (
    ParserExecutionError,
    SCANNED_IMAGE_ONLY,
    ScannedPdfError,
    UnsupportedBankError,
    convert_with_adapter,
    detect_bank,
)
from core.paths import BB2_DIR, BB_DIR, collect_pdf_paths, ensure_output_dir
from core.validation import format_report_item
from ocr.ocr_errors import OcrDependencyError, OcrExecutionError, OcrQualityError
from ocr.ocr_preprocessor import preprocess_pdf_for_ocr
from ocr.ocr_quality import validate_ocr_quality


DEFAULT_INPUT_PATH = BB_DIR
DEFAULT_OUTPUT_DIR = BB2_DIR


def convert_one(pdf_path, output_dir, ocr_enabled=False):
    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir)
    if not ocr_enabled:
        return convert_with_adapter(pdf_path, output_dir)

    bank_code = detect_bank(pdf_path)
    if bank_code != SCANNED_IMAGE_ONLY:
        return convert_with_adapter(pdf_path, output_dir, bank_code=bank_code)

    ocr_result = preprocess_pdf_for_ocr(pdf_path)
    quality_report = validate_ocr_quality(ocr_result.text)
    return convert_with_adapter(
        ocr_result.searchable_pdf,
        output_dir,
        bank_code=quality_report.bank_code,
        output_stem=pdf_path.stem,
    )


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
    parser.add_argument("--ocr", action="store_true", help="Experimental: run OCR on image-only scanned PDFs before conversion.")
    return parser


def print_failure(pdf_path, exc):
    if isinstance(exc, ScannedPdfError):
        print(f"Failed [SCANNED_IMAGE_ONLY]: {pdf_path}")
        print(f"  {exc}")
    elif isinstance(exc, OcrDependencyError):
        print(f"Failed [OCR_DEPENDENCY]: {pdf_path}")
        print(f"  {exc}")
    elif isinstance(exc, OcrQualityError):
        print(f"Failed [OCR_QUALITY]: {pdf_path}")
        print(f"  {exc}")
    elif isinstance(exc, OcrExecutionError):
        print(f"Failed [OCR_FAILED]: {pdf_path}")
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
            bank, output_path, report = convert_one(pdf_path, output_dir, ocr_enabled=args.ocr)
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
