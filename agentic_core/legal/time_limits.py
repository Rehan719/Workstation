"""W875 (FU-1012) - HOW LONG A TIME LIMIT RUNS: arithmetic on a dated rule, read from its publisher, and a route.

A person asking how long they had was shown no deadline and no route to a person: with no model serving, the research
form put the question's own words under headings. A deadline is arithmetic on a dated rule, and a route is a row in a
directory; neither needs generation. Each rule below names the provision that sets the limit and the WORDS it was built
from. The provision is fetched from its publisher when a person asks, and nothing is computed unless those words are in
it as published for the date asked about. The limit computed is the primary one the provision sets; what it does not
account for is said with it, and so is who to ask. Nothing here composes, and nothing is legal advice.

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

W1160 (P5.11 clause 2, FU-1296) - BREACH OF CONTRACT, AND THE SCOTTISH EXCEPTION. A breach of contract claim to an
employment tribunal is brought under an Extension of Jurisdiction Order, one for England and Wales (S.I. 1994/1623) and
one for Scotland (S.I. 1994/1624), each by its article 7. Each was changed from three months to six on its own date by
its own instrument: by article 2 of S.I. 2026/759 from 1 October 2026 for England and Wales, and by article 2(2) of
S.S.I. 2026/327 from 9 November 2026 for Scotland, each applying only where the effective date of termination, or with
none the last day worked, is on or after that date (each instrument's article 3). So each rule now says the nations it
is for and the change it has. The publisher has written the England and Wales change into its text. For Scotland it
lists the change as not yet written into its text of article 7, so the Scottish rule's later period is read from the
earlier words together with the change the publisher lists, and from nothing else. All of it was read at
www.legislation.gov.uk on 2026-11-20 (docs/SOURCES.json).

W1161 (P5.11 clause 2) - WHEN NO RULE MATCHES. The calculator never answers "no deadline". A claim it holds no rule for,
and a claim whose rule is not for the nation asked about, are answered that a time limit may still apply, with where to
ask today for that nation; a question from a nation no rule here is for is given a route and not a rule (the Owner's
ruling of 2026-10-12). Every place named for it is named, with the address given, on GOV.UK's guide "Employment
tribunals", read whole through GOV.UK's content API on 2026-11-20 (docs/SOURCES.json). The places' own sites refused an
automated visit from where this was built, so none of them was read, and each says so; and each place is shown as not
recently checked ninety days after the guide was read, as the same ruling sets for a rule or a place.
"""
from __future__ import annotations

import calendar
import datetime as _dt
import re
from typing import Any, Dict, List, Optional, Tuple

#  Who to ask, for a limit on a claim about work: the free conciliation service such a claim passes through first
_ACAS = {"name": "Acas", "link": "https://www.acas.org.uk/",
         "for_what": "free advice on rights at work, and the early conciliation a tribunal claim must start with"}

#  W1157 - the one change both statutory rules share, with where it is written
CHANGE: Dict[str, str] = {
    "on": "2026-10-01",
    "by": ("Schedule 12 to the Employment Rights Act 2025, in force on 1 October 2026 by regulation 3 of "
           "S.I. 2026/954"),
    "earlier_limit_kept": ("by regulation 4 of S.I. 2026/954 the change does not apply where the relevant date is "
                           "before 1 October 2026"),
    "page": "https://www.legislation.gov.uk/uksi/2026/954/regulation/4",
}

#  W1160 - the two changes to the breach of contract limit, each with its own date and its own instrument
CHANGE_CONTRACT_ENGLAND_WALES: Dict[str, str] = {
    "on": "2026-10-01",
    "by": ("article 2 of the Employment Tribunals Extension of Jurisdiction (England and Wales) (Amendment) Order 2026 "
           "(S.I. 2026/759), in force on 1 October 2026 by its article 1(2)"),
    "earlier_limit_kept": ("by article 3 of S.I. 2026/759 the change applies only where the effective date of "
                           "termination, or with none the last day worked, is on or after 1 October 2026"),
    "page": "https://www.legislation.gov.uk/uksi/2026/759/article/3/made",
}
CHANGE_CONTRACT_SCOTLAND: Dict[str, str] = {
    "on": "2026-11-09",
    "by": ("article 2(2) of the Employment Tribunals Extension of Jurisdiction (Amendment) (Scotland) Order 2026 "
           "(S.S.I. 2026/327), in force on 9 November 2026 by its article 1"),
    "earlier_limit_kept": ("by article 3(1) of S.S.I. 2026/327 the change applies only where the effective date of "
                           "termination, or with none the last day worked, is on or after 9 November 2026"),
    "page": "https://www.legislation.gov.uk/ssi/2026/327/article/3/made",
}

