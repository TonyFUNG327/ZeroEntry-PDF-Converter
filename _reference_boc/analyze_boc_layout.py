from pathlib import Path

import pdfplumber


PDF_PATH = Path(__file__).with_name("BOC 2505.pdf")


def group_lines(words):
    rows = []
    for word in words:
        if word["top"] < 70 or word["top"] > 760:
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


with pdfplumber.open(PDF_PATH) as pdf:
    print(f"pages={len(pdf.pages)}")
    for page_no, page in enumerate(pdf.pages, start=1):
        print(f"\n--- PAGE {page_no} ---")
        rows = group_lines(page.extract_words(x_tolerance=1, y_tolerance=3) or [])
        for row in rows:
            text = " ".join(word["text"] for word in row["words"])
            has_amount = any(
                word["text"].strip("()").replace(",", "").replace(".", "").isdigit()
                and ("," in word["text"] or "." in word["text"])
                for word in row["words"]
            )
            if (
                "交易日期" in text
                or "港元儲蓄" in text
                or "港元往來" in text
                or "承前結餘" in text
                or "今期結餘" in text
                or has_amount
            ):
                coords = [f"{word['text']}@{word['x0']:.1f}-{word['x1']:.1f}" for word in row["words"]]
                print(f"top={row['top']:.1f} | {text}")
                print("  " + " | ".join(coords))
