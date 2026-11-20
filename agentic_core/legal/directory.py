"""W1163 (P5.11 clause 3) - THE DIRECTORY: a place a person can go, as a row.

Clause 3: "a place a person can go is a row with its nation, what it helps with, its public route, the page that says
so and the date read; a row past its review date is shown as not recently checked. Nothing is said about availability,
acceptance or an appointment." The Owner ruled on 2026-10-12 that a place is shown as not recently checked ninety days
after the date it was read.

The places are the help list's eight (agentic_core/api/where_help.py, W724 and W953): a name, an address and one line
of this platform's own words each. Before this round the list said one sentence for all of them, that each address
resolved when it was opened on 2026-10-13, and no nation. Each place's row in the register of sources (docs/SOURCES.json)
already said which nations it is for, the page, the day it was read and how: by one request to the address, its content
not read. That row is the page that says so, and every place now says it, with the ninety days; the register's own
words for how it was read are said too, so a place whose address only resolved is never shown as read. Nothing is
fetched here, and nothing is composed.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List

from agentic_core.legal import time_limits as _tl       # the register reader and the one ninety-day rule

#  each place's row in the register of sources, by the address the help list gives it
SAYS_SO: Dict[str, str] = {
    "https://www.gov.uk/find-legal-advice": "help-gov-find-legal-advice",
    "https://www.gov.uk/legal-aid/check-legal-aid": "help-gov-check-legal-aid",
    "https://www.citizensadvice.org.uk/": "help-citizens-advice",
    "https://www.acas.org.uk/": "help-acas",
    "https://www.lawcentres.org.uk/": "help-law-centres-network",
    "https://www.advicenow.org.uk/": "help-advicenow",
    "https://weareadvocate.org.uk/": "help-advocate",
    "https://www.lawworks.org.uk/legal-advice-individuals": "help-lawworks-individuals",
}
#  said once, beside the places: the clause's own boundary
NOTHING_SAID = ("Nothing here says whether a place is open, whether it will take your question, or whether it has an "
                "appointment for you.")
_NOT_READ = "the page's content was NOT read"
_UNSET = object()


def _how(read_by: str) -> str:
    """How the page that says so was read, in the register's own terms: its content read, or its address resolved only."""
    return ("its address resolved when it was opened; its content was not read" if _NOT_READ in (read_by or "")
            else "its content was read")


def place(entry: Dict[str, str], rows: Any = _UNSET) -> Dict[str, Any]:
    """One place of the help list as a row of the directory: the nations its register row gives, the page that says so,
    the day that page was read and how, and whether that was within ninety days. A place the register holds no reading
    of is said as not checked, never as read."""
    rows = _tl._register() if rows is _UNSET else rows
    sid = SAYS_SO.get(entry["link"])
    r = (rows or {}).get(sid) if sid else None
    if r is None or not r.get("read_on"):
        return {**entry, "nations": None, "says_so": None, "how_read": None, "recently_checked": False,
                "checked": ("NOT CHECKED - the register of sources could not be read" if rows is None else
                            "NOT CHECKED - the register of sources holds no reading of this place")}
    return {**entry, "nations": list(r.get("nation") or []), "says_so": r.get("page"), "how_read": _how(r.get("read_by")),
            **_tl.checked(r["read_on"])}


def rows(entries: Iterable[Dict[str, str]]) -> List[Dict[str, Any]]:
    """Every place of `entries` as a row of the directory, the register read once for all of them."""
    reg = _tl._register()
    return [place(dict(e), reg) for e in entries]
