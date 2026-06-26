# ZeroEntry PDF Converter V.19.1 OCR Reliability Patch Release Notes

## Positioning

V.19.1 is an OCR Reliability Patch. It keeps the V.18 OCR Parser Calibration workflow and focuses on safer BOC OCR fallback behavior, richer parser diagnostics, and better BOC OCR line parsing.

## V.18 Behavior Preserved

- OCR remains opt-in with `--ocr`.
- Text-layer PDFs continue to use the existing bank parsers.
- Image-only PDFs without `--ocr` still report the scanned-PDF error.
- `BB/`, `BB2/`, `BB3/`, and `OCR_WORK/` workflow remains unchanged.
- Excel columns remain:
  `Bank_Account, Date, Description, Deposit, Withdrawal, Balance, Control`

## What Changed In V.19.1

- BOC OCR fallback is now attempted only when the existing BOC parser specifically returns a no-account-rows error.
- Non no-row parser failures do not trigger fallback, which avoids masking write, validation, or layout errors.
- Added more BOC OCR date formats:
  - `YYYY/MM/DD`
  - `YYYY-MM-DD`
  - `DD-Mon-YY`
  - `DD-Mon-YYYY`
  - `DD Mon YY`
  - `DD Mon YYYY`
- BOC OCR fallback now preserves parser warnings, parsed rows, skipped lines, and skip reasons.
- OCR diagnostics now include:
  - candidate transaction lines
  - parsed transaction rows
  - skipped candidate lines
  - skip reasons
- BOC account type detection now supports common current/savings headings and records a warning when it defaults to current account.

## V.19.1 Hardening Notes

- Added `NoAccountRowsError` in the bank registry so no-row parser results have an explicit exception type.
- Kept backward-compatible no-row string detection only as a safety fallback for older parser failure messages.
- Added stronger BOC OCR date-format tests that verify parsed row dates and deposit/balance classification.
- Added parser diagnostics tests for parsed rows, skipped lines, skip reasons, and warning propagation.
- Added `inspect_ocr_output.py --parser BOC` for optional BOC parser-level diagnostics without changing the default OCR-level diagnostic behavior.
- Added a concise BOC OCR fallback CLI summary:
  parsed row count, skipped candidate line count, warning count, and parser diagnostic path.

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

## Fallback Trigger

The BOC OCR fallback parser runs only when all of these are true:

- `--ocr` is enabled
- the source PDF was image-only
- OCR quality gate passes
- OCR bank detection returns `BOC`
- the existing BOC parser failed specifically because it returned no account rows

## Known Limitations

- BOC OCR fallback remains experimental.
- OCR accuracy depends on scan quality.
- Coordinate-based parsers may still fail after OCR.
- Not all scanned bank statements are supported.
- OCRmyPDF/Tesseract must be installed separately for real OCR execution.

## Not Included In V.19.1

- All-bank OCR guarantee
- GUI
- Full production OCR guarantee
- Large-scale parser rewrite
- OCR enabled by default
