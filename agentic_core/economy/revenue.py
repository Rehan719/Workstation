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

import math
import time
import uuid
from typing import Any, Dict, List, Optional

from agentic_core.config import atomic_write_json, data_path, load_json_tolerant, store_lock

_STORE = data_path("revenue_events.json")
_CAP = 2000


class RevenueStoreUnavailable(RuntimeError):
    """W467 (register FU-043) — the revenue-events store exists but cannot be read whole. Nothing is written."""

# DECLARED simulation constants (virtual WST) — labelled at every use, never presented as real.
SIM_DELIVERY_TARIFF_WST = 250.0     # earned per QMS-passed, VSB-scoped cascade delivery


def _load() -> list:
    """Tolerant read — READ-ONLY summaries only (pending_summary). Writers and the governed peek use _read_rows."""
    return load_json_tolerant(_STORE, []) or []


def _event_ok(ev: Any) -> bool:
    if not (isinstance(ev, dict) and isinstance(ev.get("id"), str) and isinstance(ev.get("vsb_id"), str)):
        return False
    amount = ev.get("amount_wst")
    if isinstance(amount, bool) or not isinstance(amount, (int, float)):
        return False
    try:
        return math.isfinite(amount) and isinstance(ev.get("consumed", False), bool)
    except OverflowError:
        return False


def _read_rows() -> List[Dict[str, Any]]:
    """W467 (register FU-043) — STRICT read for every writer and for the governed peek. The tolerant read answered []
    for a store it could not read (a BOM, a re-encoding, a partial write), and the next record_event wrote one event
    back over every recognised event (reproduced: 1 of 2000 kept)."""
    import json as _json
    if not _STORE.exists():
        return []
    raw = None
    for attempt in range(5):
        try:
            raw = _STORE.read_text(encoding="utf-8")
            break
        except FileNotFoundError:
            return []
        except UnicodeDecodeError as e:
            raise RevenueStoreUnavailable(f"the revenue-events store is not valid UTF-8 ({e}); nothing was written") from e
        except PermissionError as e:
            if attempt == 4:
                raise RevenueStoreUnavailable(f"the revenue-events store stayed locked ({e})") from e
            time.sleep(0.05 * (attempt + 1))
        except OSError as e:
            raise RevenueStoreUnavailable(f"the revenue-events store could not be read ({e})") from e
    try:
        rows = _json.loads(raw)
    except ValueError as e:
        raise RevenueStoreUnavailable(f"the revenue-events store is unreadable ({e}); nothing was written") from e
    if not isinstance(rows, list) or not all(_event_ok(ev) for ev in rows):
        raise RevenueStoreUnavailable("the revenue-events store holds something that is not an event list; nothing "
                                      "was written")
    return rows


