from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any

from .mappings import ClassificationMapping
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


def anomaly_notes(row: dict[str, Any]) -> list[str]:
    deposit = number(row.get("Deposit"))
    withdrawal = number(row.get("Withdrawal"))
    notes: list[str] = []
    if deposit < 0:
        notes.append("Negative Deposit amount")
    if withdrawal < 0:
        notes.append("Negative Withdrawal amount")
    if deposit != 0 and withdrawal != 0:
        notes.append("Both Deposit and Withdrawal contain values")
    elif deposit == 0 and withdrawal == 0:
        notes.append("Deposit and Withdrawal are both blank or zero")
    return notes


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


def classify_row(
    row: dict[str, Any],
    rules: list[ClassificationRule],
    mappings: list[ClassificationMapping] | None = None,
) -> dict[str, Any]:
    direction = detect_direction(row)
    amount = transaction_amount(row, direction)
    description = text(row.get("Description"))
    anomalies = anomaly_notes(row)

    if direction == "Unknown":
        return unclassified_row(
            row,
            direction=direction,
            amount=amount,
            notes=["Unable to determine transaction direction", *anomalies],
        )

    for mapping in mappings or []:
        if mapping.matches(description, direction, amount):
            notes = [f"confirmed mapping {mapping.mapping_id}"]
            if mapping.notes:
                notes.append(mapping.notes)
            notes.extend(anomalies)
            return {
                **row,
                "Direction": direction,
                "Amount": amount,
                "Category": mapping.category,
                "Account_Code": mapping.account_code,
                "Account_Name": mapping.account_name,
                "Tax_Type": mapping.tax_type,
                "Counterparty": mapping.counterparty,
                "Confidence": mapping.confidence,
                "Rule_ID": text(row.get("Rule_ID")),
                "Review_Needed": "No",
                "Classification_Source": "confirmed_mapping",
                "Notes": "; ".join(notes),
            }

    for rule in rules:
        if rule.matches(description, direction, amount):
            notes = [rule.notes] if rule.notes else []
            notes.extend(anomalies)
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
                "Notes": "; ".join(notes),
            }

    return unclassified_row(row, direction=direction, amount=amount, notes=["No matching enabled rule", *anomalies])


def unclassified_row(row: dict[str, Any], *, direction: str, amount: float, notes: list[str]) -> dict[str, Any]:
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
        "Notes": "; ".join(dict.fromkeys(note for note in notes if note)),
    }


def classify_transactions(
    rows: list[dict[str, Any]],
    rules: list[ClassificationRule],
    mappings: list[ClassificationMapping] | None = None,
) -> list[dict[str, Any]]:
    return [classify_row(row, rules, mappings) for row in rows]


def unclassified_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [row for row in rows if row.get("Classification_Source") == "unclassified" or row.get("Review_Needed") == "Yes"]


def summarize_classification(rows: list[dict[str, Any]]) -> dict[str, Any]:
    category_counts = Counter(text(row.get("Category")) or "Unclassified" for row in rows)
    source_counts = Counter(text(row.get("Classification_Source")) or "unknown" for row in rows)
    rule_hit_counts = Counter(text(row.get("Rule_ID")) for row in rows if text(row.get("Rule_ID")))
    mapping_hit_counts = Counter()
    direction_amounts: dict[str, float] = defaultdict(float)
    category_amounts: dict[str, float] = defaultdict(float)
    top_unclassified = Counter(
        text(row.get("Description")) or "(blank)"
        for row in rows
        if text(row.get("Classification_Source")) == "unclassified"
    )
    anomaly_counts = Counter()

    for row in rows:
        direction = text(row.get("Direction")) or "Unknown"
        category = text(row.get("Category")) or "Unclassified"
        amount = number(row.get("Amount"))
        direction_amounts[direction] += amount
        category_amounts[category] += amount
        deposit = number(row.get("Deposit"))
        withdrawal = number(row.get("Withdrawal"))
        if direction == "Unknown":
            anomaly_counts["unknown_direction"] += 1
        if deposit != 0 and withdrawal != 0:
            anomaly_counts["both_deposit_and_withdrawal"] += 1
        if deposit == 0 and withdrawal == 0:
            anomaly_counts["zero_amount"] += 1
        if deposit < 0:
            anomaly_counts["negative_deposit"] += 1
        if withdrawal < 0:
            anomaly_counts["negative_withdrawal"] += 1
        if text(row.get("Classification_Source")) == "confirmed_mapping":
            for part in text(row.get("Notes")).split(";"):
                part = part.strip()
                if part.startswith("confirmed mapping "):
                    mapping_hit_counts[part.replace("confirmed mapping ", "", 1)] += 1

    return {
        "transaction_count": len(rows),
        "classified_count": source_counts.get("rule", 0),
        "unclassified_count": source_counts.get("unclassified", 0),
        "unclassified_ratio": round(source_counts.get("unclassified", 0) / len(rows), 4) if rows else 0,
        "review_needed_count": sum(1 for row in rows if text(row.get("Review_Needed")).casefold() == "yes"),
        "category_counts": dict(sorted(category_counts.items())),
        "source_counts": dict(sorted(source_counts.items())),
        "rule_hit_counts": dict(sorted(rule_hit_counts.items())),
        "mapping_classified_count": source_counts.get("confirmed_mapping", 0),
        "mapping_hit_counts": dict(sorted(mapping_hit_counts.items())),
        "top_unclassified_descriptions": [
            {"description": description, "count": count}
            for description, count in top_unclassified.most_common(10)
        ],
        "anomaly_counts": {
            key: anomaly_counts.get(key, 0)
            for key in [
                "unknown_direction",
                "both_deposit_and_withdrawal",
                "zero_amount",
                "negative_deposit",
                "negative_withdrawal",
            ]
        },
        "direction_amounts": {key: round(value, 2) for key, value in sorted(direction_amounts.items())},
        "category_amounts": {key: round(value, 2) for key, value in sorted(category_amounts.items())},
    }
