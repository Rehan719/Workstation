"""The work budget — measured in what is actually spent, and it can run down.

OWNER RULING 2026-09-30 (§18.1): the metabolic budget is measured in **wall-clock seconds and tokens**, the
things actually spent, because a figure may only carry the name of what it measured and "ATP" measures nothing.
This module is that budget. It is the honest instrument the ATP ratio was standing in for.

WHAT IT MEASURES, and what it refuses to measure
  · **seconds** — real. Every run path already records `duration_ms` into
    `api/operational_excellence.record_outcome`, and that one writer feeds this. So the figure comes from work
    the platform actually did, not from a coefficient.
  · **tokens** — counted where a model answers (W741). The producer existed all along and was thrown away:
    Ollama's final answer object carries `prompt_eval_count` and `eval_count`, and the local-model routes read
    only `response`. The native orchestrator's local route and the gateway's stream now read that count and
    hand it to `record_outcome(tokens=...)`, which passes it to `spend()` in the SAME call as the run's
    seconds, so a counted run is still one run. A run nothing counted (the deterministic floor runs no model;
    an external accelerant's reported usage is not read) adds nothing, and `tokens_spent` stays None with a
    reason until something has counted, because zero would read as "no tokens were used" when the truth is
    "nobody counted".

WHY IT CAN DEPLETE, which the thing it replaces could not
  `atp_simulator` consumes `0.1 * load` against a production of `0.5 * efficiency`, so production always won and
  `atp_depletion_state()` computes `can_deplete = False`. Every threshold written against that term — the
  economy's reserve raise, the heartbeat's `self_recovery` and `metabolic_throttle` — was unreachable for the
  whole life of the process, and the UI already told viewers it never limits a run. A budget that cannot run down
  is not a budget. This one is a fraction of a stated capacity and reaches 1.0 when the capacity is spent.

IT SHIPS INERT. `enabled()` is False unless `WORKSTATION_WORK_BUDGET=true`. Off, no admission changes and
no throttle is reachable — the ruling requires that, because making `atp < 0.3` reachable switches on
behaviour that has never once fired and would cap all cognition to serial.
ON (W742), `gate()` is read by one consumer, which registers itself when it is imported: the native homeostasis
controller's admission. While the gate holds (the window's capacity is spent, or the store cannot be read
whole), the native workflow tree and the org cascade run their nodes one at a time; single model calls,
deliverables and every other AI door are not held, and no run is refused or deferred. `gates_anything` is
computed from the switch AND the readers loaded.

EACH ENTITY HAS ITS OWN FIGURE, AND THE PLATFORM DERIVES ITS CARRYING CAPACITY (S18.6, W743). A run that names
its owner - and its VSB, when it ran for one - is booked to them as well as to the platform total, and to no
other entity: a VSB's figure sits under the owner whose run named it, so no run is booked to a sibling's figure
or to another owner's, and one VSB id run by two owners is two entities. The runs that name an owner are an AI
call, a cascade tier, a deliverable and a fabric swarm run. An entity's capacity is an equal share of its
parent's among the parent's entities measured this window - derived, never set - and the least headroom on its
chain (the platform, its owner, its VSB) is reported. The carrying capacity is the stated capacity divided by
the mean measured spend per entity, computed on every read and stored nowhere. These figures are REPORTED, NOT
ENFORCED: gate() reads the platform total, not an entity's own figure.
"""
from __future__ import annotations

import os
import time
from typing import Any, Dict, Optional

from agentic_core.config import atomic_write_json, data_path, read_json_reported, store_lock

# A stated capacity, per window, in the unit named. Not derived from anything measured yet — so it is
# declared here as an assumption rather than presented as a measurement, and the state() basis says so.
WINDOW_SECONDS = 6 * 3600.0            # the length of a circadian window in this platform's clock
CAPACITY_SECONDS = 3600.0              # one hour of real work per window
_ENV = "WORKSTATION_WORK_BUDGET"


def enabled() -> bool:
    """The ruling requires this ships inert. Off, the budget records and reports but gates nothing."""
    return os.getenv(_ENV, "false").strip().lower() == "true"


#  W742 (S18.1) - WHO READS THE GATE, registered by each reader when it loads. `gates_anything` is computed from
#  this and the switch rather than typed, so a process that never loads a reader reports that nothing gates there.
_CONSUMERS: Dict[str, str] = {}


