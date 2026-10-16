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


def spend(seconds: float = 0.0, tokens: Optional[int] = None) -> None:
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
            atomic_write_json(_store(), rec)
    except Exception:                                  # noqa: BLE001 — accounting never breaks a run
        return


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
