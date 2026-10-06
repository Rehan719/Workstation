"""R7 (Owner ruling 2026-10-05b, A.12.3) — a named human scholar approves AI-composed religious content
BEFORE a learner sees it, enforced as a gate. Unreviewed content is WITHHELD, never shown with a
disclaimer: §11 requires the audit, and a disclaimer is not a review.

WHAT THIS REPLACES. `QEPAuthoringReactor` already looked like this mechanism and gated nothing. Measured
W593: its `annotations` and `approval_queue` are plain lists on the instance, so every approval died with
the process; its approval test was `approver_trust = params.get("trust_score", 0.0)` — A NUMBER THE CALLER
SUPPLIES ABOUT ITSELF — with `scholar_id` likewise whatever the caller typed, so `approved_by` recorded a
name nobody verified; and nothing in the learner path ever consulted it. A.12.3's premise that no mechanism
exists was therefore accurate.

CORRECT AND INERT BY CONSTRUCTION. Approval requires the reviewer to be in a ROSTER, and the roster is
EMPTY until the Owner puts a real person in it. So today nothing can reach `approved`, every learner-facing
item stays withheld, and the surfaces behave exactly as W593 left them — while the behaviour becomes
principled instead of incidental. No caller can assert its way past it.

APPROVAL IS OF A BODY, NOT OF A SLOT. Each record binds a `body_hash`; if the body changes afterwards the
hash no longer matches and the item falls back to withheld. A later edit cannot inherit an earlier
sign-off — the same class as a mark that keeps applying after the thing it described has moved.

SCOPE, STATED BECAUSE IT IS AN INTERPRETATION. A.12.3 says "before a LEARNER sees it" and names what it
blocks: QEP features 5/6/7, all of A.7, P3.10 and the guidance surfaces. So this gate covers the
LEARNER / CURRICULUM path — study plans, rule cards, lesson and memorisation content: anything presented as
something to learn FROM. It does not silently switch off the five Religion RESEARCH tools, which already
withhold on the floor and already say "AI-assisted scholarly research only — NOT a fatwa and NOT a
substitute", with a referral to a qualified scholar. A tool that says "take this to a scholar" is a
different act from teaching a curriculum. That line is the author's, not the Owner's, and is registered as
its own row rather than buried here.
"""
from __future__ import annotations

import hashlib
import time
from typing import Any, Dict, Optional, Tuple

#  THE PATH IS RESOLVED LAZILY, NOT AS A MODULE CONSTANT. `living_vsbs._STORE = data_path(...)` is
#  evaluated at first import, so whichever test imported it first froze the path for the whole session and
#  a guard spent a round driving a store nothing read (W593). A function re-resolves it per call, so a
#  redirected DATA_DIR is honoured whenever it is set.
REVIEW_STORE = "scholar_review.json"
ROSTER_STORE = "scholar_roster.json"

DRAFT, IN_REVIEW, APPROVED, REJECTED = "draft", "in_review", "approved", "rejected"
STATES = (DRAFT, IN_REVIEW, APPROVED, REJECTED)


def _review_path():
    from agentic_core.config import data_path
    return data_path(REVIEW_STORE)


def _roster_path():
    from agentic_core.config import data_path
    return data_path(ROSTER_STORE)


def body_hash(body: str) -> str:
    """What was approved. Stable, and cheap enough to check on every render."""
    return hashlib.sha256((body or "").encode("utf-8")).hexdigest()[:32]


def _load(path) -> Dict[str, Any]:
    from agentic_core.config import read_json_strict
    if not path.exists():
        return {}
    return read_json_strict(path, dict, expect=dict) or {}


def _save(path, data: Dict[str, Any]) -> None:
    #  the shared-store concurrency class is a recorded defect here: a plain write loses records when the
    #  heartbeat and a request touch the same file, so every write is locked and atomic
    from agentic_core.config import atomic_write_json, store_lock
    path.parent.mkdir(parents=True, exist_ok=True)
    with store_lock(path):
        atomic_write_json(path, data)


# ── the roster ────────────────────────────────────────────────────────────────────────────────────
def roster() -> Dict[str, Any]:
    """The people who may approve. EMPTY until the Owner adds one, which is why the gate is inert."""
    return _load(_roster_path())


def roster_is_empty() -> bool:
    return not roster()


