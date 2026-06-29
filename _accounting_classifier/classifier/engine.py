from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any

from .rules import ClassificationRule, text


INPUT_COLUMNS = ["Bank_Account", "Date", "Description", "Deposit", "Withdrawal", "Balance", "Control"]
CLASSIFICATION_COLUMNS = [
    "Direction",
    "Amount",
    "Category",
    "Account_Code",
    "Account_Name",
    "Tax_Type",
    "Counterparty",
    "Confidence",
    "Rule_ID",
    "Review_Needed",
    "Classification_Source",
    "Notes",
]
OUTPUT_COLUMNS = INPUT_COLUMNS + CLASSIFICATION_COLUMNS


def number(value: Any) -> float:
    if value in (None, ""):
        return 0.0
    if isinstance(value, str):
        value = value.replace(",", "").strip()
        if not value:
            return 0.0
    return float(value)


def detect_direction(row: dict[str, Any]) -> str:
    deposit = number(row.get("Deposit"))
    withdrawal = number(row.get("Withdrawal"))
    if deposit != 0 and withdrawal == 0:
        return "Deposit"
    if withdrawal != 0 and deposit == 0:
        return "Withdrawal"
    return "Unknown"


def transaction_amount(row: dict[str, Any], direction: str) -> float:
    if direction == "Deposit":
        return abs(number(row.get("Deposit")))
    if direction == "Withdrawal":
        return abs(number(row.get("Withdrawal")))
    return 0.0


def classify_row(row: dict[str, Any], rules: list[ClassificationRule]) -> dict[str, Any]:
    direction = detect_direction(row)
    amount = transaction_amount(row, direction)
    description = text(row.get("Description"))

    if direction == "Unknown":
        return unclassified_row(
            row,
            direction=direction,
            amount=amount,
            note="Unable to determine transaction direction",
        )

    for rule in rules:
        if rule.matches(description, direction, amount):
            return {
                **row,
                "Direction": direction,
                "Amount": amount,
                "Category": rule.category,
                "Account_Code": rule.account_code,
                "Account_Name": rule.account_name,
                "Tax_Type": rule.tax_type,
                "Counterparty": rule.counterparty,
                "Confidence": rule.confidence,
                "Rule_ID": rule.rule_id,
                "Review_Needed": rule.review_needed,
                "Classification_Source": "rule",
                "Notes": rule.notes,
            }

    return unclassified_row(row, direction=direction, amount=amount, note="No matching enabled rule")


def unclassified_row(row: dict[str, Any], *, direction: str, amount: float, note: str) -> dict[str, Any]:
    return {
        **row,
        "Direction": direction,
        "Amount": amount,
        "Category": "Unclassified",
        "Account_Code": "",
        "Account_Name": "",
        "Tax_Type": "",
        "Counterparty": "",
        "Confidence": 0,
        "Rule_ID": "",
        "Review_Needed": "Yes",
        "Classification_Source": "unclassified",
        "Notes": note,
    }


def classify_transactions(rows: list[dict[str, Any]], rules: list[ClassificationRule]) -> list[dict[str, Any]]:
    return [classify_row(row, rules) for row in rows]


def unclassified_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [row for row in rows if row.get("Classification_Source") == "unclassified" or row.get("Review_Needed") == "Yes"]


def summarize_classification(rows: list[dict[str, Any]]) -> dict[str, Any]:
    category_counts = Counter(text(row.get("Category")) or "Unclassified" for row in rows)
    source_counts = Counter(text(row.get("Classification_Source")) or "unknown" for row in rows)
    direction_amounts: dict[str, float] = defaultdict(float)
    category_amounts: dict[str, float] = defaultdict(float)

    for row in rows:
        direction = text(row.get("Direction")) or "Unknown"
        category = text(row.get("Category")) or "Unclassified"
        amount = number(row.get("Amount"))
        direction_amounts[direction] += amount
        category_amounts[category] += amount

    return {
        "transaction_count": len(rows),
        "classified_count": source_counts.get("rule", 0),
        "unclassified_count": source_counts.get("unclassified", 0),
        "unclassified_ratio": round(source_counts.get("unclassified", 0) / len(rows), 4) if rows else 0,
        "review_needed_count": sum(1 for row in rows if text(row.get("Review_Needed")).casefold() == "yes"),
        "category_counts": dict(sorted(category_counts.items())),
        "source_counts": dict(sorted(source_counts.items())),
        "direction_amounts": {key: round(value, 2) for key, value in sorted(direction_amounts.items())},
        "category_amounts": {key: round(value, 2) for key, value in sorted(category_amounts.items())},
    }
