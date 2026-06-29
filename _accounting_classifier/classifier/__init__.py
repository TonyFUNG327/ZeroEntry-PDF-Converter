"""Rule-based accounting classifier for merged bank transactions."""

from .engine import classify_transactions, summarize_classification
from .rules import ClassificationRule, load_rules

__all__ = [
    "ClassificationRule",
    "classify_transactions",
    "load_rules",
    "summarize_classification",
]
