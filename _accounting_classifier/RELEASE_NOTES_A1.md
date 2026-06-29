# Release Notes A.1

## Rule-Based Bank Transaction Classifier

Initial isolated accounting classification module for merged ZeroEntry bank transaction workbooks.

## Added

- Rules CSV schema and synthetic sample rules
- Rule loading, validation, priority ordering, and enabled flag handling
- Classification engine for direction, amount, keyword, direction, and amount-range matching
- CLI for `.xlsx` and `.csv` inputs
- Classified Excel output
- Unclassified review workbook
- Summary JSON and text report
- Synthetic unittest coverage
- Module README

## Out of Scope

- AI auto-classification
- Formal accounting journal entries
- Final tax decisioning
- Production accounting guarantee
- Real bank data fixtures
- PDF parser, OCR parser, or BOC OCR workflow changes
- `_accounting_engine/` changes
