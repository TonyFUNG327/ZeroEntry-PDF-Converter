from dataclasses import dataclass

import pdfplumber

import boc_pdf_converter
import comm_pdf_converter
import dbs_pdf_converter
import hsb_pdf_converter
import hsbc_pdf_converter
import icbc_asia_pdf_converter
import ncb_pdf_converter
import ocbc_pdf_converter


SCANNED_IMAGE_ONLY = "SCANNED_IMAGE_ONLY"


class UnsupportedBankError(ValueError):
    pass


class ScannedPdfError(ValueError):
    pass


class ParserExecutionError(RuntimeError):
    pass


@dataclass(frozen=True)
class BankAdapter:
    code: str
    module: object
    display_name: str

    def extract_pdf(self, pdf_path):
        return self.module.extract_pdf(pdf_path)

    def validate_accounts(self, accounts):
        return self.module.validate_accounts(accounts)

    def write_workbook(self, accounts, output_path):
        return self.module.write_workbook(accounts, output_path)


BANKS = {
    "HSBC": BankAdapter("HSBC", hsbc_pdf_converter, "HSBC"),
    "HSB": BankAdapter("HSB", hsb_pdf_converter, "Hang Seng Bank"),
    "BOC": BankAdapter("BOC", boc_pdf_converter, "Bank of China (Hong Kong)"),
    "DBS": BankAdapter("DBS", dbs_pdf_converter, "DBS Bank (Hong Kong)"),
    "ICBC_ASIA": BankAdapter("ICBC_ASIA", icbc_asia_pdf_converter, "ICBC Asia"),
    "COMM": BankAdapter("COMM", comm_pdf_converter, "Bank of Communications"),
    "OCBC": BankAdapter("OCBC", ocbc_pdf_converter, "OCBC"),
    "NCB": BankAdapter("NCB", ncb_pdf_converter, "Nanyang Commercial Bank"),
}


def detect_bank_from_text(text, page_checks=None):
    text = text or ""
    page_checks = page_checks or []

    if "HSBC Business Direct" in text or "HSBC Sprint Account Statement" in text:
        return "HSBC"
    if "DBS Bank (Hong Kong) Limited" in text:
        return "DBS"
    if "INDUSTRIAL AND COMMERCIAL BANK OF CHINA (ASIA)" in text or "中國工商銀行（亞洲）" in text or "中国工商银行（亚洲）" in text:
        return "ICBC_ASIA"
    if "OCBC" in text or "OCBC Bank" in text or ("BANK REFERENCE" in text and "PORTFOLIO SUMMARY" in text):
        return "OCBC"
    if (
        "南洋商業銀行" in text
        or "南洋商业银行" in text
        or "Nanyang Commercial Bank" in text
        or ("NCB" in text and ("賬戶交易詳情" in text or "账户交易详情" in text or "Account Transaction Details" in text))
        or ("Consolidated Statement" in text and "BIA Customer No." in text)
    ):
        return "NCB"
    if "Bank of Communications" in text or ("CONSOLIDATED STATEMENT" in text and "SAVINGS/CURRENT DEPOSITS ACTIVITIES" in text):
        return "COMM"
    if "BANK OF CHINA" in text or "中國銀行" in text or "中国银行" in text:
        return "BOC"
    if "Hang Seng" in text or "HKD Statement Savings" in text:
        return "HSB"
    if page_checks and all(text_len == 0 and image_count > 0 for text_len, image_count in page_checks):
        return SCANNED_IMAGE_ONLY
    return None


def read_pdf_detection_context(pdf_path, max_pages=3):
    text_parts = []
    page_checks = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages[:max_pages]:
            text = page.extract_text() or ""
            text_parts.append(text)
            page_checks.append((len(text.strip()), len(page.images or [])))
    return "\n".join(text_parts), page_checks


def detect_bank(pdf_path):
    text, page_checks = read_pdf_detection_context(pdf_path)
    return detect_bank_from_text(text, page_checks)


def get_adapter(bank_code):
    if bank_code == SCANNED_IMAGE_ONLY:
        raise ScannedPdfError(
            "Image-only scanned PDF detected. This portable version requires a selectable text layer; "
            "run OCR first or use a future OCR-enabled converter."
        )
    if not bank_code:
        raise UnsupportedBankError(
            "Unsupported or unrecognized bank statement. The PDF text layer did not match any V.17 supported bank layout."
        )
    try:
        return BANKS[bank_code]
    except KeyError as exc:
        raise UnsupportedBankError(f"Unsupported bank code detected: {bank_code}") from exc


def convert_with_adapter(pdf_path, output_dir, bank_code=None, output_stem=None):
    bank_code = bank_code or detect_bank(pdf_path)
    adapter = get_adapter(bank_code)
    try:
        accounts = adapter.extract_pdf(pdf_path)
        if not accounts:
            raise ParserExecutionError(f"{adapter.code} parser returned no account rows.")
        report = adapter.validate_accounts(accounts)
        stem = output_stem or pdf_path.stem
        output_path = adapter.write_workbook(accounts, output_dir / f"{stem}.xlsx")
    except ParserExecutionError:
        raise
    except Exception as exc:
        raise ParserExecutionError(f"{adapter.code} parser failed for {pdf_path.name}: {exc}") from exc
    return adapter.code, output_path, report
