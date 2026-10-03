"""Three guardrails, attached to the v5 interceptor, each stating what it did NOT look at (P2.12).

THE RULE THAT SHAPES EVERY GATE HERE: a screen may ESCALATE but may never certify that nothing was
sought. These are word-and-phrase screens. A screen that matches has found something; a screen that does
not match has found nothing WITH ITS OWN PATTERNS, which is a different and much weaker statement than
"no religious ruling was sought" or "this person is not in distress". So there is no CLEAR verdict in
this module. The three verdicts are ESCALATE, NOT_DETECTED (with the coverage stated and
`certifies_absence` false), and CANNOT_DECIDE — and the escalation flag defaults ON for the last, because
a screen that could not run is not a screen that passed.

THE DISTRESS ROUTES ARE NOT SUPPLIED, AND THAT IS VISIBLE RATHER THAN SILENT. The Owner's ruling (FU-270)
is that this item closes on its refusal paths with the unfilled field VISIBLE on the surface, and the
list arrives later with its reviewer. So `DISTRESS_ROUTES` is empty and every response says so in words.

AND THE SHAPE THAT LIST MUST ARRIVE IN IS NOW BUILT, WHICH IS A DIFFERENT THING FROM THE LIST ARRIVING.
The Owner's later ruling is that the mechanism is built now and the data stays the Owner's. (THE RULING'S
DATE IS NOT WRITTEN HERE AND THAT IS NOT AN OVERSIGHT: the leg governing this file forbids any
dash-separated digit run, and an ISO date is one — a reader scanning for something to dial does not
stop to check whether a digit run is a calendar date. It is in the delivery plan, in words, where it
belongs.) So `accept_route` REFUSES a record that does not name WHO reviewed it and WHEN they checked it, and
`distress_routes` keeps three states apart that a single empty list would collapse: NOT SUPPLIED (no
record at all), SUPPLIED_STALE (a record whose check is older than the staleness horizon, listed WITH
that fact rather than silently trusted) and SUPPLIED_FRESH. A route nobody has checked recently is not
the same as no route, and neither is the same as a route — a surface that cannot tell them apart would
present a number last confirmed years ago as though someone had just verified it.

NOTHING IN THIS MODULE SUPPLIES A ROUTE, AND THE MECHANISM DOES NOT MAKE IT EASIER TO INVENT ONE. There
is no example record, no default, no template value and no test fixture here. The validator's subject is
the METADATA, never the route string: it has no opinion about whether a route is dialable, reachable or
real, and it must not be mistaken for one — only a human reviewer can say that, which is precisely why
their name and the date they said it are required fields.
NOTHING IN THIS MODULE MAY CONTAIN A PLAUSIBLE-LOOKING NUMBER. A fabricated helpline is the single most
dangerous thing this repository could produce — a person in distress might dial it — and it is the one
fabrication that cannot be corrected after the fact. A guard asserts that no digit sequence resembling a
telephone number exists anywhere in this file.

WHAT IS UNCHANGED AND UNRELAXED, because this module sits next to it: Quran Arabic is never generated,
Quranic text comes only from the three cited sources with provenance, recitation is never scored, AI
content is labelled, and Ruling A.9.5 stands — the Fitrah Spectrum is never a measurement and no AI
verdict is passed on a person's spiritual state. NOTHING HERE GRADES A PERSON. Each gate screens a
REQUEST or an OUTPUT for a subject the platform must not answer; none of them assesses the human asking.
"""
from __future__ import annotations

import datetime as _dt
import re
from typing import Any, Dict, List, Optional, Tuple

ESCALATE = "ESCALATE"
NOT_DETECTED = "NOT_DETECTED"
CANNOT_DECIDE = "CANNOT_DECIDE"

