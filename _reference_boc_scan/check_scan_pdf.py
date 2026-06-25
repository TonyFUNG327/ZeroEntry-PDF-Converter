from pathlib import Path

import pdfplumber


PDF_PATH = Path(__file__).with_name("BOC Bs-2411.pdf")
REPORT_PATH = Path(__file__).with_name("text_layer_report.txt")


lines = []
with pdfplumber.open(PDF_PATH) as pdf:
    lines.append(f"pages={len(pdf.pages)}")
    for page_no, page in enumerate(pdf.pages, start=1):
        text = page.extract_text() or ""
        words = page.extract_words(x_tolerance=1, y_tolerance=3) or []
        images = page.images or []
        lines.append(
            f"page={page_no} text_length={len(text)} words={len(words)} images={len(images)} "
            f"width={page.width:.1f} height={page.height:.1f}"
        )
        if page_no <= 5:
            lines.append(f"sample={text[:1200]!r}")

REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
print(REPORT_PATH)
