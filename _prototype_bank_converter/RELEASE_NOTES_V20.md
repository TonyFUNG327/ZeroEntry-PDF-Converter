# ZeroEntry PDF Converter V.20 OCR Calibration Workflow Release Notes

## Positioning

V.20 introduces an OCR Calibration Workflow for BOC scanned statement output. It builds on V.18 OCR diagnostics and V.19.1 fallback hardening by adding redacted OCR text fixtures, calibration summaries, and fixture-driven regression tests.

V.20 is not a production OCR guarantee. It is a repeatable workflow for turning real-world OCR observations into safe, redacted test fixtures before parser calibration.

## V.19.1 Behavior Preserved

- OCR remains opt-in with `--ocr`.
- BOC OCR fallback still runs only for no-account-rows parser failures.
- `NoAccountRowsError` fallback behavior and backward-compatible string detection remain unchanged.
- `BB/`, `BB2/`, `BB3/`, and `OCR_WORK/` workflow remains unchanged.
- Excel columns remain:
  `Bank_Account, Date, Description, Deposit, Withdrawal, Balance, Control`

## What Changed In V.20

- Added redacted synthetic BOC OCR text fixtures under:
  `tests/fixtures/ocr_boc/`
- Added `build_calibration_summary(report)` in `ocr/ocr_diagnostics.py`.
- Added `calibrate_ocr_output.py` for parser calibration from OCR text or searchable PDF output.
- Added calibration tests for:
  - redacted fixture parsing
  - parsed rows / skipped lines / warnings
  - skip reason counts
  - parse success ratio
  - zero-candidate-count safety

## Usage

Run calibration on redacted OCR text:

```bat
python calibrate_ocr_output.py "tests\fixtures\ocr_boc\boc_scanned_sample_01_redacted.txt" --parser BOC
```

The calibration helper writes:

- `.diagnostic.txt`
- `.diagnostic.json`
- `.calibration_summary.json`

The calibration summary includes:

- candidate transaction line count
- parsed transaction row count
- skipped candidate line count
- warning count
- skipped line reason counts
- parse success ratio

## V.20.1 Calibration Output Safety

- Generated calibration outputs such as `.diagnostic.txt`, `.diagnostic.json`, and `.calibration_summary.json` should not be committed.
- The repository `.gitignore` excludes these generated calibration reports.
- Redacted OCR `.txt` fixtures under `tests/fixtures/ocr_boc/` remain intentionally tracked.

## Redaction Policy

Fixtures must remain synthetic or redacted. Do not commit:

- real scanned bank PDFs
- real Excel outputs
- `OCR_WORK/` files
- real customer names
- real full account numbers
- real addresses
- real transaction parties or sensitive financial data

Use placeholders such as:

- `CUSTOMER NAME: REDACTED CUSTOMER`
- `ACCOUNT NO. XXXXXXXX1234`
- `ADDRESS: REDACTED ADDRESS`
- synthetic amounts such as `100.00` and `1,000.00`

## Known Limitations

- BOC OCR fallback remains experimental.
- OCR accuracy depends on scan quality.
- Calibration fixtures are not a guarantee that all scanned BOC statements will convert.
- Coordinate-based text-layer parsers may still require separate layout calibration.

## Not Included In V.20

- All-bank OCR guarantee
- GUI
- OCR enabled by default
- Production-grade OCR guarantee
- Real scanned bank PDF fixtures
- Real customer data
- New OCR parsers for HSBC / DBS / ICBC / OCBC / NCB
