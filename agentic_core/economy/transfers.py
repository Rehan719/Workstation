"""Inter-VSB transfers (§federation seed) — generated Enterprise IDBOs TRANSACT with each other.

Semantics (virtual WST only — no real funds, real-money rails stay Owner-gated):
  • The SENDER pays from its reserve fund — a balanced double-entry posting
    (Dr transfer_out expense / Cr reserve_fund), refused when the fund can't cover it
    (no negative virtual balances, no money from nothing).
  • The RECEIVER's amount queues as PENDING and is consumed by its NEXT metabolic cycle as
    intake revenue — so the received WST genuinely enters the receiver's §4 waterfall
    (the same recycle pattern as venture returns, W259).
  • The receiver must be a REGISTERED living VSB (no transfers into the void).
"""
from __future__ import annotations

import time
import uuid
from typing import Any, Dict

from agentic_core.config import atomic_write_json, data_path, load_json_tolerant

_PENDING_STORE = data_path("economy_pending_transfers.json")


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def validate_transfer(from_vsb: str, to_vsb: str, amount: float) -> float:
    """Side-effect-free validation (callable BEFORE the governance gate so errors map to clean HTTP
    codes). Raises ValueError (→400) on bad amounts/self-transfer/insufficient funds, KeyError
    (→404) when the receiver is not a registered living VSB. Returns the rounded amount."""
    amount = round(float(amount), 2)
    if amount <= 0:
        raise ValueError("Transfer amount must be positive.")
    if from_vsb == to_vsb:
        raise ValueError("A VSB cannot transfer to itself.")
    from agentic_core.economy.living_vsbs import _load as _living
    if to_vsb not in _living():
        raise KeyError(f"Receiver '{to_vsb}' is not a registered living VSB — no transfers into the void.")
    from agentic_core.economy.ledger import VirtualLedger
    reserve = round((VirtualLedger(from_vsb)._data.get("accounts") or {}).get("reserve_fund", 0.0), 2)
    if reserve < amount:
        raise ValueError(f"Insufficient virtual funds: {from_vsb} reserve fund holds {reserve} WST "
                         f"< transfer {amount} WST.")
    return amount


def record_transfer(from_vsb: str, to_vsb: str, amount: float, memo: str = "") -> Dict[str, Any]:
    """One inter-VSB transfer: validates (see validate_transfer), posts the sender's books, queues
    the receiver's intake. Virtual funds are conserved — nothing created, nothing negative."""
    amount = validate_transfer(from_vsb, to_vsb, amount)
    from agentic_core.economy.ledger import VirtualLedger
    sender = VirtualLedger(from_vsb)
    reserve = round((sender._data.get("accounts") or {}).get("reserve_fund", 0.0), 2)
    transfer_id = f"xfer-{uuid.uuid4().hex[:10]}"
    sender.post("transfer_out", "reserve_fund", amount,
                memo=f"inter-VSB transfer → {to_vsb} ({transfer_id})" + (f" — {memo}" if memo else ""))

    # queue the receiver's intake (consumed by its next metabolic cycle → enters its waterfall)
    d = load_json_tolerant(_PENDING_STORE, {}) or {}
    rec = d.get(to_vsb) or {"vsb_id": to_vsb, "pending_wst": 0.0, "transfers": []}
    rec["pending_wst"] = round(rec.get("pending_wst", 0.0) + amount, 2)
    rec["transfers"] = (rec.get("transfers") or [])[-49:] + [{
        "transfer_id": transfer_id, "from_vsb": from_vsb, "amount_wst": amount,
        "memo": memo, "at": _now()}]
    d[to_vsb] = rec
    atomic_write_json(_PENDING_STORE, d)

    return {
        "transfer_id": transfer_id, "from_vsb": from_vsb, "to_vsb": to_vsb,
        "amount_wst": amount, "memo": memo, "at": _now(),
        "sender_reserve_fund_after_wst": round(reserve - amount, 2),
        "receiver_pending_wst": rec["pending_wst"],
        "settlement": "the receiver's next metabolic cycle consumes this as intake revenue "
                      "(enters its §4 waterfall)",
        "disclaimer": "Virtual/simulated WST — no real funds moved.",
    }


def consume_pending_transfers(vsb_id: str) -> float:
    """Drain the queued inter-VSB receipts for a VSB — called by the metabolic cycle at intake.
    Returns the consumed amount (0.0 when none pending)."""
    d = load_json_tolerant(_PENDING_STORE, {}) or {}
    rec = d.get(vsb_id)
    if not rec:
        return 0.0
    pending = round(rec.get("pending_wst", 0.0), 2)
    if pending <= 0:
        return 0.0
    rec["pending_wst"] = 0.0
    rec["consumed_total_wst"] = round(rec.get("consumed_total_wst", 0.0) + pending, 2)
    d[vsb_id] = rec
    atomic_write_json(_PENDING_STORE, d)
    return pending
