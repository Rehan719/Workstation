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


def refuse_if_religious_teaching(what: str, subject: Any, *more: Any) -> Dict[str, Any]:
    """W659 (ledger v15) - THE REFUSAL, in one place, for every route that composes TEACHING content.

    The screen had one caller. A lesson plan, an assessment and marking feedback are learner-facing teaching
    content exactly as a curriculum is, and each composed a religious subject without a word about the scholar
    gate. Raises the 409 the curriculum route has always raised; when nothing matched it RETURNS THE SCREEN'S
    OWN RECORD (unflagged, with what it cannot clear), so a route can carry it with what it composed - which is
    NOT a clearance (see CANNOT_CLEAR).

    THE DETAIL IS SHAPED FOR THE READER IT REACHES. apps/.../lib/api.ts turns a non-string `detail` into
    JSON.stringify(detail).slice(0, 300) and the hub renders that, so `message` carries ONE readable sentence
    and comes first, and the whole dict stringifies well inside the 300 characters that survive."""
    from fastapi import HTTPException
    _screen = screen_subject(subject, *more)
    if not _screen["flagged"]:
        return _screen
    raise HTTPException(
        status_code=409,
        detail={
            "message": (
                f"Not composed here: \"{subject}\" is religious teaching content, which needs a "
                f"named scholar's approval before a learner sees it. Use /api/v1/qep/curriculum, "
                f"which submits it for review. Matched: {', '.join(_screen['matched'][:3])}."),
            "where_instead": "/api/v1/qep/curriculum",
            "matched": _screen["matched"],
            "ruling": "2026-10-05b R7 (§A.12.3)",
            "refused": what,
        },
    )


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
#  W1242c (the Owner's ruling of 2026-11-22: religious content stays barred from leaving the platform) - THE SCREEN FOR
#  AN EXTERNAL CALL. It decides one thing only: whether a call may declare a class that lets it leave the platform
#  (agentic_core/ai/data_class.py). A request it flags is still served, by the floor or a local model, and says why it
#  stayed in; it refuses nothing, and the curriculum screen above (screen_subject) is not changed by it.
#  WHERE THE LIST CAME FROM: every term of RELIGIOUS_SUBJECT_TERMS above (the curriculum screen, W596/W659); the faith
#  terms the religious-ruling screen already reads (composed_text.FAITH_CONTEXT_TERMS, W734), among them "god",
#  "prayer", "ramadan", "zakat", "hajj" and "scripture", less the ones named below; the terms the brief for W1242c
#  (2026-11-27) named after the Owner's genesis attempt of 2026-11-22, whose problem asked for work "to seek love and
#  pleasure of Allah SWT" and was missed by the curriculum list, which does not hold the name of God: Allah,
#  Quran/Qur'an, surah, ayah, hadith, sunnah, tafsir, tajwid/tajweed, salah, du'a, fiqh, fatwa; and the usual English
#  transliterations and inflections of each, their one-word spellings ("inshaallah"), and the common devotional phrases
#  that carry the name, written here by this round. With them, added by its review of 2026-11-27: the spelling "Allaah";
#  "subhanahu" and "ta'ala", the phrase the attempt abbreviated as SWT written out (SWT itself is not a term: a software
#  toolkit has the name); "sallallahu" and "rasulullah"; and, because the Owner's ruling keeps religion on the platform
#  and not one faith only, the scriptures of other faiths and a practice ("bible", "biblical", "torah", "talmud",
#  "psalm", "sermon"). They are not taken from a published list, and no scholar has reviewed them. Arabic-script text
#  is flagged whatever it says, because this screen cannot read it. Marks over or under a letter are read as the letter
#  ("Allāh", "Qurʾān", "Ḥadīth"), as transliteration writes them.
#  Left out on purpose: a bare "dua" (a common given name) and "aya" (likewise); "eid" (also an electronic identity,
#  "eID"); "halal", "muslim", "mosque" and "imam", and likewise "church", "temple", "synagogue", "christian", "jewish"
#  and "hindu", which a business can name without sending religious content (the domain the founder chose still keeps
#  the religion domain in); and, of the ruling screen's terms, "sin", "sinful", "fasting", "religious" and
#  "religiously", which ordinary secular text uses in another sense ("sin" in a formula, a fasting diet, a
#  religious-discrimination claim).
#  "salah" stays, though it is also a surname, and so does "god", though it is also an exclamation: a false flag keeps
#  a call on the platform and refuses nothing.
#  Every term matches as a whole word (an "s" or "'s" may follow), so "Allahabad", "Islamabad", "Salahuddin",
#  "Godalming" and "dual" are not matched; the curriculum screen above matches inside words.
from agentic_core.religious_domain.composed_text import FAITH_CONTEXT_TERMS as _FAITH_CONTEXT_TERMS   # W734's list

_FAITH_TERMS_LEFT_OUT = {"muslim", "muslims", "halal", "sin", "sinful", "fasting", "religious", "religiously"}

