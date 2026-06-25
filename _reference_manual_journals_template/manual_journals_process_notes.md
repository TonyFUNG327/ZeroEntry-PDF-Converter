# Manual Journals Template Process Notes

Source template:
`009-Template-AR,AP, Accruals schedule-dd.mm.yy.xlsx`

## Purpose

This workbook is the expected user input template for current-period manual schedules covering:

- Trade receivables
- Trade payables
- Accruals
- Salaries & MPF

The accounting engine should treat these schedules as a manual journal source layer, used together with the classified Bank/Cash record and any prior-year closing GL/TB/BS/PL values supplied for opening balances.

## Master Pg

`Master Pg` is the shared metadata source.

Important fields:

- `B1`: client name
- `B2`: year end / period label formula
- `B3`: file number
- `B5`: reporting currency
- `B7`: accounting period start
- `B8`: accounting period end
- `B9`: incorporation / cessation flag
- `B11`: job-in-charge

The parser should read these fields once and pass the metadata into generated journal descriptions, report labels, and output workbook naming where needed.

## Chart of Accounts

The `Chart of Accounts` sheet maps account names to account codes.

The parser should build a case-normalized account lookup from this sheet and use it for all manual journal schedules. Account names in schedule rows should not be hardcoded to account numbers if the workbook provides a chart.

Key accounts observed in the template include:

- Trade receivable: `1100`
- Prepayment: `1300`
- Trade payable: `2000`
- Trade deposit received: `2100`
- Accruals: `2200`
- Salaries: `7300`
- MPF: `6800`
- COS Salaries: `5500`
- COS MPF: `5600`
- Director's remuneration: `6450`

## Common Schedule Layout

`Trade Receivables`, `Trade payables`, and `Accruals` share a common table model.

Rows 1-5 link to `Master Pg`.

Row 6 contains group headers:

- `K: 1st s/s`
- `O: 2nd s/s`
- `W:AC`: Peachtree / accounting import helper columns

Row 7 contains the transaction headers:

- `A`: No.
- `B`: Ref. no.
- `C`: Date
- `D`: Nature
- `E`: Customer
- `F`: Invoices no.
- `G`: Details
- `I`: Amount
- `K`: Bank
- `L`: Date
- `M`: Amount
- `O`: Bank
- `P`: Date
- `Q`: Amount
- `S`: o/s bal.
- `W`: Date
- `X`: Reference
- `Y`: first G/L account
- `Z`: second G/L account
- `AA`: Description
- `AB`: first amount
- `AC`: second amount

Rows with a transaction date and amount are source rows. Totals and check rows should be excluded from journal generation.

## Settlement Columns

Settlement columns track cash settlement against the gross invoice/accrual amount:

- First settlement: bank/date/amount in `K:M`
- Second settlement: bank/date/amount in `O:Q`
- Outstanding balance: `S = I - M - Q`

Journal recognition should be based on the gross amount in column `I`, not only the outstanding balance. The outstanding balance is used for AR/AP/accrual closing validation, BS balance support, and reconciliation against bank settlement records.

## Trade Receivables Rule

Schedule account label in `B4`: `Trade receivable`

Reference prefix: `AR-`

Canonical double entry:

- Dr Trade receivable
- Cr Nature account

Helper columns:

- `Y`: G/L Account (AR)
- `Z`: G/L Account (Nature)
- `AB`: AR amount, positive
- `AC`: Nature amount, negative

Generated journal line example:

- Debit: account from `B4` / `Y`, amount = `I`
- Credit: account from `D` / `Z`, amount = `I`

## Trade Payables Rule

Schedule account label in `B4`: `Trade payable`

Reference prefix: `AP-`

Canonical double entry:

- Dr Nature account
- Cr Trade payable

Helper columns:

- `Y`: G/L Account (Nature)
- `Z`: G/L Account (AP)
- `AB`: Nature amount, positive
- `AC`: AP amount, negative

Generated journal line example:

- Debit: account from `D` / `Y`, amount = `I`
- Credit: account from `B4` / `Z`, amount = `I`

## Accruals Rule

Schedule account label in `B4`: `Accruals`

Reference prefix: `JV-`

Canonical double entry:

- Dr Nature account
- Cr Accruals

Helper columns:

- `Y`: G/L Account (Nature)
- `Z`: G/L Account (Accruals)
- `AB`: Nature amount, positive
- `AC`: Accruals amount, negative

Generated journal line example:

- Debit: account from `D` / `Y`, amount = `I`
- Credit: account from `B4` / `Z`, amount = `I`

## Helper Columns as Canonical Output

If helper columns `W:AC` contain formulas or values, the parser can use them as the canonical normalized journal representation.

If helper columns are blank or formulas are unavailable, generate equivalent fields from source columns:

- Date: source date in `C`
- Reference: schedule prefix + Ref. no. in `B`
- Account 1 / Account 2: account lookup against `Chart of Accounts`
- Description: `Nature:Customer - Invoice - Details`
- Amount 1 / Amount 2: equal and opposite signed values according to the schedule rule

Every generated journal reference must balance to zero.

## Receipt in Advance and Prepayment

Receipt in advance and Prepayment are usually recorded in the classified Bank/Cash record, not primarily through this Manual Journals template.

However, they often require JV settlement or reclassification, especially where opening balances exist. For companies with opening and closing values, the accounting engine should accept prior-year GL/TB/BS/PL closing values and use them to establish current-year opening balances.

Required future flow:

1. Import prior-year closing TB/GL when supplied.
2. Convert prior-year ending balances into current-year opening GL balances.
3. Record current-period bank/cash movements for receipt in advance and prepayment.
4. Record JV settlements/reclassifications where manual schedules or output reports require them.
5. Validate closing balances against generated TB/BS and supporting schedules.

## Salaries & MPF

`Salaries & MPF` is not the same row-level AR/AP/accrual table.

Observed sections include:

- Gross salaries
- Employee MPF portion
- Employer MPF portion
- Total MPF
- Net salaries by bank

This sheet should be parsed as a separate payroll schedule module. It can support salary expense, MPF expense/payable, director remuneration, and bank settlement reconciliation, but it should not be forced through the AR/AP/Accruals row model.

## Validation Rules

Minimum validations for this workbook:

- Account names used in `B4` and `D` must exist in `Chart of Accounts`.
- For generated helper rows, amount column 1 plus amount column 2 must equal zero.
- Outstanding balance should equal gross amount less listed settlement amounts.
- Total/check rows must not generate duplicate journal entries.
- Generated references should be unique within each schedule unless intentionally split.
- Manual journal totals should agree to the GL/TB movements after combining with Bank/Cash records and opening balances.

## Integration Position

The future accounting engine should combine sources in this order:

1. Prior-year closing values, if supplied, as opening balances.
2. Classified Bank/Cash records as cash/bank movement journals.
3. Manual Journals template schedules for AR/AP/Accruals and payroll-related journals.
4. Any explicit JV/reclassification schedules.
5. Generated GL by account.
6. Generated TB from GL closing balances.
7. Generated BS and PL/IS from account categories.

