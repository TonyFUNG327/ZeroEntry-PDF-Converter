# Accounting AI Engine System V.2 - Offline Test Guide

## 1. Quick Start

1. Unzip the package.
2. Put source Excel workbooks into `BB`.
3. Double-click `run_executive.bat`.
4. Check `review_outputs` first.
5. If Stage 2 review outputs are correct, double-click `run_combine.bat` to rebuild Stage 3 only.
6. Check `final_outputs\full_period_tb_gl_bs_is.xlsx`.
7. If the run fails, open the latest file in `logs`.

The current prototype follows the ZeroEntry_PDF converter V.14 folder-based style. No GUI upload entry is required.

## 2. Folder Structure

- `BB`: source files from user.
- `payloads`: generated JSON payloads.
- `review_outputs`: intermediate review Excel workbooks.
- `final_outputs`: final TB, GL, BS, and IS workbook.
- `logs`: run logs.
- `_accounting_engine`: parser, combiner, and Excel builders.

## 2A. Launchers

- `run_executive.bat`: full workflow launcher. It parses source files, builds review outputs, and also produces the final workbook.
- `run_combine.bat`: Stage 3 only. Use this after manual review confirms Stage 2 outputs are correct. It does not re-parse Bank, Cash, or Manual Journals files; it only reads existing JSON payloads in `payloads`.

## 3. File Auto-Detection

The launcher auto-detects files in `BB` by filename keywords:

- Opening TB: `opening`, `trial`, or `tb`
- Bank record: `bank`
- Cash record: `cash`
- Manual Journals: `manual`, `journal`, `accrual`, or `ar...ap`
- Sample report: `sample`, `tb...gl`, `tb...bs`, `tb...pl`, or `tb...is`

Recommended filenames:

- `999-I026-Trial Balance 31.12.2024.xlsx`
- `001-I026-Bank record-31.12.25.xlsx`
- `002-I026-Cash record-31.12.25.xlsx`
- `003-I026-Manual Journals-31.12.25.xlsx`
- `999-I026-TB, GL, BS, IS-31.12.25.xlsx`

If the Opening TB filename contains a date such as `31.12.2024`, the launcher uses it as the closing date and sets the opening date to the next day. If no date is detected, it defaults to closing date `2024-12-31` and opening date `2025-01-01`.

## 4. What run_executive Does

The launcher performs these steps when matching files exist:

1. Converts `.xls` files to `.xlsx` using local Excel COM.
2. Parses Opening TB into `payloads\opening_payload.json`.
3. Builds `review_outputs\opening_balance_review.xlsx`.
4. Parses Bank record into `payloads\bank_payload.json`.
5. Builds `review_outputs\bank_journal_lines.xlsx`.
6. Parses Cash record into `payloads\cash_payload.json`.
7. Builds `review_outputs\cash_journal_lines.xlsx`.
8. Parses optional Manual Journals into `payloads\manual_payload.json`.
9. Builds `review_outputs\manual_journals_review.xlsx`.
10. Combines available payloads into `payloads\full_period_payload.json`.
11. Builds `final_outputs\full_period_tb_gl_bs_is.xlsx`.

Opening TB is required for the final combination. At least one current-period source is required: Bank, Cash, or Manual Journals.

## 4A. What run_combine Does

Use `run_combine.bat` after reviewing:

- `review_outputs\opening_balance_review.xlsx`
- `review_outputs\bank_journal_lines.xlsx`
- `review_outputs\cash_journal_lines.xlsx`
- `review_outputs\manual_journals_review.xlsx`

The combine-only launcher reads:

- `payloads\opening_payload.json`
- `payloads\bank_payload.json`, if present
- `payloads\cash_payload.json`, if present
- `payloads\manual_payload.json`, if present

Then it generates:

- `payloads\full_period_payload.json`
- `final_outputs\full_period_tb_gl_bs_is.xlsx`

It is safe to run `run_combine.bat` repeatedly after adjusting payloads or adding an optional Manual Journals payload.

## 5. Advanced Run

Run with explicit dates:

```powershell
.\run_executive.ps1 -ClosingDate "2024-12-31" -OpeningDate "2025-01-01"
```

Run combine-only with a custom output filename:

```powershell
.\run_combine.ps1 -OutputName "full_period_tb_gl_bs_is_review2.xlsx"
```

Run with explicit file paths:

```powershell
.\run_executive.ps1 `
  -OpeningFile "BB\999-I026-Trial Balance 31.12.2024.xlsx" `
  -BankFile "BB\001-I026-Bank record-31.12.25.xlsx" `
  -CashFile "BB\002-I026-Cash record-31.12.25.xlsx" `
  -SampleReport "BB\999-I026-TB, GL, BS, IS-31.12.25.xlsx" `
  -ClosingDate "2024-12-31" `
  -OpeningDate "2025-01-01"
```

## 6. Current Limitations

- COA reconciliation currently outputs JSON only; workbook output is still pending.
- Manual Journals generated template parser is not yet fully separated from the older AR/AP/Accruals parser.
- Mixed-company smoke tests confirm interface compatibility only, not accounting correctness.
