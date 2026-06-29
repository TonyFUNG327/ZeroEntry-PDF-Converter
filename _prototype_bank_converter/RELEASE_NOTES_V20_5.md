# ZeroEntry PDF Converter V.20.5 BOC OCR Line Merge & OCR Noise Expansion

## Positioning

V.20.5 expands the BOC OCR parser calibration work with line-merge support and additional OCR noise fixtures.

This release only calibrates the experimental BOC OCR fallback parser. It does not change the text-layer BOC parser or production conversion workflow.

## What Changed

- Added redacted BOC OCR fixtures:
  - `boc_scanned_sample_06_redacted.txt`
  - `boc_scanned_sample_07_redacted.txt`
  - `boc_scanned_sample_08_redacted.txt`
- Added `prepare_ocr_lines(text)` for merging split OCR transaction lines before parsing.
- Added amount-token-only normalization for OCR `O` vs `0` confusion, such as `1,O00.00` and `1,0O0.00`.
- Added line merge regression tests for split transaction descriptions and split amount lines.
- Preserved parser diagnostics with parsed rows, skipped lines, warnings, and skip reasons.

## Behavior Preserved

- OCR remains opt-in.
- Text-layer PDFs continue to use existing parsers.
- BOC OCR fallback trigger remains limited to no-account-rows failures.
- Generated diagnostic outputs remain ignored.
- Redacted fixtures remain tracked.
- Excel output columns remain unchanged.

## Not Included In V.20.5

- Full BOC OCR parser rewrite
- Changes to the text-layer BOC parser
- OCR parsers for HSBC / DBS / ICBC / OCBC / NCB
- GUI
- OCR enabled by default
- Changes to `_accounting_engine/`
- Real PDF, Excel, OCR_WORK, generated output, or sensitive-data fixtures
