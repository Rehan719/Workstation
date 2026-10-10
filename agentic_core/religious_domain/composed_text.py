"""The faith-content rules for text a GENERAL route composes - one place, so every door applies the same two.

W659 (ledger v15: the swarm accepted a request for a ruling; a deliverable accepted a brief asking for Qur'an
Arabic and a fatwa). OWNER RULING 2026-10-10: a general document is NOT refused because its subject matches the
religious-subject list - "an Islamic finance prospectus" and "a madrasah's business plan" are enterprise documents.
What a general route does instead is exactly two things:

  1. REFUSE A REQUEST FOR A RULING. A religious ruling or a theological proof is something no AI on this platform
     gives (the Horizon guardrails; ruling A.9.5). The same two gaas.v5 gates the cognitive engines use, over the
     PERSON'S OWN TEXT, before anything is asked of a model.

  2. WITHHOLD ARABIC SCRIPT FROM COMPOSED TEXT. Section 11 rule 1: Qur'anic Arabic is NEVER AI-generated; it comes
     only from a sourced edition. A general route has no sourced edition in hand, so Arabic script in text a model
     or the floor composed there is withheld, and the answer says how many passages and why. A person's own typed
     text is never passed through this.

WHAT NEITHER DOES: clear. The gates are phrase screens and the withholding is a script test. A request that is not
refused was not found sound, and composed text with no Arabic script was not found free of error. Both say so.

The four TEACHING routes (curriculum, lesson plan, assessment, marking feedback) are different and stricter: they
refuse a religious subject outright (religious_domain/subject_screen.refuse_if_religious_teaching), because what
they compose is learner-facing teaching content, which needs a named scholar's approval first (A.12.3).
"""
from __future__ import annotations

import re
from typing import Any, Dict, Tuple

#  Arabic, Arabic Supplement, Arabic Extended-A, and the two Arabic Presentation Forms blocks - the same ranges
#  qep_intelligence uses to recognise a sacred source. One definition now.
ARABIC_SCRIPT_RE = re.compile(r"[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]")
_ARABIC_RUN_RE = re.compile(
    r"[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]"
    r"[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿\s‌‍،؛؟]*")

#  Words that put a "may I / is it allowed / give a ruling" sentence in a FAITH context. Whole words only. Kept
#  short on purpose: a term here turns an ordinary question into a refused one, so each must be a word whose
#  presence beside a ruling request leaves little doubt what kind of ruling is meant.
FAITH_CONTEXT_TERMS = (
    "islam", "islamic", "islamically", "muslim", "muslims", "sharia", "shariah", "fiqh", "fatwa", "halal", "haram",
    "haraam", "quran", "qur'an", "koran", "sunnah", "hadith", "prayer", "prayers", "salah", "salat", "wudu",
    "fasting", "ramadan", "zakat", "hajj", "umrah", "nikah", "riba", "sin", "sinful", "religious", "religiously",
    "theological", "theology", "god", "allah", "scripture",
)

WITHHELD_MARK ="[Arabic text withheld: on this route it could only be AI-composed, and Arabic and Qur'anic text come only from a sourced edition]"

COVERAGE = ("a phrase screen over what was asked and a script test over what was composed. Either can withhold or "
            "refuse; neither clears: a request that was not refused was not found sound, and text with no Arabic "
            "script was not checked for anything else")


def refuse_faith_ruling(text: Any, what: str) -> None:
    """Raise 409 when the person's text asks for a religious ruling or a theological proof. Returns None
    otherwise - which is NOT a clearance. Raised as an HTTPException so a route places it where it can be
    received: as its first statement, never inside an except-pass and never after a stream has started."""
    from fastapi import HTTPException
    from agentic_core.gaas.v5 import horizon_guardrails as _hg
    hits = [g for g in (_hg.religious_ruling_gate(text), _hg.theological_proof_gate(text)) if g.get("escalate")]
    if not hits:
        return
    #  ON A GENERAL ROUTE THE GATE ALONE IS TOO WIDE. Its patterns were written for the Horizon membrane, where
    #  every request is a person's own question: "is ... allowed", "ruling on", "verdict about". On a general
    #  route those are ordinary enterprise sentences - "is remote work allowed under the policy", "summarise the
    #  tribunal's ruling on unfair dismissal" - and refusing them as requests for a RELIGIOUS ruling would be a
    #  false statement about what the person asked. So here the gate must fire AND the text must carry a faith
    #  term. Read from the patterns 2026-10-10, before any false refusal shipped; the guard drives both.
    low = " " + re.sub(r"[^a-z0-9']+", " ", str(text or "").lower()) + " "
    faith = sorted(t for t in FAITH_CONTEXT_TERMS if f" {t} " in low)
    if not faith:
        return
    raise HTTPException(status_code=409, detail={
        "message": (f"Not done: this {what} asks for a religious ruling or a theological proof, which no AI on "
                    f"this platform gives. A qualified scholar is the route for that question."),
        "refused_by": [g.get("gate") for g in hits],
        "coverage": COVERAGE,
    })


def withheld_record(passages: int) -> Dict[str, Any]:
    """The record of a withholding, the same shape whether the text was whole or streamed."""
    n = int(passages or 0)
    if not n:
        return {"arabic_passages_withheld": 0, "basis": None, "coverage": COVERAGE}
    return {
        "arabic_passages_withheld": n,
        "basis": (f"{n} passage(s) of Arabic script were in the composed text and are withheld: on this "
                  f"route they could only have been AI-composed, and Arabic and Qur'anic text come only from a "
                  f"sourced edition (the faith-content constitution, rule 1). Nothing else was changed."),
        "coverage": COVERAGE,
    }


def withhold_arabic(composed: Any) -> Tuple[str, Dict[str, Any]]:
    """(text with every run of Arabic script replaced by WITHHELD_MARK, a record of what was done).

    For text a model or the floor COMPOSED on a general route. Never call it on what a person typed, and never on
    text fetched from a sourced edition - those are not composed. The record is the same shape every time."""
    text = str(composed or "")
    runs = _ARABIC_RUN_RE.findall(text)
    if not runs:
        return text, withheld_record(0)
    return _ARABIC_RUN_RE.sub(WITHHELD_MARK + " ", text), withheld_record(len(runs))


class ArabicStreamFilter:
    """withhold_arabic for text that arrives a token at a time. A run of Arabic script can be split across
    tokens, so the state is kept between them: the mark is written once where a run starts and everything up
    to the run's end is dropped. Feeding the tokens of a text gives exactly withhold_arabic of the whole text -
    the guard splits a run mid-word and compares the two."""

    def __init__(self) -> None:
        self.in_run = False
        self.passages = 0

    def feed(self, token: Any) -> str:
        out = []
        for ch in str(token or ""):
            if ARABIC_SCRIPT_RE.match(ch):
                if not self.in_run:
                    self.in_run = True
                    self.passages += 1
                    out.append(WITHHELD_MARK + " ")
            elif self.in_run and (ch.isspace() or ch in "‌‍"):
                continue                      # inside the run, as the whole-text pattern treats it
            else:
                self.in_run = False
                out.append(ch)
        return "".join(out)

    def record(self) -> Dict[str, Any]:
        return withheld_record(self.passages)