#  THE LIST THE OWNER SUPPLIES LATER, WITH ITS REVIEWER. Empty is the honest state and the surface says
#  so; a placeholder here would be indistinguishable from a real route to the person who needed one.
DISTRESS_ROUTES: Tuple[Dict[str, str], ...] = ()
DISTRESS_ROUTES_BASIS = (
    "NOT SUPPLIED: no human distress route is recorded on this platform. This is an UNFILLED FIELD shown "
    "as unfilled, not an absence of need — the Owner supplies the list with its reviewer, and until then "
    "the honest answer is that this platform cannot name a route. No number, service name or placeholder "
    "stands in for one, because a person in distress might act on it")

#  WHAT A ROUTE MUST CARRY. Every one required, and the three that are not the route itself are the
#  point: a route with no reviewer is a number somebody typed, a route with no check date cannot go
#  stale so it would be trusted forever, and A ROUTE WITH NO JURISDICTION CAN BE SHOWN TO SOMEONE IT
#  DOES NOT ANSWER FOR — which is worse than NOT SUPPLIED, because it sends a person somewhere
#  instead of telling them the truth. FU-361 required this from the start ("real, current and
#  appropriate to the jurisdiction") and the first cut of this mechanism did not carry it.
ROUTE_FIELDS: Tuple[str, ...] = ("route", "reviewed_by", "checked_on", "jurisdiction")
#  The one value that means "the reviewer attested this is correct wherever the person is". It is
#  ONLY honestly available to a route that names no specific service — see _looks_dialable.
JURISDICTION_ANY = "ANY"
#  The horizon is a POLICY, stated here so a reader can see it rather than inferring it from behaviour.
#  It is deliberately short: a route is a thing in the world and the world changes it without telling us.
ROUTE_STALE_AFTER_DAYS = 180

NOT_SUPPLIED = "NOT_SUPPLIED"
SUPPLIED_STALE = "SUPPLIED_STALE"
SUPPLIED_FRESH = "SUPPLIED_FRESH"

ROUTE_FIELD_WHY = {
    "route": "how a person actually reaches a human being. This module never checks whether it works",
    "reviewed_by": "the person or body who confirmed this route reaches a human. NOT the platform, and "
                   "not an agent: a software verdict on whether a distress route is real is worth "
                   "nothing to the person dialling it",
    "checked_on": "the ISO date (YYYY-MM-DD) they confirmed it. Without this the route cannot go stale, "
                  "and a route that cannot go stale is trusted forever",
    "jurisdiction": "where this route answers \u2014 a named place, or ANY when the reviewer attests it is "
                    "correct wherever the person is. ANY is only honest for a route that names no "
                    "specific service: a dialable number answers in one country and nowhere else",
}


def _looks_dialable(value: str) -> bool:
    """Does this route string contain something a person would read as a number to dial?

    The same shape the suite forbids in this file, applied to DATA rather than to source — because the
    data arrives later and the file-level leg cannot see it. It is deliberately broad: a false positive
    costs the Owner a rephrasing, and a false negative lets a number be marked correct for everywhere.
    """
    return bool(_DIALABLE.search(value or ""))


_DIALABLE = re.compile(r"(?:\+?\d[\d\s().-]{6,}\d)|(?:\b\d{4,}\b)")


def _as_date(value: Any) -> Optional[_dt.date]:
    """An ISO calendar date or None. No coercion, no partial parse, no 'today' fallback."""
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        return _dt.date.fromisoformat(value.strip())
    except ValueError:
        return None


