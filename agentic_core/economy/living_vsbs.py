"""
Living-VSB registry (§4) — established VSB IDBO enterprises that the organism tends AUTONOMOUSLY.

When a VSB is established (Genesis /establish), it is registered here. The circadian heartbeat then
periodically runs a light, paced operating tick — `operate_one()` runs ONE virtual economy cycle for the
least-recently-operated VSB (round-robin) — so each established enterprise "continually, intelligently and
autonomously operates" forever, led by the Chief. Cheap + deterministic (no AI) + virtual WST only; richer
self-improvement/evolution is handled by the Sovereign Evolution Office and the metabolism's `tune()`.
"""
from __future__ import annotations

import json
import time
from typing import Any, Dict, List, Optional

from agentic_core.config import atomic_write_json, data_path

_STORE = data_path("living_vsbs.json")


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _load() -> Dict[str, Any]:
    try:
        return json.loads(_STORE.read_text()) if _STORE.exists() else {}
    except Exception:
        return {}


def _save(d: Dict[str, Any]) -> None:
    _STORE.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_json(_STORE, d)


def register(vsb_id: str, name: str = "", entity_type: str = "waqf_ltd_hybrid",
             domain: str = "enterprise", owner: str = "Rehan") -> Dict[str, Any]:
    """Register an established VSB as a living entity the organism will autonomously tend.
    §12 (W349) — serialised: the Round-10 concurrency audit lost 28 of 32 concurrent
    registrations to the unserialised load-modify-write."""
    from agentic_core.config import store_lock
    with store_lock(_STORE):
        d = _load()
        if vsb_id not in d:
            d[vsb_id] = {"vsb_id": vsb_id, "name": name or vsb_id, "entity_type": entity_type,
                         "domain": domain, "owner": owner, "registered_at": _now(),
                         "operating_cycles": 0, "last_operated": None, "status": "living"}
            _save(d)
        return d[vsb_id]


def deregister(vsb_id: str) -> bool:
    """Remove an entity from the autonomous operating roster. Returns True if it was there.

    W417 — this module could register a VSB into the roster but never remove one, so anything that
    ever registered was tended by the organism forever. By 2026-08-31 the roster held 191 entries of
    which 157 were pytest fixtures, and the heartbeat had run 2,113 operating cycles round-robin —
    so the Owner's own entities received about a sixth of the attention while the rest went to test
    data. Deregistering does not delete the entity; it only stops the organism tending it.
    """
    d = _load()
    if vsb_id not in d:
        return False
    del d[vsb_id]
    _save(d)
    return True


def list_living() -> Dict[str, Any]:
    """§11 × §13 (W421) — each row now carries the entity's LIVE compliance standing and any economic
    hold it causes. Both existed only as side effects before: `_latest_screen` was read by
    `operate_vsb` to decide a hold, and the hold was written to the store and the UEG — but the
    entity's OWNER had no way to see either. A held enterprise looked simply idle."""
    d = _load()
    rows = sorted(d.values(), key=lambda v: v.get("registered_at", ""), reverse=True)
    try:
        from agentic_core.config import data_path, load_json_tolerant
        hist = load_json_tolerant(data_path("vsb_compliance_history.json"), {}) or {}
    except Exception:
        hist = {}
    for r in rows:
        h = hist.get(r.get("vsb_id")) or {}
        verdict = h.get("overall")
        r["compliance"] = {
            # None means NOT YET SCREENED — never rendered as a pass. An entity established before
            # auto_compliance was switched on has no verdict, and that is different from a clean one.
            "verdict": verdict,
            "screened_at": h.get("screened_at") or h.get("at"),
            "verdicts": h.get("verdicts") or [],
            "never_screened": not bool(verdict),
        }
        r["economy_held"] = {
            "held": bool(r.get("last_hold")),
            "reason": r.get("last_hold"),
            "consequence": ("distributions are held — no economy cycle runs until a re-screen clears it"
                            if r.get("last_hold") == "compliance_fail_hold"
                            else ("this entity's cycle is held by governance" if r.get("last_hold") else None)),
        }
    return {"living_vsbs": rows, "total": len(rows),
            "note": "Established VSB enterprises the organism autonomously tends (paced virtual economy "
                    "cycles on the circadian heartbeat). Virtual/simulated — no real funds."}


