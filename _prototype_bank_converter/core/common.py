import re


AMOUNT_RE = re.compile(r"^\(?\d{1,3}(?:,\d{3})*(?:\.\d{2})\)?$|^\(?\d+\.\d{2}\)?$")


def clean_text(text):
    return " ".join((text or "").replace("(cid:10)", " ").replace("(cid:13)", " ").replace("\ufeff", " ").split())


def amount_value(text):
    if text is None:
        return None
    value = str(text).strip()
    if not value or value == "-":
        return None
    sign = -1 if value.startswith("(") and value.endswith(")") else 1
    return sign * float(value.strip("()").replace(",", ""))


def safe_float(value, default=None):
    if value is None or value == "":
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def money(value):
    if value is None:
        return "n/a"
    return f"{float(value):,.2f}"

