"""P3.21 — THE VERIFIER, AND THE WITHHOLD IT CAN TRIGGER. Checkable checks only.

Three checks, each returning MET / UNMET / NOT ASSESSABLE with its basis:

  1. does every citation resolve to a document this verifier may read
  2. does the quoted line exist AT the cited location
  3. does the figure appear in the cited source

An UNMET check WITHHOLDS the output and names the check that failed. There is no confidence float anywhere
in this path, and that is the point of the item rather than a detail of it: the roadmap proposed withholding
whenever a verifier-confidence number fell below a threshold, and this repository already carries registered
rows against that exact shape — a quality pipeline that starts at 0.90 and adds 0.05 per iteration without reading the content, a
consultation contract that REQUIRES a float so every implementer returns 0.96, and a cognitive base class
hard-coding 0.95 on every success. A threshold over an invented number is a gate that cannot refuse.

SO NOTHING HERE PRODUCES OR READS A NUMBER AS A VERDICT. Every function returns one of three strings. The
only integers are line numbers and counts of checks, and neither is compared against a threshold.

WHAT "NOT ASSESSABLE" MEANS, AND WHY IT IS NOT A SOFT PASS. A citation with no document named cannot be
resolved — that is not the same as resolving to nothing, and it is not the same as resolving correctly. The
three states are kept apart everywhere because collapsing them is how an unmeasured thing comes to read as
a measured one. NOT ASSESSABLE NEVER WITHHOLDS and never passes: it is reported, and the output carries the
fact that a check could not be run.

READING BOUNDS. A citation may only resolve inside this repository. A path that escapes it — absolute,
or climbing out with `..` — is NOT ASSESSABLE with that stated as the reason, because this verifier is not
a file reader for arbitrary paths and saying "UNMET" would imply it looked and found nothing.
"""
from __future__ import annotations

import pathlib
import re
from typing import Any, Dict, List, Optional

MET = "MET"
UNMET = "UNMET"
NOT_ASSESSABLE = "NOT ASSESSABLE"
VERDICTS = (MET, UNMET, NOT_ASSESSABLE)

#  the three checks, named so a withheld output can say which one failed
CHECK_RESOLVES = "citation_resolves_to_a_document"
CHECK_QUOTE = "quoted_line_exists_at_the_cited_location"
CHECK_FIGURE = "figure_appears_in_the_cited_source"
CHECKS = (CHECK_RESOLVES, CHECK_QUOTE, CHECK_FIGURE)

_ROOT = pathlib.Path(__file__).resolve().parents[2]


def _verdict(check: str, verdict: str, basis: str, **extra: Any) -> Dict[str, Any]:
    """One check's result. A verdict is always one of three strings — never a score."""
    if verdict not in VERDICTS:                      # pragma: no cover - a programming error, not input
        raise ValueError(f"a verdict must be one of {VERDICTS}, not {verdict!r}")
    return {"check": check, "verdict": verdict, "basis": basis, **extra}


def _resolve(document: Optional[str]) -> Dict[str, Any]:
    """(path or None, reason). A path outside this repository is not read and says so."""
    if not str(document or "").strip():
        return {"path": None, "why": "the citation names no document"}
    raw = str(document).strip()
    p = pathlib.Path(raw)
    if p.is_absolute():
        return {"path": None, "why": (f"{raw!r} is an absolute path; this verifier reads only inside the "
                                      f"repository, so it did NOT look")}
    try:
        full = (_ROOT / p).resolve()
        full.relative_to(_ROOT)
    except (ValueError, OSError):
        return {"path": None, "why": (f"{raw!r} resolves outside the repository, so this verifier did NOT "
                                      f"look - which is not the same as looking and finding nothing")}
    return {"path": full, "why": ""}


def check_citation_resolves(citation: Dict[str, Any]) -> Dict[str, Any]:
    """Check 1 — does the citation resolve to a document this verifier may read?"""
    r = _resolve(citation.get("document"))
    if r["path"] is None:
        return _verdict(CHECK_RESOLVES, NOT_ASSESSABLE, r["why"])
    if not r["path"].is_file():
        return _verdict(CHECK_RESOLVES, UNMET,
                        f"{citation.get('document')!r} names a document that does not exist in this "
                        f"repository, so the citation resolves to nothing")
    return _verdict(CHECK_RESOLVES, MET,
                    f"{citation.get('document')!r} exists and was read")