def register_consumer(name: str, effect: str) -> None:
    """Called once, at import, by code that reads gate() and acts on `holds`."""
    _CONSUMERS[str(name)] = str(effect)


def _store():
    return data_path("work_budget.json")


def _blank() -> Dict[str, Any]:
    return {"window_started": time.time(), "seconds_spent": 0.0, "tokens_spent": None, "calls": 0}


def _load() -> tuple[Dict[str, Any], Optional[str]]:
    rec, why = read_json_reported(_store(), None)
    if not isinstance(rec, dict):
        return _blank(), why
    # a window that has expired starts a new one rather than accumulating for ever
    if time.time() - float(rec.get("window_started") or 0) > WINDOW_SECONDS:
        return _blank(), why
    return rec, why


def _book(rec: Dict[str, Any], owner_id: Optional[str], vsb_id: Optional[str], seconds: float) -> None:
    """S18.6 (W743) - book one spend to the entity that ran it (its owner, and its VSB under that owner) and to
    no other.

    The carrying capacity is derived from measured PER-ENTITY spend, so the budget keeps each entity's own figure
    beside the platform total. A VSB's figure sits UNDER the owner that ran the work: one owner's run is never
    booked to another owner's entity, and one VSB's spend is never booked to a sibling's. A run that names no
    owner is booked to the platform total alone - including one that names a VSB, because whose entity it is
    cannot be guessed - and that share is reported as unattributed, never apportioned to anyone. A spend of no
    seconds books nothing here, so every entity counted is one that spent. An entity map that is not a
    mapping is left as found (the platform total still books), never replaced by a reader's default; a
    figure inside it that is not a number fails the whole spend, as a malformed platform figure does, and
    every reader of the budget then reports it unreadable rather than show a figure.
    """
    s = max(0.0, float(seconds))
    if not owner_id or s <= 0:
        return
    owners = rec.setdefault("owners", {})
    owner = owners.setdefault(str(owner_id), {}) if isinstance(owners, dict) else None
    if not isinstance(owner, dict):
        return
    owner["seconds_spent"] = round(float(owner.get("seconds_spent") or 0.0) + s, 3)
    owner["calls"] = int(owner.get("calls") or 0) + 1
    if not vsb_id:
        return
    vsbs = owner.setdefault("vsbs", {})
    vsb = vsbs.setdefault(str(vsb_id), {}) if isinstance(vsbs, dict) else None
    if isinstance(vsb, dict):
        vsb["seconds_spent"] = round(float(vsb.get("seconds_spent") or 0.0) + s, 3)
        vsb["calls"] = int(vsb.get("calls") or 0) + 1


def spend(seconds: float = 0.0, tokens: Optional[int] = None, *,
          owner_id: Optional[str] = None, vsb_id: Optional[str] = None) -> None:
    """Record work actually done. Never raises into a caller — accounting is not the work.

    Written under `store_lock` + `atomic_write_json`: this is a shared store, and the concurrency class that
    cost three data-loss incidents applies here as much as anywhere.
    """
    try:
        if seconds <= 0 and tokens is None:
            return
        with store_lock(_store()):
            rec, _why = _load()
            if _why:
                # W577 (FU-395) — the TENTH write path of this class, found by the guard rather than by
                # me. `_load` already returns its reason and `spend` discarded it, then wrote `rec` back:
                # a partial read loses accumulated spend, and persisting the lower total UNDERSTATES
                # consumption, which makes the budget look more available than it is. Accounting never
                # raises into a caller (that contract stands), so this does not refuse - it declines to
                # WRITE, which is the part that would have made the loss permanent, and says so.
                import logging as _lg577
                _lg577.getLogger("molecular.work_budget").error(
                    "a spend of %.3fs/%s tokens was NOT recorded: the budget store could not be read "
                    "whole (%s), and writing back the recoverable part would have discarded spend "
                    "already accumulated and understated consumption", float(seconds), tokens, _why)
                return
            rec["seconds_spent"] = round(float(rec.get("seconds_spent") or 0.0) + max(0.0, float(seconds)), 3)
            #  W741 (S18.1) - a count is a MEASUREMENT even when it is 0, so the test is `is not None`
            #  (a truthiness test dropped a counted zero and left "nobody counted"). How many spends carried a
            #  count is kept beside the total, because a total over some runs is not a total over all of them.
            if tokens is not None:
                rec["tokens_spent"] = int(rec.get("tokens_spent") or 0) + int(tokens)
                rec["token_calls"] = int(rec.get("token_calls") or 0) + 1
            rec["calls"] = int(rec.get("calls") or 0) + 1
            _book(rec, owner_id, vsb_id, seconds)       # S18.6 (W743) - the entity that ran it, and no other
            atomic_write_json(_store(), rec)
    except Exception:                                  # noqa: BLE001 — accounting never breaks a run
        return


