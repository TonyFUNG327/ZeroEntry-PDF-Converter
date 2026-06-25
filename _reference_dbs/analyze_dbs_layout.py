from pathlib import Path

import pdfplumber


def group_lines(words):
    rows = []
    for word in words:
        if word["top"] < 80 or word["top"] > 760:
            continue
        for row in rows:
            if abs(row["top"] - word["top"]) <= 2.2:
                row["words"].append(word)
                row["top"] = (row["top"] + word["top"]) / 2
                break
        else:
            rows.append({"top": word["top"], "words": [word]})
    rows.sort(key=lambda row: row["top"])
    for row in rows:
        row["words"].sort(key=lambda word: word["x0"])
    return rows


for pdf_path in sorted(Path(__file__).parent.glob("*.pdf")):
    print(f"\n===== {pdf_path.name} =====")
    with pdfplumber.open(pdf_path) as pdf:
        for page_no, page in enumerate(pdf.pages, start=1):
            print(f"\n--- PAGE {page_no} ---")
            rows = group_lines(page.extract_words(x_tolerance=1, y_tolerance=3) or [])
            for row in rows:
                text = " ".join(word["text"] for word in row["words"])
                has_amount = any(
                    word["text"].strip("-").replace(",", "").replace(".", "").isdigit()
                    and "." in word["text"]
                    for word in row["words"]
                )
                if (
                    "Currency:" in text
                    or "Grand Total" in text
                    or "Closing Balance" in text
                    or "Balance Brought Forward" in text
                    or (has_amount and any(ch.isdigit() for ch in text[:10]))
                ):
                    coords = [f"{word['text']}@{word['x0']:.1f}-{word['x1']:.1f}" for word in row["words"]]
                    print(f"top={row['top']:.1f} | {text}")
                    print("  " + " | ".join(coords))
