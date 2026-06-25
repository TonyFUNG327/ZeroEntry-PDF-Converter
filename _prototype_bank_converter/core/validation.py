from .common import money


def balance_mismatches(rows):
    mismatches = []
    for idx, row in enumerate(rows):
        balance = row.get("Balance")
        control = row.get("Control")
        if balance is not None and control is not None and abs(balance - control) > 0.01:
            mismatches.append(idx + 2)
    return mismatches


def summarize_account(account, rows):
    rows = rows or []
    deposit_total = round(sum(row.get("Deposit") or 0 for row in rows), 2)
    withdrawal_total = round(sum(row.get("Withdrawal") or 0 for row in rows), 2)
    return {
        "account": account,
        "rows": len(rows),
        "deposit_count": sum(1 for row in rows if row.get("Deposit") is not None),
        "withdrawal_count": sum(1 for row in rows if row.get("Withdrawal") is not None),
        "deposit_total": deposit_total,
        "withdrawal_total": withdrawal_total,
        "final_balance": rows[-1].get("Balance") if rows else None,
        "final_control": rows[-1].get("Control") if rows else None,
        "balance_mismatches": balance_mismatches(rows),
    }


def summarize_accounts(accounts):
    return [summarize_account(account, rows) for account, rows in (accounts or {}).items()]


def format_report_item(item):
    deposits = item.get("deposit_count", "n/a")
    withdrawals = item.get("withdrawal_count", "n/a")
    mismatches = item.get("balance_mismatches") or []
    return (
        f"{item['account']}: rows={item.get('rows', 0)}, "
        f"deposits={deposits} amount={money(item.get('deposit_total'))}, "
        f"withdrawals={withdrawals} amount={money(item.get('withdrawal_total'))}, "
        f"final_balance={money(item.get('final_balance'))}, "
        f"final_control={money(item.get('final_control'))}, "
        f"balance_mismatches={len(mismatches)}"
    )