def accept_route(record: Any, today: Optional[_dt.date] = None) -> Dict[str, Any]:
    """REFUSE a route record that cannot say who checked it and when, and say which field was missing.

    It returns a verdict rather than raising, and `accepted` is three-state: False for a record that is
    present and wrong, None for something that is not a record at all. It never returns the record
    repaired, defaulted or partially filled — a half-accepted distress route is the failure mode this
    whole mechanism exists to prevent.
    """
    _today = today or _dt.date.today()
    if not isinstance(record, dict):
        return {"accepted": None, "missing": list(ROUTE_FIELDS), "state": NOT_SUPPLIED,
                "basis": f"not a record: {type(record).__name__} was given where a mapping with "
                         f"{', '.join(ROUTE_FIELDS)} is required. No part of it is read"}
    missing = [f for f in ROUTE_FIELDS
               if not isinstance(record.get(f), str) or not record.get(f, "").strip()]
    if missing:
        return {"accepted": False, "missing": missing, "state": NOT_SUPPLIED,
                "basis": "REFUSED — " + "; ".join(
                    f"{f} is absent or blank: {ROUTE_FIELD_WHY[f]}" for f in missing)}
    checked = _as_date(record["checked_on"])
    if checked is None:
        return {"accepted": False, "missing": ["checked_on"], "state": NOT_SUPPLIED,
                "basis": "REFUSED — checked_on is not an ISO calendar date (YYYY-MM-DD), so the age "
                         "of this check cannot be computed and the route cannot go stale"}
    if checked > _today:
        return {"accepted": False, "missing": ["checked_on"], "state": NOT_SUPPLIED,
                "basis": "REFUSED — checked_on is in the future, so it records no check that has "
                         "happened. A date nobody could have met is worse than a missing one: it reads "
                         "as the most recent confirmation there is"}
    #  THE INVARIANT ONLY THIS FIELD CAN CARRY. A number answers in one country and nowhere else, so a
    #  route holding a dialable digit run may never be marked correct for everywhere. This is the one
    #  check in the module that reads the route STRING, and it reads it to refuse, never to approve:
    #  passing it says nothing about whether the route works.
    if (record["jurisdiction"].strip().upper() == JURISDICTION_ANY
            and _looks_dialable(record["route"])):
        return {"accepted": False, "missing": ["jurisdiction"], "state": NOT_SUPPLIED,
                "basis": "REFUSED \u2014 this route contains something a person would read as a number to "
                         "dial and is marked correct for ANY jurisdiction. A number answers in one "
                         "place and nowhere else, so name the place it answers in. ANY is for a route "
                         "that names no specific service"}
    age = (_today - checked).days
    stale = age > ROUTE_STALE_AFTER_DAYS
    return {
        "accepted": True,
        "jurisdiction": record["jurisdiction"].strip(),
        "missing": [],
        "state": SUPPLIED_STALE if stale else SUPPLIED_FRESH,
        "age_days": age,
        "stale": stale,
        "basis": (f"accepted, AND STALE: reviewed by {record['reviewed_by'].strip()} and last checked "
                  f"{age} day(s) ago, which is past the {ROUTE_STALE_AFTER_DAYS}-day horizon. It is "
                  f"shown WITH that fact, never as a current route — a route last confirmed long ago "
                  f"may have changed, and the person acting on it cannot tell"
                  if stale else
                  f"accepted: reviewed by {record['reviewed_by'].strip()} and last checked {age} day(s) "
                  f"ago, within the {ROUTE_STALE_AFTER_DAYS}-day horizon"),
    }


