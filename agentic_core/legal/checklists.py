"""W1168 (P5.11 clause 8) - CHECKLISTS: what to gather for a subject is a list with its source, not prose.

Clause 8: "what to gather for a subject is a list with its source, not prose." Each checklist is a row: the subject,
the nations its page is for, and groups of items; every item, and every line that leads a group, is the page's own
words, quoted as read whole at GOV.UK's content records on 2026-11-20, with the part of the page it is in. Each list
says the pages read and the day each was read, said as NOT RECENTLY CHECKED ninety days on by the one rule the time
limits use. The only words of this platform's own are each group's heading and the line saying what this platform
has for the subject. A list says nothing about whether a claim will succeed, what it is worth, or whether a time
limit has passed; nothing here is composed and nothing is fetched.
"""
from __future__ import annotations

from typing import Any, Dict, List

from agentic_core.legal import time_limits as _tl       # the register reader and the one ninety-day rule
from agentic_core.legal import urgent as _urg            # the one way a page's readings are said

CHECKLISTS = (
    {"id": "employment_tribunal_claim",
     "subject": "Making an employment tribunal claim",
     "nations": ("England", "Wales", "Scotland"),
     "elsewhere": "There’s a different way to make a claim to an employment tribunal in Northern Ireland.",
     "groups": (
         {"heading": "To make the claim", "part": "Make a claim", "lead": "To use this service, you’ll need:",
          "items": ("the names and addresses of all the people making the claim (the ‘claimants’)",
                    "the names and addresses of the employer or organisation you’re claiming against (the "
                    "‘respondents’)",
                    "your Acas early conciliation certificate number")},
         {"heading": "Documents to share", "part": "After you make a claim",
          "lead": "Examples of relevant documents could include:",
          "items": ("a contract of employment", "pay slips", "details of your pension scheme",
                    "notes from relevant meetings you attended at work")},
         {"heading": "At the hearing", "part": "Going to a tribunal hearing", "lead": None,
          "items": ("You must have all the documents you’re using to support your case with you.",)}),
     "here": ("For the time limit, the time-limit tool on this page works out the date from a dated rule, or says that "
              "a limit may still apply and where to ask today."),
     "sources": ("gov-uk-employment-tribunals-guide",)},
    {"id": "court_claim_for_money",
     "subject": "Making a court claim for money",
     "nations": ("England", "Wales"),
     "elsewhere": None,
     "groups": (
         {"heading": "To claim online", "part": "Make a claim", "lead": None,
          "items": ("You’ll be asked for the name, address and email address of the person you’re claiming against.",)},
         {"heading": "To pay the court fee", "part": "Make a claim", "lead": "You’ll also need either:",
          "items": ("a debit or credit card to pay the court fee",
                    "your ‘help with fees’ reference number if you’ve already applied for help with fees online")}),
     "here": None,
     "sources": ("gov-uk-make-court-claim-for-money",)},
)
BASIS = ("Each list is in the words of the page it names, with the part of the page each item is in and the day the "
         "page was read, and is said as not recently checked ninety days on. A list says nothing about whether a claim "
         "will succeed, what it is worth, or whether a time limit has passed. Nothing here is legal advice.")


def row(c: Dict[str, Any], rows: Any = None) -> Dict[str, Any]:
    """One checklist as it is said: its subject, its nations, its groups in the page's words, and the pages read."""
    rows = _tl._register() if rows is None else rows
    return {"id": c["id"], "subject": c["subject"], "nations": list(c["nations"]), "elsewhere": c["elsewhere"],
            "groups": [{"heading": g["heading"], "part": g["part"], "lead": g["lead"], "items": list(g["items"])}
                       for g in c["groups"]],
            "here": c["here"], "sources": _urg._sources(c["sources"], rows)}


def rows() -> List[Dict[str, Any]]:
    reg = _tl._register()
    return [row(c, reg) for c in CHECKLISTS]
