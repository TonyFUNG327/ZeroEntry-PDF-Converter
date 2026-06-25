from pathlib import Path

import pdfplumber


PDF_PATH = Path(__file__).with_name("hsbc_Apr2025.pdf")
AMOUNT_CHARS = set("0123456789,.")


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
    print(f"pages={len(pdf.pages)}")
    for page_no, page in enumerate(pdf.pages, start=1):
        print(f"\n--- PAGE {page_no} ---")
        rows = group_lines(page.extract_words(x_tolerance=1, y_tolerance=3) or [])
        for row in rows:
            text = " ".join(word["text"] for word in row["words"])
            has_amount = any(
                word["text"].replace(",", "").replace(".", "").isdigit()
                and any(char in AMOUNT_CHARS for char in word["text"])
                for word in row["words"]
            )
            if (
                text.startswith("Date")
                or "Date TransactionDetails" in text
                or "HSBC Business Direct HKD" in text
                or "B/F BALANCE" in text
                or "CHEQUE" in text
                or "DLF PRODUCTION LTD" in text
                or "TotalNo.of" in text
                or "TotalDepositAmount" in text
                or "CR TO" in text
                or "CREDIT INTEREST" in text
                or "APS CHARGES" in text
                or has_amount
            ):
                coords = [
                    f"{word['text']}@{word['x0']:.1f}-{word['x1']:.1f}"
                    for word in row["words"]
                ]
                print(f"top={row['top']:.1f} | {text}")
                print("  " + " | ".join(coords))