def distress_routes(today: Optional[_dt.date] = None,
                    records: Optional[Tuple[Dict[str, str], ...]] = None) -> Dict[str, Any]:
    """The reader a surface uses. THREE STATES, which a bare list would collapse into one.

    `records` exists so a caller — including a guard — can drive this function without a route being
    written into this module. Its default is `DISTRESS_ROUTES`, which is empty and stays empty: the
    Owner supplies the list, and nothing on this path may invent one.
    """
    #  MATERIALISED ONCE, because this function iterates _src TWICE — once to judge and once to zip the
    #  verdicts back. Handed a one-shot iterable, the second pass saw an exhausted iterator, every
    #  accepted route was silently dropped, and the function returned NOT_SUPPLIED with the bare basis
    #  "no human distress route is recorded on this platform" about a call that had just been given a
    #  valid, reviewed, in-horizon route — a basis asserting what it did not compute. No live caller
    #  passes a generator today; that is why it is a one-line hardening and not a break.
    _src = tuple(DISTRESS_ROUTES if records is None else records)
    verdicts = [accept_route(r, today) for r in _src]
    kept = [(r, v) for r, v in zip(_src, verdicts) if v["accepted"] is True]
    refused = [v for v in verdicts if v["accepted"] is not True]
    if not kept:
        return {
            "state": NOT_SUPPLIED,
            #  None rather than [], so a surface cannot render an empty list as "nothing needed".
            "routes": None,
            "basis": DISTRESS_ROUTES_BASIS + (
                f". {len(refused)} supplied record(s) were REFUSED for want of a reviewer or a check "
                f"date, which is why none is shown" if refused else ""),
            "refused": [v["basis"] for v in refused],
            "stale_count": 0,
            #  PRESENT AND EMPTY, never absent. A caller that has to test whether the key exists will
            #  eventually forget to, and then an unfilled field reads as full coverage.
            "jurisdictions": [],
            "covers_anywhere": False,
        }
    _stale = [v for _, v in kept if v["stale"]]
    return {
        "state": SUPPLIED_STALE if _stale else SUPPLIED_FRESH,
        #  Each route travels WITH its reviewer, its date and its freshness. A surface that wants only
        #  the route string has to drop them deliberately rather than never having been given them.
        "routes": [{"route": r["route"], "reviewed_by": r["reviewed_by"],
                    "checked_on": r["checked_on"], "jurisdiction": v["jurisdiction"],
                    "stale": v["stale"], "age_days": v["age_days"]}
                   for r, v in kept],
        #  WHAT IS AND IS NOT COVERED, stated rather than left for a surface to work out. A person
        #  outside every named jurisdiction is told that, not shown the nearest route.
        "jurisdictions": sorted({v["jurisdiction"] for _, v in kept}),
        "covers_anywhere": any(v["jurisdiction"].upper() == JURISDICTION_ANY for _, v in kept),
        "basis": (f"{len(kept)} route(s) supplied, {len(_stale)} of them STALE (last checked more than "
                  f"{ROUTE_STALE_AFTER_DAYS} days ago and shown as such, never as current)"
                  if _stale else
                  f"{len(kept)} route(s) supplied, each with a named reviewer and a check date inside "
                  f"the {ROUTE_STALE_AFTER_DAYS}-day horizon"),
        "refused": [v["basis"] for v in refused],
        "stale_count": len(_stale),
    }


#  A statement, not counsel. It says what the platform is, which is the one thing it can say truthfully.
NOT_A_PERSON = (
    "I am not a person. I am software, I cannot judge how you are, and I must not give you counsel about "
    "this. Please reach a human being who can.")

#  Each screen's coverage, stated so a reader can see the shape of what it misses: these are English
#  phrase patterns, so another language, an indirect phrasing or an unusual spelling passes them.
_COVERAGE = ("English phrase patterns only. Another language, an indirect phrasing, a misspelling or a "
             "paraphrase is NOT matched by this screen, and a non-match is therefore not a finding that "
             "the subject is absent. The patterns cover the common INFLECTIONS of each verb they name "
             "(enumerated, not derived) because two faults in this screen were both in a slot nobody "
             "had driven — but an inflection nobody enumerated is still a miss, and this sentence is "
             "not a claim that the enumeration is complete")

#  A ruling is being SOUGHT — the shape of the question, not a judgement about the asker.
_RULING_PATTERNS = (
    r"\bis\s+(?:it|this|that)\s+(?:halal|haram|haraam|permissible|forbidden|sinful)\b",
    r"\b(?:fatwa|fatwā)\b",
    r"\bwhat\s+does\s+(?:islam|the\s+(?:qur\s?'?an|quran|shariah|sharia))\s+say\s+(?:i|we)\s+should\b",
    r"\b(?:am|are|was|were)\s+i\s+(?:sinning|sinful|a\s+sinner|committing\s+a\s+sin)\b",
    r"\bgive\s+me\s+a\s+(?:ruling|fatwa|verdict)\b",
    r"\bis\s+.{0,40}\b(?:halal|haram|haraam)\b",
)