def operate_one() -> Optional[Dict[str, Any]]:
    """Autonomously operate the least-recently-operated living VSB: one virtual economy cycle. Round-robin,
    paced by the heartbeat. Returns a compact record, or None when there are no living VSBs. Best-effort."""
    d = _load()
    if not d:
        return None
    # pick the least-recently-operated (None sorts first). §8 (W340) — FAIR under bursts: the
    # second-resolution timestamps tie when beats fire sub-second (the audit observed 23×/8×/7×
    # starvation), so ties break by FEWEST operating cycles, then registration order — every
    # entity gets tended even under a burst of manual beats.
    target = sorted(d.values(), key=lambda v: (v.get("last_operated") or "",
                                               int(v.get("operating_cycles", 0)),
                                               v.get("registered_at", "")))[0]
    return operate_vsb(target["vsb_id"])


DEV_SPEND_WST = 50.0   # §12 (W330) — the per-action development cost drawn from self_investment


def spend_self_investment(vsb_id: str, purpose: str, amount: float = DEV_SPEND_WST) -> Dict[str, Any]:
    """§12 (W330) — 'reinvests in its own growth' becomes REAL: the waterfall's self_investment
    stage was the only stage with no consumer (pure accounting). The entity's OWN development
    actions (autonomous evolution · repo re-ship) now SPEND from it — a balanced double-entry
    posting (self_investment → development_spend), UEG-logged, honest zero-spend when the
    balance is empty (development never blocks on an empty fund; the spend is recorded as
    unfunded). Virtual WST only."""
    try:
        from agentic_core.economy.metabolism import EconomicMetabolism
        d = _load()
        reg = d.get(vsb_id) or {}
        m = EconomicMetabolism(vsb_id, reg.get("entity_type", "waqf_ltd_hybrid"),
                               reg.get("owner", "Rehan"))
        bal = float((m.ledger.statement().get("balances") or {}).get("self_investment", 0.0))
        spent = round(min(max(bal, 0.0), float(amount)), 6)
        if spent > 0:
            # §12 (W339) — the spend must hit the SAME surface the balance check reads: post()
            # moves only the double-entry `accounts`, so the `balances` fund never depleted and
            # every spend reported funded:true forever (audit-proven: 200 WST "spent" from a fund
            # that never dropped). record() decrements `balances` AND makes the balanced posting.
            m.ledger.record("self_investment", spent, kind="debit",
                            memo=f"reinvestment: {purpose[:120]}")
        rec = {"vsb_id": vsb_id, "purpose": purpose[:120], "requested_wst": float(amount),
               "spent_wst": spent, "funded": spent > 0,
               "note": ("self_investment funded this development action" if spent > 0 else
                        "self_investment balance empty — action ran unfunded (recorded honestly)")}
        try:
            from agentic_core.economy.governance import _ueg_log
            _ueg_log({"type": "economy.self_investment_spend", **rec,
                      "disclaimer": "Virtual/simulated WST — no real funds moved."})
        except Exception:
            pass
        return rec
    except Exception as exc:
        return {"vsb_id": vsb_id, "error": str(exc)[:160], "funded": False}


def _latest_screen(vsb_id: str) -> Optional[str]:
    """The entity's latest §11 screen verdict from the per-VSB compliance history (W288), or None."""
    try:
        from agentic_core.config import data_path, load_json_tolerant
        hist = load_json_tolerant(data_path("vsb_compliance_history.json"), {}) or {}
        return (hist.get(vsb_id) or {}).get("overall")
    except Exception:
        return None


