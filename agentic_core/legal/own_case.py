"""W874 (FU-1082, plan item P5.20, clause 5) - A QUESTION ABOUT A PERSON'S OWN LIVE DISPUTE IS ROUTED TO PEOPLE.

The research form answered "my employer sacked me, can I sue?" like any other question: a frame under IRAC headings,
composed from the person's own words when no model served, a model's draft when one did. The Owner's ruling of
2026-10-13 (P5.20, clause 5): recognise a request for advice on a live dispute, do not answer it as one, route it to
people, and show the published material that bears on it. A request for a religious ruling is already refused at the
gateway for every caller that passes the person's words (faith_ruling_refusal), the law forms included.

THE RECOGNITION IS A SCREEN: it may route, and it NEVER CLEARS. A question it does not recognise is answered only as
information, with the statement every answer carries. Its coverage is stated below, and its phrasings are driven in
the suite, each labelled for or not-for before the result was known (the method of scripts/screen_phrasings.py).
Nothing here composes, and no model is called.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

#  Three conditions, all required: the person speaks of themselves, names a dispute or a legal step, and asks what to
#  do, whether it will succeed, or what they are owed. Each alone is ordinary in a general legal question.
_FIRST_PERSON = re.compile(r"\b(?:i|i'm|im|i've|ive|i'd|me|my|mine|we|we're|we've|our|us)\b")
_DISPUTE = re.compile(r"\b(?:sue|sued|sues|suing|tribunal|court|claim|dismissed|dismissal|sacked|fired|evict|evicted|"
                      r"evicting|eviction|settlement|compensation|charged|arrested|prison|custody|divorce|redundancy|"
                      r"redundant|landlord|employer|boss|neighbour|lawsuit|case|offer|deposit)\b")
_ADVICE = re.compile(r"\b(?:should i|should we|can i|can we|could i|will i|would i|do i|am i|what should|what do i|"
                     r"what can i|what are my|is that|is this|how much|will they|can they|what happens to me)\b")

COVERAGE = ("recognises a question written in the first person that names a dispute or a legal step and asks what to "
            "do, whether it will succeed, or what the person is owed. A question about one's own case written in the "
            "third person, or in another language, is not recognised: it is answered as information, with the "
            "statement every answer carries. Recognising nothing is not a clearance.")

#  Who is listed first when the question is about work: the free conciliation service a work claim passes through
_WORK = re.compile(r"\b(?:employer|boss|dismissed|dismissal|sacked|fired|redundancy|redundant|tribunal|work|job)\b")


def recognises(text: Any) -> bool:
    low = " " + re.sub(r"[^a-z0-9']+", " ", str(text or "").lower()) + " "
    return bool(_FIRST_PERSON.search(low) and _DISPUTE.search(low) and _ADVICE.search(low))


def own_case_route(question: Any, context: Any = "") -> Optional[Dict[str, Any]]:
    """The routing for a question about the person's own dispute, or None. None is NOT a clearance."""
    text = f"{question or ''} {context or ''}"
    if not recognises(text):
        return None
    from agentic_core.api.law import HELP_FROM_A_PERSON
    people: List[Dict[str, str]] = [dict(h) for h in HELP_FROM_A_PERSON]
    if _WORK.search(text.lower()):
        people.sort(key=lambda h: 0 if h["name"] == "Acas" else 1)
    return {
        "message": ("This asks about your own case, so it is not answered here. No AI on this platform can advise on "
                    "a person's own dispute, and an answer shaped like advice would be worse than none. A person can: "
                    "the services listed with this answer give free or regulated help. The law itself can be read "
                    "word for word with 'Read a provision of an Act' on this page; this screen does not choose which "
                    "provision bears on your case. Nothing here is legal advice."),
        "people": people,
        "published_material": [
            {"name": "Read a provision of an Act",
             "how": ("on this page, by the provision's address; the text is fetched from its publisher when you ask "
                     "and shown word for word")}],
        "coverage": COVERAGE,
        "composed": False,
    }
