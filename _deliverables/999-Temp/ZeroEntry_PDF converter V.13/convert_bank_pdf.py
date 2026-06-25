import argparse
from pathlib import Path

import pdfplumber

import boc_pdf_converter
import comm_pdf_converter
import dbs_pdf_converter
import hsb_pdf_converter
import hsbc_pdf_converter
import ncb_pdf_converter
import ocbc_pdf_converter


DEFAULT_INPUT_PATH = Path(__file__).resolve().parent / "BB"
DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parent / "BB2"


def detect_bank(pdf_path):
    text_parts = []
    page_checks = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages[:3]:
            text = page.extract_text() or ""
            text_parts.append(text)
            page_checks.append((len(text.strip()), len(page.images or [])))
    text = "\n".join(text_parts)

    if "HSBC Business Direct" in text or "HSBC Sprint Account Statement" in text:
        return "HSBC"
    if "DBS Bank (Hong Kong) Limited" in text:
        return "DBS"
    if "OCBC" in text or "OCBC Bank" in text or "BANK REFERENCE" in text and "PORTFOLIO SUMMARY" in text:
        return "OCBC"
    if "南洋商業銀行" in text or "NCB" in text and "賬戶交易詳情" in text:
        return "NCB"
    if "Bank of Communications" in text or "CONSOLIDATED STATEMENT" in text and "SAVINGS/CURRENT DEPOSITS ACTIVITIES" in text:
        return "COMM"
    if "中國銀行" in text or "BANK OF CHINA" in text or "綜合月結單" in text:
        return "BOC"
    if "Hang Seng" in text or "HKD Statement Savings" in text:
        return "HSB"
    if page_checks and all(text_len == 0 and image_count > 0 for text_len, image_count in page_checks):
        return "SCANNED_IMAGE_ONLY"
    return None


def collect_pdf_paths(input_path):
    input_path = Path(input_path)
    if input_path.is_file():
        if input_path.suffix.lower() != ".pdf":
            raise ValueError(f"Input file is not a PDF: {input_path}")
        return [input_path]
    if input_path.is_dir():
        return sorted(path for path in input_path.iterdir() if path.is_file() and path.suffix.lower() == ".pdf")
    raise FileNotFoundError(f"Input path does not exist: {input_path}")


def convert_one(pdf_path, output_dir):
    bank = detect_bank(pdf_path)
    if bank == "HSBC":
        accounts = hsbc_pdf_converter.extract_pdf(pdf_path)
        report = hsbc_pdf_converter.validate_accounts(accounts)
        output_path = hsbc_pdf_converter.write_workbook(accounts, output_dir / f"{pdf_path.stem}.xlsx")
    elif bank == "HSB":
        accounts = hsb_pdf_converter.extract_pdf(pdf_path)
        report = hsb_pdf_converter.validate_accounts(accounts)
        output_path = hsb_pdf_converter.write_workbook(accounts, output_dir / f"{pdf_path.stem}.xlsx")
    elif bank == "BOC":
        accounts = boc_pdf_converter.extract_pdf(pdf_path)
        report = boc_pdf_converter.validate_accounts(accounts)
        output_path = boc_pdf_converter.write_workbook(accounts, output_dir / f"{pdf_path.stem}.xlsx")
    elif bank == "DBS":
        accounts = dbs_pdf_converter.extract_pdf(pdf_path)
        report = dbs_pdf_converter.validate_accounts(accounts)
        output_path = dbs_pdf_converter.write_workbook(accounts, output_dir / f"{pdf_path.stem}.xlsx")
    elif bank == "COMM":
        accounts = comm_pdf_converter.extract_pdf(pdf_path)
        report = comm_pdf_converter.validate_accounts(accounts)
        output_path = comm_pdf_converter.write_workbook(accounts, output_dir / f"{pdf_path.stem}.xlsx")
    elif bank == "OCBC":
        accounts = ocbc_pdf_converter.extract_pdf(pdf_path)
        report = ocbc_pdf_converter.validate_accounts(accounts)
        output_path = ocbc_pdf_converter.write_workbook(accounts, output_dir / f"{pdf_path.stem}.xlsx")
    elif bank == "NCB":
        accounts = ncb_pdf_converter.extract_pdf(pdf_path)
        report = ncb_pdf_converter.validate_accounts(accounts)
        output_path = ncb_pdf_converter.write_workbook(accounts, output_dir / f"{pdf_path.stem}.xlsx")
    elif bank == "SCANNED_IMAGE_ONLY":
        raise ValueError(
            "Image-only scanned PDF detected. This portable version requires a selectable text layer; "
            "run OCR first or use a future OCR-enabled converter."
        )
    else:
        raise ValueError(f"Unsupported or unrecognized bank statement: {pdf_path}")

    return bank, output_path, report


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


def main(argv=None):
    args = build_arg_parser().parse_args(argv)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

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
            print(f"Failed: {pdf_path} ({exc})")
            continue

        print(f"Saved [{bank}]: {output_path}")
        for item in report:
            deposits = item.get("deposit_count", "n/a")
            withdrawals = item.get("withdrawal_count", "n/a")
            print(
                f"{item['account']}: rows={item['rows']}, "
                f"deposits={deposits} amount={item['deposit_total']:,.2f}, "
                f"withdrawals={withdrawals} amount={item['withdrawal_total']:,.2f}, "
                f"final_balance={item['final_balance']:,.2f}, final_control={item['final_control']:,.2f}, "
                f"balance_mismatches={len(item['balance_mismatches'])}"
            )
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
