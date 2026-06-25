# H026 Process Upgrade Notes

## What H026 Adds Beyond S240

- The input workbook now includes a `Chart of Accounts` sheet. Account IDs should be read from this sheet instead of being hardcoded.
- Bank sheets have a richer structure:
  - rows 1-5: company, period, bank account, bank COA name, bank display name
  - row 9: main transaction headers, classification columns, and Peachtree import helper columns
  - row 10: subheaders for nature, payer/payee, invoice/cheque, details, and currency
  - data starts at row 11
- Classification headers are not fixed at row 7 as in S240. H026 uses row 9.
- The workbook has multiple bank accounts:
  - `HSBC HKD CA`
  - `HSBC HKD SA`
  - `HSBC USD SA`
- H026 includes foreign currency handling:
  - USD sheet stores original USD deposit/withdrawal/balance
  - HKD conversion columns are calculated using an exchange rate
  - accounting entries and financial statements use HKD values
- H026 has Peachtree import helper columns that already encode the double-entry logic:
  - `G/L Account (Bank)`
  - `G/L Account (Nature)`
  - `Bank (Amount$)`
  - `Nature (Amount$)`
  - `Reference`
  - `Number of Distributions`
  - `Description`
- Output reports include bank-generated entries plus separate manual JV entries.

## Revised Bank Record Parsing Rules

1. Detect bank-record sheets by finding `Bank record` / `Bank COA` / `Bank name` in the top rows.
2. Detect the transaction header row dynamically by locating `No.`, `Date`, `Particular`, `Deposit`, `Withdrawal`, `Balance`, and `Control`.
3. Identify the account name from `Bank COA` / `Bank COA (Peachtree)` cell value, then map it through `Chart of Accounts`.
4. Identify classification columns between `Control` and the Peachtree helper section.
5. Identify helper columns by exact labels:
   - `Reference`
   - `G/L Account (Bank)`
   - `G/L Account (Nature)`
   - `Description`
   - `Bank (Amount$)`
   - `Nature (Amount$)`
6. Generate entries only from transaction rows with a date and a nature/particular.
7. Treat rows without date but with totals as validation rows, not journal-entry rows.
8. Opening balance rows should create GL beginning balances, not current-year movement entries.
9. For each transaction row:
   - bank side uses `G/L Account (Bank)` and `Bank (Amount$)`
   - nature side uses `G/L Account (Nature)` and `Nature (Amount$)`
   - positive amount is debit; negative amount is credit
10. Validate every transaction row with:
    - `Control = HKD deposit/withdrawal total - classification total`
    - expected `Control = 0`

## Multi-Line and Multi-Distribution Logic

- Same `Reference` can appear on more than one row.
- Example: `HSBC HKD CA-2501-005` is split into:
  - Company secretarial fee
  - Business registration fee
- The journal should preserve the same reference and create all corresponding debit/credit lines.
- `Number of Distributions` is useful for Peachtree import style, but for GL/TB generation the core grouping key should be `Reference`.

## Interbank and FX Logic

- Interbank transfer uses account `1090 Interbank` as a clearing account.
- Example:
  - USD sheet withdrawal creates credit bank / debit interbank.
  - HKD sheet deposit creates debit bank / credit interbank.
- If HKD received differs from USD converted amount, the residual is classified to `Exchange losses/(gains), net` account `6580`.
- Interbank account should net to zero when the transfer pair is complete.

## Manual Journal Requirement

H026 cannot be fully reconstructed from bank records alone. The output GL includes manual year-end journals:

- `JV2512001`: provision of accounting and audit fee
  - Dr Accounting fee `4000`
  - Dr Auditor's remuneration `6200`
  - Cr Accruals `10200`
- `JV2512005`: tax payable adjustment
  - Dr Director's C/A `13377`
  - Cr Tax payable `13377`
  - Dr Tax payable `6000`
  - Cr Income tax expenses `6000`

Therefore the upgraded workflow needs a second input layer:

- `Bank/Cash Records`: source for bank/cash movements
- `Manual Journals`: source for accruals, tax, depreciation, closing adjustments, and other non-bank entries

## Output Report Rules

- GL remains account-centric:
  - one block per account
  - beginning balance
  - all movements
  - change row
  - ending balance row
- TB is derived from GL ending balances:
  - positive ending balance => Debit Amt
  - negative ending balance => Credit Amt as positive display amount
- BS is derived from TB/GL by account type and statement section.
- IS is derived from income and expense accounts:
  - income accounts display as positive revenue
  - ordinary expenses display as positive expenses
  - contra-expense or income-tax overprovision can display as negative expense
  - percentage columns use total revenue as denominator

## Implementation Upgrade

The next implementation should introduce these internal tables:

- `account_master`
  - account_id
  - account_name
  - account_type
  - statement
  - statement_section
  - normal_balance
  - display_order
- `source_transactions`
  - source_sheet
  - row_no
  - date
  - reference
  - description
  - original_currency
  - original_amount
  - hkd_amount
  - bank_account_id
  - nature_account_id
- `journal_lines`
  - date
  - reference
  - journal_type
  - description
  - account_id
  - debit
  - credit
  - source
- `manual_journals`
  - same structure as journal lines, entered separately from bank records

This will allow the program to generate TB, GL, BS, and IS consistently across S240-style simple records and H026-style advanced records.
