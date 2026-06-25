# Accounting Engine Prototype

This folder contains the first prototype layer for converting classified accounting schedules into normalized double-entry journal lines.

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

## P003 Test Result

The P003 sample generated:

- 10 journal lines
- 3 journal references
- total debit: 840,313.00
- total credit: 840,313.00
- net check: 0.00

One incomplete `Trade Receivables` row was skipped with a warning rather than stopping the run.