#  A claim that science PROVES a theological truth (in either direction). The defect is the proof claim,
#  not the subject: a theological truth is not the kind of thing a measurement settles.
_PROOF_PATTERNS = (
    r"\bscien(?:ce|tifically|tists?)\s+(?:ha(?:s|ve)\s+)?(?:prove[sdn]?|proving)\b",
    r"\bprove[sdn]?\s+(?:that\s+)?(?:god|allah|the\s+(?:qur\s?'?an|quran))\b",
    r"\b(?:scientific|empirical)\s+proof\s+(?:of|that)\b",
    r"\b(?:qur\s?'?an|quran)\s+(?:is\s+)?scientifically\s+(?:proven|accurate|verified)\b",
    r"\bdisprove[sdn]?\s+(?:god|allah|religion)\b",
)

#  A distress signal. These patterns are deliberately broad in ONE direction only: a false match costs a
#  withheld answer and a statement that the platform is not a person, which is a safe outcome. A missed
#  match costs the opposite, which is not.
#  THIS SCREEN WAS WRONG TWICE AND BOTH FAULTS WERE IN A SLOT NOBODY HAD DRIVEN.
#  First the DETERMINER: `(?:my\s+own\s+)?` made "my" and "own" one optional unit, so it matched "end
#  life" and "end my own life" and NOT "end my life" — the plainest phrasing of the subject — while
#  escalating correctly for "kill myself". Fixed in W564.
#  Then the VERB, found by a refuter driving that very fix: every verb was a bare literal followed by
#  \s+, so the character after the lemma had to be whitespace, and in "killing" it is "i". So "ending my
#  life", "killing myself", "cutting myself", "harming myself", "taking my own life" and "ending it all"
#  all passed — AND THE PROGRESSIVE IS THE COMMONEST FORM A PERSON WRITES. None of them is an
#  indirect phrasing, a misspelling, a paraphrase or another language, so the declared coverage below
#  did not cover them: they were defects, not stated limits.
#  THE INFLECTIONS ARE SPELLED OUT, NOT DERIVED. A clever `(?:s|ed|ing)?` is the thing that failed
#  twice: it yields "cuted", misses "cutting", and no reviewer would catch either. Enumerated, every
#  form is visible, and the guard drives all of them in both directions.
#  THE FAILURE DIRECTION IS DELIBERATE. These patterns are broad and will escalate some benign text
#  ("take my life in a new direction"). An escalation withholds AI counsel and points to a human, which
#  is a poor answer; A MISS GIVES AI COUNSEL TO SOMEONE IN CRISIS, which is not an answer at all. Where
#  the two trade off, this screen chooses the false positive, and that choice is stated rather than
#  discovered.
_DISTRESS_PATTERNS = (
    r"\b(?:kill(?:s|ed|ing)?|harm(?:s|ed|ing)?|hurt(?:s|ing)?|cut(?:s|ting)?)"
    r"\s+(?:my\s?self|myself)\b",
    r"\b(?:end(?:s|ed|ing)?|take(?:s|n)?|taking|took)"
    r"\s+(?:(?:my|his|her|their|ones?|his\s+or\s+her)\s+(?:own\s+)?)?life\b",
    r"\bend(?:s|ed|ing)?\s+it\s+all\b",
    r"\bsuicid(?:e|es|al|ality)\b",
    r"\b(?:want(?:s|ed|ing)?|wish(?:es|ed|ing)?)\s+to\s+die\b",
    r"\bwish\s+(?:i|he|she|they)\s+(?:was|were|had\s+never\s+been)\b[^.]{0,12}\b(?:dead|born)\b",
    r"\bno\s+reason\s+to\s+(?:live|go\s+on|carry\s+on|keep\s+going)\b",
    r"\b(?:can'?t|cannot|could\s?n'?t)\s+(?:go\s+on|carry\s+on|keep\s+going|take\s+(?:it|this)"
    r"\s+(?:any\s?more|longer))\b",
    r"\bself[\s-]?harm(?:s|ed|ing)?\b",
)


