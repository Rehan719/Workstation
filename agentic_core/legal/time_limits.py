"""W875 (FU-1012) - HOW LONG A TIME LIMIT RUNS: arithmetic on a dated rule, read from its publisher, and a route.

A person asking how long they had was shown no deadline and no route to a person: with no model serving, the research
form put the question's own words under headings. A deadline is arithmetic on a dated rule, and a route is a row in a
directory; neither needs generation. Each rule below names the provision that sets the limit and the WORDS it was built
from. The provision is fetched from its publisher when a person asks, and nothing is computed unless those words are in
it as published for the date asked about. The limit computed is the primary one the Act sets; what it does not account
for is said with it, and so is who to ask. Nothing here composes, and nothing is legal advice.

W1157 (P5.11 clause 2) - THE LIMITS EITHER SIDE OF 1 OCTOBER 2026, AS DATED DATA. Schedule 12 to the Employment Rights
Act 2025 put "six" for "three" in section 111(2) of the Employment Rights Act 1996 (paragraph 4(25)) and "6" for "3" in
section 123(1)(a) of the Equality Act 2010 (paragraph 18). Regulation 3 of S.I. 2026/954 brought Schedule 12 into force
on 1 October 2026, and by regulation 4 it does not apply where the relevant date is before 1 October 2026; its Schedule
gives the relevant date for each complaint - for unfair dismissal the effective date of termination, for a complaint
under section 120 of the Equality Act 2010 the date of the act. The rules W875 wrote held the three-month words alone, so
once the publisher wrote the change into its text no date was worked out for either claim. Each rule now has one period
on each side of 1 October 2026, each with the words of the provision as it stood in that period, read from the
publisher's own version for that period. All of it was read at www.legislation.gov.uk on 2026-11-20
(docs/SOURCES.json).
"""
from __future__ import annotations

import calendar
import datetime as _dt
import re
from typing import Any, Dict, List, Optional

#  Who to ask, for a limit on a claim about work: the free conciliation service such a claim passes through first
_ACAS = {"name": "Acas", "link": "https://www.acas.org.uk/",
         "for_what": "free advice on rights at work, and the early conciliation a tribunal claim must start with"}

#  W1157 - the one change both rules share, with where it is written
CHANGE: Dict[str, str] = {
    "on": "2026-10-01",
    "by": ("Schedule 12 to the Employment Rights Act 2025, in force on 1 October 2026 by regulation 3 of "
           "S.I. 2026/954"),
    "earlier_limit_kept": ("by regulation 4 of S.I. 2026/954 the change does not apply where the relevant date is "
                           "before 1 October 2026"),
    "page": "https://www.legislation.gov.uk/uksi/2026/954/regulation/4",
}

RULES: Dict[str, Dict[str, Any]] = {
    "unfair_dismissal": {
        "name": "an unfair dismissal claim to an employment tribunal",
        "provision": {"kind": "ukpga", "year": 1996, "number": 18, "section": "111",
                      "act": "Employment Rights Act 1996"},
        "event": "the effective date of termination",
        "relevant_date": "the effective date of termination (S.I. 2026/954, the Schedule's first table)",
        #  each period's words are the provision's as it stood in that period, read from the publisher's own version
        "periods": [
            {"until": "2026-09-30", "months": 3, "version": "2026-09-30",
             "words": "three months beginning with the effective date of termination"},
            {"from": "2026-10-01", "months": 6, "version": None,
             "words": "six months beginning with the effective date of termination"},
        ],
        "does_not_account_for": ("early conciliation through Acas, which must be started before this limit and can "
                                 "extend it, and the tribunal's narrow power to allow a later claim"),
        "route": _ACAS,
    },
    "discrimination_at_work": {
        "name": "a discrimination claim about work to an employment tribunal",
        "provision": {"kind": "ukpga", "year": 2010, "number": 15, "section": "123",
                      "act": "Equality Act 2010"},
        "event": "the date of the act the complaint is about",
        "relevant_date": ("the date of the act, the end of conduct extending over a period, or the date a failure was "
                          "decided on (S.I. 2026/954, the Schedule's first table)"),
        "periods": [
            {"until": "2026-09-30", "months": 3, "version": "2026-09-30",
             "words": "3 months starting with the date of the act to which the complaint relates"},
            {"from": "2026-10-01", "months": 6, "version": None,
             "words": "6 months starting with the date of the act to which the complaint relates"},
        ],
        "does_not_account_for": ("early conciliation through Acas, which must be started before this limit and can "
                                 "extend it, conduct extending over a period, and the tribunal's power to allow a "
                                 "later claim where it thinks that just and equitable"),
        "route": _ACAS,
    },
}

