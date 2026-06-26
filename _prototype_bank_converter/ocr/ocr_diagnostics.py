import json
import re
from datetime import date, datetime
from pathlib import Path

import pdfplumber

from core.bank_registry import detect_bank_from_text
from .ocr_quality import AMOUNT_RE, DATE_RE


TRANSACTION_LINE_RE = re.compile(
    r"(?:"
    r"\d{4}[/-]\d{1,2}[/-]\d{1,2}"
    r"|\d{1,2}\s+[A-Z][a-z]{2}\s+\d{2,4}"
    r"|\d{1,2}-[A-Z][a-z]{2}-\d{2,4}"
    r").*"
)


def extract_text_from_pdf(pdf_path):
    text_parts = []
    page_count = 0
    with pdfplumber.open(pdf_path) as pdf:
        page_count = len(pdf.pages)
        for page in pdf.pages:
            text_parts.append(page.extract_text() or "")
    return "\n".join(text_parts), page_count


def candidate_transaction_lines(text, limit=None):
    candidates = []
    for raw_line in (text or "").splitlines():
        line = " ".join(raw_line.split())
        if not line:
            continue
        if TRANSACTION_LINE_RE.search(line) and AMOUNT_RE.search(line):
            candidates.append(line)
    return candidates[:limit] if limit else candidates


def analyze_ocr_text_for_diagnostics(text: str) -> dict:
    text = text or ""
    candidates = candidate_transaction_lines(text)
    warnings = []
    bank_code = detect_bank_from_text(text)
    if not bank_code:
        warnings.append("Supported bank could not be detected from OCR text.")
    if len(text.strip()) < 80:
        warnings.append("OCR text is short; scan quality or OCR language pack may be insufficient.")
    if not candidates:
        warnings.append("No candidate transaction lines were found.")

    return {
        "source_file": None,
        "text_length": len(text.strip()),
        "detected_bank_code": bank_code,
        "date_count": len(DATE_RE.findall(text)),
        "amount_count": len(AMOUNT_RE.findall(text)),
        "candidate_transaction_line_count": len(candidates),
        "page_count": None,
        "first_candidate_lines": candidates[:10],
        "parsed_transaction_row_count": 0,
        "skipped_candidate_line_count": 0,
        "parsed_rows": [],
        "skipped_lines": [],
        "warnings": warnings,
    }


def _json_safe(value):
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, dict):
        return {key: _json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    return value


def attach_parser_diagnostics(report: dict, parser_result) -> dict:
    parsed_rows = getattr(parser_result, "parsed_rows", []) or []
    skipped_lines = getattr(parser_result, "skipped_lines", []) or []
    parser_warnings = getattr(parser_result, "warnings", []) or []
    report["parsed_transaction_row_count"] = len(parsed_rows)
    report["skipped_candidate_line_count"] = len(skipped_lines)
    report["parsed_rows"] = _json_safe(parsed_rows[:20])
    report["skipped_lines"] = _json_safe(skipped_lines[:20])
    report["warnings"] = list(report.get("warnings") or []) + parser_warnings
    return report


def analyze_ocr_file_for_diagnostics(input_path) -> dict:
    input_path = Path(input_path)
    if input_path.suffix.lower() == ".pdf":
        text, page_count = extract_text_from_pdf(input_path)
    else:
        text = input_path.read_text(encoding="utf-8", errors="replace")
        page_count = None
    report = analyze_ocr_text_for_diagnostics(text)
    report["source_file"] = str(input_path)
    report["page_count"] = page_count
    return report


def format_diagnostic_report(report: dict) -> str:
    lines = [
        f"Source file: {report.get('source_file') or 'n/a'}",
        f"Detected bank: {report.get('detected_bank_code') or 'UNKNOWN'}",
        f"Text length: {report.get('text_length', 0)}",
        f"Date count: {report.get('date_count', 0)}",
        f"Amount count: {report.get('amount_count', 0)}",
        f"Candidate transaction lines: {report.get('candidate_transaction_line_count', 0)}",
        f"Parsed transaction rows: {report.get('parsed_transaction_row_count', 0)}",
        f"Skipped candidate lines: {report.get('skipped_candidate_line_count', 0)}",
    ]
    if report.get("page_count") is not None:
        lines.append(f"Page count: {report.get('page_count')}")
    lines.append("")
    lines.append("First candidate lines:")
    for idx, line in enumerate(report.get("first_candidate_lines") or [], start=1):
        lines.append(f"{idx}. {line}")
    if not report.get("first_candidate_lines"):
        lines.append("(none)")
    lines.append("")
    lines.append("Parsed rows:")
    for idx, item in enumerate(report.get("parsed_rows") or [], start=1):
        lines.append(f"{idx}. {item.get('line', item)}")
    if not report.get("parsed_rows"):
        lines.append("(none)")
    lines.append("")
    lines.append("Skipped lines:")
    for idx, item in enumerate(report.get("skipped_lines") or [], start=1):
        if isinstance(item, dict):
            lines.append(f"{idx}. {item.get('line', '')}")
            lines.append(f"   reason: {item.get('reason', 'n/a')}")
        else:
            lines.append(f"{idx}. {item}")
    if not report.get("skipped_lines"):
        lines.append("(none)")
    lines.append("")
    lines.append("Warnings:")
    for warning in report.get("warnings") or []:
        lines.append(f"- {warning}")
    if not report.get("warnings"):
        lines.append("(none)")
    return "\n".join(lines) + "\n"


def write_diagnostic_report(report: dict, output_path: Path) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.suffix.lower() == ".json":
        output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    else:
        output_path.write_text(format_diagnostic_report(report), encoding="utf-8")
    return output_path
