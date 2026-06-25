# HSBC PDF Converter Reference Notes

Purpose: record the HSBC Business Direct PDF-to-Excel parsing logic derived from `hsbc_Apr2025.pdf`.

## Source Materials

- Sample PDF copied for analysis: `hsbc_Apr2025.pdf`
- Coordinate dump: `layout_dump.txt`
- Generated workbook: `generated_output/hsbc_Apr2025.xlsx`

## Output Contract

The HSBC prototype keeps the same Excel columns as the Hang Seng converter:

```text
Bank_Account, Date, Description, Deposit, Withdrawal, Balance, Control
```

Each HKD account is written to a separate sheet:

- `HSBC HKD Current Account`
- `HSBC HKD Savings Account`

The Foreign Currency Savings section is deliberately ignored in this prototype because the current requested output structure has no currency column.

## HSBC Parsing Logic

The parser is coordinate-based using `pdfplumber`, matching the HSB production approach.

Main table markers:

- Account title `HSBC Business Direct HKD Current`
- Account title `HSBC Business Direct HKD Savings`
- Table header starts with `Date Transaction`
- Account table ends at `Total No. of` or `Total Deposit Amount`
- Foreign currency section starts at `HSBC Business Direct Foreign Currency Savings` and is ignored

Statement date:

- Read from lines such as `17 April 2025`
- Transaction dates are normalized using statement month/year

Column coordinate rules:

- Date words: `55 <= x0 <= 85`
- Description words: `96 <= x0 <= 300`
- Deposit amount: `330 <= x1 <= 382`
- Withdrawal amount: `405 <= x1 <= 457`
- Balance amount: `x0 >= 480`

The parser supports multi-line transaction descriptions. For example:

```text
27 Mar DLF PRODUCTION LTD
N32752162774(27MAR25) 100,000.00
```

becomes one row with description:

```text
DLF PRODUCTION LTD N32752162774(27MAR25)
```

## Verification Result For `hsbc_Apr2025.pdf`

Generated workbook:

```text
_reference_hsbc/generated_output/hsbc_Apr2025.xlsx
```

Validation summary:

```text
HSBC HKD Current Account:
  rows=60
  deposits=8
  deposit_total=4,476,378.58
  withdrawals=51
  withdrawal_total=4,803,322.99
  final_balance=379,068.00
  final_control=379,068.00
  balance_mismatches=0

HSBC HKD Savings Account:
  rows=28
  deposits=14
  deposit_total=2,751,472.74
  withdrawals=13
  withdrawal_total=4,966,818.81
  final_balance=0.00
  final_control=0.00
  balance_mismatches=0
```

These totals match the HSBC statement's own summary lines:

- Current: `Total No. of Deposits: 8`, `Total No. of Withdrawals: 51`
- Current: `Total Deposit Amount: HKD 4,476,378.58`, `Total Withdrawal Amount: HKD 4,803,322.99`
- Savings: `Total No. of Deposits: 14`, `Total No. of Withdrawals: 13`
- Savings: `Total Deposit Amount: HKD 2,751,472.74`, `Total Withdrawal Amount: HKD 4,966,818.81`

## Risks To Watch

- This is verified against one HSBC Business Direct PDF layout only.
- The Foreign Currency Savings section is not yet exported.
- If HSBC changes the PDF coordinates, the parser needs another coordinate calibration pass.
- Some transactions have blank Balance cells in the PDF; Control is used to reconcile running balance between visible balance rows.

