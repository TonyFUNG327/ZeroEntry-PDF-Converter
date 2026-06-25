from pathlib import Path

import pdfplumber


PDF_PATH = Path(__file__).with_name("hsbc 04-2025 STATEMENT.pdf")


def group_lines(words):
    rows = []
    for word in words:
        if word["top"] < 85 or word["top"] > 755:
            continue
        for row in rows:
            if abs(row["top"] - word["top"]) <= 2.0:
                row["words"].append(word)
                row["top"] = (row["top"] + word["top"]) / 2
                break
        else:
            rows.append({"top": word["top"], "words": [word]})
    rows.sort(key=lambda row: row["top"])
    for row in rows:
        row["words"].sort(key=lambda word: word["x0"])
    return rows


with pdfplumber.open(PDF_PATH) as pdf:
    for page_no, page in enumerate(pdf.pages, start=1):
        print(f"\n--- PAGE {page_no} ---")
        rows = group_lines(page.extract_words(x_tolerance=1, y_tolerance=3) or [])
        for row in rows:
            text = " ".join(word["text"] for word in row["words"])
            if (
                "Foreign Currency Savings" in text
                or text.startswith("CCY ")
                or text.startswith("USD ")
                or text.startswith("CNY ")
                or text.startswith("DEPOSIT")
                or text.startswith("WITHDRAWAL")
                or text.startswith("BIB-")
                or "Total No. of" in text
                or "Total Deposit Amount" in text
            ):
                coords = [f"{word['text']}@{word['x0']:.1f}-{word['x1']:.1f}" for word in row["words"]]
                print(f"top={row['top']:.1f} | {text}")
                print("  " + " | ".join(coords))
