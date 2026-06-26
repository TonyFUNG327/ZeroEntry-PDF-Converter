# ZeroEntry PDF Converter V.17 OCR Experimental Release Notes

## Positioning

V.17 is an OCR Experimental release. It adds an opt-in OCR layer for image-only scanned PDFs while preserving V.16 behavior for normal text-layer PDFs.

V.17 does not promise that every scanned bank statement can be converted. Its purpose is to establish a controlled OCR pipeline with dependency detection, OCR preprocessing, bank redetection, and a quality gate.

## V.16 Behavior Preserved

- Text-layer PDFs continue to use the existing parser registry and bank parsers.
- `python convert_bank_pdf.py` remains unchanged.
- `python convert_bank_pdf.py BB -o BB2` remains unchanged.
- Image-only scanned PDFs still fail with `SCANNED_IMAGE_ONLY` when `--ocr` is not supplied.
- `BB/`, `BB2/`, and `BB3/` workflow remains unchanged.
- Excel columns remain:
  `Bank_Account, Date, Description, Deposit, Withdrawal, Balance, Control`

## How To Use OCR

OCR mode is opt-in:

```bat
python convert_bank_pdf.py --ocr
python convert_bank_pdf.py BB -o BB2 --ocr
```

Behavior:

- Text-layer PDF + no `--ocr`: normal V.16 conversion.
- Text-layer PDF + `--ocr`: normal conversion; OCR is not used.
- Image-only scanned PDF + no `--ocr`: V.16 scanned-PDF error.
- Image-only scanned PDF + `--ocr`: OCR preprocessor runs first, then bank detection and parser dispatch are attempted.

## OCR Dependencies

V.17 uses an external command-line OCR backend. The primary backend is:

- OCRmyPDF
- Tesseract OCR language packs

If OCRmyPDF or its Tesseract backend is not installed, the converter reports an OCR dependency error and does not crash.

The general `requirements.txt` is unchanged. OCR dependencies are documented separately in `requirements-ocr.txt` so normal text-layer PDF users are not forced to install OCR tools.

## OCR Working Folder

OCR intermediate files are written to:

```text
OCR_WORK/
```

Typical files:

- `original_file.ocr.pdf`
- `original_file.ocr.txt`
- `original_file.ocr.log`

`OCR_WORK/` is ignored by git.

## OCR Quality Gate

Before conversion continues, OCR output must pass quality checks:

- text length is sufficient
- supported bank can be detected from OCR text
- enough date patterns are present
- enough amount patterns are present
- optional OCR confidence can be checked when available

If the quality gate fails, conversion stops with `OCR_QUALITY` and no unreliable Excel is produced.

## Known Limitations

- OCR accuracy depends on scan quality, skew, noise, and language packs.
- Coordinate-based parsers may still fail after OCR even when text is extracted.
- Not all scanned bank statements are supported.
- OCRmyPDF/Tesseract installation differs by machine and is not bundled.
- V.17 quality thresholds are conservative and may need calibration with real scanned samples.

## Not Included In V.17

- Full production OCR guarantee
- GUI
- All-bank scanned PDF guarantee
- Major parser rewrite
- OCR enabled by default
