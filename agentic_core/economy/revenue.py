"""
Revenue recognition (§12×§5×§7, W293) — the economic organism is fed by the enterprise's REAL work.

Before this module, the autonomous economy ran on a fabricated flat 1000-WST-per-tick constant:
the delivery org's actual work never funded anything, and marketplace WST sales never reached any
VSB's books. Now every economic event is RECORDED when the real activity happens and CONSUMED
(exactly once) by the entity's next autonomous cycle:

  - marketplace_sale   — a buyer's WST spend on a VSB-attributed listing (the same amount the
                         TokenLedger deducted from the buyer is recognised as the seller's revenue —
                         two ledgers, one flow, counted once per side).
  - cascade_delivery   — a QMS-PASSED, VSB-scoped org-cascade delivery earns the DECLARED simulated
                         tariff (virtual WST — an honest simulation constant, never real money);
                         its cost side is the W271 BMS estimate for the run.

With NO recorded events, the next cycle is an honest ZERO-revenue maintenance cycle — the organism
still tends the entity (governed), but distributes only what real activity brought. Never fabricated.
Virtual/simulated WST only; real-money rails remain Owner-gated.
"""
from __future__ import annotations

import time
import uuid
from typing import Any, Dict

from agentic_core.config import atomic_write_json, data_path, load_json_tolerant

_STORE = data_path("revenue_events.json")

# DECLARED simulation constants (virtual WST) — labelled at every use, never presented as real.
SIM_DELIVERY_TARIFF_WST = 250.0     # earned per QMS-passed, VSB-scoped cascade delivery


def _load() -> list:
    return load_json_tolerant(_STORE, []) or []


def record_event(vsb_id: str, kind: str, amount_wst: float, source: str, ref: str = "",
                 note: str = "") -> Dict[str, Any]:
    """Append one economic event (kind: revenue | cost; VIRTUAL simulated WST only).
    §12 (W349) — the append is SERIALISED: the Round-10 concurrency audit measured 89% of
    recorded events destroyed under concurrent writers (unserialised load-modify-write clobbered
    the store). The cross-process store_lock makes recording exactly-once."""
    from agentic_core.config import store_lock
    ev = {"id": f"rev-{uuid.uuid4().hex[:10]}", "vsb_id": vsb_id, "kind": kind,
          "amount_wst": round(float(amount_wst), 6), "source": source, "ref": ref,
          "note": note, "consumed": False,
          "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    with store_lock(_STORE):
        rows = _load()
        rows.append(ev)
        atomic_write_json(_STORE, rows[-2000:])
    return ev


def peek_pending(vsb_id: str) -> Dict[str, Any]:
    """§12 (W313) — NON-CONSUMING view of a VSB's pending intake, with the exact event ids.
    The governed cycle peeks first and consumes ONLY after every gate passes — a materiality or
    policy hold must PRESERVE the recognised revenue it holds, never destroy it."""
    revenue = costs = 0.0
    sources: Dict[str, int] = {}
    ids = []
    for ev in _load():
        if ev.get("vsb_id") == vsb_id and not ev.get("consumed"):
            if ev.get("kind") == "revenue":
                revenue += float(ev.get("amount_wst") or 0.0)
            else:
                costs += float(ev.get("amount_wst") or 0.0)
            sources[ev.get("source", "?")] = sources.get(ev.get("source", "?"), 0) + 1
            ids.append(ev["id"])
    return {"revenue": round(revenue, 6), "costs": round(costs, 6), "events": len(ids),
            "sources": sources, "ids": ids}


def consume_events(vsb_id: str, ids: list) -> Dict[str, Any]:
    """Consume (exactly once) the SPECIFIC events a passed cycle recognised — the ids its peek saw.
    Events that arrived after the peek stay pending for the next cycle (never silently absorbed).
    §12 (W349) — serialised under the same store lock so exactly-once genuinely holds."""
    from agentic_core.config import store_lock
    want = set(ids or [])
    with store_lock(_STORE):
        return _consume_locked(vsb_id, want)


def _consume_locked(vsb_id: str, want: set) -> Dict[str, Any]:
    rows = _load()
    revenue = costs = 0.0
    sources: Dict[str, int] = {}
    n = 0
    for ev in rows:
        if ev.get("id") in want and ev.get("vsb_id") == vsb_id and not ev.get("consumed"):
            if ev.get("kind") == "revenue":
                revenue += float(ev.get("amount_wst") or 0.0)
            else:
                costs += float(ev.get("amount_wst") or 0.0)
            sources[ev.get("source", "?")] = sources.get(ev.get("source", "?"), 0) + 1
            ev["consumed"] = True
            ev["consumed_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            n += 1
    if n:
        atomic_write_json(_STORE, rows[-2000:])
    return {"revenue": round(revenue, 6), "costs": round(costs, 6), "events": n, "sources": sources}


def consume_pending(vsb_id: str) -> Dict[str, Any]:
    """Consume (exactly once) all pending events for a VSB → the next cycle's REAL intake.
    Returns {"revenue": X, "costs": Y, "events": n, "sources": {...}}.
    §12 (W349) — serialised: two concurrent consumers previously both read the same pending set."""
    from agentic_core.config import store_lock
    with store_lock(_STORE):
        return _consume_pending_locked(vsb_id)


def _consume_pending_locked(vsb_id: str) -> Dict[str, Any]:
    rows = _load()
    revenue = costs = 0.0
    sources: Dict[str, int] = {}
    n = 0
    for ev in rows:
        if ev.get("vsb_id") == vsb_id and not ev.get("consumed"):
            if ev.get("kind") == "revenue":
                revenue += float(ev.get("amount_wst") or 0.0)
            else:
                costs += float(ev.get("amount_wst") or 0.0)
            sources[ev.get("source", "?")] = sources.get(ev.get("source", "?"), 0) + 1
            ev["consumed"] = True
            ev["consumed_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            n += 1
    if n:
        atomic_write_json(_STORE, rows[-2000:])
    return {"revenue": round(revenue, 6), "costs": round(costs, 6), "events": n, "sources": sources}


def pending_summary(vsb_id: str | None = None) -> Dict[str, Any]:
    """Read-only view of unconsumed events (all VSBs, or one)."""
    rows = [e for e in _load() if not e.get("consumed")
            and (vsb_id is None or e.get("vsb_id") == vsb_id)]
    return {"pending_events": len(rows),
            "pending_revenue_wst": round(sum(e["amount_wst"] for e in rows if e["kind"] == "revenue"), 6),
            "pending_cost_wst": round(sum(e["amount_wst"] for e in rows if e["kind"] == "cost"), 6),
            "events": rows[-50:]}