ARITHMETIC = ("a period of N months beginning, or starting, with a day includes that day, so it ends at the end of "
              "the day before the same date N months later")


def _flat(s: Any) -> str:
    return re.sub(r"\s+", " ", str(s or "")).strip().lower()


def last_day(event: _dt.date, months: int) -> Optional[_dt.date]:
    """The last day of a period of `months` beginning with `event`, or None when the same date `months` later does
    not exist (30 November + 3 months): there the arithmetic depends on a rule this does not apply."""
    m = event.month - 1 + months
    y, m = event.year + m // 12, m % 12 + 1
    if event.day > calendar.monthrange(y, m)[1]:
        return None
    return _dt.date(y, m, event.day) - _dt.timedelta(days=1)


def _side(period: Dict[str, Any]) -> str:
    return ("a relevant date before 1 October 2026" if period.get("until") else
            "a relevant date on or after 1 October 2026")


def period_for(rule_id: str, event_date: Any) -> Optional[Dict[str, Any]]:
    """W1157 - the period of the rule that the date falls in, or None when the date given is not a date."""
    try:
        ev = _dt.date.fromisoformat(str(event_date))
    except ValueError:
        return None
    for p in RULES[rule_id]["periods"]:
        lo = _dt.date.fromisoformat(p["from"]) if p.get("from") else _dt.date.min
        hi = _dt.date.fromisoformat(p["until"]) if p.get("until") else _dt.date.max
        if lo <= ev <= hi:
            return p
    return None


def periods(rule_id: str) -> List[Dict[str, Any]]:
    """Each period of the rule as the answers show it: which relevant dates it covers, its months and its words."""
    return [{"applies_to": _side(p), "months": p["months"], "words": p["words"],
             "read_from": ("the provision as it stood on " + p["version"]) if p.get("version") else
                          "the provision as it stands now"} for p in RULES[rule_id]["periods"]]


def limit(rule_id: str, event_date: str, provision: Dict[str, Any]) -> Dict[str, Any]:
    """The primary limit for `rule_id` from `event_date`, checked against `provision` as its publisher returned it
    for that date's period, with the limit on the other side of the change beside it."""
    rule = RULES[rule_id]
    period = period_for(rule_id, event_date)
    base = {"rule": rule_id, "name": rule["name"], "act": rule["provision"]["act"],
            "section": rule["provision"]["section"], "words": period["words"] if period else None,
            "months": period["months"] if period else None, "event": rule["event"], "event_date": event_date,
            "relevant_date": rule["relevant_date"], "change": dict(CHANGE), "either_side": periods(rule_id),
            "does_not_account_for": rule["does_not_account_for"], "route": rule["route"],
            "provision_address": provision.get("address"), "version_dated": provision.get("version_dated"),
            "arithmetic": ARITHMETIC, "composed": False, "not_advice": "Nothing here is legal advice."}
    if period is None:
        return {**base, "last_day": None, "computed": False,
                "basis": "NOT COMPUTED - the date given is not a date (write it as YYYY-MM-DD)."}
    shown = _flat(" ".join(str(p.get("text") or "") for p in (provision.get("parts") or [])))
    if _flat(period["words"]) not in shown:
        return {**base, "last_day": None, "computed": False,
                "basis": ("NOT COMPUTED - the provision as its publisher returned it for this date does not contain "
                          "the words this rule was built from, so the rule may have changed. Read the provision, and "
                          f"ask {rule['route']['name']}.")}
    ev = _dt.date.fromisoformat(str(event_date))
    end = last_day(ev, period["months"])
    if end is None:
        return {**base, "last_day": None, "computed": False,
                "basis": (f"NOT COMPUTED - the same date {period['months']} months later does not exist, and how such "
                          f"a period ends is a rule this does not apply. Ask {rule['route']['name']}.")}
    other = next(p for p in rule["periods"] if p is not period)
    earlier = next(p for p in rule["periods"] if p.get("until"))
    later = next(p for p in rule["periods"] if p.get("from"))
    return {**base, "last_day": end.isoformat(), "computed": True,
            "basis": (f"the primary limit the Act sets, from its words as its publisher gives them for this date "
                      f"('{period['words']}'): {period['months']} months beginning with {ev.isoformat()} end at the "
                      f"end of {end.isoformat()}. This is the limit for {_side(period)}, the relevant date being "
                      f"{rule['relevant_date'].split(' (')[0]}. The change from {earlier['months']} to "
                      f"{later['months']} months is {CHANGE['by']}, and {CHANGE['earlier_limit_kept']}. For "
                      f"{_side(other)} the limit is {other['months']} months. It does not account for "
                      f"{rule['does_not_account_for']}.")}
