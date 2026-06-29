# ZeroEntry PDF Converter V.20.3 Pre-V21 Safety Gate & Regression Checklist Patch

## Positioning

V.20.3 is a Pre-V21 Safety Gate & Regression Checklist Patch. It adds registry and scanned-PDF safety tests plus a written checklist before starting V.21 BOC OCR parser calibration.

This release does not calibrate or rewrite the BOC OCR parser.

## What Changed

- Added bank registry / scanned PDF safety regression tests.
- Added `PRE_V21_SAFETY_CHECKLIST.md`.
- Documented the safety gate for the upcoming V.21 BOC OCR parser calibration work.

## Behavior Preserved

- V.16 parser registry remains the default conversion path.
- OCR remains opt-in.
- Text-layer PDFs continue to use existing parsers.
- Image-only scanned PDFs without `--ocr` still fail with the scanned PDF error.
- BOC OCR fallback remains limited to no-account-rows failures.
- Calibration generated outputs remain ignored.
- Redacted OCR fixtures remain tracked.

## Not Included In V.20.3

- BOC OCR parser calibration
- New bank OCR parsers
- GUI
- OCR enabled by default
- BOC parser rewrite
- Changes to `_accounting_engine/`
- Real PDF, Excel, OCR_WORK, generated output, or sensitive-data fixtures