def _owners(rec: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """The per-owner figures; a malformed map reads as none, and a reader never repairs it."""
    o = rec.get("owners")
    return {k: v for k, v in o.items() if isinstance(v, dict)} if isinstance(o, dict) else {}


def _vsbs(owner: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    v = owner.get("vsbs")
    return {k: x for k, x in v.items() if isinstance(x, dict)} if isinstance(v, dict) else {}


def _secs(figure: Dict[str, Any]) -> float:
    return float(figure.get("seconds_spent") or 0.0)


#  S18.6 (W743) - what an entity's own figures are FOR, said once wherever they are reported. gate() reads the
#  platform total, so an entity's own figure holds nothing back; leg 7 of the W743 guard drives gate() against an
#  entity with no headroom of its own, so this sentence cannot outlive the code it describes.
_ENTITY_GATE_NOTE = ("reported, not enforced: the S18.1 gate (gate()) reads the platform total, not an "
                     "entity's own figure")


def _per_entity(rec: Dict[str, Any]) -> Dict[tuple, float]:
    """Each entity's seconds this window, keyed (owner, VSB). An entity is a VSB under the owner whose runs named
    it, so one VSB id run by two owners is two entities - the same rows entity_states lists. Only entities that
    spent are counted."""
    per: Dict[tuple, float] = {}
    for okey, owner in _owners(rec).items():
        for vid, fig in _vsbs(owner).items():
            if _secs(fig) > 0:
                per[(okey, vid)] = _secs(fig)
    return per


def _entities_summary(rec: Dict[str, Any], spent: float) -> Dict[str, Any]:
    """How much of the platform's spend named the owner it ran for - as counts only, because this record is
    platform-wide and names no owner and no entity (each one's own figures are entity_state's)."""
    attributed = sum(_secs(o) for o in _owners(rec).values())
    return {"owners_measured": len(_owners(rec)), "entities_measured": len(_per_entity(rec)),
            "attributed_seconds": round(attributed, 3),
            "unattributed_seconds": round(max(0.0, spent - attributed), 3),
            "basis": (f"{attributed:.1f}s of the {spent:.1f}s recorded this window came from runs that named the "
                      "owner they ran for; the rest named none, so it counts in the platform total and is "
                      "apportioned to no one. These figures are " + _ENTITY_GATE_NOTE)}


def _carrying_capacity(rec: Dict[str, Any]) -> Dict[str, Any]:
    """S18.6 - how many entities the stated capacity carries at the per-entity demand MEASURED this window.

    DERIVED on every read and stored nowhere, so it moves when the budget moves; nothing sets it. An entity here
    is a VSB under the owner whose runs named it. With no run attributed to an entity this window the demand is
    unmeasured, and the capacity is None with that reason - never a number.
    """
    per = _per_entity(rec)
    if not per:
        return {"entities": None, "entities_measured": 0, "mean_seconds_per_entity": None, "over_capacity": None,
                "basis": ("UNMEASURED - no run this window was attributed to an entity, so no per-entity demand "
                          "is measured and no carrying capacity is derived; it is never set by hand")}
    n = len(per)
    mean = sum(per.values()) / n
    k = int(CAPACITY_SECONDS // mean)
    return {"entities": k, "entities_measured": n, "mean_seconds_per_entity": round(mean, 3),
            "over_capacity": n > k,
            "basis": (f"DERIVED, never set: the stated {CAPACITY_SECONDS:.0f}s per window divided by {mean:.1f}s, "
                      f"the mean recorded spend of the {n} entit{'y' if n == 1 else 'ies'} whose runs were "
                      f"attributed this window, carries {k}. It moves whenever the budget or the measured demand "
                      "moves; spend that named no entity is not in the mean, and the capacity it divides is a "
                      "STATED ASSUMPTION (capacity_basis). It is " + _ENTITY_GATE_NOTE)}


def _entity_view(rec: Dict[str, Any], why: Optional[str], owner_id: Optional[str],
                 vsb_id: Optional[str]) -> Dict[str, Any]:
    owners = _owners(rec)
    levels = [("platform", CAPACITY_SECONDS, float(rec.get("seconds_spent") or 0.0))]
    n_owners = n_vsbs = 0
    if owner_id:
        n_owners = len(set(owners) | {str(owner_id)})
        owner_cap = CAPACITY_SECONDS / n_owners
        own = owners.get(str(owner_id)) or {}
        levels.append(("owner", owner_cap, _secs(own)))
        if vsb_id:
            vsbs = _vsbs(own)
            n_vsbs = len(set(vsbs) | {str(vsb_id)})
            levels.append(("vsb", owner_cap / n_vsbs, _secs(vsbs.get(str(vsb_id)) or {})))
    rows = [{"level": name, "capacity_seconds": round(cap, 3), "seconds_spent": round(used, 3),
             "headroom_seconds": round(max(0.0, cap - used), 3)} for name, cap, used in levels]
    least = min(r["headroom_seconds"] for r in rows)
    return {"owner_id": owner_id, "vsb_id": vsb_id if owner_id else None,
            "unit": "wall-clock seconds of recorded run time",
            "levels": rows,
            "least_headroom_seconds": least,
            "bound_by": [r["level"] for r in rows if r["headroom_seconds"] == least],
            "capacity_basis": (
                f"DERIVED, never set: the stated {CAPACITY_SECONDS:.0f}s per window"
                + (f", shared equally among the {n_owners} owner(s) measured this window (this one counted)"
                   if n_owners else "; no owner was named, so only the platform level applies")
                + (f", then among this owner's {n_vsbs} entit{'y' if n_vsbs == 1 else 'ies'} measured this "
                   "window (this one counted)" if n_vsbs else "")
                + ". The least headroom on the chain is reported, every level at that least is named, and a "
                  "sibling's spend never enters an entity's own level. It is " + _ENTITY_GATE_NOTE),
            "store_incomplete": why}


def entity_state(owner_id: Optional[str] = None, vsb_id: Optional[str] = None) -> Dict[str, Any]:
    """ONE entity's own figures beside the platform's: what it spent, its derived capacity, and the LEAST headroom
    on its chain (the platform, its owner, its VSB), so no entity shows more room than a level above it, while a
    sibling's spend never reduces its own level. Reported, not enforced (_ENTITY_GATE_NOTE)."""
    rec, why = _load()
    return _entity_view(rec, why, owner_id, vsb_id)


def entity_states(limit: int = 5) -> list:
    """The entities measured this window (the rows _per_entity counts), busiest first, each as entity_state
    reports it - for the admin-only organism status. The platform-wide state() names no one."""
    rec, why = _load()
    ranked = sorted(((s, okey, vid) for (okey, vid), s in _per_entity(rec).items()), reverse=True)
    return [_entity_view(rec, why, okey, vid) for _used, okey, vid in ranked[:max(0, int(limit))]]


def state() -> Dict[str, Any]:
    """The budget, with every figure named for what it measures."""
    rec, why = _load()
    spent = float(rec.get("seconds_spent") or 0.0)
    fraction = min(1.0, spent / CAPACITY_SECONDS) if CAPACITY_SECONDS else 0.0
    tokens = rec.get("tokens_spent")
    return {
        "unit": "wall-clock seconds of recorded run time",
        "enabled": enabled(),
        "capacity_seconds": CAPACITY_SECONDS,
        "seconds_spent": round(spent, 3),
        "fraction_spent": round(fraction, 4),
        "calls_recorded": int(rec.get("calls") or 0),
        "window_seconds": WINDOW_SECONDS,
        "window_started": rec.get("window_started"),
        "tokens_spent": tokens,
        #  W741 (S18.1) - how many spends carried a count; the total covers THOSE model answers only
        "tokens_counted_calls": int(rec.get("token_calls") or 0),
        "tokens_basis": (f"measured - {tokens} token(s) reported by the serving model itself, over "
                         f"{int(rec.get('token_calls') or 0)} counted model answer(s) this window; "
                         f"{int(rec.get('calls') or 0)} spend(s) were recorded in all, which is not a count of "
                         "answers: a wrapper that times the same call records its own, and a run nothing "
                         "counted adds no tokens (the deterministic floor runs no model, and an external "
                         "accelerant's reported usage is not read)"
                         if tokens is not None else
                         "NOT RECORDED — no run this window reported a token count (a count comes only from a "
                         "model's own answer; the deterministic floor runs no model), so this is null rather "
                         "than 0; zero would read as 'no tokens were used' when nobody counted"),
        "capacity_basis": (f"{CAPACITY_SECONDS:.0f} seconds per {WINDOW_SECONDS / 3600:.0f}-hour window is a "
                           "STATED ASSUMPTION, not a measurement — nothing here has yet measured what this "
                           "platform's sustainable rate is"),
        #  W742 (S18.1) - true only with the switch on AND a reader of the gate loaded in this process
        "gates_anything": enabled() and bool(_CONSUMERS),
        "consumers": dict(_CONSUMERS),
        "holding_reason": _hold_reason(fraction, why),
        "gate_basis": _gate_basis(fraction, why),
        #  W742 - what the figure is a sum OF, said where the gate reads it
        "spend_basis": ("the sum of every run duration the platform recorded; a run recorded inside another "
                        "(a model attempt inside the AI call or run that made it) can be counted at each level, "
                        "so this can exceed the wall-clock time actually worked. Durations a caller reported "
                        "through /api/v1/operations/record are not counted"),
        "basis": (f"{spent:.1f}s of a stated {CAPACITY_SECONDS:.0f}s capacity is recorded spent this window, "
                  f"from {int(rec.get('calls') or 0)} run(s) whose duration was measured — and "
                  + _gate_basis(fraction, why)),
        #  S18.6 (W743) - derived on this read from the per-entity figures, as COUNTS: this record is platform-wide,
        #  so it names no owner and no entity (entity_state reports one entity's own)
        "entities": _entities_summary(rec, spent),
        "carrying_capacity": _carrying_capacity(rec),
        "store_incomplete": why,
    }


def _hold_reason(fraction: float, why: Optional[str]) -> Optional[str]:
    """Why the S18.1 throttle holds right now, or None. Off, it never holds."""
    if not enabled():
        return None
    if why:
        return (f"the budget store could not be read whole ({why}); an unreadable budget is not an "
                "available one, so the throttle holds")
    if fraction >= 1.0:
        return (f"the stated capacity of {CAPACITY_SECONDS:.0f}s for this {WINDOW_SECONDS / 3600:.0f}-hour "
                "window is recorded spent")
    return None


def _gate_basis(fraction: float, why: Optional[str]) -> str:
    """What the gate does in THIS process, computed from the switch, the registered readers and the figure."""
    if not enabled():
        return f"it GATES NOTHING: the budget ships inert until {_ENV}=true, per the Owner's ruling"
    if not _CONSUMERS:
        return f"{_ENV} is on, but no reader of the gate is loaded in this process, so it gates nothing here"
    readers = "; ".join(f"{k} ({v})" for k, v in sorted(_CONSUMERS.items()))
    held = _hold_reason(fraction, why)
    return (f"it GATES: {readers}. "
            + (f"It is HOLDING now: {held}" if held else "It is not holding: the capacity is not yet spent"))


def gate() -> Dict[str, Any]:
    """THE S18.1 THROTTLE (W742), read where cognition is admitted. `holds` is True only with the switch on and
    the window's capacity spent, or the store unreadable. Never raises into a caller: if the budget cannot be
    read at all while the switch is on, it holds and says why."""
    try:
        st = state()
    except Exception as exc:                           # noqa: BLE001 - said, never substituted
        on = enabled()
        why = f"the work budget could not be read ({exc.__class__.__name__}: {exc})"
        return {"enabled": on, "holds": on,
                "reason": (why + "; an unreadable budget is not an available one, so the throttle holds")
                if on else None,
                "basis": why}
    return {"enabled": st["enabled"], "holds": st["holding_reason"] is not None,
            "reason": st["holding_reason"], "fraction_spent": st["fraction_spent"],
            "basis": st["basis"], "spend_basis": st["spend_basis"]}