def add_scholar(scholar_id: str, name: str, credential: str, added_by: str) -> Dict[str, Any]:
    """Only the Owner's hand puts a person here; every field is recorded, none is inferred."""
    r = roster()
    r[scholar_id] = {"name": name, "credential": credential, "added_by": added_by,
                     "added_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    _save(_roster_path(), r)
    return r[scholar_id]


# ── the queue ─────────────────────────────────────────────────────────────────────────────────────
def submit(content_key: str, surface: str, body: str, reference: str = "") -> Dict[str, Any]:
    """Record a composed item as awaiting review. Submitting never approves anything."""
    recs = _load(_review_path())
    rec = {
        "content_key": content_key,
        "surface": surface,
        "reference": reference,
        "body": body,
        "body_hash": body_hash(body),
        "state": IN_REVIEW,
        "submitted_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "reviewer_id": None,
        "reviewed_at": None,
        "decision_note": None,
    }
    recs[content_key] = rec
    _save(_review_path(), recs)
    return rec


def submit_if_new(content_key: str, surface: str, body: str, reference: str = "") -> Dict[str, Any]:
    """Queue this item unless an identical one is already queued or approved.

    `submit` overwrites, which would make the request AFTER an approval reset that approval to
    `in_review` — a scholar's sign-off surviving until the next page load. So composition goes through
    here instead, and an approval is only invalidated by the text actually changing.
    """
    recs = _load(_review_path())
    rec = recs.get(content_key)
    if rec and rec.get("body_hash") == body_hash(body):
        return rec
    return submit(content_key, surface, body, reference)


def decide(content_key: str, reviewer_id: str, approve: bool, note: str = "") -> Dict[str, Any]:
    """Approve or reject. THE REVIEWER MUST BE ON THE ROSTER — there is no trust score to assert.

    The refusals are distinguished on purpose: an empty roster and an unknown reviewer are different
    facts, and telling a caller "your id is wrong" when in truth NO scholar has ever been engaged would
    send them hunting for a typo.
    """
    r = roster()
    if not r:
        return {"ok": False, "record": None, "reason": "no_scholar_engaged",
                "detail": ("No scholar is on the roster, so nothing can be approved and every item stays "
                           "withheld. This is the designed state until the Owner engages a reviewer - it "
                           "is not a lookup failure.")}
    if reviewer_id not in r:
        return {"ok": False, "record": None, "reason": "reviewer_not_on_roster",
                "detail": (f"{reviewer_id!r} is not on the scholar roster. Approval is by recorded "
                           f"identity, never by a trust score the caller supplies about itself.")}
    recs = _load(_review_path())
    rec = recs.get(content_key)
    if not rec:
        return {"ok": False, "record": None, "reason": "not_submitted",
                "detail": f"No item {content_key!r} has been submitted for review."}
    rec["state"] = APPROVED if approve else REJECTED
    rec["reviewer_id"] = reviewer_id
    rec["reviewed_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    rec["decision_note"] = note or None
    recs[content_key] = rec
    _save(_review_path(), recs)
    #  SHAPE-COMPLETE: the refusals above all carry `reason` and `detail`, so this carries them too and
    #  the refusals carry `record: None`. A caller that reads `reason` after a success, or `record` after
    #  a refusal, gets a value rather than a KeyError.
    return {"ok": True, "record": rec, "reason": "approved" if approve else "rejected",
            "detail": (f"recorded by {reviewer_id}"
                       + (f": {note}" if note else ""))}


# ── the gate the learner surface calls ────────────────────────────────────────────────────────────
def published_body(content_key: str, body: str) -> Tuple[Optional[str], str, str]:
    """(body or None, state, why). A learner surface renders the body ONLY when this returns one.

    Returning the reason rather than a bare None matters: "no scholar is engaged yet" and "a reviewer
    rejected this" are different things to tell a learner, and collapsing them into one silence is the
    shape of defect this platform keeps finding.
    """
    if roster_is_empty():
        return (None, "withheld", (
            "This is not shown because no scholar has reviewed it. §11 requires a qualified human to "
            "approve religious teaching content before a learner sees it, and no reviewer is engaged yet. "
            "A disclaimer is not a review, so nothing is shown in its place."))
    rec = _load(_review_path()).get(content_key)
    if not rec:
        return (None, "withheld", (
            "This has not been submitted for scholarly review, so it is withheld rather than shown with a "
            "caveat."))
    state = str(rec.get("state"))
    if state == APPROVED:
        if rec.get("body_hash") != body_hash(body):
            return (None, "withheld", (
                "This was approved, but the text has CHANGED since that approval, so the approval no "
                "longer covers what would be shown. It is withheld until the new text is reviewed."))
        return (rec.get("body") or body, APPROVED, (
            f"Reviewed and approved by {rec.get('reviewer_id')} on "
            f"{str(rec.get('reviewed_at'))[:10]}."))
    if state == REJECTED:
        return (None, "withheld", (
            "A reviewer rejected this content, so it is not shown."
            + (f" Reason recorded: {rec.get('decision_note')}" if rec.get("decision_note") else "")))
    return (None, "withheld", "This is awaiting scholarly review and is not shown until it is approved.")


def gate_status() -> Dict[str, Any]:
    """What a surface or an operator can read about the gate itself, with no item in hand."""
    recs = _load(_review_path())
    by_state = {s: sum(1 for r in recs.values() if r.get("state") == s) for s in STATES}
    return {
        "scholars_on_roster": len(roster()),
        "roster_is_empty": roster_is_empty(),
        "items": len(recs),
        "by_state": by_state,
        "basis": (
            "Approval requires a reviewer recorded on the scholar roster; there is no trust score a "
            "caller can assert. With an empty roster NOTHING can be approved and every learner-facing "
            "item is withheld - the designed state until the Owner engages a reviewer. An approval is "
            "bound to the exact text approved, so an edit afterwards falls back to withheld."),
    }
