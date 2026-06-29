# ZeroEntry PDF Converter V.20.2 Parser Stability Guard & Calibration Output Convenience Patch

## Positioning

V.20.2 protects the existing V.16 parser stabilization behavior while keeping the V.20 OCR calibration workflow convenient and contained.

This is a stability and workflow patch. It does not add a new OCR parser and does not change production conversion behavior.

## V.16 Behavior Guarded

- The parser registry remains the default path for normal conversion.
- Running without `--ocr` does not call OCR preprocessing.
- Text-layer PDFs still use existing parsers even when `--ocr` is enabled.
- `BB/`, `BB2/`, and `BB3/` workflow remains unchanged.
- Excel columns remain unchanged:
  `Bank_Account, Date, Description, Deposit, Withdrawal, Balance, Control`

## V.20 / V.20.1 Behavior Preserved

- The OCR calibration workflow remains available.
- Generated calibration outputs remain ignored by `.gitignore`.
- Redacted OCR `.txt` fixtures remain intentionally tracked.
- OCR remains opt-in only.

## What Changed In V.20.2

- Added OCR isolation regression tests to ensure OCR preprocessing does not run for non-OCR conversion paths.
- Added BOC fallback trigger guard tests to ensure fallback runs only for no-account-rows failures.
- Added `calibrate_ocr_output.py --output-dir` so generated calibration reports can be written outside the fixture folder.

## Calibration Output Directory

Default behavior is unchanged:

```bat
python calibrate_ocr_output.py "tests\fixtures\ocr_boc\boc_scanned_sample_01_redacted.txt" --parser BOC
```

Outputs are written beside the input file.

Optional output directory:

```bat
python calibrate_ocr_output.py "tests\fixtures\ocr_boc\boc_scanned_sample_01_redacted.txt" --parser BOC --output-dir OCR_WORK\calibration
```

Output filenames keep the input basename:

- `boc_scanned_sample_01_redacted.txt.diagnostic.txt`
- `boc_scanned_sample_01_redacted.txt.diagnostic.json`
- `boc_scanned_sample_01_redacted.txt.calibration_summary.json`

## Not Included In V.20.2

- New bank OCR parsers
- GUI
- OCR enabled by default
- BOC parser rewrite
- Changes to `_accounting_engine/`
- Real PDF, Excel, OCR_WORK, diagnostic output, or sensitive-data fixtures