def operate_vsb(vsb_id: str) -> Optional[Dict[str, Any]]:
    """Operate ONE living VSB (one governed virtual economy cycle). §11×§12 (W309): an entity whose
    LATEST compliance screen is FAIL has its distributions HELD — the survival instinct has teeth;
    the hold lifts as soon as a re-screen clears it. Best-effort; honest records either way."""
    d = _load()
    target = d.get(vsb_id)
    if not target:
        return None
    # §11 teeth (W309) — last screen FAIL → the economy is held, no cycle runs. The tending is
    # still RECORDED (last_operated advances) so a held entity never starves the round-robin —
    # the organism visited it; the visit's outcome was a hold.
    if _latest_screen(vsb_id) == "fail":
        target["last_operated"] = _now()
        target["last_hold"] = "compliance_fail_hold"
        d[vsb_id] = target
        _save(d)
        try:
            from agentic_core.organism.biobus import biobus
            biobus.fire_signal("reflex", "economy.compliance_hold",
                               f"{vsb_id}: distributions held on FAIL screen", 0.8)
        except Exception:
            pass
        # §11×§13 (W319) — the teeth engaging is a TAMPER-EVIDENT record, not just a response field.
        try:
            from agentic_core.economy.governance import _ueg_log
            _ueg_log({"type": "economy.compliance_fail_hold", "vsb_id": vsb_id,
                      "note": "distributions held on latest FAIL screen (lifts on a clearing re-screen)"})
        except Exception:
            pass
        return {"vsb_id": vsb_id, "name": target.get("name"), "cycle_ran": False,
                "held": "compliance_fail_hold",
                "note": "latest §11 screen is FAIL — distributions held until a re-screen clears it"}
    try:
        # §3 — the ALWAYS-ON path is governed too: constitutional pre-gate + materiality hold +
        # per-cycle UEG split logging (previously this path ran completely ungated + unlogged).
        from agentic_core.economy.governance import governed_cycle_sync
        # §12 (W293) — the cycle's intake is the entity's REAL recorded activity (marketplace sales
        # attributed to it + QMS-passed delivery tariffs, consumed exactly once), NOT the old
        # fabricated flat 1000-WST constant. With no events: an honest ZERO-revenue maintenance
        # cycle — the organism still tends the entity, but distributes only what real work brought.
        # §12 (W313) — PEEK-then-consume: the cycle's intake is measured WITHOUT consuming, the
        # governance gates run on the peeked totals, and the events are consumed ONLY after every
        # gate passes. A materiality/policy hold therefore PRESERVES the recognised revenue it
        # holds (previously consume-before-gate destroyed it — the CCA approval then authorised a
        # distribution of nothing).
        from agentic_core.economy.revenue import peek_pending, consume_events
        peek = peek_pending(vsb_id)
        res = governed_cycle_sync(vsb_id, target.get("entity_type", "waqf_ltd_hybrid"),
                                  target.get("owner", "Rehan"), peek["revenue"], peek["costs"],
                                  source="heartbeat")
        report = res.get("cycle")
        if report is None:   # held/blocked by governance — revenue preserved, hold recorded,
            # and the visit still advances the rotation (a hold must intercept EVERY cycle,
            # not just the first — mirror of the W309 compliance-hold pattern).
            gov = res.get("governance") or {}
            target["last_operated"] = _now()
            target["last_hold"] = str(gov.get("status") or "governance_hold")
            d[vsb_id] = target
            _save(d)
            return {"vsb_id": vsb_id, "name": target.get("name"),
                    "governance": gov, "cycle_ran": False,
                    "pending_preserved_wst": peek["revenue"],
                    "note": "recognised revenue events remain PENDING (unconsumed) while held"}
        pend = consume_events(vsb_id, peek["ids"])   # consume exactly what the passed cycle saw
        target["operating_cycles"] = int(target.get("operating_cycles", 0)) + 1
        target["last_operated"] = _now()
        target.pop("last_hold", None)   # a real cycle ran — no standing hold implied
        target["last_distributable"] = report.get("distributable_profit")
        d[vsb_id] = target
        _save(d)
        # §13 (W309/W340) — autonomous DRIFT is honest AND material: only a cycle that genuinely
        # moved the entity's shipped-visible state marks the repo stale. A zero-activity
        # maintenance cycle changed nothing a page shows — marking it stale caused a perpetual
        # stale→re-ship churn under auto_economy+auto_ship (full 5-surface regeneration + a git
        # commit per beat, audit-measured 81KB DCMS growth in 80s).
        if pend["events"] or (report.get("distributable_profit") or 0) > 0:
            try:
                from agentic_core.api.vsb import mark_repo_stale
                mark_repo_stale(vsb_id, f"autonomous operating cycle {target['operating_cycles']}")
            except Exception:
                pass
        return {"vsb_id": vsb_id, "name": target.get("name"), "cycle": target["operating_cycles"],
                "distributable_wst": report.get("distributable_profit"),
                "revenue_events_consumed": pend["events"],
                "revenue_recognised_wst": pend["revenue"],
                "revenue_basis": ("recognised_events" if pend["events"]
                                  else "no_activity_maintenance_cycle"),
                "governance": (res.get("governance") or {}).get("status")}
    except Exception as e:
        return {"vsb_id": vsb_id, "error": str(e)[:160]}
