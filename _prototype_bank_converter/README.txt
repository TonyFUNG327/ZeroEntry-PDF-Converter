Hong Kong Bank PDF to Excel Converter Prototype
===============================================

Supported statement layouts in this prototype:
- Hang Seng Bank / HSB statement layout from the tested sample
- HSBC Business Direct HKD Current and HKD Savings layouts
- HSBC Sprint Account HKD Current and HKD Savings layouts
- HSBC Business Direct Foreign Currency Savings layouts, split into one sheet per currency
- Bank of China (Hong Kong) / BOC HKD Savings and HKD Current statement layout
- DBS Bank (Hong Kong) Current Account and Multi-currency Savings Account statement layouts
- ICBC Asia HKD/USD/CNY Current Account statement layout
- Bank of Communications consolidated statement HKD/USD Savings and HKD Current layouts
- OCBC Business Account / Integrated Account Statement Savings layouts, split into one sheet per currency
- Nanyang Commercial Bank / NCB HKD Current Account and Consolidated Statement layouts

How to use
----------
1. Put PDF files into the BB folder.
2. Double-click run_converter.bat.
3. Generated Excel files will appear in the BB2 folder.

How to combine monthly Excel files
----------------------------------
1. Convert monthly PDFs first, so monthly Excel files are in the BB2 folder.
2. Double-click run_combine.bat.
3. The combined Excel file and a combine control report will appear in the BB3 folder.
4. For each sheet/account, the combiner keeps the first month's B/F BALANCE row and skips later months' B/F BALANCE rows.
5. Before skipping a later B/F BALANCE row, the combiner checks that the previous month's ending balance matches the next month's B/F balance. If a mismatch is found, the combine process stops and reports the mismatch.

Release ZIP naming
------------------
Portable converter ZIP files use this naming format:
ZeroEntry_PDF converter V.19.1.zip

Output columns
--------------
Bank_Account, Date, Description, Deposit, Withdrawal, Balance, Control

Experimental OCR mode
---------------------
V.17 adds opt-in OCR support for image-only scanned PDFs. The default text-layer PDF workflow remains unchanged.

CLI examples:
python convert_bank_pdf.py --ocr
python convert_bank_pdf.py BB -o BB2 --ocr

OCR mode requires external OCR tools, such as OCRmyPDF with Tesseract OCR. If OCR tools are not installed, text-layer PDFs still work normally without --ocr, and scanned PDFs in --ocr mode will show an OCR dependency error.

OCR intermediate files are written to OCR_WORK and should not be committed.

OCR parser calibration
----------------------
V.18 adds OCR diagnostics and an experimental BOC OCR fallback parser for OCR output calibration.

Inspect OCR output:
python inspect_ocr_output.py "OCR_WORK\file.ocr.txt"
python inspect_ocr_output.py "OCR_WORK\file.ocr.pdf"

The BOC OCR fallback parser is used only in OCR mode when OCR quality passes, the detected bank is BOC, and the existing BOC parser returns no account rows.

OCR reliability patch
---------------------
V.19.1 refines the V.18 BOC OCR fallback flow. The fallback parser now runs only when the existing BOC parser specifically returns a no-account-rows error after OCR. Other parser failures are reported directly so validation, workbook writing, or layout problems are not hidden by fallback behavior.

BOC OCR fallback parser diagnostics now include candidate lines, parsed rows, skipped lines, skip reasons, and account-type warnings. Use the OCR inspector for calibration:
python inspect_ocr_output.py "OCR_WORK\file.ocr.txt"

Notes
-----
- The converter auto-detects HSBC vs HSB from the first pages of each PDF.
- BOC Chinese descriptions are preserved from the PDF text layer.
- DBS statements are exported into separate sheets by account/currency, such as DBS HKD Current Account and DBS USD MCY Savings.
- ICBC Asia statements are exported into separate sheets by currency, such as ICBC Asia HKD Current, ICBC Asia USD Current and ICBC Asia CNY Current.
- Bank of Communications statements are exported into separate account/currency sheets, such as COMM HKD Savings, COMM USD Savings and COMM HKD Current.
- OCBC integrated account statements are exported into separate sheets by currency, such as OCBC HKD Statement Savings, OCBC CNY Statement Savings and OCBC NOK Statement Savings.
- NCB account statements are exported into sheets such as NCB HKD Current Account.
- NCB consolidated statements are exported into separate sheets such as NCB HKD Savings Account, NCB HKD MCY Savings Account and NCB HKD Current Account.
- HSBC Foreign Currency Savings is exported into separate sheets such as:
  - HSBC USD Foreign Currency Savings
  - HSBC CNY Foreign Currency Savings
  - HSBC JPY Foreign Currency Savings
  - HSBC EUR Foreign Currency Savings
- The parser is coordinate-based, so new bank/PDF layouts should be calibrated with sample PDFs before production use.
- V.16 is a stabilization release that keeps the V.15 user workflow and parser behavior while adding a parser registry, clearer errors, safer repository hygiene, release notes, and smoke tests.
- V.17 is an OCR Experimental release. OCR is opt-in with --ocr and does not guarantee all scanned PDFs can be converted.
- V.18 is an OCR Parser Calibration release with OCR diagnostics and an experimental BOC OCR fallback parser.
- V.19.1 is an OCR Reliability Patch that narrows BOC fallback triggers and improves OCR parser diagnostics.
