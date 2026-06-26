import shutil

import pdfplumber


def is_image_only_pdf(pdf_path, max_pages=3):
    page_checks = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages[:max_pages]:
            text = page.extract_text() or ""
            page_checks.append((len(text.strip()), len(page.images or [])))
    return bool(page_checks) and all(text_len == 0 and image_count > 0 for text_len, image_count in page_checks)


def find_ocrmypdf():
    return shutil.which("ocrmypdf")


def ocrmypdf_available():
    return find_ocrmypdf() is not None

