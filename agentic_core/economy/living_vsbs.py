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

from agentic_core.config import StoreUnavailable, atomic_write_json, data_path, read_json_strict

_STORE = data_path("living_vsbs.json")
_HISTORY = data_path("vsb_compliance_history.json")
HISTORY_UNREADABLE = "unreadable"          # W472 — _latest_screen's answer when the history cannot be read whole


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _load() -> Dict[str, Any]:
    """W472 (register FU-050) — THE roster read: whole, or StoreUnavailable. The tolerant read answered {} for a roster
    it could not parse, and register() then wrote back a roster holding only the new entity (a BOM roster kept 1 of 3
    entries) — the heartbeat stopped tending every other enterprise."""
    return read_json_strict(_STORE, dict, expect=dict)


def _int0(v: Any) -> int:
    """A malformed entry's count never stops the rotation for every entity (FU-050)."""
    try:
        return int(v or 0)
    except (TypeError, ValueError):
        return 0


def _history() -> Dict[str, Any]:
    """W472 (register FU-049) — the compliance history, whole or StoreUnavailable (a BOM history read as {} lifted
    every FAIL hold and ran distributions for entities whose latest screen failed)."""
    return read_json_strict(_HISTORY, dict, expect=dict)


def _save(d: Dict[str, Any]) -> None:
    _STORE.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_json(_STORE, d)


def living_statement() -> dict:
    """W475 (ledger v4 R2.0) — what a newly registered entity is told about being tended, for EVERY writer (the
    blocking and streamed establishment, /vsb/spawn, the Studio): the present tense only when the heartbeat's economy
    lever is ON — it is off by default, so only the birth cycle ran and every founder was told otherwise."""
    try:
        from agentic_core.organism.heartbeat import heartbeat as _hb
        lever = bool(getattr(_hb, "auto_economy", False))
        beating = bool(getattr(_hb, "running", False))
        auto = lever and beating                    # (refutation) a stopped heartbeat tends nothing, lever or not
    except Exception:
        lever, beating, auto = False, False, False
    return {"autonomous_operation": ("registered — the organism tends this VSB on the circadian heartbeat (paced "
                                     "virtual economy cycles)" if auto else
                                     "registered on the living roster — autonomous economy cycles are OFF ("
                                     + ("the heartbeat's Self-run lever is off" if not lever else
                                        "the heartbeat is stopped, so nothing beats although Self-run is on")
                                     + "), so only the birth cycle ran; enable Self-run and start the heartbeat on the "
                                     "Heartbeat page for the organism to tend this VSB"),
            "autonomous_cycles": auto, "virtual": True}


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
    from agentic_core.config import store_lock
    with store_lock(_STORE):          # W463 (sixth refutation) — serialised with every other roster write
        d = _load()
        if vsb_id not in d:
            return False
        del d[vsb_id]
        _save(d)
    return True


def _update_entry(vsb_id: str, mutate) -> Optional[Dict[str, Any]]:
    """W463 (sixth refutation) — operate_vsb held a roster snapshot across a whole governed cycle and wrote it back,
    erasing registrations made meanwhile and undoing deregistrations. Its bookkeeping now re-reads the roster under
    the store lock and changes only this entry; an entry deregistered meanwhile stays gone (None is returned)."""
    from agentic_core.config import store_lock
    with store_lock(_STORE):
        d = _load()
        entry = d.get(vsb_id)
        if not entry:
            return None
        mutate(entry)
        d[vsb_id] = entry
        _save(d)
        return dict(entry)


def _ledger_hold_text(vsb_id: Any, decision: Any = None) -> str:
    """W468 (refutation) — the hold is what the LAST visit found; the ledger is read now, so a repaired ledger is never
    still described as unreadable. A Change Control decision behind it is named (sixth refutation)."""
    behind = (f" — and a Change Control decision ({str(decision).replace('_', ' ')}) stands behind it" if decision else "")
    try:
        from agentic_core.economy.ledger import VirtualLedger
        readable = VirtualLedger(str(vsb_id)).load_error is None
    except Exception:
        readable = False
    if readable:
        return ("its ledger could not be read whole at the last visit and reads whole now — the next visit tries its "
                "cycle again" + behind)
    return "its ledger could not be read whole — no cycle runs and nothing is posted to it until it can be" + behind


