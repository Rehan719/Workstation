"""The legal specialist: a meticulous clerk, never counsel (P3.23, FU-278's acceptance bar).

It ASSEMBLES; it does not write prose about a matter. Every particular is filled only from a line located in a
document inside the ONE named folder (legal/bundle.py, the only reader), and carries that document and line;
a particular nothing in the bundle states is rendered as a BLANK the user must fill, never as text. Every
authority (a statute or a case) is emitted only if the corpus the platform holds names it; otherwise it is
REFUSED by name. A filing-shaped artefact is a DRAFT until the Owner records an approval against it. Nothing
here is legal advice, and every response says so where it is read.

THE CORPUS IS THIN, and that is reported rather than hidden: knowledge/Law/EmploymentTribunal names one statute.
An authority outside it is refused, not paraphrased.
"""
from __future__ import annotations

import pathlib
import re
import time
import uuid
from typing import Any, Dict, List

from agentic_core.config import atomic_write_json, data_path, read_json_strict, store_lock

FILING_SHAPED = ("et1_claim", "cease_desist")
NOT_LEGAL_ADVICE = ("Nothing here is legal advice. This platform assembles and cites as a clerk would; it is "
                    "never counsel, and it never forecasts an outcome.")
_CORPUS = pathlib.Path(__file__).resolve().parents[2] / "knowledge" / "Law" / "EmploymentTribunal"


def _corpus_text() -> str:
    parts = []
    for p in sorted(_CORPUS.rglob("*.json")) + sorted(_CORPUS.rglob("*.md")):
        try:
            parts.append(p.read_text(encoding="utf-8", errors="replace"))
        except OSError:
            continue
    return "\n".join(parts)


def resolve_authority(name: str) -> Dict[str, Any]:
    n = str(name or "").strip()
    if not n:
        return {"authority": n, "resolved": False, "basis": "no authority was named"}
    if n.lower() in _corpus_text().lower():
        return {"authority": n, "resolved": True,
                "basis": "named in the employment-law corpus this platform holds (knowledge/Law/EmploymentTribunal)"}
    return {"authority": n, "resolved": False,
            "basis": ("REFUSED: the corpus this platform holds does not name it, so it is not cited - an authority "
                      "is resolved against a real source or not emitted at all")}


def locate(words: List[str]) -> Dict[str, Any]:
    """The first line in the bundle containing every word, with its document and 1-based line, or a blank."""
    from agentic_core.legal import bundle
    ws = [w.lower() for w in words if str(w).strip()]
    ls = bundle.list_documents()
    if not ws or ls["documents"] is None:
        return {"found": False, "document": None, "line": None, "text": None,
                "basis": ls["basis"] if ls["documents"] is None else "no search words were given"}
    for doc in ls["documents"]:
        o = bundle.open_document(doc)
        if not o["opened"]:
            continue
        for i, ln in enumerate(o["text"].splitlines(), start=1):
            low = ln.lower()
            if all(w in low for w in ws):
                return {"found": True, "document": doc, "line": i, "text": ln.strip(),
                        "basis": f"located at {doc}:{i}"}
    return {"found": False, "document": None, "line": None, "text": None,
            "basis": f"no line in the {ls['count']} document(s) of the named folder states this"}


def verify_located(p: Dict[str, Any]) -> Dict[str, Any]:
    """Re-read the cited line through the bundle reader and check the quoted text is there."""
    from agentic_core.legal import bundle
    if not p.get("found"):
        return {"verdict": "NOT_ASSESSABLE", "basis": "a blank cites nothing, so there is nothing to verify"}
    o = bundle.open_document(p["document"])
    if not o["opened"]:
        return {"verdict": "NOT_ASSESSABLE", "basis": o["basis"]}
    lines = o["text"].splitlines()
    ok = 1 <= p["line"] <= len(lines) and p["text"] in lines[p["line"] - 1]
    return {"verdict": "MET" if ok else "UNMET",
            "basis": (f"the quoted text is present at {p['document']}:{p['line']}" if ok else
                      f"the quoted text is NOT at {p['document']}:{p['line']}")}


def assemble(template_id: str, particulars: List[Dict[str, Any]], authorities: List[str]) -> Dict[str, Any]:
    from agentic_core.legal import bundle
    filled = []
    for spec in particulars or []:
        name = str((spec or {}).get("name") or "").strip()
        words = [w for w in (spec or {}).get("words") or [] if str(w).strip()]
        loc = locate(words)
        item = {"particular": name, **loc}
        item["verification"] = verify_located(loc)
        item["rendered"] = (loc["text"] if loc["found"] else
                            f"[BLANK: {name} - no document in the bundle states this; fill it in yourself]")
        filled.append(item)
    auth = [resolve_authority(a) for a in authorities or []]
    sourced = [f["particular"] for f in filled if f["found"]]
    blanks = [f["particular"] for f in filled if not f["found"]]
    unresolved_checks = [f["particular"] for f in filled if f["verification"]["verdict"] != "MET" and f["found"]]
    filing = template_id in FILING_SHAPED
    art = {"artefact_id": "lgl-" + uuid.uuid4().hex[:10], "template_id": template_id,
           "status": "draft_awaiting_owner_approval" if filing else "draft",
           "filing_shaped": filing, "particulars": filled, "authorities": auth,
           "sourced": sourced, "blanks": blanks, "unresolved_checks": unresolved_checks,
           "authorities_refused": [a["authority"] for a in auth if not a["resolved"]],
           "is_template": not sourced,
           "bundle": bundle.status(), "not_legal_advice": NOT_LEGAL_ADVICE,
           "face": (f"{len(sourced)} particular(s) from a document, {len(blanks)} BLANK for you to fill"
                    + (f"; {len(unresolved_checks)} located line(s) failed re-verification" if unresolved_checks else "")
                    + ("; this is a TEMPLATE - the bundle stated none of its particulars" if not sourced else "")),
           "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    with store_lock(_store()):
        d = read_json_strict(_store(), missing={"artefacts": {}}, expect=dict)
        d.setdefault("artefacts", {})[art["artefact_id"]] = art
        atomic_write_json(_store(), d)
    return art


def _store():
    return data_path("legal/artefacts.json")


def approve(artefact_id: str, by: str) -> Dict[str, Any]:
    if not str(by or "").strip():
        return {"approved": False, "refused": "unattributed", "basis": "REFUSED: the approver is not named"}
    with store_lock(_store()):
        d = read_json_strict(_store(), missing={"artefacts": {}}, expect=dict)
        a = (d.get("artefacts") or {}).get(artefact_id)
        if not a:
            return {"approved": False, "refused": "not_found", "basis": f"REFUSED: no artefact {artefact_id}"}
        if not a.get("filing_shaped"):
            return {"approved": False, "refused": "not_filing_shaped",
                    "basis": "REFUSED: only a filing-shaped artefact needs the Owner's approval"}
        a["status"] = "approved_by_owner"
        a["approved_by"], a["approved_at"] = str(by), time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        atomic_write_json(_store(), d)
    return {"approved": True, "refused": None, "artefact": a,
            "basis": f"approved by {by}; it is still not legal advice and nothing about the matter leaves this machine"}