def _screen(text: Any, patterns: Tuple[str, ...]) -> Tuple[Optional[bool], List[str], str]:
    """Run a phrase screen. Returns (matched, which, why) — `matched` None when it could not run."""
    if not isinstance(text, str):
        return None, [], (f"CANNOT DECIDE: the subject is {type(text).__name__}, not text, so no screen "
                          f"ran over it")
    if not text.strip():
        return None, [], "CANNOT DECIDE: the subject is empty, so no screen ran over it"
    hits = [p for p in patterns if re.search(p, text, re.I)]
    return bool(hits), hits, (f"{len(hits)} pattern(s) matched" if hits else "no pattern matched")


def _verdict(matched: Optional[bool], hits: List[str], why: str, subject: str,
             on_match: str) -> Dict[str, Any]:
    """The common shape. There is no CLEAR: a non-match is NOT_DETECTED and certifies nothing."""
    if matched is None:
        #  FAIL CLOSED. A screen that could not run is not a screen that passed.
        return {"verdict": CANNOT_DECIDE, "escalate": True, "matched": None, "patterns_matched": [],
                "certifies_absence": False, "coverage": _COVERAGE,
                "not_looked_at": f"everything — no screen ran. {why}",
                "basis": (f"CANNOT DECIDE whether {subject} is present, so the escalation defaults ON. "
                          f"{why}")}
    if matched:
        return {"verdict": ESCALATE, "escalate": True, "matched": True,
                "patterns_matched": hits, "certifies_absence": False, "coverage": _COVERAGE,
                "not_looked_at": ("whether anything ELSE in this text needs escalating — this screen "
                                  "stops at its own patterns"),
                "basis": f"{subject} detected: {why}. {on_match}"}
    return {"verdict": NOT_DETECTED, "escalate": False, "matched": False, "patterns_matched": [],
            #  THE SENTENCE THIS WHOLE MODULE EXISTS FOR.
            "certifies_absence": False, "coverage": _COVERAGE,
            "not_looked_at": (f"whether {subject} is present in any form these patterns do not cover. "
                              f"THIS IS NOT A FINDING THAT IT IS ABSENT"),
            "basis": (f"NOT DETECTED by this screen: {why}. A non-match means these patterns found "
                      f"nothing, NOT that {subject} was not sought — the screen cannot certify an "
                      f"absence and does not claim to")}


def religious_ruling_gate(text: Any) -> Dict[str, Any]:
    """A religious ruling is referred to a qualified human scholar. The platform issues none."""
    m, hits, why = _screen(text, _RULING_PATTERNS)
    out = _verdict(m, hits, why, "a request for a religious ruling",
                   "The platform issues no ruling.")
    out["gate"] = "religious_ruling"
    out["action"] = ("WITHHOLD any ruling and refer to a QUALIFIED HUMAN SCHOLAR. The platform does not "
                     "issue religious rulings, and an answer that reads like one would be a ruling "
                     "whatever it was labelled"
                     if out["escalate"] else
                     "none taken by this gate, which is not the same as the request being cleared")
    out["human_referral"] = None
    out["human_referral_basis"] = (
        "NOT SUPPLIED: no named scholar or scholarly body is recorded on this platform, so none is "
        "offered. The referral is to a qualified human scholar the person chooses or is already "
        "connected to — naming one here would be a recommendation nobody reviewed")
    return out


def theological_proof_gate(text: Any) -> Dict[str, Any]:
    """No scientific-proof claim over a theological truth, in either direction."""
    m, hits, why = _screen(text, _PROOF_PATTERNS)
    out = _verdict(m, hits, why, "a claim that science proves or disproves a theological truth",
                   "The platform makes no such claim.")
    out["gate"] = "theological_proof"
    out["action"] = ("WITHHOLD the proof claim. A theological truth is not the kind of statement a "
                     "measurement settles, and asserting that it is — in either direction — misrepresents "
                     "both the science and the theology"
                     if out["escalate"] else
                     "none taken by this gate, which is not the same as the text being cleared")
    return out


