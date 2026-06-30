# ZeroEntry Accounting Classification Module A.1

This module provides a first-pass, rule-based classifier for merged bank transaction workbooks created by ZeroEntry PDF Converter, usually from the converter `BB3` combined workbook.

It is intentionally isolated from PDF parsing, OCR parsing, formal double-entry posting, tax decisioning, and AI auto-classification.

## Input

The input workbook or CSV must contain these ZeroEntry bank columns:

- `Bank_Account`
- `Date`
- `Description`
- `Deposit`
- `Withdrawal`
- `Balance`
- `Control`

## Output

The CLI writes:

- classified Excel workbook
- unclassified review workbook
- summary JSON
- summary text report

Classification columns appended to each row:

- `Direction`
- `Amount`
- `Category`
- `Account_Code`
- `Account_Name`
- `Tax_Type`
- `Counterparty`
- `Confidence`
- `Rule_ID`
- `Review_Needed`
- `Classification_Source`
- `Notes`

## Rules CSV

Rules live in `rules/classification_rules.csv` and use these columns:

```text
rule_id,priority,enabled,match_type,keyword,direction,amount_min,amount_max,category,account_code,account_name,tax_type,counterparty,confidence,review_needed,notes
```

A.1 supports:

- `match_type`: `contains`
- `direction`: `Deposit`, `Withdrawal`, or `Any`
- `enabled`: `Yes` or `No`
- lower numeric `priority` runs first
- optional `amount_min` and `amount_max`

A.1.2 validates rules before classification:

- `rule_id`, `keyword`, and `category` are required
- `rule_id` values must be unique
- `priority` must be an integer
- `enabled` accepts only `Yes`, `No`, `True`, `False`, `1`, or `0`
- `match_type` supports only `contains`
- `direction` supports only `Deposit`, `Withdrawal`, or `Any`
- `confidence` must be numeric from `0` to `1`
- `amount_min` and `amount_max` must be numeric and zero or positive when supplied
- `amount_min` cannot be greater than `amount_max`
- `account_code`, `account_name`, and `tax_type` remain optional in A.1.2

The bundled rules are synthetic examples only: `BANK_CHARGE`, `RENT_PAYMENT`, `CUSTOMER_RECEIPT`, `TRANSFER`, and `INTEREST`.

## CLI

From the repository root:

```powershell
python _accounting_classifier\classify_bank_transactions.py "path\to\combined.xlsx" --rules _accounting_classifier\rules\classification_rules.csv --output "path\to\classified.xlsx"
```

From this folder:

```powershell
python classify_bank_transactions.py input.xlsx --rules rules\classification_rules.csv --output classified.xlsx
```

Defaults derived from `--output`:

- `classified.summary.json`
- `classified.summary.txt`
- `classified_unclassified.xlsx`

## A.1.1 Safety Behavior

If `Deposit` and `Withdrawal` are both blank/zero, or both contain values, the transaction direction is `Unknown`.

Unknown direction rows do not match ordinary rules, including `direction=Any`. They are classified as:

- `Category`: `Unclassified`
- `Confidence`: `0`
- `Review_Needed`: `Yes`
- `Classification_Source`: `unclassified`
- `Notes`: `Unable to determine transaction direction`

The summary text report includes:

- `transaction_count`
- `classified_count`
- `unclassified_count`
- `review_needed_count`
- `unclassified_ratio`
- `category_counts`
- `source_counts`
- `rule_hit_counts`
- `anomaly_counts`
- `top_unclassified_descriptions`
- `direction_amounts`
- `category_amounts`

Anomaly diagnostics currently count:

- `unknown_direction`
- `both_deposit_and_withdrawal`
- `zero_amount`
- `negative_deposit`
- `negative_withdrawal`

When a row has an anomaly, the classifier keeps the output columns unchanged and appends the anomaly to `Notes`.

## A.1 Non-Goals

- No OpenAI API or other AI API calls
- No fully automated accounting guarantee
- No formal journal entries
- No final tax advice
- No PDF converter or OCR parser changes
- No real bank data fixtures

## A.1.2 Non-Goals

- No PDF or OCR parser changes
- No AI classifier
- No formal journal entry posting
- No manual override workflow
- No confirmed mappings or experience base
- No real bank, customer, supplier, address, account number, or sensitive amount fixtures

## A.2.0 Manual Review Workflow

A.2.0 adds a manual review pass after A.1.2 classification. It can either add blank review columns to a classified workbook, or apply completed manual review fields to produce a reviewed workbook and review summary.

Manual review columns:

- `Manual_Category`
- `Manual_Account_Code`
- `Manual_Account_Name`
- `Manual_Tax_Type`
- `Manual_Counterparty`
- `Manual_Review_Status`
- `Manual_Notes`

Allowed `Manual_Review_Status` values:

- `Pending`
- `Confirmed`
- `Corrected`
- `Ignore`
- `Need_Advice`

Status behavior:

- `Pending`: keeps classification fields unchanged, sets `Review_Needed=Yes`, and appends `manual review pending` to `Notes`.
- `Confirmed`: keeps classification fields unchanged, sets `Review_Needed=No`, sets `Classification_Source=manual_confirmed`, and appends `Manual_Notes`.
- `Corrected`: copies manual category/account/tax/counterparty fields into classification fields, sets `Review_Needed=No`, `Classification_Source=manual_corrected`, `Confidence=1.0`, and appends `Manual_Notes`.
- `Ignore`: sets `Category=Ignored`, `Review_Needed=No`, `Classification_Source=manual_ignored`, `Confidence=1.0`, and appends `Manual_Notes`.
- `Need_Advice`: keeps classification fields unchanged, sets `Review_Needed=Yes`, `Classification_Source=manual_need_advice`, and appends `Manual_Notes`.

Validation:

- Reviewed input must contain all A.1.2 output columns before review can be applied.
- Applying review requires all manual review columns.
- Invalid manual review status raises `ValueError` with the row number.
- `Corrected` requires `Manual_Category`.
- `Confirmed`, `Corrected`, `Ignore`, and `Need_Advice` require `Manual_Notes`.

CLI examples:

Create a review template from an A.1.2 classified workbook:

```powershell
python review_bank_transactions.py classified.xlsx --output review_template.xlsx --add-template-columns
```

Apply completed manual review:

```powershell
python review_bank_transactions.py reviewed_input.xlsx --output reviewed_output.xlsx
```

Optional summary paths:

```powershell
python review_bank_transactions.py reviewed_input.xlsx --output reviewed_output.xlsx --summary-json review.summary.json --summary-txt review.summary.txt
```

Review summary fields include:

- `transaction_count`
- `manual_pending_count`
- `manual_confirmed_count`
- `manual_corrected_count`
- `manual_ignored_count`
- `manual_need_advice_count`
- `manual_blank_status_count`
- `review_completed_count`
- `review_needed_count`
- `classification_source_counts`
- `category_counts`
- `corrected_category_counts`
- `need_advice_descriptions`
- `ignored_count`

## A.2.0 Non-Goals

- No PDF or OCR parser changes
- No OpenAI API or AI classification
- No formal journal entries
- No confirmed mappings or experience base
- No supplier/customer memory
- No automatic rule learning from manual review

## Tests

Run from this folder:

```powershell
python -m unittest discover tests
```

The tests and baseline fixtures use synthetic data only.
