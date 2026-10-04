"""The work budget — measured in what is actually spent, and it can run down.

OWNER RULING 2026-09-30 (§18.1): the metabolic budget is measured in **wall-clock seconds and tokens**, the
things actually spent, because a figure may only carry the name of what it measured and "ATP" measures nothing.
This module is that budget. It is the honest instrument the ATP ratio was standing in for.

WHAT IT MEASURES, and what it refuses to measure
  · **seconds** — real. Every run path already records `duration_ms` into
    `api/operational_excellence.record_outcome`, and that one writer feeds this. So the figure comes from work
    the platform actually did, not from a coefficient.
  · **tokens** — NOT RECORDED anywhere in this repository. Measured before writing this: no token accounting
    exists at any call site. So `tokens_spent` is None with a reason, never 0, because zero would read as "no
    tokens were used" when the truth is "nobody counted". When a producer appears, it feeds `spend(tokens=...)`
    and the field starts reporting.

WHY IT CAN DEPLETE, which the thing it replaces could not
  `atp_simulator` consumes `0.1 * load` against a production of `0.5 * efficiency`, so production always won and
  `atp_depletion_state()` computes `can_deplete = False`. Every threshold written against that term — the
  economy's reserve raise, the heartbeat's `self_recovery` and `metabolic_throttle` — was unreachable for the
  whole life of the process, and the UI already told viewers it never limits a run. A budget that cannot run down
  is not a budget. This one is a fraction of a stated capacity and reaches 1.0 when the capacity is spent.

IT SHIPS INERT. `enabled()` is False unless `WORKSTATION_WORK_BUDGET=true`. Off, nothing reads differently and
no throttle becomes reachable — the ruling requires that, because making `atp < 0.3` reachable switches on
behaviour that has never once fired and would cap all cognition to serial.
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
        if seconds <= 0 and not tokens:
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
            if tokens:
                rec["tokens_spent"] = int(rec.get("tokens_spent") or 0) + int(tokens)
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
        "tokens_basis": ("measured" if tokens is not None else
                         "NOT RECORDED — no call site in this repository counts tokens, so this is null "
                         "rather than 0; zero would read as 'no tokens were used' when nobody counted"),
        "capacity_basis": (f"{CAPACITY_SECONDS:.0f} seconds per {WINDOW_SECONDS / 3600:.0f}-hour window is a "
                           "STATED ASSUMPTION, not a measurement — nothing here has yet measured what this "
                           "platform's sustainable rate is"),
        "gates_anything": enabled(),
        "basis": (f"{spent:.1f}s of a stated {CAPACITY_SECONDS:.0f}s capacity is recorded spent this window, "
                  f"from {int(rec.get('calls') or 0)} run(s) whose duration was measured"
                  + ("" if enabled() else " — and it GATES NOTHING: the budget ships inert until "
                                          f"{_ENV}=true, per the Owner's ruling")),
        "store_incomplete": why,
    }
