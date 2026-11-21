"""WHETHER A REVIEWER AGENT IS CALIBRATED - measured from recorded runs, never ticked.

OWNER RULING 2026-10-12 (the review cell, clause 3): a reviewer agent's reviews COUNT only after it is calibrated
on planted defects and clean answers; its catch rate and false-alarm rate are shown beside its reviews; an
uncalibrated agent's review is labelled so. THE PASS BAR, as ruled: every planted case flagged FOR ITS REASON, and
at most one false alarm in six clean cases.

THE FAULT THIS REPLACES (W688 to W690): a review record carried `agent_calibrated`, a flag that was whatever the
person recording it ticked - a claim standing where a measurement was ruled. Calibration is now arithmetic over
a RUN: the cases of a named set, what the agent flagged on each, and the two rates this module computes from
them. A caller cannot assert a rate; a run on a different version of the set does not count for this one.

THE SET. `docs/CARE_REVIEW_CALIBRATION.json` holds the Care cases, each written out from the tree (W1099): a
route's answer, a prompt it sends or an entry it held, and for a planted case one of those with one fix undone,
named in its `from`. WHETHER IT CAN BE RUN IS COMPUTED (runnable, below), never read from a flag: W1099 found
`"runnable": false` typed in the file and read as the state - a claim where the rule is a measurement.

ONLY THE AGENT'S OWN RUN COUNTS (W1183). A run typed through the record door (POST /calibration/run) is a person's
account of what was flagged: it is kept, and calibrates nothing. A run counts only when the agent made it through
its own door (POST /calibration/agent-run), dated the day it was made, on the set as it stands (its checklist and
cases hashed, so a case edited under the same version voids it), with every case answered by a FLAG line. What is
said of an agent's calibration wherever its reviews are read is calibration_statement(): with no run of its own
there are no rates, and none is said as nought.
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
#  W1183 (FU-1054) - each discipline's one reviewer agent, and the two doors a run comes in by
REVIEWER_OF = {"care": "care-reviewer"}
AGENT_DOOR = "agent-run"          # the agent over the set, through its own route: evidence of what it catches
TYPED_DOOR = "typed"              # flags a person typed through the record door: kept, and calibrating nothing


def _today():
    """W1183 - the one clock the calibration reads: the server's own date. A guard pins it, so what a capture says is
    what the routes say on the day it was taken."""
    import datetime as _dt
    return _dt.date.today()


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


def _register():
    """The one register of sources (docs/SOURCES.json): its rows by id, and its review period in days."""
    d = json.loads((_root() / "docs" / "SOURCES.json").read_text(encoding="utf-8"))
    return ({str(r["id"]): r for r in d.get("rows") or [] if isinstance(r, dict) and r.get("id")},
            int(d.get("review_days") or 90))


def _not_read(row: Dict[str, Any]) -> List[str]:
    """What a row says was NOT READ, in its own words: each 'NOT READ: ...' to the end of its sentence."""
    return [part.split(".")[0].strip() for part in str(row.get("says") or "").split("NOT READ:")[1:]]


def runnable(the_set: Dict[str, Any], on: Any = None) -> Dict[str, Any]:
    """W1099 (FU-1054) - whether a set can be run on date `on` (today when not given), and EVERY reason it cannot.
    Computed from the cases and the register of sources; a `runnable` key in the file is not read. It cannot be run
    while a case is not written out (`shown`), a planted case does not say where this repository had its defect
    (`from`), or a row a case relies on is not in the status the case names: missing from the register, in another
    status, a current row not read within the register's review period of `on` (or read after it), or a part of
    the row the case relies on that the row says was NOT READ."""
    import datetime as _dt
    if isinstance(on, _dt.date):
        day = on
    else:
        try:
            day = _dt.date.fromisoformat(str(on)[:10]) if on else _today()
        except ValueError:
            return {"runnable": False, "on": None, "why_not": [f"{on!r} is not a date"]}
    try:
        rows, review = _register()
    except Exception as e:                       # noqa: BLE001 - said: no source is known to be read
        return {"runnable": False, "on": day.isoformat(), "why_not": [
            f"the register of sources could not be read ({type(e).__name__}), so no source a case relies on is "
            f"known to be read"]}
    why: List[str] = []
    for c in the_set.get("cases") or []:
        cid, shown = c.get("id"), c.get("shown")
        if not ((isinstance(shown, str) and shown.strip()) or (isinstance(shown, dict) and shown)):
            why.append(f"{cid} is described, not written out in full"
                       + (f": {c['not_written']}" if c.get("not_written") else ""))
        if c.get("planted") and not str(c.get("from") or "").strip():
            why.append(f"{cid} does not say where this repository had its defect")
        for need in c.get("relies_on") or []:
            rid, status, part = str(need.get("row")), need.get("status"), need.get("part")
            r = rows.get(rid)
            if r is None:
                why.append(f"{cid} relies on {rid}, which is not a row of the register of sources")
                continue
            if r.get("status") != status:
                why.append(f"{cid} relies on {rid} being {status}, and the register holds it as {r.get('status')}")
                continue
            if status == "current":
                try:
                    age = (day - _dt.date.fromisoformat(str(r.get("read_on")))).days
                except ValueError:
                    age = None
                if age is None or age < 0 or age > review:
                    why.append(f"{cid} relies on {rid}, which was not read within the register's {review}-day "
                               f"review period before {day.isoformat()}")
            if part and part in _not_read(r):
                why.append(f"{cid} relies on {part} ({rid}), which the register says was NOT READ")
    return {"runnable": not why, "on": day.isoformat(), "why_not": why}


def set_digest(the_set: Dict[str, Any]) -> str:
    """W1183 - what a run was made on: the set's checklist and its cases, hashed. A case or the checklist edited
    under the same version is another set, and a run on the old one does not count for it."""
    import hashlib
    body = {"checklist": the_set.get("checklist"), "cases": the_set.get("cases")}
    return hashlib.sha256(json.dumps(body, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def runnable_window(the_set: Dict[str, Any]) -> Optional[Dict[str, str]]:
    """W1183 - the days the set can be run as the register stands: from the latest read of a current row a case
    relies on, through the earliest such read plus the register's review period. None when the set cannot be run
    at both ends (a case not written out, a part not read, a row in another status) or no case relies on a current
    row: no window is guessed."""
    import datetime as _dt
    try:
        rows, review = _register()
    except Exception:                       # noqa: BLE001 - not known, so no window is said
        return None
    reads = []
    for c in the_set.get("cases") or []:
        for need in c.get("relies_on") or []:
            r = rows.get(str(need.get("row")))
            if need.get("status") == "current" and r and r.get("status") == "current":
                try:
                    reads.append(_dt.date.fromisoformat(str(r.get("read_on"))))
                except ValueError:
                    return None
    if not reads:
        return None
    start, through = max(reads), min(reads) + _dt.timedelta(days=review)
    if start > through or not (runnable(the_set, on=start)["runnable"] and runnable(the_set, on=through)["runnable"]):
        return None
    return {"from": start.isoformat(), "through": through.isoformat()}


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
    """Whether `agent` is calibrated for a discipline NOW: its latest run of its OWN (W1183: made through its own door,
    in the MODEL configuration), on the set as it stands, re-scored here from the run's own flags. A stored verdict is
    never trusted - the flags are. Every answer carries `reason`, one of: no_set, set_cannot_run, store_unreadable,
    never_run, floor_only, typed_only, older_version, set_changed, not_answered, below_bar, calibrated."""
    the_set = load_set(discipline)
    if not the_set:
        return {"calibrated": False, "known": True, "reason": "no_set",
                "why_not": f"no calibration set exists for {discipline!r}"}
    can = runnable(the_set)
    if not can["runnable"]:
        #  W1099 (FU-1054) - computed now, never read from a flag; while the set cannot be run, no agent counts as
        #  calibrated on it, so a calibration whose sources have gone unread past their period stops counting
        return {"calibrated": False, "known": True, "reason": "set_cannot_run", "set_version": the_set.get("version"),
                "set_cannot_run": can["why_not"],
                "why_not": ("the calibration set cannot be run yet, so no agent has been calibrated on it: "
                            + "; ".join(can["why_not"]))}
    runs = _runs()
    if runs is None:
        return {"calibrated": False, "known": False, "reason": "store_unreadable",
                "why_not": "the record of calibration runs could not be read, so no agent is treated as calibrated"}
    mine = [r for r in runs if str(r.get("agent") or "") == str(agent or "") and r.get("discipline") == discipline]
    if not mine:
        return {"calibrated": False, "known": True, "reason": "never_run", "set_version": the_set.get("version"),
                "why_not": "this agent has never been run on the calibration set"}
    on_model = [r for r in mine if r.get("configuration") == "model"]
    if not on_model:
        return {"calibrated": False, "known": True, "reason": "floor_only", "set_version": the_set.get("version"),
                "why_not": "this agent has only been run with no model serving; the floor cannot review"}
    #  W1183 - ONLY A RUN THE AGENT MADE THROUGH ITS OWN DOOR COUNTS: a typed run is a person's account of what was
    #  flagged, and a run kept before runs said which door made them says nothing either way
    own = [r for r in on_model if r.get("door") == AGENT_DOOR]
    if not own:
        return {"calibrated": False, "known": True, "reason": "typed_only", "set_version": the_set.get("version"),
                "why_not": ("no run of its own: its runs were typed through the run door, a person's account of what "
                            "was flagged, or kept before a run said which door made it, and such a run calibrates "
                            "nothing")}
    #  the latest by its date; of runs made the same day, the last one entered (a stable sort keeps their order)
    latest = sorted(own, key=lambda r: str(r.get("date")))[-1]
    run = {"run_id": latest.get("run_id"), "date": latest.get("date"), "model": latest.get("model"),
           "served_identity": latest.get("served_identity"), "set_version": latest.get("set_version")}
    if latest.get("set_version") != the_set.get("version"):
        return {"calibrated": False, "known": True, "reason": "older_version", "set_version": the_set.get("version"),
                "run": run,
                "why_not": (f"its latest run was on version {latest.get('set_version')!r} of the set, which is now "
                            f"{the_set.get('version')!r}")}
    if latest.get("set_digest") != set_digest(the_set):
        return {"calibrated": False, "known": True, "reason": "set_changed", "set_version": the_set.get("version"),
                "run": run,
                "why_not": ("its latest run was made on cases or a checklist that have changed since under the same "
                            "version, so it does not count for the set as it stands")}
    s = score(the_set.get("cases") or [], latest.get("flags") or {})
    out = {"known": True, "set_version": the_set.get("version"), "run": run,
           "run_date": latest.get("date"), "model": latest.get("model"),
           "catch_rate": s["catch_rate"], "caught": s["caught"], "planted_cases": s["planted_cases"],
           "false_alarm_rate": s["false_alarm_rate"], "false_alarms": s["false_alarms"], "clean_cases": s["clean_cases"],
           "rates_basis": s["basis"], "bar": s["bar"]}
    #  W1183 - A CASE THE AGENT ANSWERED WITH NO FLAG LINE was not reviewed, so the run calibrates nothing
    unanswered = [str(x) for x in latest.get("not_answered") or []]
    if unanswered:
        return {**out, "calibrated": False, "reason": "not_answered", "not_answered": unanswered,
                "why_not": (f"its latest run did not answer {', '.join(unanswered)} with one of the set's reasons or "
                            f"'FLAG: none', so those were not reviewed and the run calibrates nothing")}
    return {**out, "calibrated": bool(s["meets_bar"]), "reason": "calibrated" if s["meets_bar"] else "below_bar",
            "why_not": None if s["meets_bar"] else f"its latest run did not meet the bar: {s['basis']}"}


def _model_said(run: Dict[str, Any]) -> str:
    """The run's model as its record holds it, with the model and build the runtime reported for it, or that the build
    is not known."""
    ident = run.get("served_identity") or {}
    digest = str(ident.get("build_digest") or "")
    return (f"{run.get('model')} ({ident.get('model') or run.get('model')}, build "
            + (f"{digest[:12]})" if digest else "not known)"))


def calibration_statement(agent: str, discipline: str = "care") -> Dict[str, Any]:
    """W1183 (FU-1054, P5.15 clause 3) - what is said of a reviewer agent's calibration wherever its reviews are read,
    made in one place: whether it is calibrated and why, in a sentence, and its two rates with their counts once it has
    a run of its own. With no run there are no rates: none is said as nought. Nothing here is typed by a caller."""
    cal = calibration_of(agent, discipline)
    the_set = load_set(discipline) or {}
    cases = the_set.get("cases") or []
    planted = sum(1 for c in cases if c.get("planted"))
    reason, run = cal.get("reason"), cal.get("run")
    allowed_n, allowed_of = FALSE_ALARMS_ALLOWED_PER_CLEAN
    bar = cal.get("bar") or (f"every planted case flagged for its reason, and at most {allowed_n} false alarm in "
                             f"{allowed_of} clean cases")
    on = f"on {run.get('date')} with {_model_said(run)}" if run else None
    if reason == "never_run":
        basis = (f"never run on its calibration set (version {the_set.get('version')}: {planted} planted cases, "
                 f"{len(cases) - planted} clean), so it has no catch rate and no false-alarm rate, and no review by it "
                 f"raises a tool's tier")
    elif reason == "typed_only":
        basis = str(cal.get("why_not"))          # one sentence, calibration_of's own
    elif reason == "set_cannot_run":
        basis = ("uncalibrated because the calibration set cannot be run today, so no agent is calibrated on it: "
                 + "; ".join(cal.get("set_cannot_run") or []))
    elif reason == "calibrated" and on:
        basis = f"calibrated by its run {on}, which met the bar ({bar})"
    elif reason == "below_bar" and on:
        basis = f"its latest run, {on}, did not meet the bar ({bar})"
    elif reason == "not_answered" and on:
        basis = (f"its latest run, {on}, did not answer {', '.join(cal.get('not_answered') or [])} with one of the "
                 f"set's reasons or 'FLAG: none', so those were not reviewed and the run calibrates nothing")
    else:
        basis = str(cal.get("why_not") or ("calibrated" if cal.get("calibrated") else "not calibrated"))
    rates = None
    if cal.get("caught") is not None and cal.get("planted_cases") is not None:
        rates = {k: cal.get(k) for k in ("caught", "planted_cases", "catch_rate", "false_alarms", "clean_cases",
                                         "false_alarm_rate")}
        rates["basis"] = (f"catch rate: {cal['caught']} of {cal['planted_cases']} planted case(s) flagged for their "
                          f"own reason; false-alarm rate: {cal['false_alarms']} of {cal['clean_cases']} clean case(s) "
                          f"flagged")
    can = runnable(the_set) if the_set else {"runnable": False}
    label = ("Calibrated" if cal.get("calibrated") else
             "Calibration not known" if cal.get("known") is False else "Uncalibrated")
    return {"agent": agent, "discipline": discipline, "calibrated": bool(cal.get("calibrated")),
            "known": cal.get("known") is not False, "reason": reason, "label": label, "basis": basis, "rates": rates,
            "run": run, "bar": bar,
            "set": {"version": the_set.get("version"), "cases": len(cases), "planted": planted,
                    "clean": len(cases) - planted, "runnable_today": bool(can.get("runnable")),
                    "window": runnable_window(the_set) if the_set else None}}
