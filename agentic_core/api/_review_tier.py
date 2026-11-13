"""THE TIER OF REVIEW A TOOL HAS REACHED - said on every answer, and UNREVIEWED until a record exists.

OWNER RULING 2026-10-12 (the review cell, first clause): every tool states the HIGHEST of three tiers it has
reached - checked by rule, reviewed by Workstation's specialist agent, signed by a qualified person - and
nothing reads as a higher tier than its record shows; a tool with no record says UNREVIEWED.

THIS MODULE READS AND STATES. It writes no record: the doors by which a review is recorded (an agent's review
with its checklist and sources, a person's signature with their stated credential) are the next clauses' work.
So today every tool says UNREVIEWED, and that is the true statement. What is here is the one function every
answer passes through, and the rules by which a stored record does or does not count:

  - a record names the tool it is for, the tier it claims, and the date;
  - an agent's review counts only when it names its checklist and the sources it read, and the agent is marked
    CALIBRATED - an uncalibrated agent's review is reported, labelled, and does not raise the tier;
  - W921 (clause 2): and only when it is a whole record - the tool version it reviewed, each source read as a row of
    the register of sources with its page and the date it was read, and what it could not check;
  - a person's signature counts only when it carries a name, a credential AS STATED (this platform verifies no
    credential, and says so), what was reviewed, and a date on which it lapses that has not passed;
  - a record that does not meet its tier's rule is counted as not meeting it, never read down to a lower tier.

No tier, record or sentence here claims a professional's role for an agent.
"""
from __future__ import annotations

import datetime as _dt
from typing import Any, Dict, List, Optional

UNREVIEWED = "unreviewed"
CHECKED_BY_RULE = "checked_by_rule"
REVIEWED_BY_AGENT = "reviewed_by_workstation_agent"
SIGNED_BY_PERSON = "signed_by_a_qualified_person"
#  lowest to highest; a tool states the HIGHEST it has reached
ORDER = (UNREVIEWED, CHECKED_BY_RULE, REVIEWED_BY_AGENT, SIGNED_BY_PERSON)
LABEL = {
    UNREVIEWED: "Unreviewed",
    CHECKED_BY_RULE: "Checked by rule",
    REVIEWED_BY_AGENT: "Reviewed by Workstation's specialist agent",
    SIGNED_BY_PERSON: "Signed by a qualified person",
}
STORE = "review_tier_records.json"
NOT_VERIFIED = "this platform does not verify a person's credential; it records what the person stated"


def _path():
    #  resolved when called, never held as a module constant: the data root differs per test worker
    from agentic_core.config import data_path
    return data_path(STORE)


def _records() -> Optional[List[Dict[str, Any]]]:
    """Every stored record, [] when none has been written, None when the store exists and cannot be read."""
    p = _path()
    if not p.exists():
        return []
    try:
        from agentic_core.config import read_json_strict
        data = read_json_strict(p, list, expect=list)
    except Exception:                       # noqa: BLE001 - unreadable is reported as unreadable, below
        return None
    return [r for r in (data or []) if isinstance(r, dict)]


def _source_register() -> Optional[Dict[str, Dict[str, Any]]]:
    """The register of sources (docs/SOURCES.json) by id, or None when it cannot be read."""
    import json
    from pathlib import Path
    try:
        rows = json.loads((Path(__file__).resolve().parents[2] / "docs" / "SOURCES.json").read_text(encoding="utf-8"))["rows"]
        return {str(r["id"]): r for r in rows if isinstance(r, dict) and r.get("id")}
    except (OSError, ValueError, KeyError, TypeError):
        return None


def _clause2_missing(record: Dict[str, Any], today: _dt.date) -> Optional[str]:
    """W921 (P5.15 clause 2) - what an agent's review lacks of a whole record, or None when it lacks nothing."""
    if not str(record.get("tool_version") or "").strip():
        return "it does not say which version of the tool it reviewed"
    if not str(record.get("could_not_check") or "").strip():
        return "it does not say what it could not check (it says 'nothing' when that is so)"
    register = _source_register()
    if register is None:
        return "the register of sources (docs/SOURCES.json) could not be read, so no source it names can be checked"
    for s in record.get("sources_read") or []:
        if not isinstance(s, dict):
            return (f"the source {str(s)[:60]!r} is not recorded with the page read and the date it was read "
                    f"(a record from before clause 2 is not counted)")
        sid = str(s.get("source") or "").strip()
        if sid not in register:
            return f"the source {sid!r} is not a row of the register of sources (docs/SOURCES.json)"
        if not str(s.get("page") or "").strip():
            return f"the source {sid!r} does not say which page or section was read"
        read_on = _date(s.get("read_on"))
        if not read_on:
            return f"the source {sid!r} does not say on what date it was read"
        if read_on > today:
            return f"the source {sid!r} is dated {read_on.isoformat()}, after today"
        if register[sid].get("status") == "replaced":
            return (f"the source {sid!r} is marked replaced in the register (by {register[sid].get('replaced_by')}), "
                    f"so the review was made against a superseded text")
    return None


def _date(value) -> Optional[_dt.date]:
    try:
        return _dt.date.fromisoformat(str(value)[:10])
    except (TypeError, ValueError):
        return None