def _trim(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """W467 (register FU-043) — the cap drops only CONSUMED events, oldest first. It used to drop the oldest rows
    whatever their state, so a held entity's pending revenue vanished once 2000 newer events existed anywhere."""
    excess = len(rows) - _CAP
    if excess <= 0:
        return rows
    kept: List[Dict[str, Any]] = []
    for ev in rows:
        # W467 (refutation) — an event a cycle consumed and has not settled (it still carries the cycle's token) is in
        # flight: dropping it would leave that cycle nothing to give back if its first ledger write then fails
        if excess > 0 and ev.get("consumed") and not ev.get("consume_token"):
            excess -= 1
            continue
        kept.append(ev)
    return kept


def record_event(vsb_id: str, kind: str, amount_wst: float, source: str, ref: str = "",
                 note: str = "") -> Dict[str, Any]:
    """Append one economic event (kind: revenue | cost; VIRTUAL simulated WST only).
    §12 (W349) — the append is SERIALISED: the Round-10 concurrency audit measured 89% of
    recorded events destroyed under concurrent writers (unserialised load-modify-write clobbered
    the store). The cross-process store_lock makes recording exactly-once."""
    ev = {"id": f"rev-{uuid.uuid4().hex[:10]}", "vsb_id": vsb_id, "kind": kind,
          "amount_wst": round(float(amount_wst), 6), "source": source, "ref": ref,
          "note": note, "consumed": False,
          "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    with store_lock(_STORE):
        rows = _read_rows()
        rows.append(ev)
        atomic_write_json(_STORE, _trim(rows))
    return ev


def peek_pending(vsb_id: str) -> Dict[str, Any]:
    """§12 (W313) — NON-CONSUMING view of a VSB's pending intake, with the exact event ids.
    The governed cycle peeks first and consumes ONLY after every gate passes — a materiality or
    policy hold must PRESERVE the recognised revenue it holds, never destroy it."""
    revenue = costs = 0.0
    sources: Dict[str, int] = {}
    ids = []
    items: Dict[str, Dict[str, Any]] = {}
    for ev in _read_rows():
        if ev.get("vsb_id") == vsb_id and not ev.get("consumed"):
            if ev.get("kind") == "revenue":
                revenue += float(ev.get("amount_wst") or 0.0)
            else:
                costs += float(ev.get("amount_wst") or 0.0)
            sources[ev.get("source", "?")] = sources.get(ev.get("source", "?"), 0) + 1
            ids.append(ev["id"])
            # W463 — per-event amounts, so a governed cycle can release exactly the events an approval names
            items[ev["id"]] = {"kind": ev.get("kind"), "amount_wst": float(ev.get("amount_wst") or 0.0)}
    return {"revenue": round(revenue, 6), "costs": round(costs, 6), "events": len(ids),
            "sources": sources, "ids": ids, "items": items}


def consume_events(vsb_id: str, ids: list, token: Optional[str] = None) -> Dict[str, Any]:
    """Consume (exactly once) the SPECIFIC events a passed cycle recognised — the ids its peek saw.
    Events that arrived after the peek stay pending for the next cycle (never silently absorbed).
    §12 (W349) — serialised under the same store lock so exactly-once genuinely holds.

    W467 (register FU-022) — a governed cycle consumes BEFORE it runs, under a `token` stamped on each event it flips,
    and the answer names exactly the ids it flipped (`ids`), so a cycle that then writes nothing can give back exactly
    its own events (unconsume_events)."""
    want = set(ids or [])
    with store_lock(_STORE):
        return _consume_locked(vsb_id, want, token)


def _consume_locked(vsb_id: str, want: set, token: Optional[str] = None) -> Dict[str, Any]:
    rows = _read_rows()
    revenue = costs = 0.0
    sources: Dict[str, int] = {}
    flipped: List[str] = []
    for ev in rows:
        if ev.get("id") in want and ev.get("vsb_id") == vsb_id and not ev.get("consumed"):
            if ev.get("kind") == "revenue":
                revenue += float(ev.get("amount_wst") or 0.0)
            else:
                costs += float(ev.get("amount_wst") or 0.0)
            sources[ev.get("source", "?")] = sources.get(ev.get("source", "?"), 0) + 1
            ev["consumed"] = True
            ev["consumed_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            if token:
                ev["consume_token"] = token
            flipped.append(ev["id"])
    if flipped:
        atomic_write_json(_STORE, _trim(rows))
    return {"revenue": round(revenue, 6), "costs": round(costs, 6), "events": len(flipped), "sources": sources,
            "ids": flipped}


def unconsume_events(vsb_id: str, token: str) -> Dict[str, Any]:
    """W467 (register FU-022) — give back the events ONE cycle consumed (those stamped with its token) when that cycle
    wrote nothing to the ledger. Events another consumer took are never touched."""
    if not token:
        return {"events": 0, "ids": []}
    with store_lock(_STORE):
        rows = _read_rows()
        back: List[str] = []
        for ev in rows:
            if ev.get("vsb_id") == vsb_id and ev.get("consumed") and ev.get("consume_token") == token:
                ev["consumed"] = False
                ev.pop("consumed_at", None)
                ev.pop("consume_token", None)
                back.append(ev["id"])
        if back:
            atomic_write_json(_STORE, _trim(rows))
    return {"events": len(back), "ids": back}


def settle_consume_token(vsb_id: str, token: str) -> int:
    """W467 (refutation) — a cycle that wrote its ledger settles its consume: the token is cleared (the events stay
    consumed), so the cap may drop them in time. A settle that fails only keeps them longer."""
    if not token:
        return 0
    with store_lock(_STORE):
        rows = _read_rows()
        n = 0
        for ev in rows:
            if ev.get("vsb_id") == vsb_id and ev.get("consume_token") == token:
                ev.pop("consume_token", None)
                n += 1
        if n:
            atomic_write_json(_STORE, _trim(rows))
    return n


def reconcile_stranded_consumes(min_age_s: float = 900.0) -> Dict[str, Any]:
    """W467 (refutation) — a cycle consumes its events BEFORE it runs; a process that died between that consume and the
    cycle's first ledger write left them consumed and never distributed, with nothing to find them. A consume still
    carrying a cycle token older than `min_age_s` is checked against its VSB's ledger (read strictly): an intake entry
    stamped with that token means the cycle posted — the token is settled; no such entry means nothing was posted —
    the events are given back to pending (economy.cycle_intake_reconciled). An unreadable ledger is skipped. A spent
    approval is left as it is (unmarked, it reads as still in flight — the restrictive side; the next cycle asks the
    Owner again)."""
    import calendar as _cal
    from agentic_core.economy.transfers import _ledger_path, _read_ledger_strict
    from agentic_core.economy.governance import _ueg_log
    report: Dict[str, Any] = {"stranded": 0, "given_back": 0, "settled": 0, "ledgers_unreadable": 0}
    now = time.time()
    groups: Dict[tuple, List[Dict[str, Any]]] = {}
    for ev in _read_rows():
        tok = ev.get("consume_token")
        if not (ev.get("consumed") and isinstance(tok, str) and tok.startswith("cyc-")):
            continue
        try:
            age = now - _cal.timegm(time.strptime(str(ev.get("consumed_at")), "%Y-%m-%dT%H:%M:%SZ"))
        except (ValueError, OverflowError):
            continue
        if age >= min_age_s:
            groups.setdefault((ev["vsb_id"], tok), []).append(ev)
    for (vsb_id, tok), evs in groups.items():
        report["stranded"] += 1
        path = _ledger_path(vsb_id)
        try:
            entries = _read_ledger_strict(path).get("entries", []) if path.exists() else []
        except Exception:
            report["ledgers_unreadable"] += 1
            continue
        if any(isinstance(e, dict) and e.get("ref") == tok for e in entries):
            settle_consume_token(vsb_id, tok)
            report["settled"] += 1
            try:        # a hold filed for events that were in fact distributed is retired now, not on some later cycle
                from agentic_core.economy.governance import retire_heartbeat_holds_for_consumed_events
                retire_heartbeat_holds_for_consumed_events(vsb_id)
            except Exception:
                pass
            continue
        back = unconsume_events(vsb_id, tok)
        report["given_back"] += 1
        _ueg_log({"type": "economy.cycle_intake_reconciled", "vsb_id": vsb_id, "token": tok, "event_ids": back["ids"],
                  "revenue_wst": round(sum(float(e.get("amount_wst") or 0.0) for e in evs if e.get("kind") == "revenue"), 6),
                  "note": "a cycle consumed these events and never wrote its ledger (its process stopped, or its "
                          "own give-back failed); they are pending again for the next cycle",
                  "disclaimer": "Virtual/simulated WST — no real funds moved."})
    return report


def consume_pending(vsb_id: str) -> Dict[str, Any]:
    """Consume (exactly once) all pending events for a VSB → the next cycle's REAL intake.
    Returns {"revenue": X, "costs": Y, "events": n, "sources": {...}}.
    §12 (W349) — serialised: two concurrent consumers previously both read the same pending set."""
    with store_lock(_STORE):
        return _consume_pending_locked(vsb_id)


def _consume_pending_locked(vsb_id: str) -> Dict[str, Any]:
    rows = _read_rows()
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
        atomic_write_json(_STORE, _trim(rows))
    return {"revenue": round(revenue, 6), "costs": round(costs, 6), "events": n, "sources": sources}


def pending_summary(vsb_id: str | None = None) -> Dict[str, Any]:
    """Read-only view of unconsumed events (all VSBs, or one)."""
    rows = [e for e in _load() if not e.get("consumed")
            and (vsb_id is None or e.get("vsb_id") == vsb_id)]
    return {"pending_events": len(rows),
            "pending_revenue_wst": round(sum(e["amount_wst"] for e in rows if e["kind"] == "revenue"), 6),
            "pending_cost_wst": round(sum(e["amount_wst"] for e in rows if e["kind"] == "cost"), 6),
            "events": rows[-50:]}
