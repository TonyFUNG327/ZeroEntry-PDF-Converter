import re
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from ocr.ocr_preprocessor import extract_text_from_pdf
import boc_pdf_converter


DATE_FORMATS = (
    "%Y/%m/%d",
    "%Y-%m-%d",
    "%d-%b-%y",
    "%d-%b-%Y",
    "%d %b %y",
    "%d %b %Y",
)
DATE_TOKEN_RE = re.compile(
    r"^("
    r"\d{4}[/-]\d{1,2}[/-]\d{1,2}"
    r"|\d{1,2}-[A-Za-z]{3}-\d{2,4}"
    r"|\d{1,2}\s+[A-Za-z]{3}\s+\d{2,4}"
    r")\s+(.+)$"
)
AMOUNT_RE = re.compile(r"\(?\d{1,3}(?:,\d{3})*(?:\.\d{2})\)?|\(?\d+\.\d{2}\)?")
AMOUNT_LIKE_WITH_O_RE = re.compile(r"\(?[0-9O]{1,3}(?:,[0-9O]{3})*(?:\.[0-9O]{2})\)?|\(?[0-9O]+\.[0-9O]{2}\)?")

CURRENT_PATTERNS = (
    "HKD CURRENT",
    "CURRENT ACCOUNT",
    "STATEMENT CURRENT",
    "支票",
    "往來",
    "往来",
)
SAVINGS_PATTERNS = (
    "HKD SAVINGS",
    "SAVINGS ACCOUNT",
    "STATEMENT SAVINGS",
    "儲蓄",
    "储蓄",
)
DESCRIPTION_CONTINUATION_PATTERNS = (
    "REDACTED MERCHANT",
    "TRANSACTION PARTY",
    "PAYMENT REFERENCE",
    "REFERENCE",
    "REF",
    "CUSTOMER RECEIPT",
    "CHEQUE",
    "PAYMENT",
    "TRANSFER",
    "ATM",
    "FEE",
    "CHARGE",
    "INTEREST",
)


@dataclass
class BocOcrParseResult:
    accounts: dict = field(default_factory=dict)
    warnings: list = field(default_factory=list)
    parsed_rows: list = field(default_factory=list)
    skipped_lines: list = field(default_factory=list)
    line_merge_diagnostics: dict = field(default_factory=dict)


@dataclass
class BocOcrLinePreparationResult:
    lines: list = field(default_factory=list)
    diagnostics: dict = field(default_factory=dict)


def parse_amount(text):
    text = text.strip()
    sign = -1 if text.startswith("(") and text.endswith(")") else 1
    return sign * float(text.strip("()").replace(",", ""))


def _normalize_amount_token(match):
    return match.group(0).replace("O", "0")


def normalize_ocr_line(line):
    line = " ".join((line or "").split())
    line = re.sub(r"(?<=[0-9O])\s*,\s*(?=[0-9O]{3}(?:\D|$))", ",", line)
    return AMOUNT_LIKE_WITH_O_RE.sub(_normalize_amount_token, line)


def _has_amount(line):
    return bool(AMOUNT_RE.search(line))


def _amount_count(line):
    return len(AMOUNT_RE.findall(line))


def _is_balance_marker(line):
    upper = line.upper()
    return any(marker in upper for marker in ["B/F", "BROUGHT FORWARD", "BALANCE BF", "BAL BF", "OPENING BALANCE", "C/F", "CARRIED FORWARD"])


def _is_metadata_line(line):
    upper = line.upper()
    if any(pattern in upper for pattern in CURRENT_PATTERNS + SAVINGS_PATTERNS):
        return True
    return any(marker in upper for marker in ["CUSTOMER NAME", "ACCOUNT NO", "ADDRESS"])


def _is_description_continuation(line):
    if not line or _candidate_line(line) or _is_metadata_line(line) or _has_amount(line):
        return False
    upper = line.upper()
    return any(pattern in upper for pattern in DESCRIPTION_CONTINUATION_PATTERNS)


def _is_amount_continuation(line):
    if not line or _candidate_line(line):
        return False
    if _is_metadata_line(line):
        return False
    return _has_amount(line)


