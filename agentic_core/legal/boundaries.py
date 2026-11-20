"""W1167 (P5.11 clause 7) - BOUNDARIES AS ROWS: a subject that is regulated advice is information and a route to an
authorised person.

Clause 7: "a subject that is regulated advice - immigration, a debt solution, a claim managed for someone - is
information and a route to an authorised person, and the row says which regulator's page was read and when." The
Owner ruled on 2026-10-12 (advice, 3): information and a route to an authorised person, never advice. Before this round
the coverage register held immigration and the choice of a debt solution as excluded, with nothing built, and a
research question on either went to the composer like any other.

Each boundary is a row: the subject, who regulates it as the pages read say, the pages' own words, the places they
name for each nation, the pages read with the day each was read (NOT RECENTLY CHECKED ninety days on, by the one rule
the time limits use), and its regulator's own page: read, with the day, or not read and why. Every sentence in `words`
is a page's own, quoted as read whole on 2026-11-20 at GOV.UK's content records or, for the Financial Conduct
Authority's pages, at the FCA's own site (W1179); " ... " marks words left out. Each says the page it is from (W1181):
`words_from` names, for each sentence, the one page of the row whose reading in the register of sources holds it in
order, word for word; a sentence no read page holds, or more than one, names none, and none is guessed.

A question naming one of these subjects is recognised by its words and answered with the row, the urgent routes and
the places a person can go; nothing composes an answer to it. THE RECOGNITION IS A SCREEN: it may route and it never
clears. A question it does not recognise goes on as before, and says that clears nothing. Its phrasings are driven in
the suite, each labelled for or not-for before the result was known (scripts/screen_phrasings.py). Nothing is fetched.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

from agentic_core.legal import time_limits as _tl       # the register reader and the one ninety-day rule
from agentic_core.legal import urgent as _urg            # the one way a page's places and readings are said

BOUNDARIES = (
    {"id": "immigration",
     "subject": "Immigration and nationality",
     "asks": "immigration or nationality",
     "regulated": ("An immigration adviser must be registered with the Immigration Advice Authority (IAA) or be a "
                   "member of an approved professional body"),
     "words": ("Immigration advisers can help you with most things to do with immigration, including helping you to "
               "fill in the right forms and representing you at a tribunal. They do not make immigration decisions.",
               "Check if the adviser is registered and if they charge a fee before you use them.",
               "All immigration advisers must be registered with IAA or be a member of an approved professional body.",
               "You cannot get your money back if an adviser is not regulated.",
               "While the IAA doesn’t provide immigration advice directly, it offers an online database to help you "
               "find registered and qualified immigration advisers."),
     "places": ({"nation": "UK", "name": "Adviser Finder (Immigration Advice Authority)", "number": None,
                 "link": "https://portal.immigrationadviceauthority.gov.uk/s/adviser-finder"},
                {"nation": "England and Wales", "name": "The Law Society", "number": None,
                 "link": "https://solicitors.lawsociety.org.uk/"},
                {"nation": "Scotland", "name": "The Law Society of Scotland", "number": None,
                 "link": "https://www.lawscot.org.uk/find-a-solicitor/"},
                {"nation": "Northern Ireland", "name": "The Law Society of Northern Ireland", "number": None,
                 "link": "https://lawsoc-ni.org/using-a-solicitor"}),
     "sources": ("gov-uk-find-immigration-adviser", "iaa-information-for-advice-seekers"),
     "regulator": {"name": "the Immigration Advice Authority", "source": "iaa-information-for-advice-seekers"},
     #  a visa card is a payment card, not a visa
     "match": (r"\b(?:immigration|immigrants?|visas?(?! (?:card|debit|credit))|asylum|refugee status|deport(?:ed|ation)?|"
               r"leave to (?:remain|enter)|indefinite leave|settlement scheme|settled status|naturali[sz](?:e|ed|ation)|"
               r"citizenship|brp|evisa)\b")},
    {"id": "debt_solution",
     "subject": "Which debt solution to take",
     "asks": "choosing a way to deal with debts",
     "regulated": ("A Debt Management Plan is set up with a company authorised by the Financial Conduct Authority (FCA), "
                   "and a debt adviser helps choose the way to deal with a debt"),
     "words": ("Speak to a debt adviser to get help choosing the best way to deal with your debt.",
               "MoneyHelper has information about debt management and free debt advisory services.",
               "Set up a plan with a debt management company authorised by the Financial Conduct Authority (FCA). "
               "Search the Financial Services Register for an authorised company.",
               "To apply for the ‘Breathing Space’ scheme, you need to talk to a debt adviser.",
               "In Scotland you can arrange a Debt Payment Programme from the Debt Arrangement Scheme."),
     "places": ({"nation": "England and Wales", "name": "MoneyHelper: find a free debt adviser", "number": None,
                 "link": "https://www.moneyhelper.org.uk/en/money-troubles/dealing-with-debt/debt-advice-locator"},
                {"nation": "Scotland", "name": "Debt Arrangement Scheme", "number": None,
                 "link": "https://www.aib.gov.uk/debt-arrangement-scheme"}),
     "sources": ("gov-uk-options-for-dealing-with-debts",),
     #  W1179: the FCA's own page, read there once its site was allowed
     "regulator": {"name": "the Financial Conduct Authority", "source": "fca-unauthorised-unsuitable-debt-advice"},
     #  a debt solution or a person's own debts, not the law of debt in general (an assignment, a guarantee)
     "match": (r"\b(?:debt (?:solutions?|management(?: plans?| compan(?:y|ies))?|relief orders?|advi[cs]e(?:rs?)?|"
               r"payment programmes?|arrangement scheme|consolidation)|dmp|dro|iva|individual voluntary arrangements?|"
               r"go(?:ing)? bankrupt|declare (?:myself |me )?bankrupt|bankruptcy|breathing space|administration orders?|"
               r"in debt|(?:my|our) debts?|(?:pay(?:ing)? off|deal(?:ing)? with|clear(?:ing)?) (?:my |our |the |your )?debts?|"
               r"creditors? (?:are |is )?(?:chasing|harassing))\b")},
    {"id": "claims_management",
     "subject": "A claim managed for someone by a claims company",
     "asks": "having a claim managed by a claims company",
     #  W1179: who regulates it, from the FCA's own page; its "us" is said as the FCA, never quoted as this platform's
     "regulated": ("The Financial Conduct Authority's page says a claims management company must be authorised by "
                   "it to provide services for claims about financial services and products, personal injury, "
                   "employment matters, criminal injury, housing disrepair and certain industrial injuries "
                   "benefits, unless a legal regulator regulates it instead, and that such services on other "
                   "claims, such as aviation, are not regulated by the FCA"),
     "words": ("Many organisations offer impartial advice with no fee or obligation. If you make a successful claim "
               "without using a CMC, you’ll keep all the compensation yourself.",
               "You don’t need to use a CMC to make a claim, it’s free and simple to do it yourself."),
     "places": (),
     "sources": ("gov-uk-claim-compensation-cmc", "fca-using-claims-management-companies"),
     "regulator": {"name": "the Financial Conduct Authority", "source": "fca-using-claims-management-companies"},
     "match": r"\b(?:claims? management(?: compan(?:y|ies)| firms?)?|claims? compan(?:y|ies)|claims? firms?|cmcs?)\b"},
)
BASIS = ("Regulated advice is not given here: each subject is information in the words of the pages read, and a route "
         "to an authorised person. Each row says which pages were read and when, and whether its regulator's own page "
         "was read. Nothing here says whether a place is open, will take a case or is right for it. Nothing here is "
         "legal advice.")
COVERAGE = ("recognises a question that names immigration or nationality, a way of dealing with debts or a person's own "
            "debts, or a claims management company, in English. A question that names none of these words is not "
            "recognised, however regulated its subject: it goes on as before. Recognising nothing is not a clearance.")
_WITH_WORDS = "What the pages read say, and where to go, are listed with this answer."
_WITHOUT_WORDS = "Where to go is listed with this answer."


def _regulator(r: Dict[str, Any], rows: Any) -> Dict[str, Any]:
    """The regulator's own page as the row says it: read, with the day it was read; or not read, and why."""
    if r.get("source"):
        page = _urg._sources([r["source"]], rows)[0]
        return {"name": r["name"], "read": bool(page["read"]), "page": page,
                "why": None if page["read"] else page["checked"]}
    return {"name": r.get("name"), "read": False, "page": None, "why": r["why_not"]}


