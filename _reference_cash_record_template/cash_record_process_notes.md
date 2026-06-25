# Cash Record Template Process Notes

Source template:
`002-Template-Cash record-dd.mm.yy.xls`

Converted analysis file:
`002-Template-Cash record-dd.mm.yy.converted.xlsx`

## Purpose

This workbook is the expected template for non-bank cash and credit-card movement records.

It should be parsed into the same normalized journal-line model as Bank record:

- Date
- Reference
- Account ID
- Account Description
- Description
- Debit
- Credit
- Source row / source sheet

## Workbook Structure

Observed sheets:

- `Cash`
- `Credit Card`
- `Chart of Accounts`

`Chart of Accounts` maps account descriptions to account IDs.

## Cash Sheet

Important metadata:

- `C1`: company name
- `C2`: period
- `A3`: record type, e.g. `Cash record`
- `C4`: COA account name, e.g. `Director's C/A`
- `C5`: reference name, e.g. `Cash`

Important rows:

- Row 9: classification/account headers
- Row 10: transaction entry headers
- Row 11: opening row
- Row 12 onward: transaction rows

Core columns:

- `A`: No.
- `B`: Date
- `C`: Nature
- `D`: Payer / (Payee)
- `E`: Invoice no. (Cheque no.)
- `F`: Details
- `G`: Cash in
- `H`: Cash out
- `I`: Balance
- `K`: Control

The account classification columns start from the right side of the transaction table, including examples such as:

- Interbank
- Computer equipment
- Fixture & furniture
- Director's C/A
- Trade receivable
- Trade payable
- Accruals
- Sales
- Purchases
- Advertisement
- Bank charges
- Legal and professional fee
- Local travelling

The sheet also includes Peachtree/import helper columns near the right side:

- Date
- Reference
- G/L Account
- G/L Account
- Description
- Cash/Card amount
- Nature amount

## Credit Card Sheet

The `Credit Card` sheet follows the same logic as `Cash`, but uses card account metadata:

- `C3`: credit card record label
- `C4`: card COA account name, e.g. `HSBC HKD Credit Card`
- `C5`: reference name, e.g. `CrCard:001`

Core transaction columns:

- `I`: Cash in / card in equivalent
- `J`: Cash out / card out equivalent
- `K`: Balance
- `M`: Control

This should be parsed as a liability/credit-card account movement, but the double-entry mechanics are the same:

- Positive record amount increases the record account.
- Negative record amount decreases the record account.
- The nature side is the opposite amount.

## Opening Rows

Rows where `Nature` is `Cash opening` should not generate current-period transaction journal lines.

Opening values should come from the confirmed opening-balance stage instead.

## Double Entry Rule

For each valid transaction row:

1. Record account side uses the COA account named in `C4`.
2. Nature side uses the account named in `Nature`.
3. Amount is `Cash in + Cash out` or equivalent helper amount.
4. The two journal lines must net to zero.

Example:

- Cash sale with `Cash in = 1,000`
  - Dr Cash / record account
  - Cr Sales

- Cash expense with `Cash out = -500`
  - Dr Expense account
  - Cr Cash / record account

## Parsing Preference

Use helper columns when present and populated because they normalize:

- Reference
- G/L account codes
- Description
- Record amount
- Nature amount

If helper columns are unavailable, derive equivalent values from:

- Record account name in `C4`
- Reference name in `C5`
- Transaction no. in `A`
- Nature in `C`
- Cash/card in/out columns
- Chart of Accounts

## Validation Rules

Minimum validations:

- Every Nature account must exist in `Chart of Accounts`.
- Record account from `C4` must exist in `Chart of Accounts`.
- Each transaction reference must balance to zero.
- Control column should be zero for completed rows.
- Opening row must be excluded from current-period movements.
- Hidden or unused sheets should be skipped.

## Integration Position

Cash record should join the same Stage 2 source layer as Bank record:

1. Bank record journals
2. Cash record journals
3. Generated Manual Journals workbook for user input
4. COA reconciliation output

Stage 3 should combine:

- confirmed opening balances
- bank journal lines
- cash journal lines
- completed manual journal lines

