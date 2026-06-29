# ZeroEntry Accounting Classification Module A.1

This module provides a first-pass, rule-based classifier for merged bank transaction workbooks created by ZeroEntry PDF Converter, usually from the converter `BB3` combined workbook.

It is intentionally isolated from PDF parsing, OCR parsing, formal double-entry posting, tax decisioning, and AI auto-classification.

## Input

The input workbook or CSV must contain these ZeroEntry bank columns:

- `Bank_Account`
- `Date`
- `Description`
- `Deposit`
- `Withdrawal`
- `Balance`
- `Control`

## Output

The CLI writes:

- classified Excel workbook
- unclassified review workbook
- summary JSON
- summary text report

Classification columns appended to each row:

- `Direction`
- `Amount`
- `Category`
- `Account_Code`
- `Account_Name`
- `Tax_Type`
- `Counterparty`
- `Confidence`
- `Rule_ID`
- `Review_Needed`
- `Classification_Source`
- `Notes`

## Rules CSV

Rules live in `rules/classification_rules.csv` and use these columns:

```text
rule_id,priority,enabled,match_type,keyword,direction,amount_min,amount_max,category,account_code,account_name,tax_type,counterparty,confidence,review_needed,notes
```

A.1 supports:

- `match_type`: `contains`
- `direction`: `Deposit`, `Withdrawal`, or `Any`
- `enabled`: `Yes` or `No`
- lower numeric `priority` runs first
- optional `amount_min` and `amount_max`

The bundled rules are synthetic examples only: `BANK_CHARGE`, `RENT_PAYMENT`, `CUSTOMER_RECEIPT`, `TRANSFER`, and `INTEREST`.

## CLI

From the repository root:

```powershell
python _accounting_classifier\classify_bank_transactions.py "path\to\combined.xlsx" --rules _accounting_classifier\rules\classification_rules.csv --output "path\to\classified.xlsx"
```

From this folder:

```powershell
python classify_bank_transactions.py input.xlsx --rules rules\classification_rules.csv --output classified.xlsx
```

Defaults derived from `--output`:

- `classified.summary.json`
- `classified.summary.txt`
- `classified_unclassified.xlsx`

## A.1 Non-Goals

- No OpenAI API or other AI API calls
- No fully automated accounting guarantee
- No formal journal entries
- No final tax advice
- No PDF converter or OCR parser changes
- No real bank data fixtures

## Tests

Run from this folder:

```powershell
python -m unittest discover tests
```

The tests use synthetic data only.