def _words_from(b: Dict[str, Any], rows: Any) -> List[Optional[str]]:
    """W1181 - the page each quoted sentence is from: the one of the row's pages that the register holds a reading
    of, whose reading holds every part of the sentence in order and word for word (" ... " marks words left out; a
    run of white space counts as one space). None when no such page holds it, when more than one does, or when the
    register could not be read: a page is never guessed for a sentence."""
    def flat(s: Any) -> str:
        return " ".join(str(s).split())

    def holds(reading: str, parts: List[str]) -> bool:
        at = 0
        for p in parts:
            i = reading.find(p, at)
            if i < 0:
                return False
            at = i + len(p)
        return True

    out: List[Optional[str]] = []
    for w in b["words"]:
        parts = [flat(p) for p in str(w).split(" ... ") if p.strip()]
        hit = [sid for sid in b["sources"]
               if parts and ((rows or {}).get(sid) or {}).get("read_on")
               and holds(flat(((rows or {}).get(sid) or {}).get("says") or ""), parts)]
        out.append(hit[0] if len(hit) == 1 else None)
    return out


def row(b: Dict[str, Any], rows: Any = None) -> Dict[str, Any]:
    """One boundary as it is said: its subject, who regulates it, the pages' words, the places, the pages read and the
    regulator's own page."""
    rows = _tl._register() if rows is None else rows
    return {"id": b["id"], "subject": b["subject"], "regulated": b["regulated"], "words": list(b["words"]),
            "words_from": _words_from(b, rows), "places": [_urg._place(dict(p)) for p in b["places"]],
            "sources": _urg._sources(b["sources"], rows), "regulator": _regulator(b["regulator"], rows)}


