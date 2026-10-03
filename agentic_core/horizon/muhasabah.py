"""Systemic Muhasabah: friction becomes a GOVERNED change, or it becomes nothing (P2.14).

WHAT THIS REFUSES TO BE, first, because the brief it came from did the opposite. The architect's daemon
wrote a root cause into every record and carried the comment "Simulated LLM analysis" beside it — a
sentence asserting WHY something went wrong, produced by nothing, filed as a finding. Nothing here writes
a root cause. A record carries the OBSERVED EVIDENCE and, only when a caller supplies one with its basis,
a CANDIDATE cause. The default is `cause: not determined`, and a candidate is never promoted to a finding
by this module.

THE THREE STEPS ARE SEPARATE AND NAMED, because collapsing any two of them is how an observation becomes
an unreviewed change:

    an observation          something happened, and here is what was seen
    a candidate cause       someone or something proposes why, WITH ITS BASIS — not a finding
    an approved change      the Change Control Agency decided, through its own gate

ONE REGISTER, NOT TWO. A filed lesson goes through change_control.submit_change — the same call the
compliance screen, the VSB evolution gate, homeostasis and the Sovereign Evolution Office use. There is
no second governance store here and no second approval path; the lessons store below records what Horizon
OBSERVED and what it DID, and the change itself lives where every other change lives. A parallel register
would be a second place to approve things, which is the thing this item exists to prevent.

THE DISPOSITION NAMES A change_type, NEVER A RANK. The rank is derived from the type by _TIER_MAP, so a
module that chose a rank would still have to invent a type, and the invented choice is what decides
whether the Board ever sees the lesson. The three dispositions and their types are in DISPOSITIONS below,
each with what it does and whether it reaches the Board — including SUBMIT_ONLY, which is the one that
must never be self-applied.
"""
from __future__ import annotations

import time
import uuid
from typing import Any, Dict, List, Optional, Tuple

from agentic_core.config import atomic_write_json, data_path, read_json_strict, store_lock

#  The triggers the item names. A lesson is written on friction, not on a schedule.
TRIGGERS: Tuple[str, ...] = ("raised_handler", "refused_gate", "owner_correction")

NOT_DETERMINED = "not determined"

#  The dispositions, each naming the change_type it FILES. `reaches_board` is stated because the surface
#  must not imply an escalation that does not happen: a config_minor record is reviewable after the fact
#  and never reaches the Board, which is correct for what it covers and was once left unsaid.
DISPOSITIONS: Dict[str, Dict[str, Any]] = {
    "APPLIED_AND_LOGGED": {
        "files_change": False,
        "change_type": None,
        "reaches_board": False,
        "what_it_is": (
            "the lesson was applied and recorded HERE and no change was filed with the Agency, so it "
            "carries no rank at all — a rank describes a change, and there is none"),
    },
    "APPLIED_AND_RECORDED": {
        "files_change": True,
        "change_type": "config_minor",
        "reaches_board": False,
        "what_it_is": (
            "a small change Horizon applied, filed as config_minor so it is reviewable AFTER THE FACT. "
            "_TIER_MAP ranks config_minor LOW and awaiting_board_ratification() is reached only by a "
            "change ranking HIGH or above, so this NEVER REACHES THE BOARD — by design, and the surface "
            "must not imply otherwise"),
    },
    "SUBMIT_ONLY": {
        "files_change": True,
        "change_type": "policy_amendment",
        "reaches_board": True,
        "what_it_is": (
            "the lesson is SUBMITTED AND NOT APPLIED. policy_amendment ranks HIGH, so once a review "
            "approves it the change awaits Board ratification. Filing this band as config_minor would "
            "be an escalation that silently does not escalate, which is the trap this item names"),
    },
    "REFUSED": {
        "files_change": False,
        "change_type": None,
        "reaches_board": False,
        "what_it_is": (
            "Horizon may not reach for this subject at all. The lesson is recorded and surfaced to the "
            "Owner, and nothing is applied and nothing is filed"),
    },
}