def list_living() -> Dict[str, Any]:
    """§11 × §13 (W421) — each row now carries the entity's LIVE compliance standing and any economic
    hold it causes. Both existed only as side effects before: `_latest_screen` was read by
    `operate_vsb` to decide a hold, and the hold was written to the store and the UEG — but the
    entity's OWNER had no way to see either. A held enterprise looked simply idle."""
    try:
        d = _load()
    except StoreUnavailable as e:
        # W472 — a roster that cannot be read whole is said, never shown as an empty roster
        return {"living_vsbs": [], "total": 0, "roster_unavailable": str(e),
                "note": "the living roster could not be read whole — no entity is tended and nothing is written to "
                        "it until it can be read (virtual/simulated — no real funds)"}
    rows = sorted([v for v in d.values() if isinstance(v, dict)], key=lambda v: str(v.get("registered_at") or ""),
                  reverse=True)
    hist_error = None
    try:
        hist = _history()
    except StoreUnavailable as e:
        hist, hist_error = {}, str(e)
    for r in rows:
        h = hist.get(r.get("vsb_id")) or {}
        verdict = h.get("overall")
        r["compliance"] = {
            # None means NOT YET SCREENED — never rendered as a pass. An entity established before
            # auto_compliance was switched on has no verdict, and that is different from a clean one.
            "verdict": verdict,
            "screened_at": h.get("screened_at") or h.get("at"),
            "verdicts": h.get("verdicts") or [],
            "never_screened": (not bool(verdict)) if not hist_error else None,
            # W472 (FU-049) — a history that cannot be read whole: the standing is UNKNOWN, not clean
            "history_unavailable": hist_error,
        }
        r["economy_held"] = {
            "held": bool(r.get("last_hold")),
            "reason": r.get("last_hold"),
            "consequence": ("distributions are held — no economy cycle runs until a re-screen clears it"
                            if r.get("last_hold") == "compliance_fail_hold"
                            else ("its compliance standing cannot be known — the compliance history could not be "
                                  "read whole; no cycle runs until it can be")
                            if r.get("last_hold") == "compliance_history_unavailable"
                            else (_ledger_hold_text(r.get("vsb_id"), r.get("decision_hold"))
                                  if r.get("last_hold") == "ledger_unavailable"
                                  else ("this entity's cycle is held by governance" if r.get("last_hold") else None))),
            # W468 — the last visit's raise, when that is what happened (a raise is not a hold)
            "last_visit_error": r.get("last_error"),
            # W468 (sixth refutation) — a Change Control decision (pending or already decided) the ledger hold stands
            # in front of
            "standing_decision": r.get("decision_hold"),
        }
        # W491 (FU-192) — `operating_cycles` counts the cycles THIS roster ran, which is not the number of
        # metabolic cycles the entity has: one run through any other path posts to the books and never
        # touches this counter, so a row read "1 cycles" beside a ledger holding three. The row now names
        # the population its own counter covers and carries the books' own count beside it.
        r["operating_cycles_basis"] = ("cycles this autonomous roster ran and booked; a cycle run through any "
                                       "other path is posted to the books but not counted here")
        try:
            from agentic_core.economy.metabolism import EconomicMetabolism
            _m = EconomicMetabolism(r.get("vsb_id"))
            if _m.ledger.load_error:
                r["ledger_cycles"] = None
                r["ledger_cycles_unavailable"] = str(_m.ledger.load_error)[:160]
            else:
                _st = _m.ledger.statement()
                r["ledger_cycles"] = _st.get("cycles_posted")
                r["ledger_cycles_basis"] = _st.get("cycles_posted_basis")
        except Exception as _le:
            r["ledger_cycles"] = None
            r["ledger_cycles_unavailable"] = f"{type(_le).__name__}: {str(_le)[:140]}"
    return {"living_vsbs": rows, "total": len(rows), "history_unavailable": hist_error,
            "cycle_counts_basis": ("`operating_cycles` is this roster's own tally; `ledger_cycles` is what the "
                                   "entity's books record. They differ whenever a cycle ran outside the roster."),
            "note": "Established VSB enterprises the organism autonomously tends (paced virtual economy "
                    "cycles on the circadian heartbeat). Virtual/simulated — no real funds."}


