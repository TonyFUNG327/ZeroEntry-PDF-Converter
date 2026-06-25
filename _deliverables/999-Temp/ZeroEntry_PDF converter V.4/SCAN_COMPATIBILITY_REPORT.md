# BOC Scanned PDF Compatibility Report

Sample:

```text
BOC Bs-2411.pdf
```

## Result

This PDF is an image-only scanned statement.

`pdfplumber` inspection:

```text
pages=3
page=1 text_length=0 words=0 images=1
page=2 text_length=0 words=0 images=1
page=3 text_length=0 words=0 images=1
```

The current portable converter depends on selectable PDF text with word coordinates. It cannot directly parse this file.

## Stress Test Outcome

The converter was updated to detect image-only scanned PDFs and report a clear error:

```text
Image-only scanned PDF detected. This portable version requires a selectable text layer; run OCR first or use a future OCR-enabled converter.
```

Regression test with the scanned PDF placed alongside supported samples:

- `BOC 2505.pdf`: converted successfully, Balance/Control mismatch = 0
- `HSB 2502.pdf`: converted successfully, Balance/Control mismatch = 0
- `hsbc 04-2025 STATEMENT.pdf`: converted successfully, Balance/Control mismatch = 0
- `hsbc_Apr2025.pdf`: converted successfully, Balance/Control mismatch = 0
- `BOC Bs-2411.pdf`: correctly rejected as image-only scanned PDF

## OCR Probe

Rendered page previews are available in:

```text
_reference_boc_scan/rendered/
```

The scan is upright and visually readable, but there is no local production-ready OCR stack available in the current portable converter:

- System `tesseract`: not available
- Python OCR packages (`pytesseract`, `easyocr`, `paddleocr`, `ocrmypdf`, `cv2`): not available
- Bundled `tesseract.js`: present, but no local traineddata language files were found and direct dependency execution was not reliable enough for portable release

## Recommended Next Step

To support scanned statements reliably, add a separate OCR preprocessing stage:

1. Render each scanned PDF page to high-resolution PNG.
2. OCR with Traditional Chinese + English + digits.
3. Produce a searchable PDF or structured OCR word coordinates.
4. Feed the OCR result into a BOC scanned-layout parser.
5. Validate using Balance/Control and statement totals.

Until that stage is implemented, scanned PDFs should be OCR-processed before using this converter.
