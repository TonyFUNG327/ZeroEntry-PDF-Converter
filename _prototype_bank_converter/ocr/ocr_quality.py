import re
from dataclasses import dataclass

from core.bank_registry import detect_bank_from_text

from .ocr_config import DEFAULT_MIN_AMOUNT_COUNT, DEFAULT_MIN_DATE_COUNT, DEFAULT_MIN_TEXT_LENGTH
from .ocr_errors import OcrQualityError


DATE_RE = re.compile(
    r"\b(?:\d{4}[/-]\d{1,2}[/-]\d{1,2}|\d{1,2}\s+[A-Z][a-z]{2}\s+\d{4}|\d{1,2}-[A-Z][a-z]{2}-\d{2})\b"
)
AMOUNT_RE = re.compile(r"\(?\b\d{1,3}(?:,\d{3})*(?:\.\d{2})\b\)?|\(?\b\d+\.\d{2}\b\)?")


@dataclass(frozen=True)
class OcrQualityReport:
    text_length: int
    date_count: int
    amount_count: int
    bank_code: str
    confidence: float | None = None


def analyze_ocr_text(text, confidence=None):
    text = text or ""
    return OcrQualityReport(
        text_length=len(text.strip()),
        date_count=len(DATE_RE.findall(text)),
        amount_count=len(AMOUNT_RE.findall(text)),
        bank_code=detect_bank_from_text(text),
        confidence=confidence,
    )


def validate_ocr_quality(
    text,
    min_text_length=DEFAULT_MIN_TEXT_LENGTH,
    min_date_count=DEFAULT_MIN_DATE_COUNT,
    min_amount_count=DEFAULT_MIN_AMOUNT_COUNT,
    min_confidence=None,
    confidence=None,
):
    report = analyze_ocr_text(text, confidence=confidence)
    failures = []
    if report.text_length < min_text_length:
        failures.append(f"text length {report.text_length} < {min_text_length}")
    if not report.bank_code:
        failures.append("supported bank could not be detected from OCR text")
    if report.date_count < min_date_count:
        failures.append(f"date count {report.date_count} < {min_date_count}")
    if report.amount_count < min_amount_count:
        failures.append(f"amount count {report.amount_count} < {min_amount_count}")
    if min_confidence is not None and report.confidence is not None and report.confidence < min_confidence:
        failures.append(f"OCR confidence {report.confidence:.2f} < {min_confidence:.2f}")
    if failures:
        raise OcrQualityError("OCR quality gate failed: " + "; ".join(failures))
    return report
