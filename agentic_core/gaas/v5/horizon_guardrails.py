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

#  A statement, not counsel. It says what the platform is, which is the one thing it can say truthfully.
NOT_A_PERSON = (
    "I am not a person. I am software, I cannot judge how you are, and I must not give you counsel about "
    "this. Please reach a human being who can.")

#  Each screen's coverage, stated so a reader can see the shape of what it misses: these are English
#  phrase patterns, so another language, an indirect phrasing or an unusual spelling passes them.
_COVERAGE = ("English phrase patterns only. Another language, an indirect phrasing, a misspelling or a "
             "paraphrase is NOT matched by this screen, and a non-match is therefore not a finding that "
             "the subject is absent")

#  A ruling is being SOUGHT — the shape of the question, not a judgement about the asker.
_RULING_PATTERNS = (
    r"\bis\s+(?:it|this|that)\s+(?:halal|haram|haraam|permissible|forbidden|sinful)\b",
    r"\b(?:fatwa|fatwā)\b",
    r"\bwhat\s+does\s+(?:islam|the\s+(?:qur\s?'?an|quran|shariah|sharia))\s+say\s+(?:i|we)\s+should\b",
    r"\b(?:am|are)\s+i\s+(?:sinning|sinful|a\s+sinner)\b",
    r"\bgive\s+me\s+a\s+ruling\b",
    r"\bis\s+.{0,40}\b(?:halal|haram|haraam)\b",
)

#  A claim that science PROVES a theological truth (in either direction). The defect is the proof claim,
#  not the subject: a theological truth is not the kind of thing a measurement settles.
_PROOF_PATTERNS = (
    r"\bscien(?:ce|tifically)\s+(?:has\s+)?prove[sdn]?\b",
    r"\bprove[sdn]?\s+(?:that\s+)?(?:god|allah|the\s+(?:qur\s?'?an|quran))\b",
    r"\b(?:scientific|empirical)\s+proof\s+(?:of|that)\b",
    r"\b(?:qur\s?'?an|quran)\s+(?:is\s+)?scientifically\s+(?:proven|accurate|verified)\b",
    r"\bdisprove[sdn]?\s+(?:god|allah|religion)\b",
)

#  A distress signal. These patterns are deliberately broad in ONE direction only: a false match costs a
#  withheld answer and a statement that the platform is not a person, which is a safe outcome. A missed
#  match costs the opposite, which is not.
_DISTRESS_PATTERNS = (
    r"\b(?:kill|harm|hurt|cut)\s+(?:my\s?self|myself)\b",
    r"\b(?:end|take)\s+(?:my\s+own\s+)?life\b",
    r"\bsuicid(?:e|al)\b",
    r"\bwant\s+to\s+die\b",
    r"\bno\s+reason\s+to\s+(?:live|go\s+on)\b",
    r"\bcan'?t\s+(?:go\s+on|carry\s+on|keep\s+going)\b",
    r"\bself[\s-]?harm\b",
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
    out["human_routes"] = list(DISTRESS_ROUTES) or None
    out["human_routes_basis"] = DISTRESS_ROUTES_BASIS
    out["action"] = ("WITHHOLD AI counsel, state plainly that the platform is not a person, and show the "
                     "human route — which is NOT SUPPLIED on this platform and must render as unfilled, "
                     "never as a default, a placeholder or a plausible-looking number"
                     if out["escalate"] else
                     "none taken by this gate, which is not the same as the person being well")
    return out


GATES = (religious_ruling_gate, theological_proof_gate, clinical_care_gate)


def screen_all(text: Any) -> Dict[str, Any]:
    """Every gate, with the aggregate escalation and what none of them looked at."""
    results = [g(text) for g in GATES]
    _esc = [r["gate"] for r in results if r["escalate"]]
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
