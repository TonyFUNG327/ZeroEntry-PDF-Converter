from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Any


RULE_FIELDS = [
    "rule_id",
    "priority",
    "enabled",
    "match_type",
    "keyword",
    "direction",
    "amount_min",
    "amount_max",
    "category",
    "account_code",
    "account_name",
    "tax_type",
    "counterparty",
    "confidence",
    "review_needed",
    "notes",
]


def text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def optional_float(value: Any) -> float | None:
    raw = text(value).replace(",", "")
    if not raw:
        return None
    try:
        parsed = float(raw)
    except ValueError as exc:
        raise ValueError(f"Expected numeric value, got '{text(value)}'") from exc
    if parsed < 0:
        raise ValueError("Amount limits must be zero or positive")
    return parsed


def parse_enabled(value: Any, row_number: int) -> bool:
    raw = text(value).casefold()
    if raw in {"yes", "y", "true", "1"}:
        return True
    if raw in {"no", "n", "false", "0"}:
        return False
    raise ValueError(f"Rule row {row_number}: invalid enabled value '{text(value)}'")


@dataclass(frozen=True)
class ClassificationRule:
    rule_id: str
    priority: int
    enabled: bool
    match_type: str
    keyword: str
    direction: str
    amount_min: float | None
    amount_max: float | None
    category: str
    account_code: str
    account_name: str
    tax_type: str
    counterparty: str
    confidence: float
    review_needed: str
    notes: str

    @classmethod
    def from_row(cls, row: dict[str, Any], row_number: int) -> "ClassificationRule":
        match_type = text(row.get("match_type")) or "contains"
        if match_type.casefold() != "contains":
            raise ValueError(f"Rule row {row_number}: unsupported match_type '{match_type}'")

        direction = text(row.get("direction")) or "Any"
        if direction.casefold() not in {"deposit", "withdrawal", "any"}:
            raise ValueError(f"Rule row {row_number}: invalid direction '{direction}'")

        rule_id = text(row.get("rule_id"))
        keyword = text(row.get("keyword"))
        if not rule_id:
            raise ValueError(f"Rule row {row_number}: rule_id is required")
        if not keyword:
            raise ValueError(f"Rule row {row_number}: keyword is required")
        category = text(row.get("category"))
        if not category:
            raise ValueError(f"Rule row {row_number}: category is required")

        try:
            priority = int(text(row.get("priority")) or "100")
        except ValueError as exc:
            raise ValueError(f"Rule row {row_number}: priority must be an integer") from exc

        try:
            confidence = float(text(row.get("confidence")) or "0")
        except ValueError as exc:
            raise ValueError(f"Rule row {row_number}: confidence must be numeric") from exc
        if confidence < 0 or confidence > 1:
            raise ValueError(f"Rule row {row_number}: confidence must be between 0 and 1")

        try:
            amount_min = optional_float(row.get("amount_min"))
            amount_max = optional_float(row.get("amount_max"))
        except ValueError as exc:
            raise ValueError(f"Rule row {row_number}: {exc}") from exc
        if amount_min is not None and amount_max is not None and amount_min > amount_max:
            raise ValueError(f"Rule row {row_number}: amount_min cannot be greater than amount_max")

        return cls(
            rule_id=rule_id,
            priority=priority,
            enabled=parse_enabled(row.get("enabled"), row_number),
            match_type=match_type,
            keyword=keyword,
            direction=direction,
            amount_min=amount_min,
            amount_max=amount_max,
            category=category,
            account_code=text(row.get("account_code")),
            account_name=text(row.get("account_name")),
            tax_type=text(row.get("tax_type")),
            counterparty=text(row.get("counterparty")),
            confidence=confidence,
            review_needed=text(row.get("review_needed")) or "No",
            notes=text(row.get("notes")),
        )

    def matches(self, description: str, direction: str, amount: float) -> bool:
        if not self.enabled:
            return False
        if direction.casefold() == "unknown":
            return False
        if self.keyword.casefold() not in description.casefold():
            return False
        if self.direction.casefold() != "any" and self.direction.casefold() != direction.casefold():
            return False
        if self.amount_min is not None and amount < self.amount_min:
            return False
        if self.amount_max is not None and amount > self.amount_max:
            return False
        return True


def load_rules(path: str | Path) -> list[ClassificationRule]:
    path = Path(path)
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        missing = [field for field in RULE_FIELDS if field not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"Rules CSV missing columns: {', '.join(missing)}")
        rules = [ClassificationRule.from_row(row, idx) for idx, row in enumerate(reader, start=2)]
    rule_ids = [rule.rule_id for rule in rules]
    duplicates = sorted({rule_id for rule_id in rule_ids if rule_ids.count(rule_id) > 1})
    if duplicates:
        raise ValueError(f"Duplicate rule_id values: {', '.join(duplicates)}")
    return sorted(rules, key=lambda rule: (rule.priority, rule.rule_id))
