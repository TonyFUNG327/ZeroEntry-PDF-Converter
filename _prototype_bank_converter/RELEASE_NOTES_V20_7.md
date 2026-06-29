# ZeroEntry PDF Converter V.20.7 BOC OCR Line Merge Guard Hardening

## Positioning

V.20.7 hardens BOC OCR line merging so random OCR noise is less likely to be folded into transaction descriptions.

This release only affects the experimental BOC OCR fallback parser line preparation and diagnostics. It does not change the text-layer BOC parser or production conversion workflow.

## What Changed

- Added redacted guard fixtures:
  - `boc_scanned_sample_11_redacted.txt`
  - `boc_scanned_sample_12_redacted.txt`
- Tightened description continuation detection with an allowlist of transaction-like terms.
- Prevented random OCR noise from being merged between a date line and an amount line.
- Added `merge_type` to merged line diagnostics:
  - `one_line_continuation`
  - `two_line_continuation`
- Added blocked merge diagnostics:
  - `blocked_merge_count`
  - `blocked_merges`
  - stable blocked reasons such as `metadata_line_blocked`, `description_continuation_not_recognized`, `next_line_is_new_date`, and `missing_amount_continuation`
- Added regression tests for random noise guards, metadata guards, legitimate continuation merging, and diagnostic JSON payloads.

## Behavior Preserved

- OCR remains opt-in.
- Text-layer PDFs continue to use existing parsers.
- BOC OCR fallback trigger remains limited to no-account-rows failures.
- Generated diagnostic outputs remain ignored.
- Redacted fixtures remain tracked.
- Excel output columns remain unchanged.

## Not Included In V.20.7

- Full BOC OCR parser rewrite
- Changes to the text-layer BOC parser
- OCR parsers for HSBC / DBS / ICBC / OCBC / NCB
- GUI
- OCR enabled by default
- Changes to `_accounting_engine/`
- Real PDF, Excel, OCR_WORK, generated output, or sensitive-data fixtures
