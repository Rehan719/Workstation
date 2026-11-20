"""W1170 (P5.11 clause 6) - A NAMED AUTHORITY IS SHOWN ONLY WHEN IT RESOLVES AGAINST A HELD SOURCE.

Clause 6: "before a model is switched on no named authority is shown unless it resolves against a held source."
Before this round the research and analysis answers showed whatever statute a model named; only the clerk resolved a
name (specialist.resolve_authority), and only for the drafts it assembles. Each Act an answer names is now resolved
before the answer is shown: against the register of sources (a row naming it, read at its publisher and current), or
against the employment-law corpus the clerk holds. One that resolves against neither is withheld from the text, every
time it appears, and listed with why; one the register holds as replaced, withdrawn or not read is withheld the same
way and says which. An answer that names no Act is unchanged and says so. The floor, which names nothing it was not
given, is screened the same way. Nothing is fetched here and nothing is composed.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Tuple

from agentic_core.legal import time_limits as _tl       # the register reader and the one ninety-day rule

#  the register's own pattern for a statute's name (docs/SOURCES.json `patterns`): capitalised words, "Act", a year
ACT = re.compile(r"(?:[A-Z][A-Za-z']+ )+Act (?:19|20)\d{2}")
WITHHELD = "[an Act named here is withheld: it resolves against no source this platform holds]"
NOT_CURRENT = {"replaced": "the register of sources holds it as replaced",
               "withdrawn": "the register of sources holds it as withdrawn",
               "named_not_read": "the register of sources names it and holds no reading of it at its publisher"}


def _suffixes(name: str) -> List[str]:
    """The name, then the name with each leading word dropped while what remains is still a name of that shape, so a
    capitalised word before the title (a sentence's first word, or the article) does not stop it resolving. Longest
    first. No example is written here: one would itself be a name the register's check reads."""
    words = name.split()
    out = []
    for i in range(len(words) - 2):
        cand = " ".join(words[i:])
        if ACT.fullmatch(cand):
            out.append(cand)
    return out


def resolve(name: str, rows: Any) -> Dict[str, Any]:
    """Whether one named Act resolves against a held source, and how: the register first, then the clerk's corpus."""
    for cand in _suffixes(name):
        row = next((r for r in (rows or {}).values() if cand in (r.get("names") or [])), None)
        if row is None:
            continue
        st = row.get("status")
        if st == "current" and row.get("read_on"):
            return {"name": name, "resolved": True, "held_as": cand, "by": "register", "source": row["id"],
                    "page": row.get("page"), "read_on": row["read_on"], **_tl.checked(row["read_on"]),
                    "basis": "a row of the register of sources names it, read at its publisher"}
        return {"name": name, "resolved": False, "held_as": cand, "by": "register", "source": row["id"],
                "basis": NOT_CURRENT.get(st, f"the register of sources holds it as {st}")}
    from agentic_core.legal.specialist import resolve_authority
    for cand in _suffixes(name):
        r = resolve_authority(cand)
        if r.get("resolved"):
            return {"name": name, "resolved": True, "held_as": cand, "by": "corpus", "basis": r["basis"]}
    if rows is None:
        return {"name": name, "resolved": False, "by": None,
                "basis": "the register of sources could not be read, and the corpus the clerk holds does not name it"}
    return {"name": name, "resolved": False, "by": None,
            "basis": "no row of the register of sources names it, and the corpus the clerk holds does not name it"}


def screen(text: Any) -> Tuple[str, Dict[str, Any]]:
    """The text with every Act that resolves against no held source withheld, and what was done: each Act shown, with
    the source it resolves against; and, for each one withheld, why and how many times - never its name, which would
    show the very thing withheld."""
    t = str(text or "")
    rows = _tl._register()
    names: List[str] = []
    for m in ACT.finditer(t):
        #  the article before a title is not part of it: the same Act is one name, however a sentence begins
        n = re.sub(r"^The\s+", "", " ".join(m.group(0).split()))
        if n not in names:
            names.append(n)
    said = [resolve(n, rows) for n in names]
    out, withheld = t, []
    for s in sorted((s for s in said if not s["resolved"]), key=lambda s: -len(s["name"])):
        out, times = re.subn(re.escape(s["name"]).replace(r"\ ", r"\s+"), WITHHELD, out)
        withheld.append({"basis": s["basis"], "times": times})
    shown = [s for s in said if s["resolved"]]
    basis = ("no Act is named in this answer" if not said else
             (f"{len(shown)} of {len(said)} Act(s) named resolve against a source this platform holds"
              + (f"; {len(withheld)} withheld from the text" if withheld else "")))
    return out, {"shown": shown, "withheld": withheld, "basis": basis}