def _can_merge_two_line_continuation(line, first_continuation, second_continuation):
    return (
        _candidate_line(line)
        and not _is_balance_marker(line)
        and _amount_count(line) < 2
        and _is_description_continuation(first_continuation)
        and _is_amount_continuation(second_continuation)
    )


def _blocked_merge_reason(next_line, following_line=None):
    if not next_line:
        return "missing_amount_continuation"
    if _candidate_line(next_line):
        return "next_line_is_new_date"
    if _is_metadata_line(next_line):
        return "metadata_line_blocked"
    if _has_amount(next_line):
        return None
    if not _is_description_continuation(next_line):
        return "description_continuation_not_recognized"
    if following_line is None or not _is_amount_continuation(following_line):
        return "missing_amount_continuation"
    return None


def prepare_ocr_lines_with_diagnostics(text: str) -> BocOcrLinePreparationResult:
    raw_lines = [normalize_ocr_line(raw_line) for raw_line in (text or "").splitlines()]
    raw_lines = [line for line in raw_lines if line]
    logical_lines = []
    merged_lines = []
    blocked_merges = []
    idx = 0
    while idx < len(raw_lines):
        line = raw_lines[idx]
        merged = line
        if _candidate_line(line) and not _is_balance_marker(line) and _amount_count(line) < 2:
            next_idx = idx + 1
            if next_idx < len(raw_lines) and _is_amount_continuation(raw_lines[next_idx]):
                source_lines = [line, raw_lines[next_idx]]
                merged = " ".join(source_lines)
                merged_lines.append({"source_lines": source_lines, "merged_line": merged, "merge_type": "one_line_continuation"})
                idx = next_idx
            elif next_idx + 1 < len(raw_lines) and _can_merge_two_line_continuation(line, raw_lines[next_idx], raw_lines[next_idx + 1]):
                source_lines = [line, raw_lines[next_idx], raw_lines[next_idx + 1]]
                merged = " ".join(source_lines)
                merged_lines.append({"source_lines": source_lines, "merged_line": merged, "merge_type": "two_line_continuation"})
                idx = next_idx + 1
            else:
                next_line = raw_lines[next_idx] if next_idx < len(raw_lines) else None
                following_line = raw_lines[next_idx + 1] if next_idx + 1 < len(raw_lines) else None
                reason = _blocked_merge_reason(next_line, following_line)
                if reason:
                    source_lines = [item for item in [line, next_line, following_line] if item]
                    blocked_merges.append({"source_lines": source_lines, "reason": reason})
        logical_lines.append(merged)
        idx += 1
    diagnostics = {
        "raw_line_count": len(raw_lines),
        "logical_line_count": len(logical_lines),
        "merged_line_count": len(merged_lines),
        "merged_lines": merged_lines[:10],
        "blocked_merge_count": len(blocked_merges),
        "blocked_merges": blocked_merges[:10],
    }
    return BocOcrLinePreparationResult(lines=logical_lines, diagnostics=diagnostics)


def prepare_ocr_lines(text: str) -> list[str]:
    return prepare_ocr_lines_with_diagnostics(text).lines


def parse_date(text):
    normalized = " ".join(text.strip().split())
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(normalized, fmt)
        except ValueError:
            continue
    raise ValueError(f"Unrecognized date format: {text}")


def detect_account_type(line):
    upper = line.upper()
    if any(pattern in upper for pattern in SAVINGS_PATTERNS):
        return "BOC HKD Savings Account"
    if any(pattern in upper for pattern in CURRENT_PATTERNS):
        return "BOC HKD Current Account"
    return None


def account_from_context(line, current_account=None):
    return detect_account_type(line) or current_account or "BOC HKD Current Account"


def classify_amount(previous_balance, amount, balance):
    if previous_balance is not None:
        if abs(round(previous_balance + amount, 2) - round(balance, 2)) <= 0.01:
            return amount, None
        if abs(round(previous_balance - amount, 2) - round(balance, 2)) <= 0.01:
            return None, amount
    return None, None