def operate_one() -> Optional[Dict[str, Any]]:
    """Autonomously operate the least-recently-operated living VSB: one virtual economy cycle. Round-robin,
    paced by the heartbeat. Returns a compact record, or None when there are no living VSBs. Best-effort."""
    try:
        d = _load()
    except StoreUnavailable as e:
        # W472 (FU-050) — an unreadable roster is a said outcome of the beat, never an empty roster
        return {"cycle_ran": False, "held": "roster_unavailable", "note": str(e)}
    entries = [v for v in d.values() if isinstance(v, dict) and isinstance(v.get("vsb_id"), str)]
    if not entries:
        return None
    # pick the least-recently-operated (None sorts first). §8 (W340) — FAIR under bursts: the
    # second-resolution timestamps tie when beats fire sub-second (the audit observed 23×/8×/7×
    # starvation), so ties break by FEWEST operating cycles, then registration order — every
    # entity gets tended even under a burst of manual beats.
    target = sorted(entries, key=lambda v: (str(v.get("last_operated") or ""),
                                            _int0(v.get("operating_cycles")),        # W472 — one bad entry never stops all
                                            str(v.get("registered_at") or "")))[0]
    return operate_vsb(target["vsb_id"])


# W468 (refutations 2–4) — holds that record an Owner's decision (or a hold awaiting one): a heartbeat visit that raises
# does not change them. Every other hold is an earlier visit's outcome, which a later visit's raise supersedes.
_DECISION_HOLDS = frozenset({"held_for_change_control", "rejected_by_change_control", "governance_hold"})

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
        if m.ledger.load_error:
            # W468 (register FU-041) — an unreadable ledger read as empty books, and this reported "balance empty — ran
            # unfunded" for a fund whose balance is unknown
            rec = {"vsb_id": vsb_id, "purpose": purpose[:120], "requested_wst": float(amount), "spent_wst": 0.0,
                   "funded": False, "ledger_unavailable": True, "error": m.ledger.load_error[:200],
                   "note": "the entity's ledger could not be read whole, so nothing was drawn from self_investment and "
                           "whether the fund could have paid for this action is unknown"}
            try:
                # its own type (refutation): the audit views read "self_investment_spend" as a clean, recorded spend
                from agentic_core.economy.governance import _ueg_log
                _ueg_log({"type": "economy.self_investment_spend_refused", **rec,
                          "disclaimer": "Virtual/simulated WST — no real funds moved."})
            except Exception:
                pass
            return rec
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
        from agentic_core.economy.ledger import LedgerUnavailable, LedgerWriteRefused
        out = {"vsb_id": vsb_id, "error": str(exc)[:160], "funded": False,
               **({"ledger_unavailable": True} if isinstance(exc, LedgerUnavailable) else {}),
               **({"ledger_write_refused": True} if isinstance(exc, LedgerWriteRefused) else {})}
        if isinstance(exc, (LedgerUnavailable, LedgerWriteRefused)):
            # W468 (second refutation) — refused at its write (the ledger broke after the balance was read): recorded,
            # never only returned to a caller that discards it
            try:
                from agentic_core.economy.governance import _ueg_log
                _ueg_log({"type": "economy.self_investment_spend_refused", **out, "purpose": purpose[:120],
                          "requested_wst": float(amount), "spent_wst": 0.0,
                          "note": "the spend was refused at its ledger write; nothing was drawn from self_investment",
                          "disclaimer": "Virtual/simulated WST — no real funds moved."})
            except Exception:
                pass
        return out


def _latest_screen(vsb_id: str) -> Optional[str]:
    """The entity's latest §11 screen verdict from the per-VSB compliance history (W288), None when never screened,
    or HISTORY_UNREADABLE (W472, FU-049) when the history exists and cannot be read whole — never None for that."""
    try:
        hist = _history()
    except StoreUnavailable:
        return HISTORY_UNREADABLE
    entry = hist.get(vsb_id)
    return entry.get("overall") if isinstance(entry, dict) else None


