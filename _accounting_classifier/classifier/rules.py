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
    return float(raw)


def yes(value: Any) -> bool:
    return text(value).casefold() in {"yes", "y", "true", "1", "enabled"}


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

        return cls(
            rule_id=rule_id,
            priority=int(text(row.get("priority")) or "100"),
            enabled=yes(row.get("enabled")),
            match_type=match_type,
            keyword=keyword,
            direction=direction,
            amount_min=optional_float(row.get("amount_min")),
            amount_max=optional_float(row.get("amount_max")),
            category=text(row.get("category")),
            account_code=text(row.get("account_code")),
            account_name=text(row.get("account_name")),
            tax_type=text(row.get("tax_type")),
            counterparty=text(row.get("counterparty")),
            confidence=float(text(row.get("confidence")) or "0"),
            review_needed=text(row.get("review_needed")) or "No",
            notes=text(row.get("notes")),
        )

    def matches(self, description: str, direction: str, amount: float) -> bool:
        if not self.enabled:
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
    return sorted(rules, key=lambda rule: (rule.priority, rule.rule_id))