#  What Horizon may not apply, from the item body. Each is matched on the SUBJECT a caller declares, not
#  on the free text of the evidence — a word-scan over evidence would refuse a lesson for mentioning the
#  law and clear one that quietly amends a gate.
FORBIDDEN_SUBJECTS: Dict[str, str] = {
    "guardrail": "a guardrail is what refuses on this platform's behalf; Horizon may not edit its own brakes",
    "gate": "a gate decides what passes, so a self-applied gate change is a self-granted permission",
    "schema": (
        "a store schema changes what every reader of that store sees, and data_schema ranks MEDIUM — it "
        "would not reach the Board, so a schema lesson filed as a change would be approved without one"),
    "money": (
        "submit_change REFUSES change_type 'economy_material' with HTTP 422 because the economy files its "
        "own materiality holds and keeps them current (Owner ruling W463/W502). A money lesson is "
        "SURFACED to the Owner, never filed — and filing it under some other type would route a money "
        "decision around the gate that exists for it"),
    "faith_content": "faith content is the Owner's and a scholar's, never an automated amendment",
    "law_domain": "the law domains carry consequences for real people in live matters",
}

_CAP = 2000


def _store():
    return data_path("horizon/lessons.json")


def _read() -> List[Dict[str, Any]]:
    """STRICT: a store that cannot be read is an error, not an empty history of lessons."""
    return read_json_strict(_store(), missing=[], expect=list)


def observe(trigger: str, evidence: Dict[str, Any], *, subject: Optional[str] = None,
            candidate_cause: Optional[str] = None, cause_basis: Optional[str] = None,
            proposed_change: Optional[str] = None) -> Dict[str, Any]:
    """Write a LessonRecord. NOTHING HERE DECIDES WHY ANYTHING HAPPENED.

    `candidate_cause` is accepted only WITH a basis. A cause offered without one is not recorded as a
    cause at all — it is recorded as having been offered and rejected, with the reason, because silently
    dropping it would leave a caller believing it had been filed.
    """
    rec: Dict[str, Any] = {
        "lesson_id": f"lesson-{uuid.uuid4().hex[:12]}",
        "created_at": time.time(),
        "trigger": trigger if trigger in TRIGGERS else "unrecognised",
        "trigger_basis": (
            f"one of the three triggers this item names: {', '.join(TRIGGERS)}" if trigger in TRIGGERS
            else f"the trigger {trigger!r} is not one of {TRIGGERS}; the lesson is kept and marked, "
                 f"because discarding it would lose the observation to a naming mistake"),
        #  THE OBSERVED EVIDENCE, as given. This is the only part of a lesson that is a fact.
        "evidence": dict(evidence or {}),
        "subject": subject,
    }
    if candidate_cause and cause_basis:
        rec["candidate_cause"] = candidate_cause
        rec["cause_basis"] = cause_basis
        rec["cause_is_a_finding"] = False
        rec["cause_note"] = (
            "A CANDIDATE, NOT A FINDING. It was supplied with a basis and is recorded as a proposal about "
            "why, which nothing here has tested. Treating it as the cause is the step this module refuses "
            "to take on anyone's behalf")
    else:
        rec["candidate_cause"] = NOT_DETERMINED
        rec["cause_basis"] = None
        rec["cause_is_a_finding"] = False
        rec["cause_note"] = (
            "NOT DETERMINED, and this is the ordinary state. Nothing in this repository infers why "
            "something went wrong, so the record says so rather than carrying a sentence produced by "
            "nothing"
            + ("" if not candidate_cause else
               ". A candidate cause WAS offered and is not recorded as one, because it came with no "
               "basis — a proposal nobody can check is not better than silence"))
    rec["proposed_change"] = proposed_change
    return rec


