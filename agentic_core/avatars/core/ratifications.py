"""A learner's standing approval of what the avatar is for — the honest input clearance gate 2 counts.

OWNER RULING 2026-10-06 (FU-471, option 3). Gate 2 (Niyyah) ratifies an emission's intent by counting distinct
signatories against a stated quorum. The avatar loop had neither, so the gate could only withhold. A request is
NOT a signature: counting the asker's own message would make every request approve itself, which is a clearance
nothing checked. So a signature here is a RECORD a person made deliberately, before the turn:

  * the learner records once what they want the avatar for, for which modes, and may revoke it at any time;
  * for a HIGH-IMPACT mode the Owner co-signs as well, so the quorum is two names, not one.

SCOPE IS BY MODE, NOT BY CONTENT. Deciding whether a particular reply falls inside "help me with maths" is a
judgement this platform cannot make honestly, so the purpose is recorded and shown, and the basis says the scope
is the mode. Signatures are NAMES recorded by this platform, not cryptographic proofs (that is P3.15).
"""
from __future__ import annotations

import time
import uuid
from typing import Any, Dict, List, Optional

from agentic_core.config import data_path, read_json_strict, store_lock, atomic_write_json

HIGH_IMPACT_MODES = ("emergency", "inspector")
OWNER_SIGNATORY = "owner"


def _path():
    return data_path("avatars/ratifications.json")


def _load() -> Dict[str, Any]:
    return read_json_strict(_path(), missing={"ratifications": []}, expect=dict)


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def record(user_id: str, purpose: str, modes: List[str], by: str) -> Dict[str, Any]:
    user_id, purpose, by = str(user_id or "").strip(), str(purpose or "").strip(), str(by or "").strip()
    modes = sorted({str(m).strip().lower() for m in (modes or []) if str(m).strip()})
    problems = [p for p, bad in (("no learner is named", not user_id), ("no purpose is stated", not purpose),
                                 ("no mode is named", not modes), ("no recorder is named", not by)) if bad]
    if problems:
        return {"recorded": False, "refused": "incomplete", "basis": "REFUSED: " + "; ".join(problems)}
    rec = {"id": "rat-" + uuid.uuid4().hex[:10], "user_id": user_id, "purpose": purpose[:300], "modes": modes,
           "signatories": [user_id], "recorded_by": by, "recorded_at": _now(), "revoked_at": None}
    with store_lock(_path()):
        d = _load()
        d.setdefault("ratifications", []).append(rec)
        atomic_write_json(_path(), d)
    return {"recorded": True, "refused": None, "ratification": rec,
            "basis": ("recorded: a learner's standing approval, scoped by MODE"
                      + (f"; {', '.join(m for m in modes if m in HIGH_IMPACT_MODES)} also need the Owner's co-signature"
                         if any(m in HIGH_IMPACT_MODES for m in modes) else ""))}


def _mutate(rid: str, fn) -> Optional[Dict[str, Any]]:
    with store_lock(_path()):
        d = _load()
        for r in d.get("ratifications") or []:
            if r.get("id") == rid:
                fn(r)
                atomic_write_json(_path(), d)
                return r
    return None


def revoke(rid: str, by: str) -> Dict[str, Any]:
    r = _mutate(rid, lambda r: r.update(revoked_at=_now(), revoked_by=str(by or "")))
    return ({"revoked": True, "ratification": r} if r else
            {"revoked": False, "refused": "not_found", "basis": f"REFUSED: no ratification {rid}"})


def cosign(rid: str, by_owner: str) -> Dict[str, Any]:
    if not str(by_owner or "").strip():
        return {"cosigned": False, "refused": "unattributed", "basis": "REFUSED: the co-signer is not named"}

    def _add(r):
        if OWNER_SIGNATORY not in r["signatories"]:
            r["signatories"].append(OWNER_SIGNATORY)
        r["cosigned_by"], r["cosigned_at"] = str(by_owner), _now()
    r = _mutate(rid, _add)
    return ({"cosigned": True, "ratification": r} if r else
            {"cosigned": False, "refused": "not_found", "basis": f"REFUSED: no ratification {rid}"})


def signatures_for(user_id: str, mode: str) -> Dict[str, Any]:
    """The signatures and quorum gate 2 counts for this learner in this mode, with the basis."""
    mode = str(mode or "").strip().lower()
    quorum = 2 if mode in HIGH_IMPACT_MODES else 1
    try:
        rows = _load().get("ratifications") or []
    except Exception as exc:  # noqa: BLE001 - an unreadable store is not an empty one
        return {"signatures": None, "quorum_required": quorum, "ratification_ids": [],
                "basis": f"the ratification store could not be read ({exc.__class__.__name__}), so NOT ASSESSED"}
    live = [r for r in rows if r.get("user_id") == str(user_id) and not r.get("revoked_at")
            and mode in (r.get("modes") or [])]
    names = sorted({n for r in live for n in (r.get("signatories") or [])})
    #  in the shape Niyyah counts: one record per (signatory, approval), so the engine's own de-duplication
    #  decides the count and every signature says which recorded approval it came from
    sigs = [{"signatory": n, "ratification_id": r["id"]} for r in live for n in (r.get("signatories") or [])]
    return {"signatures": sigs, "quorum_required": quorum, "ratification_ids": [r["id"] for r in live],
            "basis": (f"{len(live)} active approval(s) for mode {mode!r}, signed by {', '.join(names) or 'nobody'}; "
                      f"quorum {quorum}" + (" because this mode is high-impact and needs the Owner's co-signature"
                                            if quorum == 2 else "") + ". Scope is by mode, not by content")}
