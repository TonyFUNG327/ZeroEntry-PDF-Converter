# ZeroEntry PDF Converter V.18 OCR Parser Calibration Release Notes

## Positioning

V.18 is an OCR Parser Calibration release. It builds on the V.17 OCR Experimental pipeline and focuses on inspecting OCR output, improving parser diagnostics, and adding a first experimental fallback parser for BOC scanned statements.

## V.17 Behavior Preserved

- OCR remains opt-in with `--ocr`.
- Text-layer PDFs continue to use existing parsers.
- Image-only PDFs without `--ocr` still report the scanned-PDF error.
- `BB/`, `BB2/`, `BB3/`, and `OCR_WORK/` workflow remains unchanged.
- Excel columns remain:
  `Bank_Account, Date, Description, Deposit, Withdrawal, Balance, Control`

## What Changed In V.18

- Added structured OCR diagnostics in `ocr/ocr_diagnostics.py`.
- Added `inspect_ocr_output.py` for manually inspecting OCR `.txt` or searchable `.pdf` output.
- Added experimental `ocr_parsers/boc_ocr_pdf_converter.py`.
- Added OCR fallback orchestration for BOC only:
  OCR PDF -> quality gate pass -> existing parser -> if no rows and bank is BOC -> BOC OCR fallback parser.
- Improved parser failure guidance after OCR with diagnostic report paths.

## Usage

Convert with OCR enabled:

```bat
python convert_bank_pdf.py --ocr
python convert_bank_pdf.py BB -o BB2 --ocr
```

Inspect OCR output:

```bat
python inspect_ocr_output.py "OCR_WORK\file.ocr.txt"
python inspect_ocr_output.py "OCR_WORK\file.ocr.pdf"
```

The inspector writes:

- `.diagnostic.txt`
- `.diagnostic.json`

## Diagnostic Report Contents

- source file
- text length
- detected bank code
- date count
- amount count
- candidate transaction line count
- page count when PDF input is provided
- first candidate transaction lines
- warnings

## BOC OCR Fallback Parser

The BOC OCR fallback parser is experimental. It uses line-based OCR text parsing and conservative balance movement checks. It reuses the existing BOC workbook writer and validation helpers to keep output format consistent.

Fallback is only attempted when:

- `--ocr` is enabled
- source PDF was image-only
- OCR quality gate passes
- detected bank is `BOC`
- the existing BOC parser returns no account rows

## Known Limitations

- OCR accuracy depends on scan quality.
- Coordinate-based parsers may still fail after OCR.
- BOC OCR fallback is not a production guarantee.
- Not all scanned bank statements are supported.
- OCRmyPDF/Tesseract must be installed separately.

## Not Included In V.18

- All-bank OCR guarantee
- GUI
- Full production OCR guarantee
- Large-scale parser rewrite
