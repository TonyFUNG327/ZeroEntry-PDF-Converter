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

## A.1.1 Stability Patch

- Added synthetic baseline classification fixtures and expected results
- Expanded unittest coverage for rules validation, matching behavior, CLI defaults, CSV/XLSX input, summaries, and review rows
- Prevented `Unknown` direction rows from matching ordinary rules, including `direction=Any`
- Expanded summary text output with unclassified ratio, source counts, direction amounts, and category amounts
- Added `.gitignore` safeguards for generated classified/review workbooks and summary reports while allowing classifier synthetic CSV fixtures

## A.1.2 Stability and Diagnostics Patch

- Strengthened rules CSV validation for duplicate rule IDs, required fields, enabled values, confidence range, and amount ranges
- Added a defensive `ClassificationRule.matches()` guard so `Unknown` direction never matches ordinary rules
- Added classification diagnostics to summary JSON: `rule_hit_counts`, `top_unclassified_descriptions`, and `anomaly_counts`
- Added anomaly notes for ambiguous, zero, and negative amount cases without changing the output column order
- Expanded summary text report with rule hits, anomaly counts, and top unclassified descriptions
- Expanded synthetic unittest coverage from 17 to 29 tests
- Kept A.1.2 limited to rule-based stability and diagnostics; no parser, AI, manual override, or journal posting changes

## A.2.0 Manual Review Workflow

- Added `review_bank_transactions.py` CLI for review templates and applying completed manual review
- Added `classifier/review.py` for manual review columns, status validation, review application, and review summaries
- Added manual statuses: `Pending`, `Confirmed`, `Corrected`, `Ignore`, and `Need_Advice`
- Added validation for required A.1.2 output columns, manual review columns, invalid statuses, required `Manual_Category`, and required `Manual_Notes`
- Added reviewed workbook output with unchanged A.1.2 columns plus `Manual_*` review columns
- Added review summary JSON/TXT fields for manual status counts, completed review counts, category/source counts, corrected categories, ignored count, and need-advice descriptions
- Added synthetic review fixtures and unittest coverage for CSV/XLSX input, CLI template creation, CLI review application, and all manual statuses
- Kept A.2.0 limited to manual review workflow; no parser, AI, confirmed mapping, experience base, supplier/customer memory, or journal posting changes
