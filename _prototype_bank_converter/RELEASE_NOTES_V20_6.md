# ZeroEntry PDF Converter V.20.6 BOC OCR Diagnostics & Multi-line Continuation Guard

## Positioning

V.20.6 extends the BOC OCR line-merge calibration work with diagnostics and guarded multi-line continuation support.

This release only affects the experimental BOC OCR fallback parser diagnostics and line preparation. It does not change the text-layer BOC parser or production conversion workflow.

## What Changed

- Added redacted BOC OCR fixtures:
  - `boc_scanned_sample_09_redacted.txt`
  - `boc_scanned_sample_10_redacted.txt`
- Added `prepare_ocr_lines_with_diagnostics(text)`.
- Added line merge diagnostics:
  - raw line count
  - logical line count
  - merged line count
  - merged line samples with source lines
- Added guarded three-line continuation support:
  date line + description continuation + amount line.
- Added regression tests for merged logical lines, metadata guards, diagnostic rendering, and diagnostic JSON output.

## Behavior Preserved

- OCR remains opt-in.
- Text-layer PDFs continue to use existing parsers.
- BOC OCR fallback trigger remains limited to no-account-rows failures.
- Generated diagnostic outputs remain ignored.
- Redacted fixtures remain tracked.
- Excel output columns remain unchanged.

## Not Included In V.20.6

- Full BOC OCR parser rewrite
- Changes to the text-layer BOC parser
- OCR parsers for HSBC / DBS / ICBC / OCBC / NCB
- GUI
- OCR enabled by default
- Changes to `_accounting_engine/`
- Real PDF, Excel, OCR_WORK, generated output, or sensitive-data fixtures
