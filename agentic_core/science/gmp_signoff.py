"""GMP record QA sign-off — the human gate P3.23 names for the GMP/science specialist.

A GMP record (a batch record, a deviation, a CAPA) is not released until a QA signatory ON THE ROSTER signs it.
Modelled on api/scholar_review.py, the one domain gate already built, so the refusals keep the same three
distinctions: no QA signatory has been engaged at all; the signer is not on the roster; the record was never
submitted. A record whose text changed after signature is withheld again, because the signature no longer
covers what would be released. Signatures are recorded identities, never a trust score, and nothing here is a
regulatory determination.
"""
from __future__ import annotations

import hashlib
import time
from typing import Any, Dict, Optional, Tuple

from agentic_core.config import atomic_write_json, data_path, read_json_strict, store_lock

SIGNED, REJECTED, PENDING = "signed", "rejected", "pending_qa"


def _p(name: str):
    return data_path(f"science/gmp_{name}.json")


def _load(name: str) -> Dict[str, Any]:
    return read_json_strict(_p(name), missing={}, expect=dict)


def _save(name: str, d: Dict[str, Any]) -> None:
    with store_lock(_p(name)):
        atomic_write_json(_p(name), d)


def _hash(body: str) -> str:
    return hashlib.sha256(str(body or "").encode("utf-8")).hexdigest()


def add_signatory(signatory_id: str, name: str, role: str, added_by: str) -> Dict[str, Any]:
    if not all(str(x or "").strip() for x in (signatory_id, name, role, added_by)):
        return {"ok": False, "reason": "incomplete", "detail": "a QA signatory needs an id, a name, a role and who added them"}
    r = _load("roster")
    r[signatory_id] = {"name": name, "role": role, "added_by": added_by,
                       "added_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    _save("roster", r)
    return {"ok": True, "reason": "added", "detail": f"{signatory_id} is on the QA roster"}


def submit(record_id: str, kind: str, body: str) -> Dict[str, Any]:
    if not str(record_id or "").strip() or not str(body or "").strip():
        return {"ok": False, "record": None, "reason": "incomplete", "detail": "a GMP record has an id and a body"}
    recs = _load("records")
    recs[record_id] = {"record_id": record_id, "kind": str(kind or "batch_record"), "body": body,
                       "body_hash": _hash(body), "state": PENDING,
                       "submitted_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    _save("records", recs)
    return {"ok": True, "record": recs[record_id], "reason": "submitted", "detail": "awaiting QA sign-off"}


def sign(record_id: str, signatory_id: str, approve: bool, note: str = "") -> Dict[str, Any]:
    roster = _load("roster")
    if not roster:
        return {"ok": False, "record": None, "reason": "no_qa_engaged",
                "detail": ("No QA signatory is on the roster, so no GMP record can be released and every one stays "
                           "withheld. This is the designed state until the Owner engages QA - not a lookup failure.")}
    if signatory_id not in roster:
        return {"ok": False, "record": None, "reason": "signatory_not_on_roster",
                "detail": f"{signatory_id!r} is not on the QA roster; release is by recorded identity only"}
    recs = _load("records")
    rec = recs.get(record_id)
    if not rec:
        return {"ok": False, "record": None, "reason": "not_submitted", "detail": f"No GMP record {record_id!r} was submitted"}
    rec.update(state=SIGNED if approve else REJECTED, signatory_id=signatory_id, signed_body_hash=rec["body_hash"],
               signed_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), note=note or None)
    _save("records", recs)
    return {"ok": True, "record": rec, "reason": "signed" if approve else "rejected", "detail": f"recorded by {signatory_id}"}


def released(record_id: str) -> Tuple[Optional[str], str, str]:
    """(body or None, state, why). A surface shows the record's body ONLY when this returns one."""
    if not _load("roster"):
        return (None, "withheld", "No QA signatory is engaged, so no GMP record is released.")
    rec = _load("records").get(record_id)
    if not rec:
        return (None, "withheld", "This record was never submitted for QA sign-off.")
    if rec.get("state") == SIGNED:
        if rec.get("signed_body_hash") != rec.get("body_hash"):
            return (None, "withheld", "Signed, but the text changed after signature, so the signature no longer covers it.")
        return (rec["body"], SIGNED, f"Signed off by {rec.get('signatory_id')} on {str(rec.get('signed_at'))[:10]}.")
    if rec.get("state") == REJECTED:
        return (None, "withheld", "QA rejected this record, so it is not released.")
    return (None, "withheld", "Awaiting QA sign-off; not released until signed.")