def counts(record: Dict[str, Any], today: Optional[_dt.date] = None) -> Dict[str, Any]:
    """Whether ONE record counts for the tier it claims, and why not when it does not."""
    today = today or _dt.datetime.now(_dt.timezone.utc).date()
    tier = record.get("tier")
    if tier not in ORDER[1:]:
        return {"counts": False, "why_not": f"it claims {tier!r}, which is not a tier"}
    if not _date(record.get("date")):
        return {"counts": False, "why_not": "it carries no date"}
    if tier == CHECKED_BY_RULE:
        if not str(record.get("rule") or "").strip() or not str(record.get("test") or "").strip():
            return {"counts": False, "why_not": "it names no rule and no test that runs it"}
    elif tier == REVIEWED_BY_AGENT:
        if not str(record.get("checklist") or "").strip() or not (record.get("sources_read") or []):
            return {"counts": False, "why_not": "it names no checklist or no source it read"}
        _short = _clause2_missing(record, today)                 # W921 (P5.15 clause 2) - a whole record, or none
        if _short:
            return {"counts": False, "why_not": _short}
        #  W691 - CALIBRATION IS MEASURED, NEVER TICKED. This used to read a flag on the record, which was
        #  whatever the person recording it set. It is now read from the agent's own recorded run on the
        #  discipline's calibration set, re-scored from that run's flags. A flag left on an older record is
        #  ignored.
        if not str(record.get("agent") or "").strip():
            return {"counts": False, "why_not": "it does not name the agent that reviewed"}
        from agentic_core.api._review_calibration import calibration_of
        cal = calibration_of(str(record["agent"]), str(record.get("discipline") or "care"))
        if not cal.get("calibrated"):
            return {"counts": False, "uncalibrated_agent_review": True, "calibration": cal,
                    "why_not": ("the agent that reviewed is not calibrated on planted defects and clean answers: "
                                + str(cal.get("why_not")))}
        return {"counts": True, "why_not": None, "calibration": cal}
    elif tier == SIGNED_BY_PERSON:
        if not str(record.get("name") or "").strip() or not str(record.get("credential_as_stated") or "").strip():
            return {"counts": False, "why_not": "it carries no name or no credential as the person stated it"}
        if not str(record.get("reviewed") or "").strip():
            return {"counts": False, "why_not": "it does not say what was reviewed"}
        lapses = _date(record.get("lapses_on"))
        if not lapses:
            return {"counts": False, "why_not": "it carries no date on which it lapses"}
        if lapses < today:
            return {"counts": False, "why_not": f"it lapsed on {lapses.isoformat()}"}
    return {"counts": True, "why_not": None}


def review_statement(tool: str, today: Optional[_dt.date] = None) -> Dict[str, Any]:
    """What an answer says about the review its tool has reached. One function, for every tool."""
    recs = _records()
    if recs is None:
        #  the store is there and unreadable: the tier is NOT KNOWN, which is not the same as unreviewed - and
        #  it is never read as reviewed
        return {"tier": UNREVIEWED, "label": LABEL[UNREVIEWED], "known": False,
                "basis": ("the record of reviews could not be read, so no review can be shown for this tool; "
                          "it is treated as unreviewed"),
                "records_counted": 0, "records_not_counted": 0}
    mine = [r for r in recs if str(r.get("tool") or "") == str(tool or "")]
    judged = [(r, counts(r, today)) for r in mine]
    good = [r for r, v in judged if v["counts"]]
    not_counted = [{"tier": r.get("tier"), "why_not": v["why_not"]} for r, v in judged if not v["counts"]]
    tier = max((r["tier"] for r in good), key=ORDER.index, default=UNREVIEWED)
    out: Dict[str, Any] = {
        "tier": tier, "label": LABEL[tier], "known": True,
        "records_counted": len(good), "records_not_counted": len(not_counted),
        "of_tiers": [LABEL[t] for t in ORDER[1:]],
    }
    if tier == UNREVIEWED:
        out["basis"] = ("no review of this tool is recorded: no rule check, no review by a calibrated agent and no "
                        "qualified person's signature. Treat what it returns as unreviewed"
                        + (f". {len(not_counted)} record(s) exist and do not count" if not_counted else ""))
    else:
        top = max((r for r in good if r["tier"] == tier), key=lambda r: str(r.get("date")))
        out["basis"] = (f"the highest tier a record supports: {LABEL[tier].lower()}, dated {str(top.get('date'))[:10]}"
                        + (f", by {top['name']} ({top['credential_as_stated']} - as stated; {NOT_VERIFIED})"
                           + f", until {str(top['lapses_on'])[:10]}" if tier == SIGNED_BY_PERSON else ""))
    #  the reviewing agent's two rates, WITH their counts, beside its review (clause 3) - when it has a run
    for r, v in judged:
        cal = v.get("calibration") or {}
        if r.get("tier") == REVIEWED_BY_AGENT and cal.get("catch_rate") is not None:
            out["agent_rates"] = {"agent": r.get("agent"), "calibrated": bool(cal.get("calibrated")),
                                  "caught": cal.get("caught"), "planted_cases": cal.get("planted_cases"),
                                  "false_alarms": cal.get("false_alarms"), "clean_cases": cal.get("clean_cases"),
                                  "basis": cal.get("rates_basis"), "bar": cal.get("bar")}
    if tier == REVIEWED_BY_AGENT and out.get("agent_rates", {}).get("basis"):
        #  the rates travel IN the sentence every page and download already shows, not only beside it
        out["basis"] += f"; the reviewing agent's calibration: {out['agent_rates']['basis']}"
    if not_counted:
        out["not_counted"] = not_counted[:5]
        if any(v.get("uncalibrated_agent_review") for _r, v in judged):
            out["uncalibrated_agent_review"] = ("an agent's review of this tool exists and does not raise its tier: "
                                                "the agent has not been calibrated")
    return out
