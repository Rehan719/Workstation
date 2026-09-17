"""
Owner-Payments Ledger (§7) — the Owner's accrued share, VIRTUAL/simulated WST only.

Each metabolic cycle's Owner stage (the §4 waterfall's `owner` split) accrues here. The Owner can record a
payout, but **real-money rails are intentionally DISABLED and gated**: no real funds move — a payout is a
virtual ledger entry until the Owner explicitly authorises real rails AND a compliance/KYC review passes.
This keeps a clean seam so real rails can be added later behind that gate, without ever representing simulated
finance as real.

W465 (register FU-016) — the store follows the shared-store convention. It used to be read with every error
swallowed (a corrupt or momentarily locked file read as EMPTY, and the next accrual or even a page view then wrote
back a store holding only one account — every other account's history gone), written with a bare, non-atomic
write_text, with no lock (two accruals lost one; two payouts could both pass the balance check), and a GET wrote
the file. Now: every change is a read-modify-write under the store lock with an atomic write; the read is STRICT —
a store that exists but cannot be read is refused (OwnerPaymentsUnavailable) and never overwritten; status() only
reads, and an account that has never accrued is answered as zeros without creating it.
"""
from __future__ import annotations

import json
import math
import time
import uuid
from typing import Any, Callable, Dict

from agentic_core.config import data_path

_STORE = data_path("economy_owner_payments.json")

# BINDING SAFEGUARD — real-money payout rails are OFF until the Owner explicitly authorises them AND a
# compliance/KYC review passes. Until then every payout is a virtual ledger entry; no real funds move.
REAL_MONEY_ENABLED = False


class OwnerPaymentsUnavailable(RuntimeError):
    """The owner-payments store exists but cannot be read (or is not an owner-payments document). Nothing was
    written; the caller answers honestly (503) instead of reporting zero balances."""


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _number(v: Any) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(float(v))


def _account_ok(a: Any) -> bool:
    return (isinstance(a, dict) and _number(a.get("accrued")) and _number(a.get("paid_out"))
            and isinstance(a.get("entries"), list))


def _read() -> Dict[str, Any]:
    """STRICT read: a missing store is empty; anything else that cannot be read whole is refused."""
    if not _STORE.exists():
        return {}
    raw = None
    for attempt in range(5):
        try:
            raw = _STORE.read_text(encoding="utf-8")
            break
        except FileNotFoundError:
            return {}
        except UnicodeDecodeError as e:       # not an OSError: without this a re-encoded store escaped as a 500/400
            raise OwnerPaymentsUnavailable(f"the owner-payments store is not valid UTF-8 ({e}); nothing was written") from e
        except PermissionError as e:          # Windows: a read that meets an atomic replace mid-flight — retry
            if attempt == 4:
                raise OwnerPaymentsUnavailable(f"the owner-payments store stayed locked ({e})") from e
            time.sleep(0.05 * (attempt + 1))
        except OSError as e:
            raise OwnerPaymentsUnavailable(f"the owner-payments store could not be read ({e})") from e
    try:
        d = json.loads(raw)
    except ValueError as e:
        raise OwnerPaymentsUnavailable(f"the owner-payments store is unreadable ({e}); nothing was written") from e
    if not isinstance(d, dict) or not all(_account_ok(a) for a in d.values()):
        raise OwnerPaymentsUnavailable("the owner-payments store is not an owner-payments document; nothing was written")
    return d


def _mutate(change: Callable[[Dict[str, Any]], Any]) -> Any:
    """Read-modify-write under the store lock. `change` raises to refuse (nothing is written); it must not call
    anything that takes this lock again (store_lock is not re-entrant on its lockfile)."""
    from agentic_core.config import atomic_write_json, store_lock
    with store_lock(_STORE):
        d = _read()
        out = change(d)
        atomic_write_json(_STORE, d)
    return out


def _new_account(vsb_id: str, owner: str) -> Dict[str, Any]:
    return {"vsb_id": vsb_id, "owner": owner, "currency": "WST", "accrued": 0.0, "paid_out": 0.0, "entries": []}


def accrue(vsb_id: str, amount: float, owner: str = "Rehan", memo: str = "cycle owner share") -> Dict[str, Any] | None:
    """Accrue the Owner's share from a cycle (virtual WST). Returns the account, or None for a zero amount.
    Raises ValueError for a non-finite amount and OwnerPaymentsUnavailable / TimeoutError when the store cannot be
    read or locked — the caller must say so (an accrual is never silently dropped)."""
    if not math.isfinite(float(amount)):
        raise ValueError("An owner accrual must be a finite amount.")
    amount = round(max(0.0, float(amount)), 2)
    if amount <= 0:
        return None

    def change(d: Dict[str, Any]) -> Dict[str, Any]:
        a = d.get(vsb_id) or _new_account(vsb_id, owner)
        d[vsb_id] = a
        a["accrued"] = round(a["accrued"] + amount, 2)
        a["entries"].append({"id": uuid.uuid4().hex[:8], "type": "accrual",
                             "amount_wst": amount, "memo": memo, "at": _now()})
        a["entries"] = a["entries"][-200:]
        return json.loads(json.dumps(a))
    return _mutate(change)


def status(vsb_id: str, owner: str = "Rehan") -> Dict[str, Any]:
    """READ-ONLY: the account as stored, or zeros for an account that has never accrued (nothing is created)."""
    a = _read().get(vsb_id) or _new_account(vsb_id, owner)
    balance = round(a["accrued"] - a["paid_out"], 2)
    return {
        "vsb_id": vsb_id, "owner": a.get("owner", owner), "currency": "WST",
        "accrued_total_wst": a["accrued"], "paid_out_total_wst": a["paid_out"],
        "balance_wst": balance, "entries": a["entries"][-50:][::-1],
        "real_money_rails": "DISABLED", "real_money_enabled": REAL_MONEY_ENABLED,
        "note": "Virtual/simulated WST only. Real-money payouts are gated until the Owner explicitly "
                "authorises real rails AND a compliance/KYC review passes — no real funds move.",
    }


def payout(vsb_id: str, amount: float, owner: str = "Rehan") -> Dict[str, Any]:
    """Record a VIRTUAL payout (reduces the accrued balance). Never moves real funds — rails are disabled. The
    balance check and the write happen under one lock, so two payouts can never both spend the same balance."""
    if not math.isfinite(float(amount)):
        raise ValueError("Payout amount must be a finite number.")
    amount = round(max(0.0, float(amount)), 2)
    if amount <= 0:
        raise ValueError("Payout amount must be positive.")

    def change(d: Dict[str, Any]) -> float:
        a = d.get(vsb_id)
        balance = round(a["accrued"] - a["paid_out"], 2) if a else 0.0
        if amount > balance:
            raise ValueError(f"Insufficient balance: {balance} WST available, {amount} WST requested.")
        a["paid_out"] = round(a["paid_out"] + amount, 2)
        a["entries"].append({"id": uuid.uuid4().hex[:8], "type": "payout_virtual", "amount_wst": amount,
                             "memo": "virtual payout — no real funds moved (rails disabled)", "at": _now()})
        a["entries"] = a["entries"][-200:]
        return round(a["accrued"] - a["paid_out"], 2)
    remaining = _mutate(change)
    return {
        "paid_wst": amount, "remaining_balance_wst": remaining,
        "real_money_moved": False, "real_money_rails": "DISABLED",
        "note": "Virtual payout recorded. No real money moved — real rails are gated pending Owner "
                "authorisation + a compliance/KYC review.",
    }
