# ZeroEntry PDF Converter V.20.8 BOC OCR Calibration Metrics & Fixture Coverage Report

## Positioning

V.20.8 adds batch calibration metrics for the redacted BOC OCR fixture set. It helps quantify parser calibration coverage across fixtures without changing production conversion behavior.

## What Changed

- Added `calibrate_ocr_fixtures.py`.
- Added aggregate fixture metrics for all `*_redacted.txt` fixtures in a folder.
- Added merge and blocked-merge metrics to the aggregate summary.
- Added batch calibration tests.

## Aggregate Metrics

Each fixture summary includes:

- `fixture_name`
- `candidate_transaction_line_count`
- `parsed_transaction_row_count`
- `skipped_candidate_line_count`
- `parse_success_ratio`
- `warning_count`
- `skip_reason_counts`
- `merged_line_count`
- `blocked_merge_count`
- `merged_line_samples`
- `blocked_merge_reasons`

## Usage

```bat
python calibrate_ocr_fixtures.py tests\fixtures\ocr_boc --parser BOC --output-dir OCR_WORK\calibration
```

The helper writes:

- `boc_ocr_fixture_calibration_summary.json`

## Behavior Preserved

- OCR remains opt-in.
- Text-layer PDFs continue to use existing parsers.
- BOC OCR fallback trigger remains limited.
- Generated diagnostic outputs remain ignored.
- Redacted fixtures remain tracked.
- Excel output columns remain unchanged.

## Not Included In V.20.8

- OCR parser for other banks
- GUI
- OCR enabled by default
- Full BOC parser rewrite
- Changes to the original text-layer BOC parser
- Changes to `_accounting_engine/`
- Real PDF, Excel, OCR_WORK, generated output, or sensitive-data fixtures