def check_quote_at_location(citation: Dict[str, Any]) -> Dict[str, Any]:
    """Check 2 — does the quoted text exist AT the cited line?

    The location is part of the claim. A quote that appears elsewhere in the document is NOT the same as a
    quote at the cited line, so this reports UNMET and says where it was actually found - a reader can then
    correct the citation rather than being told the quote is absent.
    """
    quote = str(citation.get("quote") or "").strip()
    line_no = citation.get("line")
    if not quote:
        return _verdict(CHECK_QUOTE, NOT_ASSESSABLE, "the citation quotes nothing")
    r = _resolve(citation.get("document"))
    if r["path"] is None or not r["path"].is_file():
        return _verdict(CHECK_QUOTE, NOT_ASSESSABLE,
                        f"the quote cannot be located because the document could not be read: "
                        f"{r['why'] or 'it does not exist'}")
    if not isinstance(line_no, int) or line_no < 1:
        return _verdict(CHECK_QUOTE, NOT_ASSESSABLE,
                        "the citation gives no line number, and a quote without a location is not a "
                        "checkable claim about where it appears")
    try:
        lines = r["path"].read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as e:
        return _verdict(CHECK_QUOTE, NOT_ASSESSABLE, f"the document could not be read ({e.__class__.__name__})")
    if line_no > len(lines):
        return _verdict(CHECK_QUOTE, UNMET,
                        f"the citation names line {line_no} and the document has {len(lines)} line(s)",
                        document_lines=len(lines))
    if quote in lines[line_no - 1]:
        return _verdict(CHECK_QUOTE, MET, f"the quoted text is present at line {line_no}")
    found_at = [i + 1 for i, ln in enumerate(lines) if quote in ln]
    return _verdict(CHECK_QUOTE, UNMET,
                    (f"the quoted text is NOT at line {line_no}"
                     + (f"; it appears at line(s) {found_at[:5]}, so the location is wrong rather than the "
                        f"quote" if found_at else " and does not appear anywhere in the document")),
                    found_at_lines=found_at[:5])


def check_figure_in_source(citation: Dict[str, Any]) -> Dict[str, Any]:
    """Check 3 — does the cited figure appear in the cited source?

    Matched on the digits, so 1,234 in a claim finds 1234 or 1,234 in the source. Deliberately NOT a
    numeric comparison: this check answers "is this figure in that document", and inventing a tolerance
    would make it a threshold over a number, which is what this item forbids.
    """
    figure = str(citation.get("figure") or "").strip()
    if not figure:
        return _verdict(CHECK_FIGURE, NOT_ASSESSABLE, "the citation carries no figure")
    r = _resolve(citation.get("document"))
    if r["path"] is None or not r["path"].is_file():
        return _verdict(CHECK_FIGURE, NOT_ASSESSABLE,
                        f"the figure cannot be checked because the document could not be read: "
                        f"{r['why'] or 'it does not exist'}")
    digits = re.sub(r"[^0-9]", "", figure)
    if not digits:
        return _verdict(CHECK_FIGURE, NOT_ASSESSABLE,
                        f"{figure!r} contains no digits, so there is nothing to look for")
    try:
        text = r["path"].read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return _verdict(CHECK_FIGURE, NOT_ASSESSABLE, f"the document could not be read ({e.__class__.__name__})")
    if digits in re.sub(r"[^0-9]", "", text):
        return _verdict(CHECK_FIGURE, MET,
                        f"the figure {figure!r} appears in {citation.get('document')!r}")
    return _verdict(CHECK_FIGURE, UNMET,
                    f"the figure {figure!r} does NOT appear in {citation.get('document')!r}")


def verify(output: str, citations: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """Run the three checks over every citation and WITHHOLD the output if any is UNMET.

    THE WITHHOLD NAMES THE CHECK. An output withheld without saying which check failed is indistinguishable
    from one that failed for no reason, and the author cannot correct it.

    NOT ASSESSABLE never withholds and never passes. It is carried in the response so a reader can see that
    a check could not be run — which is the difference between "this was checked and is right" and "nobody
    could check this".
    """
    cites = [c for c in (citations or []) if isinstance(c, dict)]
    results: List[Dict[str, Any]] = []
    for idx, c in enumerate(cites):
        for fn in (check_citation_resolves, check_quote_at_location, check_figure_in_source):
            r = fn(c)
            r["citation_index"] = idx
            r["document"] = c.get("document")
            results.append(r)

    failed = [r for r in results if r["verdict"] == UNMET]
    unassessable = [r for r in results if r["verdict"] == NOT_ASSESSABLE]
    met = [r for r in results if r["verdict"] == MET]

    withheld = bool(failed)
    return {
        #  the overall verdict is one of the same three strings, never a score
        "verdict": UNMET if failed else (MET if met else NOT_ASSESSABLE),
        "withheld": withheld,
        "output": None if withheld else output,
        "withheld_because": ([{"check": r["check"], "document": r.get("document"), "basis": r["basis"]}
                              for r in failed] if withheld else None),
        "withheld_basis": (
            ("the output is withheld because "
             + "; ".join(f"{r['check']} is UNMET ({r['basis']})" for r in failed))
            if withheld else
            ("nothing failed, so the output is not withheld"
             + (f" - {len(unassessable)} check(s) could NOT be assessed and are reported rather than "
                f"counted as passes" if unassessable else ""))),
        "checks": results,
        "counts": {MET: len(met), UNMET: len(failed), NOT_ASSESSABLE: len(unassessable)},
        "citations_checked": len(cites),
        "basis": (
            "three checkable checks per citation: whether it resolves to a document in this repository, "
            "whether the quoted text is at the cited line, and whether the cited figure appears in that "
            "document. Each returns MET, UNMET or NOT ASSESSABLE. NO CONFIDENCE SCORE is produced or read "
            "anywhere in this path - a threshold over an invented number is a gate that cannot refuse, and "
            "this platform already carried three of those. NOT ASSESSABLE is neither a pass nor a failure: "
            "it means the check could not be run, and it is reported so an unmeasured thing never reads as "
            "a measured one."),
    }