RELIGIOUS_CONTENT_TERMS = tuple(sorted(set(RELIGIOUS_SUBJECT_TERMS)
                                        | (set(_FAITH_CONTEXT_TERMS) - _FAITH_TERMS_LEFT_OUT) | {
    "allah", "inshallah", "insha'allah", "mashallah", "masha'allah", "subhanallah", "alhamdulillah", "bismillah",
    "pbuh", "inshaallah", "mashaallah", "allahu", "astaghfirullah", "jazakallah",
    "allaah", "subhanahu", "ta'ala", "sallallahu", "rasulullah",
    "bible", "biblical", "torah", "talmud", "psalm", "sermon",
    "quran", "qur'an", "koran", "quranic", "qur'anic", "koranic",
    "surah", "sura", "ayah", "ayat",
    "hadith", "hadeeth", "ahadith",
    "sunnah", "sunna",
    "tafsir", "tafseer",
    "tajwid", "tajweed",
    "salah", "salat", "salaat", "salaah", "namaz",
    "du'a", "duaa", "du'aa",
    "fiqh", "fatwa", "fatawa",
    "islamic",
}))

#  the Arabic script's Unicode blocks: Arabic, Arabic Supplement, Arabic Extended-A, and the two presentation-form blocks
_ARABIC_SCRIPT = re.compile("[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]")


def _words(text: Any) -> str:
    """Lower case, marks over or under a letter dropped (a transliteration's "ā" read as "a"), every apostrophe and
    the transliterations' hamza and ayn signs written as one, every other mark a space, runs collapsed."""
    import unicodedata
    t = str(text or "").lower()
    for q in ("’", "‘", "ʼ", "ʾ", "ʿ", "`", "´"):
        t = t.replace(q, "'")
    t = "".join(c for c in unicodedata.normalize("NFKD", t) if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9']+", " ", t)).strip()


_TERM_RES = tuple((t, re.compile(r"(?<![a-z0-9])" + re.escape(_words(t)) + r"(?:s|'s)?(?![a-z0-9])"))
                  for t in RELIGIOUS_CONTENT_TERMS if _words(t))


def screen_religious_content(*parts: Any) -> Dict[str, Any]:
    """W1242c - may this text leave the platform in an external call? FLAG or DON'T KNOW, never 'no'.

    flagged : True when a term matched as a whole word or the text holds Arabic script.
    matched : the terms that matched; arabic_script: whether Arabic-script text was found.
    names   : what the text was found to hold, as a clause ("names religious content (allah)").
    basis   : what the result does and does not establish. It refuses nothing: a flagged call is served on the
              platform, and says why it was not sent out."""
    raw = " ".join(str(p) for p in parts if p is not None)
    hay = _words(raw)
    matched = sorted({t for t, rx in _TERM_RES if rx.search(hay)})
    arabic = bool(_ARABIC_SCRIPT.search(raw))
    said = []
    if matched:
        said.append(f"names religious content ({', '.join(matched[:4])})")
    if arabic:
        said.append("holds Arabic-script text, which this screen cannot read")
    if said:
        return {"flagged": True, "matched": matched, "arabic_script": arabic, "names": " and ".join(said),
                "basis": ("the text " + " and ".join(said) + ", so no call carrying it is sent outside the platform; "
                          "it is served on the platform instead, and nothing is refused. " + CANNOT_CLEAR)}
    return {"flagged": False, "matched": [], "arabic_script": False, "names": "",
            "basis": ("no term of this screen's list appeared and no Arabic-script text was found. " + CANNOT_CLEAR)}


def class_unless_religious(data_class: Any, *parts: Any) -> Dict[str, Any]:
    """W1242c - THE CLASS A CALL WITH NO DOMAIN OF ITS OWN DECLARES: the native-AI console and the resource fabric
    declare person_entered around what a person typed or saved (W899), and since W1242 a declared call can leave with
    the Owner's switch on and no in-house model reachable, whether or not it asks. `parts` are the texts the call
    sends. data_class is the class given when this screen flags none of them, and None when it flags any or could not
    be run on them: nothing is declared, so no call of it is sent outside the platform (ai/data_class.py). It refuses
    nothing: the call is served on the platform. kept_in says why, in a sentence for the answer, or is None."""
    if data_class is None:
        return {"data_class": None, "kept_in": None}
    try:
        scr = screen_religious_content(*parts)
    except Exception as exc:                       # noqa: BLE001 - a screen that could not run keeps the call in
        return {"data_class": None,
                "kept_in": ("nothing was declared, so no call of this request was sent outside the platform: the "
                            f"religious-content screen could not be run on it ({type(exc).__name__})")}
    if scr["flagged"]:
        return {"data_class": None,
                "kept_in": ("nothing was declared, so no call of this request was sent outside the platform: what it "
                            f"sends {scr['names']}, and religious content is not sent outside the platform. It was "
                            "served on the platform; nothing was refused")}
    return {"data_class": data_class, "kept_in": None}