def clinical_care_gate(text: Any) -> Dict[str, Any]:
    """A distress signal withholds AI counsel, says plainly the platform is not a person, and names a
    real human route — or says, visibly, that no route is recorded.

    THE ROUTE IS THE DANGEROUS FIELD. An unfilled list shown as unfilled is safe; a placeholder is not.
    """
    m, hits, why = _screen(text, _DISTRESS_PATTERNS)
    out = _verdict(m, hits, why, "a distress signal", "AI counsel is withheld.")
    out["gate"] = "clinical_care"
    out["withhold_ai_counsel"] = bool(out["escalate"])
    out["statement"] = NOT_A_PERSON if out["escalate"] else None
    #  None, not (), and not a placeholder row. The key is present so a surface must render SOMETHING,
    #  and what it renders is the basis.
    _routes = distress_routes()
    out["human_routes"] = _routes["routes"]
    out["human_routes_basis"] = _routes["basis"]
    #  THE STATE TRAVELS WITH THE FIELD. A surface holding only a list cannot tell a route nobody has
    #  checked in years from one confirmed last week, so it would present them identically.
    out["human_routes_state"] = _routes["state"]
    out["human_routes_stale_count"] = _routes["stale_count"]
    out["human_routes_jurisdictions"] = _routes["jurisdictions"]
    out["human_routes_cover_anywhere"] = _routes["covers_anywhere"]
    out["action"] = ("WITHHOLD AI counsel, state plainly that the platform is not a person, and show the "
                     "human route — which is NOT SUPPLIED on this platform and must render as unfilled, "
                     "never as a default, a placeholder or a plausible-looking number"
                     if out["escalate"] else
                     "none taken by this gate, which is not the same as the person being well")
    return out


GATES = (religious_ruling_gate, theological_proof_gate, clinical_care_gate)


def _record_refused_gate(escalated_by: List[str], results: List[Dict[str, Any]]) -> None:
    """W556 (P2.14) — a REFUSED GATE is one of the three triggers that writes a LessonRecord.

    OBSERVATION ONLY, and that is a design decision rather than a limitation. The lesson is written with
    disposition APPLIED_AND_LOGGED, so NO CHANGE IS FILED: a gate that refuses many times in a row would
    otherwise file many changes, and an exception storm must not become a governance storm. Filing is a
    deliberate act someone takes afterwards, through POST /api/v1/horizon/lessons, which is the same
    separation the module keeps everywhere — an observation is not a finding and a finding is not an
    approved change.

    It never raises into the screen. A gate that failed because its observer failed would be the worst
    possible trade.
    """
    try:
        from agentic_core.horizon import muhasabah
        rec = muhasabah.observe(
            "refused_gate",
            {"escalated_by": list(escalated_by),
             "gates": {r["gate"]: r.get("verdict") for r in results}},
            subject=None)
        muhasabah.save(rec, muhasabah.route(rec, "APPLIED_AND_LOGGED"), None)
    except Exception:                            # noqa: BLE001 — an observer never breaks the gate
        pass


def screen_all(text: Any) -> Dict[str, Any]:
    """Every gate, with the aggregate escalation and what none of them looked at."""
    results = [g(text) for g in GATES]
    _esc = [r["gate"] for r in results if r["escalate"]]
    if _esc:
        _record_refused_gate(_esc, results)
    return {
        "gates": {r["gate"]: r for r in results},
        "escalate": bool(_esc),
        "escalated_by": _esc,
        #  NO GATE CERTIFIES AN ABSENCE, so neither does the aggregate.
        "certifies_absence": False,
        "basis": (
            f"{len(_esc)} of {len(results)} gate(s) escalated: {', '.join(_esc)}"
            if _esc else
            f"none of {len(results)} gate(s) matched. THIS IS NOT A CLEARANCE — each gate screens "
            f"English phrase patterns and none can certify that its subject was absent. The aggregate "
            f"inherits that limit rather than resolving it"),
        "fitrah_note": (
            "nothing in this module assesses the person asking. Each gate screens a REQUEST or an OUTPUT "
            "for a subject the platform must not answer; Ruling A.9.5 stands — the Fitrah Spectrum is "
            "never a measurement and no AI verdict is passed on anyone's spiritual state"),
    }
