import pathlib

import pdfplumber


for name in ["1月.pdf", "EStatement.pdf", "12月.pdf"]:
    path = pathlib.Path("_stress_unknown_h026/input") / name
    with pdfplumber.open(path) as pdf:
        print("====", name, "pages", len(pdf.pages), "====")
        for page_idx, page in enumerate(pdf.pages[:2], start=1):
            print("---PAGE", page_idx, "---")
            print((page.extract_text() or "")[:3500])
