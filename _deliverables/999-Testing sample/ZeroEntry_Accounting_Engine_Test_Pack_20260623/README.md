# ZeroEntry Accounting Engine Test Pack

This package contains the current prototype for testing the accounting workflow after the bank-record converter stage.

## Current Supported Flow

1. Prior-year Trial Balance to opening balances.
2. Classified Bank record to double-entry journal lines.
3. Opening balances + Bank journals to GL, TB, BS, and IS.
4. Comparison against a sample final workbook to confirm whether remaining differences are Manual Journals / JV only.

## Manual Journals Position

Manual Journals are not required as an uploaded input at this stage.

The intended next direction is:

- Stage 2 generates a standard Manual Journals Excel for user input.
- User fills required AR/AP/Accruals/JV data.
- Stage 3 imports that file together with Bank/Cash journals.

## Included I026 Test Outputs

- Opening balance review workbook.
- Clean Bank Journal Lines workbook.
- Full-period GL/TB/BS/IS workbook with GL running Balance column.
- JSON payloads used for verification.

## Known Scope

- Hidden sheets are excluded from Bank record parsing.
- Non-bank schedule sheets such as Finance costs are excluded from Bank record journals.
- Cash record parser is not yet added.
- Account mapping reconciliation should be added before broader rollout.

