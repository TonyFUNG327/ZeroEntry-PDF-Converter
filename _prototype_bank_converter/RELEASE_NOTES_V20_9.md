# ZeroEntry PDF Converter V.20.9 BOC OCR Calibration Baseline & Regression Thresholds

## Positioning

V.20.9 adds aggregate calibration totals and baseline regression thresholds for the redacted BOC OCR fixture set.

This release does not change the BOC OCR parser or production conversion behavior.

## What Changed

- Added aggregate totals to `calibrate_ocr_fixtures.py`.
- Added overall and average parse success ratios.
- Added lowest parse success fixture tracking.
- Added skip reason totals.
- Added merge and blocked merge totals.
- Added blocked merge reason totals.
- Added baseline regression tests for fixture coverage and parser calibration metrics.

## Baseline Threshold

The current early calibration baseline requires:

- `overall_parse_success_ratio >= 0.5`

This threshold is intentionally modest while the BOC OCR parser remains experimental and the fixture set includes difficult OCR-noise cases.

## Behavior Preserved

- OCR remains opt-in.
- Text-layer PDFs continue to use existing parsers.
- BOC OCR fallback trigger remains limited.
- Generated diagnostic outputs remain ignored.
- Redacted fixtures remain tracked.
- Excel output columns remain unchanged.

## Not Included In V.20.9

- Changes to the BOC OCR parser
- OCR parser for other banks
- GUI
- OCR enabled by default
- Full BOC parser rewrite
- Changes to the original text-layer BOC parser
- Changes to `_accounting_engine/`
- Real PDF, Excel, OCR_WORK, generated output, or sensitive-data fixtures
