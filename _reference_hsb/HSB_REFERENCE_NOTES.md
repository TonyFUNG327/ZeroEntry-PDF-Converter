# HSB PDF Converter Reference Notes

Purpose: record the current Hang Seng Bank (HSB) PDF-to-Excel conversion logic so future bank parsers, such as HSBC, can reuse the same production pattern.

## Source Materials

- Original portable package: `portable_hsb_converter.zip`
- Sample PDF copied for analysis: `HSB 2502.pdf`
- Sample expected Excel screenshot copied for analysis: `sample_output.png`
- Verified generated workbook: `generated_output/HSB 2502.xlsx`

## Portable Package Layout

```text
portable_hsb_converter/
  convert_hsb_pdf.py
  hsb_pdf_converter.py
  requirements.txt
  run_converter.bat
  BB/   input PDFs
  BB2/  output Excel files
```

The portable workflow is:

1. User puts PDF statements into `BB`.
2. User double-clicks `run_converter.bat`.
3. Batch script installs `pdfplumber` and `openpyxl` from `requirements.txt`.
4. `convert_hsb_pdf.py` calls `hsb_pdf_converter.main()`.
5. Excel files are generated into `BB2`.

## Current HSB Output Contract

Each bank account becomes one Excel sheet. Current verified sheet names:

- `Hang Seng Savings Account`
- `Hang Seng Current Account`

Each sheet uses the same seven columns:

```text
Bank_Account, Date, Description, Deposit, Withdrawal, Balance, Control
```

Important formatting behavior:

- `Date` is a typed Excel date, displayed as `dd mmm yyyy`.
- `Deposit` and `Withdrawal` use accounting-style dash for zero and parentheses for negative values.
- `Balance` and `Control` use number formatting with parentheses for negative values.
- `Control` column is grey-filled and bold.
- Top row is frozen at `A2`.

## HSB Parsing Logic

The converter is coordinate-based, not OCR-based.

Core dependency:

- `pdfplumber` extracts words with `x0`, `x1`, and `top` coordinates.

Main steps:

1. `words_to_lines()` groups extracted words into rows by similar `top` coordinate.
2. Header/footer noise is filtered by vertical coordinate, keeping only words with `120 <= top <= 785`.
3. Account section detection:
   - Exact line `HKD Statement Savings` selects `Hang Seng Savings Account`.
   - Exact line `Current` selects `Hang Seng Current Account`.
4. Transaction table starts when a line begins with `Date Transaction Details`.
5. Transaction table stops on `Transaction Summary` or `Credit Interest Accrued`.
6. Statement date is read from `Statement Date`, then used to infer year for transaction dates.
7. Transaction date is detected from words around x-coordinate `55 <= x0 <= 90`.
8. Description words are taken from `94 <= x0 <= 295`.
9. Amount classification is based on amount word coordinates:
   - `Deposit`: amount word has `320 <= x1 <= 379`
   - `Withdrawal`: amount word has `395 <= x1 <= 456`
   - `Balance`: amount word has `x0 >= 470`
10. If balance has a trailing `DR` around the balance column, balance is forced negative.
11. Description continuation lines without amounts are buffered and prepended to the next transaction line.

## Control Logic

The in-memory extractor calculates Control for validation:

- If a row has no deposit/withdrawal but has balance, Control becomes that balance.
- Otherwise Control equals previous Control plus Deposit minus Withdrawal.

The Excel writer also writes formulas into the `Control` column:

- First data row:
  `=IF(AND(D2="",E2=""),F2,IF(D2="",0,D2)-IF(E2="",0,E2))`
- Later rows:
  `=IF(AND(Dn="",En=""),Fn,G(n-1)+IF(Dn="",0,Dn)-IF(En="",0,En))`

Validation flags any row where a PDF balance exists but differs from calculated Control by more than 0.01.

## Verification Result For `HSB 2502.pdf`

The copied sample PDF was converted successfully.

Generated workbook:

```text
_reference_hsb/generated_output/HSB 2502.xlsx
```

Validation summary:

```text
Hang Seng Savings Account:
  rows=56
  deposit=1,607,876.06
  withdrawal=1,631,047.29
  final_balance=3,189.51
  final_control=3,189.51
  balance_mismatches=0

Hang Seng Current Account:
  rows=109
  deposit=1,586,003.24
  withdrawal=1,658,086.66
  final_balance=-72,398.12
  final_control=-72,398.12
  balance_mismatches=0
```

This matches the screenshot pattern: HSB current account starts with `B/F BALANCE`, then transactions like `UOD`, `CHEQUE`, `CASH WITHDRAWAL`, and transfer descriptions, with Control reconciling each available balance row.

## Expansion Guidance For HSBC And Other Banks

Keep the stable output contract and split only the bank-specific parsing layer.

Recommended future structure:

```text
converter/
  main.py
  writer.py
  validators.py
  parsers/
    base.py
    hang_seng.py
    hsbc.py
```

Suggested parser interface:

```python
class BankParser:
    bank_code: str

    def can_parse(self, pdf_path) -> bool:
        ...

    def extract(self, pdf_path) -> dict[str, list[dict]]:
        ...
```

Reusable shared modules:

- PDF page/word extraction
- Date normalization
- Amount parsing
- Workbook writing
- Control formula generation
- Balance-vs-Control validation report
- Batch input/output folder handling

Bank-specific modules should own:

- Bank/account section detection
- Table start/end markers
- Column coordinate rules
- Multi-line description rules
- Debit/credit sign rules
- Statement date/year inference rules

For HSBC support, first collect 2-3 sample PDFs and expected Excel outputs, then inspect:

- Whether text extraction is word-coordinate stable with `pdfplumber`.
- Account name markers and statement date markers.
- Transaction table header labels.
- X-coordinate ranges for date, description, deposits, withdrawals, balances.
- Whether debit balances use `DR`, negative signs, parentheses, or separate debit/credit columns.

## Risks To Watch

- Current HSB parser depends on fixed x-coordinate ranges, so a different PDF layout or zoom/template can break extraction.
- `Current` is a broad account marker and may be too loose if other page text includes a standalone `Current`.
- The script installs dependencies every run in `run_converter.bat`, which is convenient but slower and internet-dependent on first setup.
- `run_converter.bat` expects `python` to be available in PATH on the target computer.
- There is currently no automatic bank detection beyond the HSB parser.

