"""W875 (FU-1012) - HOW LONG A TIME LIMIT RUNS: arithmetic on a dated rule, read from its publisher, and a route.

A person asking how long they had was shown no deadline and no route to a person: with no model serving, the research
form put the question's own words under headings. A deadline is arithmetic on a dated rule, and a route is a row in a
directory; neither needs generation. Each rule below names the provision that sets the limit and the WORDS it was built
from. The provision is fetched from its publisher when a person asks, and nothing is computed unless those words are in
it as published now. The limit computed is the primary one the Act sets; what it does not account for is said with it,
and so is who to ask. Nothing here composes, and nothing is legal advice.
"""
from __future__ import annotations

import calendar
import datetime as _dt
import re
from typing import Any, Dict, Optional

#  Who to ask, for a limit on a claim about work: the free conciliation service such a claim passes through first
_ACAS = {"name": "Acas", "link": "https://www.acas.org.uk/",
         "for_what": "free advice on rights at work, and the early conciliation a tribunal claim must start with"}

RULES: Dict[str, Dict[str, Any]] = {
    "unfair_dismissal": {
        "name": "an unfair dismissal claim to an employment tribunal",
        "provision": {"kind": "ukpga", "year": 1996, "number": 18, "section": "111",
                      "act": "Employment Rights Act 1996"},
        "words": "three months beginning with the effective date of termination",
        "months": 3,
        "event": "the effective date of termination",
        "does_not_account_for": ("early conciliation through Acas, which must be started before this limit and can "
                                 "extend it, and the tribunal's narrow power to allow a later claim"),
        "route": _ACAS,
    },
    "discrimination_at_work": {
        "name": "a discrimination claim about work to an employment tribunal",
        "provision": {"kind": "ukpga", "year": 2010, "number": 15, "section": "123",
                      "act": "Equality Act 2010"},
        "words": "3 months starting with the date of the act to which the complaint relates",
        "months": 3,
        "event": "the date of the act the complaint is about",
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


def limit(rule_id: str, event_date: str, provision: Dict[str, Any]) -> Dict[str, Any]:
    """The primary limit for `rule_id` from `event_date`, checked against `provision` as its publisher returned it."""
    rule = RULES[rule_id]
    shown = _flat(" ".join(str(p.get("text") or "") for p in (provision.get("parts") or [])))
    base = {"rule": rule_id, "name": rule["name"], "act": rule["provision"]["act"],
            "section": rule["provision"]["section"], "words": rule["words"], "event": rule["event"],
            "event_date": event_date, "does_not_account_for": rule["does_not_account_for"], "route": rule["route"],
            "provision_address": provision.get("address"), "version_dated": provision.get("version_dated"),
            "arithmetic": ARITHMETIC, "composed": False, "not_advice": "Nothing here is legal advice."}
    if _flat(rule["words"]) not in shown:
        return {**base, "last_day": None, "computed": False,
                "basis": ("NOT COMPUTED - the provision as its publisher returned it now does not contain the words "
                          "this rule was built from, so the rule may have changed. Read the provision, and ask "
                          f"{rule['route']['name']}.")}
    try:
        ev = _dt.date.fromisoformat(str(event_date))
    except ValueError:
        return {**base, "last_day": None, "computed": False,
                "basis": "NOT COMPUTED - the date given is not a date (write it as YYYY-MM-DD)."}
    end = last_day(ev, rule["months"])
    if end is None:
        return {**base, "last_day": None, "computed": False,
                "basis": ("NOT COMPUTED - the same date three months later does not exist, and how such a period ends "
                          f"is a rule this does not apply. Ask {rule['route']['name']}.")}
    return {**base, "last_day": end.isoformat(), "computed": True,
            "basis": (f"the primary limit the Act sets, from its words as published now ('{rule['words']}'): "
                      f"{rule['months']} months beginning with {ev.isoformat()} end at the end of {end.isoformat()}. "
                      f"It does not account for {rule['does_not_account_for']}.")}
