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
from ocr.ocr_config import OCR_WORK_DIR
from ocr.ocr_diagnostics import analyze_ocr_text_for_diagnostics, attach_parser_diagnostics, write_diagnostic_report
from ocr.ocr_preprocessor import preprocess_pdf_for_ocr
from ocr.ocr_quality import validate_ocr_quality
from ocr_parsers import boc_ocr_pdf_converter


DEFAULT_INPUT_PATH = BB_DIR
DEFAULT_OUTPUT_DIR = BB2_DIR


class OcrFallbackParserError(ParserExecutionError):
    pass


class NoAccountRowsError(ParserExecutionError):
    pass


def is_no_account_rows_error(exc: Exception) -> bool:
    return "no account rows" in str(exc).lower() or "returned no account rows" in str(exc).lower()


def diagnostic_path_for(pdf_path):
    return OCR_WORK_DIR / f"{Path(pdf_path).stem}.diagnostic.txt"


def parser_diagnostic_path_for(pdf_path):
    return OCR_WORK_DIR / f"{Path(pdf_path).stem}.parser_diagnostic.txt"


def write_ocr_diagnostic(pdf_path, ocr_text):
    report = analyze_ocr_text_for_diagnostics(ocr_text)
    report["source_file"] = str(pdf_path)
    return write_diagnostic_report(report, diagnostic_path_for(pdf_path))


def write_boc_parser_diagnostic(source_pdf_path, ocr_text, parser_result):
    report = analyze_ocr_text_for_diagnostics(ocr_text)
    report["source_file"] = str(source_pdf_path)
    attach_parser_diagnostics(report, parser_result)
    return write_diagnostic_report(report, parser_diagnostic_path_for(source_pdf_path))


def convert_with_boc_ocr_fallback(ocr_pdf_path, output_dir, output_stem, diagnostic_path, source_pdf_path, ocr_text):
    parser_result = boc_ocr_pdf_converter.extract_pdf_with_diagnostics(ocr_pdf_path)
    parser_diagnostic_path = write_boc_parser_diagnostic(source_pdf_path, ocr_text, parser_result)
    accounts = parser_result.accounts
    if not accounts:
        raise OcrFallbackParserError(
            "Existing BOC parser returned no account rows after OCR. "
            "BOC OCR fallback parser also returned no transaction rows. "
            f"Diagnostic report saved: {diagnostic_path}. "
            f"Parser diagnostic saved: {parser_diagnostic_path}. "
            "Suggested next step: inspect candidate lines, skipped lines, and OCR text."
        )
    report = boc_ocr_pdf_converter.validate_accounts(accounts)
    output_path = boc_ocr_pdf_converter.write_workbook(accounts, Path(output_dir) / f"{output_stem}.xlsx")
    if parser_result.warnings:
        print(f"Warnings were recorded in: {parser_diagnostic_path}")
    return "BOC_OCR_FALLBACK", output_path, report


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
    diagnostic_path = write_ocr_diagnostic(pdf_path, ocr_result.text)
    try:
        return convert_with_adapter(
            ocr_result.searchable_pdf,
            output_dir,
            bank_code=quality_report.bank_code,
            output_stem=pdf_path.stem,
        )
    except ParserExecutionError as exc:
        if quality_report.bank_code == "BOC" and is_no_account_rows_error(exc):
            try:
                return convert_with_boc_ocr_fallback(
                    ocr_result.searchable_pdf,
                    output_dir,
                    pdf_path.stem,
                    diagnostic_path,
                    pdf_path,
                    ocr_result.text,
                )
            except OcrFallbackParserError:
                raise
        if quality_report.bank_code == "BOC":
            raise ParserExecutionError(
                f"BOC parser failed after OCR for a reason other than no account rows: {exc}. "
                f"Diagnostic report saved: {diagnostic_path}. "
                "BOC OCR fallback was not attempted."
            ) from exc
        raise ParserExecutionError(
            f"{quality_report.bank_code} parser returned no account rows after OCR. "
            f"Diagnostic report saved: {diagnostic_path}. "
            "Suggested next step: inspect OCR text and parser candidate lines."
        ) from exc


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
    elif isinstance(exc, OcrFallbackParserError):
        print(f"Failed [PARSER_FAILED]: {pdf_path}")
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
