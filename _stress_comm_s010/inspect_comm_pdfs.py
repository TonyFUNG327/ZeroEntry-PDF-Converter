from pathlib import Path

import pdfplumber


for name in [
    "20230114MHK605001B0000232.pdf",
    "20230614MHK605001B0000227.pdf",
    "20241214MHK605001B0000287.pdf",
]:
    path = Path("_stress_comm_s010") / "input" / name
    with pdfplumber.open(path) as pdf:
        print("====", name, "pages", len(pdf.pages), "====")
        for page_idx, page in enumerate(pdf.pages[:3], start=1):
            print("---PAGE", page_idx, "---")
            print((page.extract_text() or "")[:4500])
