# ZeroEntry PDF Converter V.16 Release Notes

## Positioning

V.16 is a stabilization release for the portable PDF converter. It keeps the V.15 conversion workflow and supported parser behavior while preparing the codebase for safer maintenance.

## What Changed

- Added a parser registry layer in `core/bank_registry.py`.
- Moved shared path defaults into `core/paths.py`.
- Added small common helpers in `core/common.py`.
- Added report/validation helpers in `core/validation.py`.
- Refactored `convert_bank_pdf.py` to use the registry while preserving the same CLI.
- Improved error messages for unsupported PDFs, unrecognized bank statements, image-only scanned PDFs, and parser failures.
- Improved `.gitignore` rules to reduce accidental commits of PDFs, Excel outputs, release ZIPs, generated reports, and preview files.
- Added basic smoke/regression tests under `tests/`.

## V.15 Compatibility Kept

- `BB/` remains the PDF input folder.
- `BB2/` remains the converted Excel output folder.
- `BB3/` remains the combined Excel output folder.
- `run_converter.bat` remains the double-click converter entrypoint.
- `run_combine.bat` remains the double-click combine entrypoint.
- The Excel output columns remain:
  `Bank_Account, Date, Description, Deposit, Withdrawal, Balance, Control`
- Existing parser modules are preserved and still expose:
  `extract_pdf(pdf_path)`, `validate_accounts(accounts)`, `write_workbook(accounts, output_path)`.

## Supported Bank Layouts

- Hang Seng Bank / HSB statement layout
- HSBC Business Direct HKD Current and HKD Savings layouts
- HSBC Sprint Account HKD Current and HKD Savings layouts
- HSBC Business Direct Foreign Currency Savings layouts
- Bank of China (Hong Kong) / BOC HKD Savings and HKD Current layouts
- DBS Bank (Hong Kong) Current Account layout
- DBS Multi-currency Savings Account layout
- ICBC Asia HKD / USD / CNY Current Account layout
- Bank of Communications consolidated statement layout
- OCBC Business Account / Integrated Account Statement Savings layouts
- Nanyang Commercial Bank / NCB HKD Current Account layout
- NCB Consolidated Statement layout

## How To Use

1. Put PDF files into `BB/`.
2. Run `run_converter.bat`.
3. Converted Excel files are generated in `BB2/`.
4. Run `run_combine.bat` after monthly conversions.
5. Combined workbook and control report are generated in `BB3/`.

CLI usage is unchanged:

```bat
python convert_bank_pdf.py
python convert_bank_pdf.py BB -o BB2
python combine_bank_excels.py BB2 -o BB3
```

## Known Limitations

- Parser logic is coordinate/layout based.
- Image-only scanned PDFs require OCR before conversion.
- New PDF layouts require calibration with sample PDFs.

## Not Included In V.16

- OCR pipeline
- GUI
- Large-scale new bank expansion
- Major Excel column or formatting redesign
