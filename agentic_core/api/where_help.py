"""THE ONE PAGE OF WHERE HELP IS (plan item P5.20, clause 6; W953).

The Owner's ruling of 2026-10-13 (P5.20, clause 6): one page says how to find a qualified scholar, where regulated
and free legal help is, and how to complain to the Owner about an answer; the pages of an advice charity are linked
and never copied. Measured before this round: the page (W724) said where legal help is and how to complain, and
nothing of a scholar; and it lived only on the Law route, so a person anywhere else on the platform met none of it.

This module is that page's one source. GET /api/v1/support/where-help-is serves it to the support page, and the Law
route's help (GET /api/v1/law/help) is built from it, so the two cannot say different things. Nothing here composes,
no model is called, the route reads nothing a person sends and records nothing, and no scholar or religious body is
named: the platform cannot check anyone's standing as a scholar.
"""
from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/support", tags=["where-help-is"])

#  where the page is, for a page elsewhere that points to it
THE_PAGE = "/support#where-help-is"

#  How to find a qualified scholar, in this platform's own words. No scholar, mosque or body is named: which scholar to
#  ask is a person's own choice, and nothing here can check a scholar's standing.
A_QUALIFIED_SCHOLAR: Dict[str, Any] = {
    "heading": "How to find a qualified scholar",
    "steps": (
        "Ask in person. At a mosque or a place of learning you trust, ask who answers questions like yours, and take "
        "your question to that scholar with the details of your own situation.",
        "A ruling on your own situation comes from a scholar who has heard it. No answer on this platform is one.",
        "If it matters to you, ask the scholar what they studied and with whom.",
    ),
    "names_none_because": ("This platform names no scholar and no body: it cannot check anyone's standing as a "
                           "scholar, and which scholar to ask is for you and your community to choose."),
    "this_platform": ("This platform is not a scholar and gives no religious ruling. What its AI composes on religion "
                      "is withheld until a named scholar approves that exact text, and no scholar answers questions "
                      "from the public here."),
}

#  Each entry is a NAME, an ADDRESS and one line of OUR OWN saying who it is for. No sentence of any linked
#  site is copied. Every address was opened once on 2026-10-13 and resolved; two bodies whose pages refused
#  an automated visit are not listed until a person has opened them. (Moved here from agentic_core/api/law.py in
#  W953, unchanged; law.py and the own-case screen read it from here.)
HELP_FROM_A_PERSON = (
    {"name": "Find legal advice (GOV.UK)", "link": "https://www.gov.uk/find-legal-advice",
     "for_what": "finding a solicitor, a legal adviser or free advice in England and Wales"},
    {"name": "Check if you can get legal aid (GOV.UK)", "link": "https://www.gov.uk/legal-aid/check-legal-aid",
     "for_what": "seeing whether the cost of advice or representation may be met"},
    {"name": "Citizens Advice", "link": "https://www.citizensadvice.org.uk/",
     "for_what": "free, independent advice on work, money, housing and consumer problems"},
    {"name": "Acas", "link": "https://www.acas.org.uk/",
     "for_what": "free advice on rights at work, and conciliation before a tribunal claim"},
    {"name": "Law Centres Network", "link": "https://www.lawcentres.org.uk/",
     "for_what": "free legal help from a local law centre, where one serves the area"},
    {"name": "Advicenow", "link": "https://www.advicenow.org.uk/",
     "for_what": "plain guides for a person handling a legal problem themselves"},
    {"name": "Advocate", "link": "https://weareadvocate.org.uk/",
     "for_what": "free help from a volunteer barrister, for those who cannot pay and cannot get legal aid"},
    {"name": "LawWorks", "link": "https://www.lawworks.org.uk/legal-advice-individuals",
     "for_what": "free legal advice clinics run by volunteer solicitors"},
)

THIS_PLATFORM_IS_NOT = (
    "a solicitor, a barrister or any regulated legal services provider",
    "a source of legal advice: it shows published law word for word and labels what its own AI composes",
    "able to tell you whether a provision applies to your situation",
)

#  How to complain, said as it is: a claim is the one route that reaches a person, and it is raised against a saved
#  deliverable only (P5.3, W941-W942). An answer that was not saved has no route yet; that gap is a row on P5.20.
TO_COMPLAIN = ("To complain about an answer, raise a claim. Under the answer of each of the 25 domain tools on the "
               "Law, Care, Education, Employment, Science and Religion pages, say what is wrong and the claim is "
               "raised from there; against a saved deliverable, raise a claim on the support page. A claim about an "
               "answer carries the fingerprint of its text and what served it, never the text itself. A claim is "
               "filed as a change that only a person decides, and it stays open until a person answers it; with "
               "sign-in off, the Owner answers every claim. This platform is not a regulated provider, so no "
               "ombudsman or regulator handles complaints about it.")

BASIS = ("Names and addresses only: nothing is copied from any of these sites, and none of them endorses this "
         "platform. Each address resolved when it was opened on 2026-10-13. No scholar and no religious body is named.")


def page() -> Dict[str, Any]:
    """The one page, the same wherever it is read. Nothing is composed and nothing about the reader is used."""
    return {
        "a_qualified_scholar": {**A_QUALIFIED_SCHOLAR, "steps": list(A_QUALIFIED_SCHOLAR["steps"])},
        "regulated_and_free_help": [dict(h) for h in HELP_FROM_A_PERSON],
        "this_platform_is_not": list(THIS_PLATFORM_IS_NOT),
        "to_complain": TO_COMPLAIN,
        "basis": BASIS,
        "the_page": THE_PAGE,
        "composed": False,
    }


@router.get("/where-help-is")
def where_help_is():
    """W953 (P5.20 clause 6) - how to find a qualified scholar, where regulated and free legal help is, and how to
    complain about an answer. Links and this platform's own words only; nothing is composed, read or recorded."""
    return page()