def operate_vsb(vsb_id: str) -> Optional[Dict[str, Any]]:
    """Operate ONE living VSB (one governed virtual economy cycle). §11×§12 (W309): an entity whose
    LATEST compliance screen is FAIL has its distributions HELD — the survival instinct has teeth;
    the hold lifts as soon as a re-screen clears it. Best-effort; honest records either way."""
    try:
        d = _load()
    except StoreUnavailable as e:
        return {"vsb_id": vsb_id, "cycle_ran": False, "held": "roster_unavailable", "note": str(e)}
    target = d.get(vsb_id)
    if not target:
        return None
    screen = _latest_screen(vsb_id)
    if screen == HISTORY_UNREADABLE:
        # W472 (FU-049) — a history that cannot be read whole means the standing is UNKNOWN: held, said, no cycle
        target["last_operated"] = _now()

        def _hold_unknown(e: Dict[str, Any]) -> None:
            # (refutation) a Change Control decision this hold now stands in front of is kept apart, never overwritten
            prior = e.get("last_hold") if e.get("last_hold") in _DECISION_HOLDS else e.get("decision_hold")
            e.pop("decision_hold", None)
            if prior:
                e["decision_hold"] = prior
            e.update(last_operated=target["last_operated"], last_hold="compliance_history_unavailable")
            e.pop("last_error", None)
        _update_entry(vsb_id, _hold_unknown)
        try:
            from agentic_core.economy.governance import _ueg_log
            _ueg_log({"type": "economy.compliance_history_unavailable", "vsb_id": vsb_id,
                      "note": "the compliance history could not be read whole — standing unknown, cycle held"})
        except Exception:
            pass
        return {"vsb_id": vsb_id, "name": target.get("name"), "cycle_ran": False,
                "held": "compliance_history_unavailable",
                "note": "the §11 compliance history could not be read whole — the entity's standing cannot be "
                        "known, so no cycle runs and nothing is posted until it can be read"}
    # §11 teeth (W309) — last screen FAIL → the economy is held, no cycle runs. The tending is
    # still RECORDED (last_operated advances) so a held entity never starves the round-robin —
    # the organism visited it; the visit's outcome was a hold.
    if screen == "fail":
        target["last_operated"] = _now()
        target["last_hold"] = "compliance_fail_hold"
        _update_entry(vsb_id, lambda e: (e.update(last_operated=target["last_operated"], last_hold="compliance_fail_hold"),
                                         e.pop("last_error", None)))
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
    cycle_done: Dict[str, Any] = {"report": None, "booked": False, "held": None, "held_booked": False}
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
        from agentic_core.economy.revenue import peek_pending
        peek = peek_pending(vsb_id)
        res = governed_cycle_sync(vsb_id, target.get("entity_type", "waqf_ltd_hybrid"),
                                  target.get("owner", "Rehan"), peek["revenue"], peek["costs"],
                                  source="heartbeat", events=peek)
        report = res.get("cycle")
        if report is None:   # held/blocked by governance — revenue preserved, hold recorded,
            # and the visit still advances the rotation (a hold must intercept EVERY cycle,
            # not just the first — mirror of the W309 compliance-hold pattern).
            gov = res.get("governance") or {}
            target["last_operated"] = _now()
            target["last_hold"] = str(gov.get("status") or "governance_hold")
            def _held(e: Dict[str, Any]) -> None:
                # W468 (sixth refutation) — the row has one hold: a Change Control decision an unreadable ledger now
                # stands in front of is kept apart (decision_hold), never overwritten
                prior = e.get("last_hold") if e.get("last_hold") in _DECISION_HOLDS else e.get("decision_hold")
                e.pop("decision_hold", None)
                if target["last_hold"] == "ledger_unavailable" and prior:
                    e["decision_hold"] = prior
                e.update(last_operated=target["last_operated"], last_hold=target["last_hold"])
                e.pop("last_error", None)
            cycle_done["held"] = _held           # (seventh refutation) a raise from here on is this hold's bookkeeping
            _update_entry(vsb_id, _held)
            cycle_done["held_booked"] = True
            try:
                preserved = peek_pending(vsb_id)["revenue"]      # what is ACTUALLY pending now (never a stale peek)
            except Exception:
                preserved = None
            return {"vsb_id": vsb_id, "name": target.get("name"),
                    "governance": gov, "cycle_ran": False,
                    "pending_preserved_wst": preserved,
                    "note": ("recognised revenue events remain PENDING (unconsumed) while held"
                             if gov.get("status") not in ("intake_unavailable", "intake_consumed_elsewhere",
                                                          "ledger_unavailable") else
                             gov.get("note") or "no cycle ran; recognised revenue events were not distributed")}
        cycle_done["report"] = report       # the cycle ran: a later raise is its bookkeeping, not a failed visit
        # W467 (register FU-022) — the governed cycle consumed exactly what it ran on BEFORE it ran (W463: an approval
        # releases the events it was filed for); this path no longer consumes after the ledger has posted
        pend = res.get("consumed") or {"events": 0, "revenue": 0.0, "costs": 0.0}
        if pend["events"]:
            from agentic_core.economy.governance import retire_heartbeat_holds_for_consumed_events
            retire_heartbeat_holds_for_consumed_events(vsb_id)
        stamp = _now()

        def _ran(e: Dict[str, Any]) -> None:
            e["operating_cycles"] = int(e.get("operating_cycles", 0)) + 1
            e["last_operated"] = stamp
            e.pop("last_hold", None)   # a real cycle ran — no standing hold implied
            e.pop("last_error", None)
            e.pop("decision_hold", None)
            e["last_distributable"] = report.get("distributable_profit")
        fresh_entry = _update_entry(vsb_id, _ran)
        cycle_done["booked"] = True
        _ran(target)
        if fresh_entry:
            target["operating_cycles"] = fresh_entry["operating_cycles"]
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
        # W468 — a visit that RAISED is still a visit: last_operated used to advance only on a cycle or a hold, so the
        # least-recently-operated pick chose the same failing entity on every beat and no other entity was tended again
        why = f"{type(e).__name__}: {str(e)[:160]}"
        stamp = _now()
        if cycle_done["report"] is not None:
            # (sixth refutation) the cycle RAN and posted; only the roster's bookkeeping of the visit raised. The row records
            # the cycle (the bookkeeping retried once), never a failed visit or a hold the cycle got past.
            if not cycle_done["booked"]:
                done = cycle_done["report"]

                def _late(en: Dict[str, Any]) -> None:
                    en["operating_cycles"] = int(en.get("operating_cycles", 0)) + 1
                    en["last_operated"] = stamp
                    for key in ("last_hold", "last_error", "decision_hold"):
                        en.pop(key, None)
                    en["last_distributable"] = done.get("distributable_profit")
                try:
                    _update_entry(vsb_id, _late)
                except Exception:
                    pass
            return {"vsb_id": vsb_id, "error": str(e)[:160], "cycle_ran": True,
                    "note": "the cycle ran and posted; only the roster's bookkeeping of the visit raised"}
        if cycle_done["held"] is not None:
            # (seventh refutation) the visit FOUND a hold; only the roster's bookkeeping of it raised. The row records that
            # hold (the bookkeeping retried once), never the previous visit's hold or a failed visit.
            if not cycle_done["held_booked"]:
                try:
                    _update_entry(vsb_id, cycle_done["held"])
                except Exception:
                    pass
            return {"vsb_id": vsb_id, "error": str(e)[:160], "cycle_ran": False, "held": target.get("last_hold"),
                    "note": "the visit found a hold; only the roster's bookkeeping of it raised"}
        # the ledger as it reads NOW decides the ledger hold (the raise may have come before this visit read it)
        try:
            from agentic_core.economy.ledger import VirtualLedger
            unreadable_now: Optional[bool] = VirtualLedger(vsb_id).load_error is not None
        except Exception:
            unreadable_now = None

        past_cc = bool(getattr(e, "past_change_control", False))     # the cycle got past the materiality gate

        def _raised(en: Dict[str, Any]) -> None:
            # (refutations 2–5) the row keeps only what is still true after a visit that raised: a ledger hold exactly
            # while the ledger cannot be read (it stops every cycle first); a Change Control hold unless this visit got
            # past Change Control; a ledger hold when the fresh read itself failed. Anything else — a compliance hold
            # (reaching the cycle proves the screen is not FAIL), an intake or gate hold — is an earlier outcome this
            # raise supersedes (last_error says the raise).
            en.update(last_operated=stamp, last_error=why)
            hold = en.get("last_hold")
            # (sixth refutation) a Change Control decision — the hold itself, or one kept behind a ledger hold — stands
            # unless this visit got past Change Control; it is kept apart while the ledger hold is in front of it
            decision = None if past_cc else (hold if hold in _DECISION_HOLDS else en.get("decision_hold"))
            en.pop("decision_hold", None)
            if unreadable_now or (unreadable_now is None and hold == "ledger_unavailable"):
                en["last_hold"] = "ledger_unavailable"
                if decision:
                    en["decision_hold"] = decision
            elif decision:
                en["last_hold"] = decision
            else:
                en.pop("last_hold", None)
        try:
            _update_entry(vsb_id, _raised)
        except Exception:
            pass
        return {"vsb_id": vsb_id, "error": str(e)[:160]}
