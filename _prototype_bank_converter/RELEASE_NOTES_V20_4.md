# ZeroEntry PDF Converter V.20.4 BOC OCR Parsing Attack Phase

## Positioning

V.20.4 starts the BOC OCR Parsing Attack Phase. It uses redacted synthetic OCR text fixtures to calibrate the experimental BOC OCR fallback parser against common OCR noise patterns.

This release keeps production conversion behavior unchanged.

## What Changed

- Added additional redacted BOC OCR fixtures:
  - `boc_scanned_sample_03_redacted.txt`
  - `boc_scanned_sample_04_redacted.txt`
  - `boc_scanned_sample_05_redacted.txt`
- Added BOC OCR parser calibration regression tests.
- Improved BOC OCR fallback parsing for OCR noise around spaced amount separators such as `1, 000.00`.
- Added B/F wording coverage for common opening balance labels such as `BALANCE B/F` and `OPENING BALANCE`.
- Preserved parser diagnostics with parsed rows, skipped lines, warnings, and skip reasons.

## Behavior Preserved

- OCR remains opt-in.
- Text-layer PDFs continue to use existing parsers.
- BOC OCR fallback trigger remains limited to no-account-rows failures.
- Generated diagnostic outputs remain ignored.
- Redacted fixtures remain tracked.
- Excel output columns remain unchanged.

## Not Included In V.20.4

- Full BOC OCR parser rewrite
- Changes to the text-layer BOC parser
- OCR parsers for HSBC / DBS / ICBC / OCBC / NCB
- GUI
- OCR enabled by default
- Changes to `_accounting_engine/`
- Real PDF, Excel, OCR_WORK, generated output, or sensitive-data fixtures
