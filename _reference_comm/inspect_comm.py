from pathlib import Path

import pdfplumber


for pdf_path in sorted(Path(__file__).parent.glob("*.pdf")):
    print(f"\n===== {pdf_path.name} =====")
    with pdfplumber.open(pdf_path) as pdf:
        print(f"pages={len(pdf.pages)}")
        for page_no, page in enumerate(pdf.pages[:4], start=1):
            text = page.extract_text() or ""
            words = page.extract_words(x_tolerance=1, y_tolerance=3) or []
            print(f"--- PAGE {page_no} text_len={len(text)} words={len(words)} images={len(page.images or [])} ---")
            print(text[:4500])
