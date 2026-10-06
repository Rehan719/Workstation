"""P3.10 — WHICH CURRICULUM REQUESTS ARE RELIGIOUS TEACHING, and the one thing this screen may not do.

DESTINATION: agentic_core/religious_domain/subject_screen.py (new file, LF). Prepared in W596's suite wait.

THE PROBLEM IT SOLVES. POST /api/v1/education/curriculum is a GENERAL route: subject, level, framework
(national curriculum, IB, and so on). LearnTeachModule.tsx calls it with subject "Quran & Islamic Studies"
and shows the result to a learner under a caption calling it an AI-assisted study-plan FRAME. So AI-composed
religious teaching content reaches a learner today, carrying a disclaimer — and Owner ruling 2026-10-05b R7
(§A.12.3) says in as many words that A DISCLAIMER IS NOT A REVIEW. Unreviewed religious content is WITHHELD.

Gating the whole education route behind an Islamic scholar would be wrong: a mathematics curriculum needs no
scholar, and a gate that withholds everything teaches nobody anything. So the religious requests must be
distinguished from the rest — which is where this platform's own recorded rule applies.

**A SCREEN MAY REFUSE, NEVER CLEAR.** A word list can notice that a subject is religious teaching. It CANNOT
establish that a subject is secular: the absence of a matched word is the absence of evidence, not evidence
of absence, and a curriculum titled "Comparative Ethics of the Abrahamic Traditions" would pass any list
short enough to maintain. So this screen has exactly one power — to FLAG — and its basis says so out loud.
An unflagged subject is served by the general route because that is the best this platform can do, and the
response says that it was not certified secular rather than implying a clearance nobody performed.

WHAT FLAGGING CAUSES. The general route REFUSES a flagged request and refers it to the gated QEP curriculum
path; it does not quietly compose it and hope. The refusal names the words that matched, so a teacher asking
for a genuinely secular course that tripped the list can see why and say so, rather than meeting a wall.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List

#  Terms whose presence in a subject means the output would be RELIGIOUS TEACHING CONTENT. Deliberately
#  narrow: this list exists to catch the requests that plainly are, not to adjudicate the boundary. Every
#  word here is one whose appearance in a curriculum subject makes scholarly review necessary; a word that
#  merely MIGHT indicate religion is left out, because a false flag refuses a teacher's legitimate request
#  and the honest answer to the boundary cases is that this screen cannot decide them.
RELIGIOUS_SUBJECT_TERMS = (
    "quran", "qur'an", "koran", "islamic studies", "islam", "tajweed", "tajwid", "tafsir", "tafseer",
    "hadith", "hadeeth", "sunnah", "seerah", "sirah", "fiqh", "aqeedah", "aqidah", "shariah", "sharia",
    "usul al-fiqh", "hifz", "hifdh", "memorisation of the quran", "madrasah", "maktab",
)

#  The one thing the screen may not claim.
CANNOT_CLEAR = ("this screen can only FLAG a subject as religious teaching; it CANNOT certify one as "
                "secular. An unflagged subject was NOT reviewed and NOT cleared - the words simply did not "
                "match, which is the absence of evidence and not evidence of absence.")


def _norm(text: str) -> str:
    #  punctuation to spaces so "Qur'an:" and "Quran" screen alike, then collapse runs
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9']+", " ", str(text or "").lower())).strip()


def screen_subject(*parts: Any) -> Dict[str, Any]:
    """Does this curriculum request produce religious teaching content? FLAG or DON'T KNOW — never 'no'.

    Returns a three-key dict, the same keys every time, so no caller has to guess whether a field is
    missing or false:

      flagged  : True when a term matched. There is no False meaning 'secular' - see `basis`.
      matched  : the terms that matched, so a refusal can be disputed by the person it refused.
      basis    : what the result does and does not establish, including CANNOT_CLEAR either way.
    """
    hay = " ".join(_norm(p) for p in parts if p is not None)
    matched: List[str] = sorted({t for t in RELIGIOUS_SUBJECT_TERMS if _norm(t) and _norm(t) in hay})
    if matched:
        return {
            "flagged": True,
            "matched": matched,
            "basis": (
                f"this request names {', '.join(matched)}, so its output would be religious teaching "
                f"content. Owner ruling 2026-10-05b R7 (§A.12.3) requires a named human scholar to approve "
                f"such content BEFORE a learner sees it, and records that a disclaimer is not a review. It "
                f"is therefore not composed here: it belongs to the reviewed QEP curriculum path. "
                f"If this subject is not in fact religious teaching, the matched term is the reason and can "
                f"be disputed - nothing here judges the request's intent. " + CANNOT_CLEAR),
        }
    return {
        "flagged": False,
        "matched": [],
        "basis": ("no term in this platform's religious-subject list appeared in the request, so it is "
                  "served by the general curriculum route. " + CANNOT_CLEAR),
    }
