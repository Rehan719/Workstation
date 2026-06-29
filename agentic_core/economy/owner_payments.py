"""
Owner-Payments Ledger (§7) — the Owner's accrued share, VIRTUAL/simulated WST only.

Each metabolic cycle's Owner stage (the §4 waterfall's `owner` split) accrues here. The Owner can record a
payout, but **real-money rails are intentionally DISABLED and gated**: no real funds move — a payout is a
virtual ledger entry until the Owner explicitly authorises real rails AND a compliance/KYC review passes.
This keeps a clean seam so real rails can be added later behind that gate, without ever representing simulated
finance as real.
"""
from __future__ import annotations

import json
import time
import uuid
from typing import Any, Dict

from agentic_core.config import data_path

_STORE = data_path("economy_owner_payments.json")

# BINDING SAFEGUARD — real-money payout rails are OFF until the Owner explicitly authorises them AND a
# compliance/KYC review passes. Until then every payout is a virtual ledger entry; no real funds move.
REAL_MONEY_ENABLED = False


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _load() -> Dict[str, Any]:
    try:
        return json.loads(_STORE.read_text()) if _STORE.exists() else {}
    except Exception:
        return {}


def _save(d: Dict[str, Any]) -> None:
    _STORE.parent.mkdir(parents=True, exist_ok=True)
    _STORE.write_text(json.dumps(d, indent=2))


def _account(d: Dict[str, Any], vsb_id: str, owner: str) -> Dict[str, Any]:
    a = d.get(vsb_id)
    if not a:
        a = {"vsb_id": vsb_id, "owner": owner, "currency": "WST",
             "accrued": 0.0, "paid_out": 0.0, "entries": []}
        d[vsb_id] = a
    return a


def accrue(vsb_id: str, amount: float, owner: str = "Rehan", memo: str = "cycle owner share") -> Dict[str, Any] | None:
    """Accrue the Owner's share from a cycle (virtual WST). Returns the account, or None for a zero amount."""
    amount = round(max(0.0, float(amount)), 2)
    if amount <= 0:
        return None
    d = _load()
    a = _account(d, vsb_id, owner)
    a["accrued"] = round(a["accrued"] + amount, 2)
    a["entries"].append({"id": uuid.uuid4().hex[:8], "type": "accrual",
                         "amount_wst": amount, "memo": memo, "at": _now()})
    a["entries"] = a["entries"][-200:]
    _save(d)
    return a


def status(vsb_id: str, owner: str = "Rehan") -> Dict[str, Any]:
    d = _load()
    a = _account(d, vsb_id, owner)
    _save(d)
    balance = round(a["accrued"] - a["paid_out"], 2)
    return {
        "vsb_id": vsb_id, "owner": a["owner"], "currency": "WST",
        "accrued_total_wst": a["accrued"], "paid_out_total_wst": a["paid_out"],
        "balance_wst": balance, "entries": a["entries"][-50:][::-1],
        "real_money_rails": "DISABLED", "real_money_enabled": REAL_MONEY_ENABLED,
        "note": "Virtual/simulated WST only. Real-money payouts are gated until the Owner explicitly "
                "authorises real rails AND a compliance/KYC review passes — no real funds move.",
    }


def payout(vsb_id: str, amount: float, owner: str = "Rehan") -> Dict[str, Any]:
    """Record a VIRTUAL payout (reduces the accrued balance). Never moves real funds — rails are disabled."""
    amount = round(max(0.0, float(amount)), 2)
    if amount <= 0:
        raise ValueError("Payout amount must be positive.")
    d = _load()
    a = _account(d, vsb_id, owner)
    balance = round(a["accrued"] - a["paid_out"], 2)
    if amount > balance:
        raise ValueError(f"Insufficient balance: {balance} WST available, {amount} WST requested.")
    a["paid_out"] = round(a["paid_out"] + amount, 2)
    a["entries"].append({"id": uuid.uuid4().hex[:8], "type": "payout_virtual", "amount_wst": amount,
                         "memo": "virtual payout — no real funds moved (rails disabled)", "at": _now()})
    a["entries"] = a["entries"][-200:]
    _save(d)
    return {
        "paid_wst": amount, "remaining_balance_wst": round(a["accrued"] - a["paid_out"], 2),
        "real_money_moved": False, "real_money_rails": "DISABLED",
        "note": "Virtual payout recorded. No real money moved — real rails are gated pending Owner "
                "authorisation + a compliance/KYC review.",
    }
