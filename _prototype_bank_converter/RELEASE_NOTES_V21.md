# ZeroEntry PDF Converter V.21

## BOC Real-Pattern Redacted OCR Fixture Calibration

V.21 is a small BOC OCR calibration hardening release. It uses real scanned BOC integrated statement layout patterns as reference, but only commits redacted synthetic OCR text fixtures.

## Added

- Added two redacted BOC real-pattern OCR fixtures under `tests/fixtures/ocr_boc/`.
- Added fixture coverage tests for redaction markers, parser diagnostics, batch calibration metrics, and OCR isolation.
- Added narrow BOC OCR parser calibration for scanned integrated statement wording:
  - Chinese brought-forward and closing-balance markers.
  - Common BOC OCR continuation tokens such as FPS, EXCH, GLOBAL, LIMITED, and CORPORATION.

## Behavior Preserved

- OCR remains opt-in.
- Text-layer PDFs continue to use existing parsers.
- Production conversion flow is unchanged.
- BB / BB2 / BB3 / OCR_WORK workflow is unchanged.
- Excel output columns remain unchanged.
- V20.9 batch fixture calibration remains available.
- Redacted fixtures remain tracked; generated OCR reports remain ignored.

## Not Included

- No new bank OCR parser.
- No GUI.
- No production OCR guarantee for all scanned statements.
- No broad rewrite of the BOC OCR parser.
- No changes to the original text-layer BOC parser.
- No changes to `_accounting_engine/`.
- No committed real PDF, Excel, OCR_WORK output, generated reports, or sensitive data.