_GREAT_BRITAIN = ["England", "Wales", "Scotland"]
#  the words of article 7(a) of either Order, after its number of months
_CONTRACT = "months beginning with the effective date of termination of the contract giving rise to the claim"
_CONTRACT_NOT_COUNTED = ("early conciliation through Acas, which must be started before this limit and can extend it, "
                         "a claim with no effective date of termination, whose period runs from the last day worked, "
                         "and the tribunal's narrow power to allow a later claim")

RULES: Dict[str, Dict[str, Any]] = {
    "unfair_dismissal": {
        "name": "an unfair dismissal claim to an employment tribunal",
        "provision": {"kind": "ukpga", "year": 1996, "number": 18, "section": "111",
                      "act": "Employment Rights Act 1996"},
        "nations": _GREAT_BRITAIN,
        "change": CHANGE,
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
        "nations": _GREAT_BRITAIN,
        "change": CHANGE,
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
    "breach_of_contract_england_wales": {
        "name": "a breach of contract claim to an employment tribunal, in England or Wales",
        "provision": {"kind": "uksi", "year": 1994, "number": 1623, "part": "article", "section": "7",
                      "act": "Employment Tribunals Extension of Jurisdiction (England and Wales) Order 1994"},
        "nations": ["England", "Wales"],
        "change": CHANGE_CONTRACT_ENGLAND_WALES,
        "event": "the effective date of termination of the contract",
        "relevant_date": ("the effective date of termination of the contract giving rise to the claim, or with none "
                          "the last day the employee worked (S.I. 2026/759, article 3)"),
        "periods": [
            {"until": "2026-09-30", "months": 3, "version": "2026-09-30", "words": "three " + _CONTRACT},
            {"from": "2026-10-01", "months": 6, "version": None, "words": "six " + _CONTRACT},
        ],
        "does_not_account_for": _CONTRACT_NOT_COUNTED,
        "route": _ACAS,
    },
    "breach_of_contract_scotland": {
        "name": "a breach of contract claim to an employment tribunal, in Scotland",
        "provision": {"kind": "uksi", "year": 1994, "number": 1624, "part": "article", "section": "7",
                      "act": "Employment Tribunals Extension of Jurisdiction (Scotland) Order 1994"},
        "nations": ["Scotland"],
        "change": CHANGE_CONTRACT_SCOTLAND,
        "event": "the effective date of termination of the contract",
        "relevant_date": ("the effective date of termination of the contract giving rise to the claim, or with none "
                          "the last day the employee worked (S.S.I. 2026/327, article 3)"),
        "periods": [
            {"until": "2026-11-08", "months": 3, "version": "2026-11-08", "words": "three " + _CONTRACT},
            {"from": "2026-11-09", "months": 6, "version": None, "words": "six " + _CONTRACT,
             #  the publisher lists this change as not yet written into its text of article 7: until it is, the text
             #  holds the earlier words, and the change it lists puts six for three
             "unapplied": {"class": "ScottishStatutoryInstrument", "year": "2026", "number": "327",
                           "earlier_words": "three " + _CONTRACT}},
        ],
        "does_not_account_for": _CONTRACT_NOT_COUNTED,
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


_MONTHS = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
           "November", "December")                  # fixed, so no locale changes what a date is said as


def _said(iso: str) -> str:
    d = _dt.date.fromisoformat(iso)
    return f"{d.day} {_MONTHS[d.month - 1]} {d.year}"


def _side(period: Dict[str, Any], change: Optional[Dict[str, str]] = None) -> str:
    on = _said((change or CHANGE)["on"])
    return f"a relevant date before {on}" if period.get("until") else f"a relevant date on or after {on}"


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
    rule = RULES[rule_id]
    return [{"applies_to": _side(p, rule["change"]), "months": p["months"], "words": p["words"],
             "read_from": ("the provision as it stood on " + p["version"]) if p.get("version") else
                          ("the provision as it stands now, with the change its publisher lists as not yet written "
                           "into it" if p.get("unapplied") else "the provision as it stands now")}
            for p in rule["periods"]]


def _listed(provision: Dict[str, Any], unapplied: Dict[str, str]) -> List[Dict[str, Any]]:
    """W1160 - the changes the publisher lists as not yet written into this provision that are this period's change."""
    return [e for e in (provision.get("changes_not_yet_applied_to_this_provision") or [])
            if str(e.get("AffectingYear")) == unapplied["year"] and str(e.get("AffectingNumber")) == unapplied["number"]
            and e.get("AffectingClass") in (None, unapplied["class"])]


def limit(rule_id: str, event_date: str, provision: Dict[str, Any], nation: Optional[str] = None) -> Dict[str, Any]:
    """The primary limit for `rule_id` from `event_date`, checked against `provision` as its publisher returned it
    for that date's period, with the limit on the other side of the change beside it. W1161: `nation` is the nation
    asked about, which the rule is for (a nation it is not for is answered by `no_rule`), or None when none was given."""
    rule = RULES[rule_id]
    change = rule["change"]
    period = period_for(rule_id, event_date)
    sets = "the Act sets" if rule["provision"]["kind"] == "ukpga" else "the Order sets"
    base = {"rule": rule_id, "matched": True, "nation": nation, "name": rule["name"], "act": rule["provision"]["act"],
            "part": rule["provision"].get("part", "section"), "section": rule["provision"]["section"],
            "nations": list(rule["nations"]), "words": period["words"] if period else None,
            "months": period["months"] if period else None, "event": rule["event"], "event_date": event_date,
            "relevant_date": rule["relevant_date"], "change": dict(change), "either_side": periods(rule_id),
            "does_not_account_for": rule["does_not_account_for"], "route": rule["route"],
            "provision_address": provision.get("address"), "version_dated": provision.get("version_dated"),
            "arithmetic": ARITHMETIC, "composed": False, "not_advice": "Nothing here is legal advice."}
    if period is None:
        return {**base, "last_day": None, "computed": False,
                "basis": "NOT COMPUTED - the date given is not a date (write it as YYYY-MM-DD)."}
    shown = _flat(" ".join(str(p.get("text") or "") for p in (provision.get("parts") or [])))
    unapplied = period.get("unapplied")
    read = f"from its words as its publisher gives them for this date ('{period['words']}')"
    if _flat(period["words"]) not in shown:
        #  W1160 - the earlier words, with the change the publisher itself lists as not yet written in, and nothing less
        if not (unapplied and _flat(unapplied["earlier_words"]) in shown and _listed(provision, unapplied)):
            return {**base, "last_day": None, "computed": False,
                    "basis": ("NOT COMPUTED - the provision as its publisher returned it for this date does not contain "
                              "the words this rule was built from, so the rule may have changed. Read the provision, "
                              f"and ask {rule['route']['name']}.")}
        read = (f"from its publisher's text, which still reads '{unapplied['earlier_words']}' and lists the change below "
                f"as not yet written into it; that change puts six for three, so for this date the words are "
                f"'{period['words']}'")
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
            **({"read_with_unapplied_change": True} if read.startswith("from its publisher's text") else {}),
            "basis": (f"the primary limit {sets}, {read}: {period['months']} months beginning with {ev.isoformat()} "
                      f"end at the end of {end.isoformat()}. This is the limit for {_side(period, change)}, the "
                      f"relevant date being {rule['relevant_date'].split(' (')[0]}. The change from "
                      f"{earlier['months']} to {later['months']} months is {change['by']}, and "
                      f"{change['earlier_limit_kept']}. For {_side(other, change)} the limit is {other['months']} "
                      f"months. It does not account for {rule['does_not_account_for']}.")}


# ══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
#  W1161 (P5.11 clause 2) - WHEN NO RULE MATCHES, A TIME LIMIT MAY STILL APPLY, AND WHERE TO ASK TODAY IS SAID.
#  Nothing below is fetched on a person's action or on a timer: each place is a name, an address and a line of this
#  platform's own words, and the page that names it is GOV.UK's guide, read once on the date below.
# ══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
NATIONS: Tuple[str, ...] = ("England", "Wales", "Scotland", "Northern Ireland")
#  the claim a person picks when theirs is not among the rules
NOT_LISTED: Dict[str, str] = {"id": "not_listed", "name": "A claim not listed here"}
#  the Owner's ruling of 2026-10-12 (P5.11): "a rule or a place is shown as not recently checked NINETY DAYS after
#  the date it was read"
REVIEW_DAYS = 90
#  the one page every place below is named on, with the address each is given at
GUIDE: Dict[str, str] = {
    "name": "Employment tribunals",
    "publisher": "GOV.UK",
    "page": "https://www.gov.uk/employment-tribunals",
    "read_on": "2026-11-20",
    "read_by": "round W1161, the guide's nine parts read whole through GOV.UK's content API",
}
OWN_SITES_NOT_OPENED = ("None of these places' own sites was opened: on 20 November 2026 each refused an automated "
                        "visit from where this was built, so nothing of them was read, and each is listed as the guide "
                        "names it.")


def _place(name: str, link: str, for_what: str, part: str) -> Dict[str, str]:
    return {"name": name, "link": link, "for_what": for_what, "named_on": f"{GUIDE['page']}/{part}",
            "own_site": "not opened"}


#  "To find the deadline for your claim, check the employment tribunal time limits guidance on the Acas (Advisory,
#  Conciliation and Arbitration Service) website" (the guide, "Check if you can make a claim")
_ACAS_TIME_LIMITS = _place("Acas", "https://www.acas.org.uk/employment-tribunal-time-limits",
                           "its guidance on employment tribunal time limits, which GOV.UK's guide names for finding "
                           "the deadline for a claim", "check-you-can-claim")
#  "There's a different way to make a claim to an employment tribunal in Northern Ireland" (the same part)
_NORTHERN_IRELAND_CLAIM = _place("Making a claim to an employment tribunal in Northern Ireland",
                                 "https://www.employmenttribunalsni.co.uk/how-make-claim",
                                 "how a claim is made there, which GOV.UK's guide says is a different way",
                                 "check-you-can-claim")
#  "If you're in England or Wales / If you're in Scotland - You could get legal advice from" ("Get support and legal
#  advice"); the guide names no place for legal advice in Northern Ireland
_ADVICE_ENGLAND_WALES = (
    _place("The Law Society", "https://solicitors.lawsociety.org.uk/", "finding a solicitor",
           "get-support-legal-advice"),
    _place("Citizens Advice",
           "https://www.citizensadvice.org.uk/law-and-courts/legal-system/finding-free-or-affordable-legal-help/",
           "finding free or affordable legal advice", "get-support-legal-advice"),
    _place("Law Centres Network", "https://www.lawcentres.org.uk/", "finding a local Law Centre",
           "get-support-legal-advice"),
    _place("Law Works", "https://www.lawworks.org.uk/", "being put in touch with a volunteer lawyer",
           "get-support-legal-advice"),
)
_ADVICE_SCOTLAND = (
    _place("The Law Society of Scotland", "https://www.lawscot.org.uk/", "finding a solicitor",
           "get-support-legal-advice"),
    _place("Citizens Advice Scotland", "https://www.cas.org.uk/", "finding free or affordable legal advice",
           "get-support-legal-advice"),
)
#  where to ask today, nation by nation: a question from a nation no rule here is for is given a route, not a rule
WHERE_TO_ASK: Dict[str, Tuple[Dict[str, str], ...]] = {
    "England": (_ACAS_TIME_LIMITS,) + _ADVICE_ENGLAND_WALES,
    "Wales": (_ACAS_TIME_LIMITS,) + _ADVICE_ENGLAND_WALES,
    "Scotland": (_ACAS_TIME_LIMITS,) + _ADVICE_SCOTLAND,
    "Northern Ireland": (_NORTHERN_IRELAND_CLAIM,),
}


def _today() -> _dt.date:
    return _dt.date.today()


def nation_named(asked: Any) -> Optional[str]:
    """The nation `asked` names, in any case and spacing, or None when it names none of the four."""
    s = _flat(asked)
    return next((n for n in NATIONS if n.lower() == s), None)


def _listing(items: List[str]) -> str:
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def checked(read_on: str) -> Dict[str, Any]:
    """Whether a page read on `read_on` was read recently: within REVIEW_DAYS of today it is said as read on that day,
    and after that as NOT RECENTLY CHECKED, with the day it was read."""
    age = (_today() - _dt.date.fromisoformat(read_on)).days
    if age <= REVIEW_DAYS:
        return {"recently_checked": True, "checked": f"read on {_said(read_on)}"}
    return {"recently_checked": False,
            "checked": f"NOT RECENTLY CHECKED - read on {_said(read_on)}, more than {REVIEW_DAYS} days ago"}


def no_rule(nation: Optional[str], rule_id: Optional[str] = None) -> Dict[str, Any]:
    """The answer when no rule here matches: the claim has no rule here, or its rule is not for the nation asked about.
    It never says there is no time limit: it says one may still apply, and where to ask today, for the nation asked
    about or, when none was given, for each nation. Nothing is fetched and nothing is worked out."""
    rule = RULES.get(rule_id or "")
    for_nation = [{"id": k, "name": r["name"]} for k, r in RULES.items() if nation in r["nations"]] if nation else []
    if rule is None:
        why = "No rule here is for that claim"
    else:
        why = f"The rule here for {rule['name']} is for {_listing(list(rule['nations']))}, not for {nation}"
    if nation and not for_nation:
        why += f", and no rule here is for a claim in {nation}"
    return {"rule": rule_id if rule else None, "matched": False, "nation": nation, "computed": False, "last_day": None,
            "rules_for_this_nation": for_nation,
            "basis": f"{why}, so no date is worked out. A time limit may still apply: ask today.",
            "where_to_ask": {n: [dict(p) for p in WHERE_TO_ASK[n]] for n in ([nation] if nation else NATIONS)},
            "named_on": {**{k: GUIDE[k] for k in ("name", "publisher", "page", "read_on")}, **checked(GUIDE["read_on"]),
                         "own_sites": OWN_SITES_NOT_OPENED},
            "composed": False, "not_advice": "Nothing here is legal advice."}
