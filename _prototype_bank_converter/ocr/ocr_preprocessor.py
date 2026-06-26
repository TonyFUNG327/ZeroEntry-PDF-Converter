import subprocess
from dataclasses import dataclass
from pathlib import Path

import pdfplumber

from .ocr_config import DEFAULT_OCR_LANGUAGE, OCR_WORK_DIR
from .ocr_detector import find_ocrmypdf
from .ocr_errors import OcrDependencyError, OcrExecutionError


@dataclass(frozen=True)
class OcrResult:
    source_pdf: Path
    searchable_pdf: Path
    text_path: Path
    log_path: Path
    text: str
    backend: str


def ensure_ocr_work_dir(work_dir=OCR_WORK_DIR):
    work_dir = Path(work_dir)
    work_dir.mkdir(parents=True, exist_ok=True)
    return work_dir


def extract_text_from_pdf(pdf_path):
    text_parts = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text_parts.append(page.extract_text() or "")
    return "\n".join(text_parts)


def preprocess_pdf_for_ocr(pdf_path, work_dir=OCR_WORK_DIR, language=DEFAULT_OCR_LANGUAGE):
    pdf_path = Path(pdf_path)
    work_dir = ensure_ocr_work_dir(work_dir)
    ocrmypdf = find_ocrmypdf()
    if not ocrmypdf:
        raise OcrDependencyError(
            "OCR mode requires external OCR tools. Please install OCRmyPDF with Tesseract OCR "
            "or run without --ocr for text-layer PDFs."
        )

    output_pdf = work_dir / f"{pdf_path.stem}.ocr.pdf"
    text_path = work_dir / f"{pdf_path.stem}.ocr.txt"
    log_path = work_dir / f"{pdf_path.stem}.ocr.log"
    command = [
        ocrmypdf,
        "--force-ocr",
        "--deskew",
        "--rotate-pages",
        "-l",
        language,
        str(pdf_path),
        str(output_pdf),
    ]

    try:
        completed = subprocess.run(command, capture_output=True, text=True, timeout=600)
    except subprocess.TimeoutExpired as exc:
        raise OcrExecutionError(f"OCRmyPDF timed out while processing {pdf_path.name}.") from exc
    except OSError as exc:
        raise OcrExecutionError(f"Failed to start OCRmyPDF: {exc}") from exc

    log_path.write_text((completed.stdout or "") + "\n" + (completed.stderr or ""), encoding="utf-8")
    if completed.returncode != 0:
        raise OcrExecutionError(
            f"OCRmyPDF failed for {pdf_path.name} with exit code {completed.returncode}. "
            f"See OCR log: {log_path}"
        )
    if not output_pdf.exists():
        raise OcrExecutionError(f"OCRmyPDF did not create expected searchable PDF: {output_pdf}")

    text = extract_text_from_pdf(output_pdf)
    text_path.write_text(text, encoding="utf-8")
    return OcrResult(
        source_pdf=pdf_path,
        searchable_pdf=output_pdf,
        text_path=text_path,
        log_path=log_path,
        text=text,
        backend="ocrmypdf",
    )

