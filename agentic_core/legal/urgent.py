"""W1165 (P5.11 clause 4) - URGENT ROUTES: a short fixed list of situations, each with its route, shown before anything
else.

Clause 4: "a short fixed list of situations - no safe place tonight, danger from a person, a hearing or deadline within
days - each shows its route before anything else; a screen may add one and may never remove one." ACCEPT: "clause 4 is
driven with the screen made to return nothing". Each step is a sentence of the GOV.UK page that gives it, quoted as
read whole at GOV.UK's content records on 2026-11-20; each page is a row of the register of sources (docs/SOURCES.json),
and each route says that page, the day it was read, and NOT RECENTLY CHECKED ninety days on, by the one rule the time
limits and the directory use. A place a page names whose own site was not opened is said so. The only words of this
platform's own are each situation's name and, where there is one, the line saying what this platform has for it.
Nothing here says whether a place is open, will answer or has room; nothing is fetched and nothing is composed.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional

from agentic_core.legal import time_limits as _tl       # the register reader and the one ninety-day rule

GOV_UK = "a GOV.UK page"
NOT_OPENED = "named on that GOV.UK page; its own site was not opened"

#  the fixed three, in the order they are shown. Every sentence in `steps` is the page's own, quoted; " ... " marks
#  where the page's words were left out.
SITUATIONS = (
    {"id": "danger_from_a_person",
     "situation": "You are in danger from a person",
     "nations": ("England", "Wales", "Scotland", "Northern Ireland"),
     "steps": ("If you are in immediate danger, call 999 and ask for the police.",
               "If you can’t speak and are calling on a mobile press 55 to have your call transferred to the police.",
               "For free, confidential advice, 24 hours a day contact a domestic abuse helpline."),
     "places": ({"nation": "England", "name": "Refuge’s National Domestic Abuse Helpline", "number": "0808 2000 247",
                 "link": "https://www.nationaldahelpline.org.uk/"},
                {"nation": "Wales", "name": "Live Fear Free", "number": "0808 80 10 100", "link": None},
                {"nation": "Scotland", "name": "Domestic Abuse and Forced Marriage Helpline", "number": "0800 027 1234",
                 "link": "https://sdafmh.org.uk/"},
                {"nation": "Northern Ireland", "name": "Domestic and Sexual Abuse Helpline", "number": "0808 802 1414",
                 "link": "https://dsahelpline.org/"},
                {"nation": "UK-wide", "name": "The Men’s Advice Line run by Respect", "number": "0808 801 0327",
                 "link": None}),
     "here": None,
     "sources": ("gov-uk-domestic-abuse-help",)},
    {"id": "no_safe_place_tonight",
     "situation": "You have no safe place to stay tonight",
     "nations": ("England",),
     "steps": ("In England, your council must help if you’re legally homeless or will become homeless within the next "
               "8 weeks.",
               "You may be legally homeless if: ... it’s not reasonable to stay in your home, for example you’re at risk "
               "of violence or abuse",
               "Find your council to get help and advice."),
     "places": ({"nation": "England", "name": "Find your council (GOV.UK)", "number": None,
                 "link": "https://www.gov.uk/homelessness-help-from-council"},
                {"nation": "Wales", "name": "Help if you’re homeless in Wales", "number": None,
                 "link": "https://gov.wales/support-if-you-are-homeless-or-about-become-homeless"},
                {"nation": "Scotland", "name": "Help if you’re homeless in Scotland", "number": None,
                 "link": "https://www.mygov.scot/if-youre-homeless"},
                {"nation": "Northern Ireland", "name": "Help if you’re homeless in Northern Ireland", "number": None,
                 "link": "https://www.nihe.gov.uk/Housing-Help/Homelessness"}),
     "here": None,
     "sources": ("gov-uk-homeless-help",)},
    {"id": "hearing_or_deadline_within_days",
     "situation": "You have a hearing or a deadline within days",
     "nations": ("England", "Wales"),
     "steps": ("Find contact details and information on courts and tribunals in England and Wales, and some "
               "non-devolved tribunals in Scotland.",
               "If you need help understanding or taking part in your hearing, you can ask for support from a "
               "communication specialist (known as an ‘intermediary’)."),
     "places": ({"nation": "England and Wales", "name": "Find a court or tribunal (GOV.UK)", "number": None,
                 "link": "https://www.gov.uk/find-court-tribunal"},
                {"nation": "Scotland", "name": "Scottish Courts website", "number": None, "link": None},
                {"nation": "Northern Ireland", "name": "Northern Ireland Courts and Tribunals Service", "number": None,
                 "link": None}),
     "here": ("For a time limit, the time-limit tool on the Law page works out the date from a dated rule, or says "
              "that a limit may still apply and where to ask today."),
     "sources": ("gov-uk-find-court-tribunal", "gov-uk-represent-yourself")},
)
FIXED_IDS = tuple(s["id"] for s in SITUATIONS)
BASIS = ("Shown before anything else, whatever was asked: each step is in the words of the GOV.UK page that gives it, "
         "with the day that page was read, and is said as not recently checked ninety days on. A place a page names "
         "whose own site was not opened is said so. Nothing here says whether a place is open, will answer or has room. "
         "Nothing here is legal advice.")


def _place(p: Dict[str, Any]) -> Dict[str, Any]:
    gov = bool(p.get("link") and str(p["link"]).startswith("https://www.gov.uk/"))
    return {**p, "own_site": GOV_UK if gov else NOT_OPENED}


def _sources(ids: Iterable[str], rows: Any) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for sid in ids:
        r = (rows or {}).get(sid)
        if r is None or not r.get("read_on"):
            out.append({"id": sid, "read": False, "recently_checked": False,
                        "checked": ("NOT CHECKED - the register of sources could not be read" if rows is None else
                                    "NOT CHECKED - the register of sources holds no reading of it")})
        else:
            out.append({"id": sid, "read": True, "name": (r.get("names") or [sid])[0], "page": r.get("page"),
                        "read_on": r["read_on"], "read_by": r.get("read_by"), **_tl.checked(r["read_on"])})
    return out


def _said(s: Dict[str, Any], rows: Any) -> Dict[str, Any]:
    return {"id": s["id"], "situation": s["situation"], "nations": list(s.get("nations") or ()),
            "steps": list(s["steps"]), "places": [_place(dict(p)) for p in s.get("places") or ()],
            "here": s.get("here"), "sources": _sources(s.get("sources") or (), rows)}


def shown(added: Optional[Iterable[Any]] = None) -> List[Dict[str, Any]]:
    """The fixed three first, always, then any route a screen adds. A screen can add a route and can never remove one:
    whatever it returns - nothing, None, a shorter list, something that is not a route - the three are shown, and a
    route a screen gives under a fixed id never replaces the fixed one."""
    rows = _tl._register()
    out = [_said(s, rows) for s in SITUATIONS]
    seen = set(FIXED_IDS)
    try:
        extra = list(added or ())
    except TypeError:                    # a screen that returned something that is not a list adds nothing
        extra = []
    for a in extra:
        if (isinstance(a, dict) and isinstance(a.get("id"), str) and a["id"] not in seen
                and isinstance(a.get("situation"), str) and isinstance(a.get("steps"), (list, tuple)) and a["steps"]
                and all(isinstance(x, str) for x in a["steps"])):
            seen.add(a["id"])
            out.append({**_said(a, rows), "added_by_screen": True})
    return out