def route(record: Dict[str, Any], disposition: str) -> Dict[str, Any]:
    """Decide what a lesson may DO, from its subject and the disposition asked for.

    Returns the routing, never the action. The caller then applies or submits through `enact`, which is
    where the refusal is enforced — separating them is deliberate, so a round cannot read a routing as
    permission to act.
    """
    subj = str(record.get("subject") or "").strip().lower()
    forbidden = FORBIDDEN_SUBJECTS.get(subj)
    if forbidden:
        return {"disposition": "REFUSED", "change_type": None, "files_change": False,
                "reaches_board": False, "forbidden_subject": subj,
                "basis": (f"REFUSED: Horizon may not reach for {subj!r}. {forbidden}. The lesson is kept "
                          f"and surfaced to the Owner; nothing is applied and nothing is filed")}
    if disposition not in DISPOSITIONS or disposition == "REFUSED":
        return {"disposition": None, "change_type": None, "files_change": False, "reaches_board": None,
                "basis": (f"NOT ROUTED: {disposition!r} is not one of "
                          f"{[k for k in DISPOSITIONS if k != 'REFUSED']}. A lesson with no disposition "
                          f"is not a lesson that was cleared to act")}
    d = DISPOSITIONS[disposition]
    return {"disposition": disposition, "change_type": d["change_type"],
            "files_change": d["files_change"], "reaches_board": d["reaches_board"],
            "basis": (f"{disposition}: {d['what_it_is']}."
                      + (f" Files change_type {d['change_type']!r}." if d["change_type"] else
                         " Files no change.")
                      + (" Reaches the Board once a review approves it." if d["reaches_board"] else
                         " Does NOT reach the Board."))}


def may_self_apply(routing: Dict[str, Any]) -> Tuple[bool, str]:
    """Whether the caller may APPLY this lesson itself. The one refusal the bar asks to be driven.

    A SUBMIT_ONLY lesson is the whole point of the disposition: it goes to the Agency and waits. A module
    that submitted it and then applied it anyway would have invented an approval, which is worse than not
    submitting at all — the record would show a governed change that nobody governed.
    """
    disp = (routing or {}).get("disposition")
    if disp == "SUBMIT_ONLY":
        return False, (
            "REFUSED: a SUBMIT_ONLY lesson may not be self-applied. It is submitted to the Change Control "
            "Agency as a policy_amendment and waits for a review and then the Board. Applying it here "
            "would manufacture an approval nobody gave, and the record would then show a governed change "
            "that was never governed")
    if disp == "REFUSED":
        return False, (routing or {}).get("basis") or "REFUSED: this subject is outside what Horizon may touch"
    if disp in ("APPLIED_AND_LOGGED", "APPLIED_AND_RECORDED"):
        return True, f"{disp}: this disposition applies the lesson, and the record says what it filed"
    return False, (
        "REFUSED: the lesson has no disposition, so there is nothing that cleared it to be applied. An "
        "unrouted lesson is not an approved one")


def save(record: Dict[str, Any], routing: Dict[str, Any],
         filed: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Persist the lesson with its routing and whatever the Agency returned."""
    row = {**record, "routing": routing,
           "disposition": routing.get("disposition"),
           "change_type": routing.get("change_type"),
           "reaches_board": routing.get("reaches_board"),
           "filed": filed,
           "filed_basis": (
               f"filed with the Change Control Agency as {filed.get('cca_id')}" if isinstance(filed, dict)
               and filed.get("cca_id") else
               "NOT FILED — see the routing's basis for why. This is the ordinary outcome for a lesson "
               "that was applied and logged, and the only outcome for a refused one")}
    with store_lock(_store()):
        rows = _read()
        rows.append(row)
        atomic_write_json(_store(), rows[-_CAP:])
    return row


def listing(limit: int = 50) -> List[Dict[str, Any]]:
    return _read()[-limit:][::-1]


def states() -> Dict[str, Any]:
    """Every disposition, what it files and whether it reaches the Board — stated, not implied."""
    return {
        "triggers": list(TRIGGERS),
        "dispositions": {k: dict(v) for k, v in DISPOSITIONS.items()},
        "forbidden_subjects": dict(FORBIDDEN_SUBJECTS),
        "one_register": (
            "a filed lesson goes through change_control.submit_change — the same call every other "
            "governed change uses. There is no second approval path here and no forked register; this "
            "store records what Horizon observed and what it did, and the change lives where changes live"),
        "no_root_cause": (
            "nothing here writes a root cause. A record carries the observed evidence and, only when one "
            "is supplied WITH ITS BASIS, a candidate cause — never promoted to a finding. The default is "
            f"{NOT_DETERMINED!r}, and it is the ordinary state rather than a gap"),
        "store_cap": _CAP,
    }
