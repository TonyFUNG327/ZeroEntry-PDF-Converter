# ZeroEntry Local Experience Database

This folder is for local manual review and mapping maintenance files.

Only empty templates and synthetic examples should be committed. Do not commit real bank data, customer data, supplier data, account numbers, addresses, or live reviewed workbooks.

## Files

- `manual_classification_template.csv`: blank A.2.1 manual review template columns.
- `simple_manual_classification_template.csv`: compact manual classification template with two synthetic examples.
- `reviewed_transactions.csv`: header-only holding file for sanitized reviewed rows.
- `mapping_conflicts.csv`: header-only conflict report template.
- `mapping_merge_summary.json`: empty merge summary template.

## Workflow

1. Use `manual_classification_template.csv` as a safe column reference for manual review.
2. Use `simple_manual_classification_template.csv` when entering only the fields needed for mapping maintenance.
3. Copy real local working files into `local/` or another ignored location.
4. Extract only `Confirmed` and `Corrected` rows into mapping candidates.
5. `Pending`, `Ignore`, `Need_Advice`, and blank statuses do not become mappings.
6. Review `mapping_conflicts.csv` manually before changing existing mappings.

A.3.1 is deterministic mapping maintenance only. It is not AI classification, supplier/customer memory, or formal accounting posting.
