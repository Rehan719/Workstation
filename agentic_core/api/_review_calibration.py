"""WHETHER A REVIEWER AGENT IS CALIBRATED - measured from recorded runs, never ticked.

OWNER RULING 2026-10-12 (the review cell, clause 3): a reviewer agent's reviews COUNT only after it is calibrated
on planted defects and clean answers; its catch rate and false-alarm rate are shown beside its reviews; an
uncalibrated agent's review is labelled so. THE PASS BAR, as ruled: every planted case flagged FOR ITS REASON, and
at most one false alarm in six clean cases.

THE FAULT THIS REPLACES (W688 to W690): a review record carried `agent_calibrated`, a flag that was whatever the
person recording it ticked - a claim standing where a measurement was ruled. Calibration is now arithmetic over
a RUN: the cases of a named set, what the agent flagged on each, and the two rates this module computes from
them. A caller cannot assert a rate; a run on a different version of the set does not count for this one.

THE SET. `docs/CARE_REVIEW_CALIBRATION.json` holds the Care cases. Each is DESCRIBED today, not written out in
full, and the file says so - so no reviewer can yet be run on it, no agent has met the bar, and every agent's
review is labelled uncalibrated. That is the true state.
"""
from __future__ import annotations

import json
import pathlib
from typing import Any, Dict, List, Optional

SETS = {"care": "docs/CARE_REVIEW_CALIBRATION.json"}
RUNS_STORE = "review_calibration_runs.json"
#  THE BAR, as the Owner ruled it
MUST_CATCH_EVERY_PLANTED_CASE = True
FALSE_ALARMS_ALLOWED_PER_CLEAN = (1, 6)          # at most one in six clean cases
CONFIGURATIONS = ("model", "floor")


def _root() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parents[2]


def load_set(discipline: str) -> Optional[Dict[str, Any]]:
    rel = SETS.get(str(discipline or ""))
    if not rel:
        return None
    p = _root() / rel
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def score(cases: List[Dict[str, Any]], flags: Dict[str, List[str]]) -> Dict[str, Any]:
    """The two rates, each WITH the counts it is a fraction of, and whether the bar is met.

    `flags` is {case id: [the reasons the agent flagged]}. A planted case is CAUGHT only when its own reason is
    among the flags - a flag for a different reason is a miss, and is listed as a wrong-reason flag. A clean case
    with any flag at all is a false alarm. A case the agent was never shown counts as not flagged."""
    planted = [c for c in cases if c.get("planted")]
    clean = [c for c in cases if not c.get("planted")]
    caught, missed, wrong_reason = [], [], []
    for c in planted:
        got = [str(x) for x in (flags.get(c["id"]) or [])]
        if c.get("must_flag") in got:
            caught.append(c["id"])
        else:
            missed.append({"case": c["id"], "must_flag": c.get("must_flag"), "flagged": got})
            if got:
                wrong_reason.append(c["id"])
    false_alarms = [c["id"] for c in clean if (flags.get(c["id"]) or [])]
    allowed_n, allowed_of = FALSE_ALARMS_ALLOWED_PER_CLEAN
    #  "at most one in six": compared as a fraction, so a set of twelve clean cases allows two and a set of
    #  three allows none
    within_false_alarm_bar = bool(clean) and len(false_alarms) * allowed_of <= allowed_n * len(clean)
    meets = bool(planted) and not missed and within_false_alarm_bar
    return {
        "planted_cases": len(planted), "caught": len(caught),
        "catch_rate": (len(caught) / len(planted)) if planted else None,
        "clean_cases": len(clean), "false_alarms": len(false_alarms),
        "false_alarm_rate": (len(false_alarms) / len(clean)) if clean else None,
        "missed": missed, "flagged_for_the_wrong_reason": wrong_reason, "false_alarm_cases": false_alarms,
        "meets_bar": meets,
        "bar": (f"every planted case flagged for its reason, and at most {allowed_n} false alarm in "
                f"{allowed_of} clean cases"),
        "basis": (f"{len(caught)} of {len(planted)} planted case(s) flagged for their own reason; "
                  f"{len(false_alarms)} of {len(clean)} clean case(s) flagged"
                  + ("" if planted and clean else "; a set with no planted or no clean cases cannot meet the bar")),
    }


def _runs_path():
    from agentic_core.config import data_path
    return data_path(RUNS_STORE)


def _runs() -> Optional[List[Dict[str, Any]]]:
    p = _runs_path()
    if not p.exists():
        return []
    try:
        from agentic_core.config import read_json_strict
        data = read_json_strict(p, list, expect=list)
    except Exception:                       # noqa: BLE001 - unreadable is reported as not known, below
        return None
    return [r for r in (data or []) if isinstance(r, dict)]


def calibration_of(agent: str, discipline: str = "care") -> Dict[str, Any]:
    """Whether `agent` is calibrated for a discipline NOW: its latest run in the MODEL configuration, on the set's
    CURRENT version, re-scored here from the run's own flags. A stored verdict is never trusted - the flags are."""
    the_set = load_set(discipline)
    if not the_set:
        return {"calibrated": False, "known": True, "why_not": f"no calibration set exists for {discipline!r}"}
    if not the_set.get("runnable"):
        return {"calibrated": False, "known": True, "set_version": the_set.get("version"),
                "why_not": ("the calibration set cannot be run yet: its cases are described, not written out in "
                            "full, so no agent has been calibrated on it")}
    runs = _runs()
    if runs is None:
        return {"calibrated": False, "known": False,
                "why_not": "the record of calibration runs could not be read, so no agent is treated as calibrated"}
    mine = [r for r in runs if str(r.get("agent") or "") == str(agent or "") and r.get("discipline") == discipline]
    if not mine:
        return {"calibrated": False, "known": True, "set_version": the_set.get("version"),
                "why_not": "this agent has never been run on the calibration set"}
    on_model = [r for r in mine if r.get("configuration") == "model"]
    if not on_model:
        return {"calibrated": False, "known": True, "set_version": the_set.get("version"),
                "why_not": "this agent has only been run with no model serving; the floor cannot review"}
    latest = max(on_model, key=lambda r: str(r.get("date")))
    if latest.get("set_version") != the_set.get("version"):
        return {"calibrated": False, "known": True, "set_version": the_set.get("version"),
                "why_not": (f"its latest run was on version {latest.get('set_version')!r} of the set, which is now "
                            f"{the_set.get('version')!r}")}
    s = score(the_set.get("cases") or [], latest.get("flags") or {})
    return {"calibrated": bool(s["meets_bar"]), "known": True, "set_version": the_set.get("version"),
            "run_date": latest.get("date"), "model": latest.get("model"),
            "catch_rate": s["catch_rate"], "caught": s["caught"], "planted_cases": s["planted_cases"],
            "false_alarm_rate": s["false_alarm_rate"], "false_alarms": s["false_alarms"], "clean_cases": s["clean_cases"],
            "rates_basis": s["basis"], "bar": s["bar"],
            "why_not": None if s["meets_bar"] else f"its latest run did not meet the bar: {s['basis']}"}
