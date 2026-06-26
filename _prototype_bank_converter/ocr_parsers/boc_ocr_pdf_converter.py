import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from ocr.ocr_preprocessor import extract_text_from_pdf
import boc_pdf_converter


DATE_RE = re.compile(r"^(\d{4}[/-]\d{1,2}[/-]\d{1,2})\s+(.+)$")
AMOUNT_RE = re.compile(r"\(?\d{1,3}(?:,\d{3})*(?:\.\d{2})\)?|\(?\d+\.\d{2}\)?")


def parse_amount(text):
    sign = -1 if text.startswith("(") and text.endswith(")") else 1
    return sign * float(text.strip("()").replace(",", ""))


def parse_date(text):
    return datetime.strptime(text.replace("-", "/"), "%Y/%m/%d")


def account_from_context(line, current_account=None):
    upper = line.upper()
    if "SAVINGS" in upper or "儲蓄" in line or "储蓄" in line:
        return "BOC HKD Savings Account"
    if "CURRENT" in upper or "往來" in line or "往来" in line or "支票" in line:
        return "BOC HKD Current Account"
    return current_account or "BOC HKD Current Account"


def classify_amount(previous_balance, amount, balance):
    if previous_balance is not None:
        if abs(round(previous_balance + amount, 2) - round(balance, 2)) <= 0.01:
            return amount, None
        if abs(round(previous_balance - amount, 2) - round(balance, 2)) <= 0.01:
            return None, amount
    return None, None


def extract_accounts_from_text(text):
    accounts = defaultdict(list)
    current_account = None
    current_balance = {}
    warnings = []

    for raw_line in (text or "").splitlines():
        line = " ".join(raw_line.split())
        if not line:
            continue
        if any(marker in line.upper() for marker in ["SAVINGS", "CURRENT"]) or any(marker in line for marker in ["儲蓄", "储蓄", "往來", "往来", "支票"]):
            current_account = account_from_context(line, current_account)

        match = DATE_RE.match(line)
        if not match:
            continue
        date = parse_date(match.group(1))
        rest = match.group(2)
        amounts = [parse_amount(value) for value in AMOUNT_RE.findall(rest)]
        if not amounts:
            warnings.append(f"Skipped dated line without amount: {line}")
            continue

        balance = amounts[-1]
        description = AMOUNT_RE.sub("", rest).strip(" -:")
        if not description:
            description = "BALANCE"
        current_account = account_from_context(description, current_account)

        if any(marker in description.upper() for marker in ["B/F", "BROUGHT FORWARD"]) or any(marker in description for marker in ["承上", "承前"]):
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
            continue
        if any(marker in description.upper() for marker in ["C/F", "CARRIED FORWARD"]) or any(marker in description for marker in ["結餘", "结余"]):
            current_balance[current_account] = balance
            continue

        if len(amounts) < 2:
            warnings.append(f"Skipped transaction line without transaction amount: {line}")
            continue
        amount = amounts[-2]
        previous_balance = current_balance.get(current_account)
        deposit, withdrawal = classify_amount(previous_balance, amount, balance)
        if deposit is None and withdrawal is None:
            warnings.append(f"Could not classify deposit/withdrawal: {line}")
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
    return dict(accounts), warnings


def extract_pdf(pdf_path):
    text = extract_text_from_pdf(Path(pdf_path))
    accounts, _warnings = extract_accounts_from_text(text)
    return accounts


def validate_accounts(accounts):
    return boc_pdf_converter.validate_accounts(accounts)


def write_workbook(accounts, output_path):
    return boc_pdf_converter.write_workbook(accounts, output_path)

