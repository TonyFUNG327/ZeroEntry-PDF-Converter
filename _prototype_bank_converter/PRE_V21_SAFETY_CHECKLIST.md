# Pre-V21 Safety Checklist

Use this checklist before starting V.21 BOC OCR parser calibration.

## Behavior That Must Remain Stable

- OCR remains opt-in.
- Running without `--ocr` must not call OCR preprocessing.
- Text-layer PDFs continue to use existing parsers.
- Image-only scanned PDFs without `--ocr` still fail with the scanned PDF error.
- BOC OCR fallback only triggers on no-account-rows parser failure.
- Generated diagnostic outputs are ignored by `.gitignore`.
- Redacted OCR `.txt` fixtures remain tracked.
- No real PDF, Excel, OCR_WORK output, generated diagnostic output, or sensitive data is committed.

## V.21 Calibration Scope

- Add or update redacted BOC OCR text fixtures.
- Run `calibrate_ocr_output.py` to inspect skipped reasons and warning patterns.
- Calibrate the BOC OCR parser against observed OCR noise.
- Add a regression test for each parser behavior change.

## V.21 Non-Goals

- Do not add HSBC / DBS / ICBC / OCBC / NCB OCR parsers.
- Do not enable OCR by default.
- Do not rewrite the full BOC parser.
- Do not modify `_accounting_engine/`.
- Do not commit real PDFs.
- Do not commit real Excel outputs.
- Do not commit OCR_WORK outputs.
- Do not commit generated diagnostic outputs.
- Do not commit sensitive customer or bank data.

## Recommended V.21 Work Sequence

1. Add a redacted fixture.
2. Run the calibration helper.
3. Review skipped reasons and warnings.
4. Make the smallest parser calibration change.
5. Add or update regression tests.
6. Run full unittest.
7. Confirm `git status` has no generated outputs or sensitive files.