def _skip(result, line, reason):
    result.skipped_lines.append({"line": line, "reason": reason})
    result.warnings.append(f"{reason}: {line}")


def _candidate_line(line):
    return DATE_TOKEN_RE.match(line) is not None


def extract_accounts_from_text_with_diagnostics(text):
    result = BocOcrParseResult()
    accounts = defaultdict(list)
    current_account = None
    current_balance = {}
    default_warning_added = False

    prepared = prepare_ocr_lines_with_diagnostics(text)
    result.line_merge_diagnostics = prepared.diagnostics

    for line in prepared.lines:
        if not line:
            continue

        detected_account = detect_account_type(line)
        if detected_account:
            current_account = detected_account

        if not _candidate_line(line):
            continue

        match = DATE_TOKEN_RE.match(line)
        if not match:
            _skip(result, line, "Unrecognized date format")
            continue
        try:
            date = parse_date(match.group(1))
        except ValueError:
            _skip(result, line, "Unrecognized date format")
            continue

        rest = match.group(2)
        amount_tokens = AMOUNT_RE.findall(rest)
        amounts = [parse_amount(value) for value in amount_tokens]
        if not amounts:
            _skip(result, line, "Skipped dated line without amount")
            continue

        if not current_account:
            current_account = account_from_context(rest, current_account)
            if not default_warning_added:
                result.warnings.append("Account type not confidently detected; defaulted to BOC HKD Current Account.")
                default_warning_added = True
        else:
            current_account = account_from_context(rest, current_account)

        balance = amounts[-1]
        description = AMOUNT_RE.sub("", rest).strip(" -:")
        if not description:
            description = "BALANCE"

        if any(marker in description.upper() for marker in ["B/F", "BROUGHT FORWARD", "BALANCE BF", "BAL BF", "OPENING BALANCE"]):
            row = {
                "Bank_Account": current_account,
                "Date": date,
                "Description": "B/F BALANCE",
                "Deposit": None,
                "Withdrawal": None,
                "Balance": balance,
            }
            accounts[current_account].append(row)
            current_balance[current_account] = balance
            result.parsed_rows.append({"line": line, "row": row})
            continue

        if any(marker in description.upper() for marker in ["C/F", "CARRIED FORWARD"]):
            current_balance[current_account] = balance
            continue

        if len(amounts) < 2:
            _skip(result, line, "Skipped transaction line without transaction amount")
            continue

        amount = amounts[-2]
        previous_balance = current_balance.get(current_account)
        deposit, withdrawal = classify_amount(previous_balance, amount, balance)
        if deposit is None and withdrawal is None:
            _skip(result, line, "Could not classify deposit/withdrawal")
            continue

        row = {
            "Bank_Account": current_account,
            "Date": date,
            "Description": description,
            "Deposit": deposit,
            "Withdrawal": withdrawal,
            "Balance": balance,
        }
        accounts[current_account].append(row)
        current_balance[current_account] = balance
        result.parsed_rows.append({"line": line, "row": row})

    for rows in accounts.values():
        control = None
        for row in rows:
            if row["Deposit"] is None and row["Withdrawal"] is None and row["Balance"] is not None:
                control = row["Balance"]
            else:
                if control is None:
                    control = row["Balance"] or 0.0
                control += row["Deposit"] or 0.0
                control -= row["Withdrawal"] or 0.0
            row["Control"] = round(control, 2) if control is not None else None

    result.accounts = dict(accounts)
    return result


def extract_accounts_from_text(text):
    result = extract_accounts_from_text_with_diagnostics(text)
    return result.accounts, result.warnings


def extract_pdf_with_diagnostics(pdf_path):
    text = extract_text_from_pdf(Path(pdf_path))
    return extract_accounts_from_text_with_diagnostics(text)


def extract_pdf(pdf_path):
    return extract_pdf_with_diagnostics(pdf_path).accounts


def validate_accounts(accounts):
    return boc_pdf_converter.validate_accounts(accounts)


def write_workbook(accounts, output_path):
    return boc_pdf_converter.write_workbook(accounts, output_path)