def rows() -> List[Dict[str, Any]]:
    reg = _tl._register()
    return [row(b, reg) for b in BOUNDARIES]


def recognises(text: Any) -> Optional[Dict[str, Any]]:
    """The boundary a question's words name, or None. None is NOT a clearance."""
    low = " " + re.sub(r"\s+", " ", str(text or "").lower()) + " "
    return next((b for b in BOUNDARIES if re.search(b["match"], low)), None)


def message(b: Dict[str, Any]) -> str:
    return (f"This asks about {b['asks']}, which is regulated advice, so it is not answered here. {b['regulated']}. "
            f"{_WITH_WORDS if b['words'] else _WITHOUT_WORDS} The services listed with it give free or regulated help. "
            "Nothing here is legal advice.")


def route(question: Any, context: Any = "") -> Optional[Dict[str, Any]]:
    """The answer for a question about a regulated subject: its row, the message and the places a person can go, or
    None. None is NOT a clearance."""
    b = recognises(f"{question or ''} {context or ''}")
    if b is None:
        return None
    from agentic_core.api.where_help import HELP_FROM_A_PERSON
    from agentic_core.legal import directory as _dir     # W1163 (P5.11 clause 3) - each place a row of the directory
    return {"boundary": row(b), "message": message(b), "people": _dir.rows(HELP_FROM_A_PERSON), "coverage": COVERAGE,
            "composed": False}
