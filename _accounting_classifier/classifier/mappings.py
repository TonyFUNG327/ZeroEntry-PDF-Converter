from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .rules import text


MAPPING_FIELDS = [
    "mapping_id",
    "enabled",
    "priority",
    "match_type",
    "description_pattern",
    "direction",
    "amount_min",
    "amount_max",
    "category",
    "account_code",
    "account_name",
    "tax_type",
    "counterparty",
    "confidence",
    "source_review_status",
    "source_rule_id",
    "source_classification_source",
    "use_count",
    "last_used_date",
    "notes",
]


def parse_bool(value: Any, row_number: int) -> bool:
    raw = text(value).casefold()
    if raw in {"yes", "y", "true", "1"}:
        return True
    if raw in {"no", "n", "false", "0"}:
        return False
    raise ValueError(f"Mapping row {row_number}: invalid enabled value '{text(value)}'")


def optional_float(value: Any, row_number: int, field: str) -> float | None:
    raw = text(value).replace(",", "")
    if not raw:
        return None
    try:
        return float(raw)
    except ValueError as exc:
        raise ValueError(f"Mapping row {row_number}: {field} must be numeric") from exc


@dataclass(frozen=True)
class ClassificationMapping:
    mapping_id: str
    enabled: bool
    priority: int
    match_type: str
    description_pattern: str
    direction: str
    amount_min: float | None
    amount_max: float | None
    category: str
    account_code: str
    account_name: str
    tax_type: str
    counterparty: str
    confidence: float
    source_review_status: str
    source_rule_id: str
    source_classification_source: str
    use_count: int
    last_used_date: str
    notes: str

    @classmethod
    def from_row(cls, row: dict[str, Any], row_number: int) -> "ClassificationMapping":
        mapping_id = text(row.get("mapping_id"))
        if not mapping_id:
            raise ValueError(f"Mapping row {row_number}: mapping_id is required")
        match_type = text(row.get("match_type")) or "exact_description"
        if match_type not in {"exact_description", "contains"}:
            raise ValueError(f"Mapping row {row_number}: invalid match_type '{match_type}'")
        direction = text(row.get("direction")) or "Any"
        if direction not in {"Deposit", "Withdrawal", "Any"}:
            raise ValueError(f"Mapping row {row_number}: invalid direction '{direction}'")
        description_pattern = text(row.get("description_pattern"))
        if not description_pattern:
            raise ValueError(f"Mapping row {row_number}: description_pattern is required")
        category = text(row.get("category"))
        if not category:
            raise ValueError(f"Mapping row {row_number}: category is required")
        try:
            priority = int(text(row.get("priority")) or "100")
        except ValueError as exc:
            raise ValueError(f"Mapping row {row_number}: priority must be an integer") from exc
        confidence = optional_float(row.get("confidence"), row_number, "confidence")
        confidence = 1.0 if confidence is None else confidence
        if confidence < 0 or confidence > 1:
            raise ValueError(f"Mapping row {row_number}: confidence must be between 0 and 1")
        amount_min = optional_float(row.get("amount_min"), row_number, "amount_min")
        amount_max = optional_float(row.get("amount_max"), row_number, "amount_max")
        if amount_min is not None and amount_max is not None and amount_min > amount_max:
            raise ValueError(f"Mapping row {row_number}: amount_min cannot be greater than amount_max")
        try:
            use_count = int(text(row.get("use_count")) or "0")
        except ValueError as exc:
            raise ValueError(f"Mapping row {row_number}: use_count must be an integer") from exc
        return cls(
            mapping_id=mapping_id,
            enabled=parse_bool(row.get("enabled"), row_number),
            priority=priority,
            match_type=match_type,
            description_pattern=description_pattern,
            direction=direction,
            amount_min=amount_min,
            amount_max=amount_max,
            category=category,
            account_code=text(row.get("account_code")),
            account_name=text(row.get("account_name")),
            tax_type=text(row.get("tax_type")),
            counterparty=text(row.get("counterparty")),
            confidence=confidence,
            source_review_status=text(row.get("source_review_status")),
            source_rule_id=text(row.get("source_rule_id")),
            source_classification_source=text(row.get("source_classification_source")),
            use_count=use_count,
            last_used_date=text(row.get("last_used_date")),
            notes=text(row.get("notes")),
        )

    def matches(self, description: str, direction: str, amount: float) -> bool:
        if not self.enabled:
            return False
        if direction == "Unknown":
            return False
        if self.direction != "Any" and self.direction != direction:
            return False
        if self.amount_min is not None and amount < self.amount_min:
            return False
        if self.amount_max is not None and amount > self.amount_max:
            return False
        if self.match_type == "exact_description":
            return text(description).casefold() == self.description_pattern.casefold()
        return self.description_pattern.casefold() in text(description).casefold()


def load_mappings(path: str | Path) -> list[ClassificationMapping]:
    path = Path(path)
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        missing = [field for field in MAPPING_FIELDS if field not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"Mappings CSV missing columns: {', '.join(missing)}")
        mappings = [ClassificationMapping.from_row(row, idx) for idx, row in enumerate(reader, start=2)]
    ids = [mapping.mapping_id for mapping in mappings]
    duplicates = sorted({mapping_id for mapping_id in ids if ids.count(mapping_id) > 1})
    if duplicates:
        raise ValueError(f"Duplicate mapping_id values: {', '.join(duplicates)}")
    return sorted(mappings, key=lambda mapping: (mapping.priority, mapping.mapping_id))


def write_mappings(path: str | Path, rows: list[dict[str, Any]]) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=MAPPING_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in MAPPING_FIELDS})
    return path


def mapping_row_from_review(row: dict[str, Any], mapping_id: str, use_count: int) -> dict[str, Any]:
    return {
        "mapping_id": mapping_id,
        "enabled": "Yes",
        "priority": "10",
        "match_type": "exact_description",
        "description_pattern": text(row.get("Description")),
        "direction": text(row.get("Direction")) or "Any",
        "amount_min": "",
        "amount_max": "",
        "category": text(row.get("Category")),
        "account_code": text(row.get("Account_Code")),
        "account_name": text(row.get("Account_Name")),
        "tax_type": text(row.get("Tax_Type")),
        "counterparty": text(row.get("Counterparty")),
        "confidence": "1.0",
        "source_review_status": text(row.get("Manual_Review_Status")),
        "source_rule_id": text(row.get("Rule_ID")),
        "source_classification_source": text(row.get("Classification_Source")),
        "use_count": str(use_count),
        "last_used_date": text(row.get("Date")),
        "notes": text(row.get("Notes")),
    }


def extract_confirmed_mappings(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    candidates = [
        row for row in rows
        if text(row.get("Manual_Review_Status")) in {"Confirmed", "Corrected"}
    ]
    grouped: dict[tuple[str, str, str], dict[str, Any]] = {}
    counts: dict[tuple[str, str, str], int] = {}
    for row in candidates:
        key = (text(row.get("Description")), text(row.get("Direction")), text(row.get("Category")))
        counts[key] = counts.get(key, 0) + 1
        grouped.setdefault(key, row)
    rows_out = []
    for idx, key in enumerate(sorted(grouped), start=1):
        rows_out.append(mapping_row_from_review(grouped[key], f"MAP_{idx:04d}", counts[key]))
    return rows_out
