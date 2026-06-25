# Accounting Engine Prototype

This folder contains the first prototype layer for converting classified accounting schedules into normalized double-entry journal lines.

## Folder-Based Flow

Current operation should follow the ZeroEntry_PDF converter V.14 style:

- Place user source files into the agreed input folder, such as `BB`.
- Run the parser for each file type to generate JSON payloads.
- Generate review Excel files for human checking.
- Pass approved payloads into `full_period_combiner.py` to generate TB, GL, BS, and IS payloads.

No GUI upload entry is required for this stage.

Current supported payload inputs:

- Opening balance payload
- Bank record payload
- Cash record payload
- Manual Journals payload

## Manual Journals Are Optional

Manual Journals schedules are not required input.

If a Manual Journals workbook is supplied, the parser imports supported schedules and generates normalized journal lines.

If no Manual Journals workbook is supplied, the parser returns an empty journal payload and the output workbook keeps a `Manual Entry` sheet for later user-entered JV lines.

This preserves both workflows:

- automated import from the AR/AP/Accruals schedule template
- later manual entry by the user when the schedule is not available

## Supported Schedule Sheets

Current parser support:

- `Trade Receivables`
- `Trade payables`
- `Accruals`

Current rules:

- Trade Receivables: Dr Trade receivable / Cr Nature account
- Trade payables: Dr Nature account / Cr Trade payable
- Accruals: Dr Nature account / Cr Accruals

The parser reads `Chart of Accounts` in the supplied workbook and resolves account names to account codes from that sheet.

## Commands

Parse a supplied Manual Journals workbook:

```powershell
& "C:\Users\Account\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" "_accounting_engine\manual_journals_parser.py" --manual-journals "_reference_manual_journals_p003\002a-P003-Testing Sample-31.3.26-Sch L_1-AR,AP, Accruals schedule-31.3.26.xlsx" --out-json "_reference_manual_journals_p003\p003_manual_journals_payload.json"
```

Parse with no Manual Journals workbook:

```powershell
& "C:\Users\Account\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" "_accounting_engine\manual_journals_parser.py" --out-json "_reference_manual_journals_p003\no_manual_journals_payload.json"
```

Build a review workbook from a parser payload:

```powershell
& "C:\Users\Account\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe" "_accounting_engine\build_manual_journals_output.mjs" --input-json "_reference_manual_journals_p003\p003_manual_journals_payload.json" --output-xlsx "_reference_manual_journals_p003\p003_manual_journals_output.xlsx" --preview-png "_reference_manual_journals_p003\p003_manual_journals_summary.png"
```

Parse a Cash record workbook:

```powershell
& "C:\Users\Account\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" "_accounting_engine\cash_record_parser.py" "_reference_cash_record_template\002-Template-Cash record-dd.mm.yy.converted.xlsx" --out-json "_reference_cash_record_template\cash_record_template_payload.json"
```

Build the Cash Journal Lines review workbook:

```powershell
& "C:\Users\Account\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe" "_accounting_engine\build_cash_record_output.mjs" --input-json "_reference_cash_record_template\cash_record_template_payload.json" --output-xlsx "_reference_cash_record_template\cash_record_journal_output.xlsx" --preview-png "_reference_cash_record_template\cash_record_journal_preview.png"
```

Combine opening balances with Bank, Cash, and Manual Journals payloads:

```powershell
& "C:\Users\Account\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" "_accounting_engine\full_period_combiner.py" --opening-json "_reference_opening_i026\i026_opening_balance_31_12_2024_payload.json" --bank-json "_reference_double_entry_i026\i026_bank_record_payload_clean.json" --cash-json "_reference_cash_record_template\cash_record_template_payload.json" --manual-json "_reference_manual_journals_p003\p003_manual_journals_payload.json" --out-json "_reference_cash_record_template\combined_bank_cash_manual_smoke_payload.json"
```

Add `--sample-report "path\to\TB_GL_BS_IS.xlsx"` only when a reference report exists and the run needs sample comparison.

## P003 Test Result

The P003 sample generated:

- 10 journal lines
- 3 journal references
- total debit: 840,313.00
- total credit: 840,313.00
- net check: 0.00

One incomplete `Trade Receivables` row was skipped with a warning rather than stopping the run.
