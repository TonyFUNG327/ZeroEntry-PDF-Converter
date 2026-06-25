import pathlib

import pdfplumber


def main():
    pdf_path = pathlib.Path("_reference_ncb/input/A0103_CAccountStatement_HK_04350900074362kE11Dy_20241231.pdf")
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]
        words = page.extract_words(x_tolerance=1, y_tolerance=3, keep_blank_chars=False)

    rows = {}
    for word in words:
        y = round(word["top"] / 3) * 3
        rows.setdefault(y, []).append(word)

    for y in sorted(rows):
        if 210 <= y <= 430:
            line = sorted(rows[y], key=lambda item: item["x0"])
            text = " | ".join(
                f"{item['text']}@{item['x0']:.1f}-{item['x1']:.1f}" for item in line
            )
            print(y, text)


if __name__ == "__main__":
    main()
