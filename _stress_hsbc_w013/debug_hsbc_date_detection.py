import sys

import pdfplumber

sys.path.insert(0, "_prototype_bank_converter")
import hsbc_pdf_converter as converter


for filename in ["HSBC 2501.pdf", "HSBC 2512.pdf", "HSBC 2601.pdf"]:
    print("====", filename)
    with pdfplumber.open(f"_stress_hsbc_w013/input/{filename}") as pdf:
        for page_idx, page in enumerate(pdf.pages, start=1):
            lines = converter.words_to_lines(page.extract_words(x_tolerance=1, y_tolerance=3) or [])
            for line in lines:
                text = " ".join(word["text"] for word in line["words"])
                detected = converter.detect_statement_date(text)
                if detected:
                    print("page", page_idx, "top", round(line["top"], 1), "detected", detected, "text=", text)
