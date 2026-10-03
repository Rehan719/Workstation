"""§P2.10 — THE DELIVERY METHOD, HELD BY THE ARMS-LENGTH AGENCY.

The discipline that produced this delivery used to live outside the product: the lessons were in an
assistant's notes, the mechanisms in scripts and docs, and nothing in the platform applied either to a
change. The Owner's instruction is that Change Control — the arms-length agency — holds it.

Four parts, and the risk this module must not realise is stated before any of them:

    A GREEN "METHOD COMPLIANT" BADGE OVER REQUIREMENTS NOTHING EVALUATED.

Most of the method cannot be mechanically verified from a change record. Whether a blind was added, whether a
refutation ran, whether a basis string was computed rather than asserted — none of that is visible in the
artefacts the platform holds. So `check_change` answers MET, UNMET or NOT_ASSESSABLE per requirement, and
NOT_ASSESSABLE is the MAJORITY answer by design. A gate that reported these as MET would be the exact defect
the method exists to remove, committed by the thing meant to prevent it.

  (a) THE REGISTER   — docs/DELIVERY_METHOD.json, served here. Every lesson carries the DEFECT that produced
                       it, the rule, how to apply it, and `enforced_by`: a real tool path, or null with the
                       reason none exists.
  (b) THE DERIVATION — POST /derive turns a register row into a CANDIDATE lesson. A candidate is NOT a lesson:
                       it is submitted to Change Control, so the method amends itself only through the agency
                       that holds it.
  (c) THE GATE       — check_change() is applied by Change Control to every submission, from the repo's own
                       artefacts and never from what the submitter claims.
  (d) THE SURFACE    — the Governance hub reads these routes; each change record carries its method check.
"""
from __future__ import annotations

import json
import re
import time
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from agentic_core.auth.core import get_current_user

router = APIRouter(prefix="/method", tags=["Delivery Method"])

_METHOD_DOC = "docs/DELIVERY_METHOD.json"

# The three states a method requirement may return. NOT_ASSESSABLE is not a failure and not a pass: it is the
# statement that this platform cannot tell from what it holds, which for most of the method is the truth.
MET = "MET"
UNMET = "UNMET"
NOT_ASSESSABLE = "NOT_ASSESSABLE"


def _repo_root():
    from pathlib import Path
    return Path(__file__).resolve().parents[2]


def _load_method() -> Dict[str, Any]:
    """The method, WHOLE, or a refusal. Never a partial method presented as the method.

    Strict on purpose: a method register read as `{}` would make every requirement vacuously satisfiable, and
    a gate over an empty method is worse than no gate because it reports a verdict.
    """
    p = _repo_root() / _METHOD_DOC
    if not p.exists():
        raise HTTPException(status_code=503,
                            detail=f"{_METHOD_DOC} is not present, so no method check can be made. Nothing "
                                   f"is reported as compliant in its absence.")
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        raise HTTPException(status_code=503,
                            detail=f"{_METHOD_DOC} could not be read whole ({e.__class__.__name__}: {e}); no "
                                   f"method check is made and nothing is reported as compliant.") from e
    if not isinstance(d.get("lessons"), list) or not isinstance(d.get("mechanisms"), list):
        raise HTTPException(status_code=503,
                            detail=f"{_METHOD_DOC} does not hold a lessons and mechanisms list; refusing to "
                                   f"check a change against a method it cannot read.")
    return d


def _enforcement_summary(lessons: List[Dict[str, Any]]) -> Dict[str, Any]:
    """How much of the method a tool can actually catch — stated, not implied.

    This figure is the honest headline of the whole module: most of the method is judgement, and a reader who
    is not told that will take a method check for a compliance verdict.
    """
    enforced = [l for l in lessons if (l.get("enforced_by") or "").strip()]
    return {
        "lessons_total": len(lessons),
        "mechanically_enforced": len(enforced),
        "judgement_only": len(lessons) - len(enforced),
        "share_enforced": round(len(enforced) / len(lessons), 3) if lessons else None,
        "basis": ("`enforced_by` names a real tool or guard path that would CATCH a breach. The rest are "
                  "judgement a change record cannot expose, and each says why no tool covers it. A method "
                  "check therefore answers NOT_ASSESSABLE for most requirements, which is the honest answer "
                  "and not a gap in the check."),
    }


@router.get("")
async def get_method(group: Optional[str] = None, user: dict | None = Depends(get_current_user)):
    """The delivery method: every lesson with the defect that produced it, and what enforces it."""
    d = _load_method()
    lessons = d["lessons"]
    if group:
        lessons = [l for l in lessons if l.get("group") == group]
        if not lessons:
            raise HTTPException(status_code=404,
                                detail=f"No lessons in group '{group}'. Groups: {d['about'].get('groups')}")
    # W509 — join the operational breach ledger in at READ time. A lesson breached after it was written is a
    # mechanism failure (M-LEARN-02), and a reader of the method must see which of its rules are failing.
    _counts = breach_counts()
    lessons = [dict(l, breaches_recorded=_counts.get(l.get("id"), 0)) for l in lessons]
    return {
        "about": d["about"],
        "groups": d["about"].get("groups", []),
        "breaches": {"counted_from": "data/method_breaches.json (operational; not part of the document)",
                     "total_recorded": sum(_counts.values()),
                     "lessons_with_a_recorded_breach": len(_counts),
                     "zero_is_not_none": ("nothing observes a breach, so a count of zero means none has been "
                                          "RECORDED - never that a rule has not been broken")},
        "lessons": lessons,
        "mechanisms": d["mechanisms"] if not group else
                      [m for m in d["mechanisms"] if m.get("group") == group],
        "enforcement": _enforcement_summary(d["lessons"]),
        "amended_by": ("Change Control only. POST /api/v1/method/derive proposes a CANDIDATE; the agency "
                       "ratifies it. The agency that checks changes against the method also owns it."),
    }


@router.get("/lessons/{lesson_id}")
async def get_lesson(lesson_id: str, user: dict | None = Depends(get_current_user)):
    """One lesson, with the defect behind it. A rule with no defect behind it is an opinion."""
    d = _load_method()
    for l in d["lessons"]:
        if l.get("id") == lesson_id:
            return l
    raise HTTPException(status_code=404, detail=f"No lesson {lesson_id} in the method register.")


# ── (b) THE DERIVATION MECHANISM ───────────────────────────────────────────────────────────────────────────

class DeriveRequest(BaseModel):
    row_id: str                                  # a docs/FOLLOWUPS.json row, e.g. "FU-239"
    defect_class: str                            # what class the round judged it to be
    proposed_rule: Optional[str] = None          # the imperative, if the proposer has one
    proposed_group: Optional[str] = None
    submit_to_change_control: bool = True


def _followup_row(row_id: str) -> Dict[str, Any]:
    p = _repo_root() / "docs/FOLLOWUPS.json"
    if not p.exists():
        raise HTTPException(status_code=503, detail="docs/FOLLOWUPS.json is not present.")
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        raise HTTPException(status_code=503, detail=f"the register could not be read whole ({e}).") from e
    for it in d.get("items", []):
        if it.get("id") == row_id:
            return it
    raise HTTPException(status_code=404, detail=f"No register row {row_id}.")


@router.post("/derive")
async def derive_lesson(req: DeriveRequest, user: dict | None = Depends(get_current_user)):
    """Turn a CONFIRMED DEFECT into a candidate lesson, by a stated rule rather than by remembering.

    A CANDIDATE IS NOT A LESSON. It is submitted to Change Control, because the method may only be amended
    through the agency that holds it — otherwise whoever happened to close a row could rewrite the discipline
    everything else is checked against.

    The derivation is deliberately mechanical and deliberately incomplete: it carries the row's own measured
    text across as the DEFECT, and leaves the RULE to the proposer. A rule this code invented from a row's
    title would be a sentence nobody had thought about, which is the shape of defect the method warns of.
    """
    row = _followup_row(req.row_id)
    d = _load_method()
    groups = d["about"].get("groups", [])
    group = req.proposed_group or "verification"
    if group not in groups:
        raise HTTPException(status_code=400, detail=f"group must be one of {groups}")

    if str(row.get("status")) != "done":
        # a lesson derived from an open row is derived from something that may yet turn out to be false —
        # W507 dropped two rows as factually wrong, and a lesson from either would have been fiction
        raise HTTPException(
            status_code=400,
            detail=(f"{req.row_id} is '{row.get('status')}', not 'done'. A lesson is derived from a CONFIRMED "
                    f"defect: an open row may still be refuted, and two rows were dropped as factually wrong "
                    f"in W507. Close the row first."))

    candidate = {
        "id": f"CANDIDATE-{req.row_id}",
        "group": group,
        "rule": (req.proposed_rule or "").strip() or None,
        "defect": (f"{req.row_id}: {row.get('title', '')}. "
                   f"{str(row.get('why', ''))[:1200]}").strip(),
        "defect_class": req.defect_class,
        "derived_from": {"row_id": req.row_id, "source": row.get("source"), "slot": row.get("slot"),
                         "severity": row.get("severity")},
        "apply": None,
        "enforced_by": None,
        "why_not_enforced": "not yet assessed — a proposer must name a tool that would catch this, or say none does",
        "state": "CANDIDATE",
        "not_yet": ("this is NOT part of the method. It becomes one only if Change Control ratifies it, and "
                    "it must carry a rule and an apply before it can be ratified."),
        "derived_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    incomplete = [k for k in ("rule",) if not candidate.get(k)]
    candidate["incomplete"] = incomplete or None

    submitted: Dict[str, Any] = {"submitted": False,
                                 "why": "submit_to_change_control was false; the candidate is returned only"}
    if req.submit_to_change_control:
        try:
            from agentic_core.api.change_control import SubmitChangeRequest, submit_change
            cca = await submit_change(SubmitChangeRequest(
                title=f"Method amendment from {req.row_id}: {str(row.get('title',''))[:70]}",
                change_type="config_minor",
                description=(f"A candidate delivery-method lesson derived from confirmed defect {req.row_id} "
                             f"(class: {req.defect_class}). Candidate rule: "
                             f"{candidate['rule'] or 'NOT STATED — must be supplied before ratification'}."),
                rationale=("The method is amended only through the arms-length agency that holds it, so a "
                           "lesson cannot enter the discipline without a change record."),
                affected_systems=["delivery_method", "change_control"],
                submitted_by="method_derivation",
            ))
            submitted = {"submitted": True, "cca_id": cca.get("cca_id"), "status": cca.get("status")}
        except Exception as e:                       # noqa: BLE001 — recorded, never swallowed silently
            submitted = {"submitted": False, "why": f"{e.__class__.__name__}: {e}"}

    return {"candidate": candidate, "change_control": submitted,
            "rule": ("a candidate becomes a lesson only when Change Control ratifies it AND it carries a "
                     "rule, an apply, and either an enforcer or a stated reason none exists")}


# ── (c) THE GATE, ARMS-LENGTH ──────────────────────────────────────────────────────────────────────────────
#
# Every requirement below is evaluated from the REPO'S OWN ARTEFACTS — the change record, the register, the
# tree — and never from what the submitter says about itself. A submitter claiming to have run a blind sweep
# is a claim; a guard file containing the blind is an artefact.

def _req(rid: str, lesson: str, state: str, basis: str, **extra) -> Dict[str, Any]:
    return {"requirement": rid, "lesson": lesson, "state": state, "basis": basis, **extra}


def check_change(change: Dict[str, Any]) -> Dict[str, Any]:
    """Check one Change Control submission against the method. Three states, each with a basis.

    WHAT THIS CAN AND CANNOT SEE, stated on the result rather than left to be discovered: a change record
    holds a title, a type, a description, a rationale, affected systems and a submitter. It does NOT hold
    whether a blind was added, whether a refutation ran, whether a basis string was computed, or whether every
    writer of a changed field was found. Those are the METHOD'S SUBSTANCE and they return NOT_ASSESSABLE.

    A change may not be auto-approved while a mechanically-checkable requirement is UNMET. Nothing here
    blocks a change for a NOT_ASSESSABLE requirement, because that would block every change.
    """
    reqs: List[Dict[str, Any]] = []
    try:
        method = _load_method()
    except HTTPException as e:
        return {"method_available": False, "requirements": [], "may_auto_approve": False,
                "summary": f"no method check was made: {e.detail}",
                "why_not_approvable": ("the method could not be read, so this change is not reported as "
                                       "checked; refusing is the honest state, not passing")}

    lessons = {l["id"]: l for l in method["lessons"]}

    # ── mechanically checkable from the record itself ──────────────────────────────────────────────────
    rationale = str(change.get("rationale") or "").strip()
    reqs.append(_req(
        "states-a-rationale", "M-DELIV-01",
        MET if len(rationale) >= 20 else UNMET,
        (f"the record carries a rationale of {len(rationale)} characters" if len(rationale) >= 20 else
         "the record carries no rationale of substance, so what this change is FOR is not recorded"),
        checkable_from="the change record"))

    systems = change.get("affected_systems") or []
    reqs.append(_req(
        "names-what-it-touches", "M-EXEC-03",
        MET if isinstance(systems, list) and systems else UNMET,
        (f"names {len(systems)} affected system(s): {', '.join(map(str, systems[:6]))}" if systems else
         "names no affected system, so the writers and readers it reaches cannot be reviewed"),
        checkable_from="the change record"))

    # a decision must name the MECHANISM that decided, not the caller who asked — W464
    src = str(change.get("decision_source") or "").strip()
    decided = str(change.get("decision") or "").strip()
    reqs.append(_req(
        "a-decision-names-its-mechanism", "M-DELIV-01",
        (NOT_ASSESSABLE if not decided else (MET if src else UNMET)),
        ("no decision has been taken yet, so there is no decider to name" if not decided else
         (f"the decision '{decided}' names its mechanism: {src}" if src else
          f"the decision '{decided}' names no deciding mechanism, so the record cannot say what decided it")),
        checkable_from="the change record"))

    # ── checkable from the REGISTER: found-but-not-done work must be written down (M-EXEC-06) ──────────
    try:
        reg = json.loads((_repo_root() / "docs/FOLLOWUPS.json").read_text(encoding="utf-8"))
        open_rows = [i for i in reg.get("items", []) if i.get("status") == "open"]
        orphans = [i["id"] for i in open_rows if not str(i.get("slot") or "").strip()]
        reqs.append(_req(
            "every-open-row-rides-an-item", "M-EXEC-06",
            MET if not orphans else UNMET,
            (f"all {len(open_rows)} open rows ride a plan item" if not orphans else
             f"these open rows ride no item and will not be scheduled: {orphans[:8]}"),
            checkable_from="docs/FOLLOWUPS.json"))
    except Exception as e:                           # noqa: BLE001
        reqs.append(_req("every-open-row-rides-an-item", "M-EXEC-06", NOT_ASSESSABLE,
                         f"the register could not be read ({e.__class__.__name__}: {e})",
                         checkable_from="docs/FOLLOWUPS.json"))

    # ── THE SUBSTANCE OF THE METHOD, which a change record cannot expose ──────────────────────────────
    # These are the requirements that matter most and the ones this gate cannot judge. Listing them as
    # NOT_ASSESSABLE is the whole point: a reader must see what was NOT checked, or a passing gate reads as
    # a compliance verdict over the very things nobody evaluated.
    for lid in ("M-VERIF-01", "M-VERIF-02", "M-VERIF-05", "M-VERIF-06", "M-MEAS-01", "M-MEAS-02",
                "M-EXEC-01", "M-EXEC-02", "M-DELIV-03"):
            l = lessons.get(lid)
            if not l:
                continue
            reqs.append(_req(
                lid.lower(), lid, NOT_ASSESSABLE,
                (f"{l['rule']} — NOT VISIBLE in a change record. "
                 f"{l.get('why_not_enforced') or 'no artefact exposes it'}"),
                checkable_from=None))

    unmet = [r for r in reqs if r["state"] == UNMET]
    not_assessable = [r for r in reqs if r["state"] == NOT_ASSESSABLE]
    met = [r for r in reqs if r["state"] == MET]
    return {
        "method_available": True,
        "checked_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "requirements": reqs,
        "counts": {"met": len(met), "unmet": len(unmet), "not_assessable": len(not_assessable)},
        # A change may not be auto-approved while a MECHANICALLY CHECKABLE requirement is UNMET.
        "may_auto_approve": not unmet,
        "why_not_approvable": (None if not unmet else
                               f"{len(unmet)} mechanically-checkable requirement(s) are UNMET: "
                               + "; ".join(r["requirement"] for r in unmet)),
        # the limit, on the result — not in a docstring, not in a log
        "limits": ("this check reads the change record, the register and the tree. It CANNOT see whether a "
                   f"blind was added, whether a refutation ran, whether a basis string was computed rather "
                   f"than asserted, or whether every writer of a changed field was found — "
                   f"{len(not_assessable)} of {len(reqs)} requirements are NOT ASSESSABLE for that reason. "
                   f"A green result here is NOT a statement that this change follows the method."),
        "never": ("no requirement is reported MET because the submitter said so; every MET above was read "
                  "from an artefact"),
    }


class CheckRequest(BaseModel):
    cca_id: Optional[str] = None
    change: Optional[Dict[str, Any]] = None


@router.post("/check")
async def check_a_change(req: CheckRequest, user: dict | None = Depends(get_current_user)):
    """Check a change against the method — by cca_id (read from the store) or on a supplied record."""
    change = req.change
    if req.cca_id:
        from agentic_core.api.change_control import _load_change
        change = _load_change(req.cca_id)
        if change is None:
            raise HTTPException(status_code=404, detail=f"No change record {req.cca_id}.")
    if not isinstance(change, dict):
        raise HTTPException(status_code=400, detail="supply either cca_id or change")
    return {"cca_id": req.cca_id, "method_check": check_change(change)}


# ── THE METHOD APPLIED TO THE PLATFORM'S OWN WORK (W508, P2.10 — the weaving) ──────────────────────────────
#
# A register the platform merely SERVES is a document. A register the platform checks its own delivery against
# is the learning made operative, which is what the Owner asked for. Four lessons are properties of a
# cascade's own output and are therefore genuinely checkable here; the rest stay NOT_ASSESSABLE, exactly as at
# the change gate, because a cascade's output cannot show whether a blind was added.

# a stage whose `checks` kind cannot fail must never be reported verified — this module's own stage() helper
# documents `presence` as "CANNOT fail: never 'verified'"
_CANNOT_FAIL = ("presence", "none")


def check_cascade(cascade: List[Dict[str, Any]], validation: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Check a transformation cascade's OWN OUTPUT against the method. Three states, each with a basis.

    Reads the artefact the cascade produced — its stages and its validation figure — and never a claim about
    them. Returns the same shape as `check_change` so one surface can render either.
    """
    reqs: List[Dict[str, Any]] = []
    v = validation or {}
    stages = [s for s in (cascade or []) if isinstance(s, dict)]

    if not stages:
        # W508 — the SAME SHAPE as the normal return. The first version answered with the change gate's keys
        # (`may_auto_approve`, `why_not_approvable`), so a caller reading this function's own contract got a
        # KeyError on the one branch that means "nothing was checked" — the sibling-return defect the
        # mechanical pre-flight exists to catch, committed inside the module that holds the method.
        return {"method_available": True, "checked_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "requirements": [], "counts": {"met": 0, "unmet": 0, "not_assessable": 0},
                "follows_the_method_where_checkable": False,
                "why_not": "no stages were supplied, so nothing about this run was checked",
                "limits": ("an empty cascade is not a run that followed the method; it is a run with nothing "
                           "to check, and those are different statements")}

    # ── M-VERIF-10 · three-state verdicts, each with a basis ──────────────────────────────────────────
    bad_state = [st.get("step") for st in stages
                 if st.get("verified") not in (True, False, None)]
    no_basis = [st.get("step") for st in stages if not str(st.get("basis") or "").strip()]
    reqs.append(_req(
        "three-state-verdicts", "M-VERIF-10",
        MET if not bad_state and not no_basis else UNMET,
        ("every stage carries a True/False/None verdict and a basis saying what it rests on"
         if not bad_state and not no_basis else
         f"stages with a non-three-state verdict: {bad_state or 'none'}; stages with no basis: "
         f"{no_basis or 'none'} — a verdict with no basis cannot be read"),
        checkable_from="the cascade's own stages"))

    # ── M-VERIF-01 · a check that CANNOT fail must not report success ──────────────────────────────────
    cannot_fail_but_verified = [st.get("step") for st in stages
                               if st.get("checks") in _CANNOT_FAIL and st.get("verified") is True]
    reqs.append(_req(
        "a-check-that-cannot-fail-reports-nothing", "M-VERIF-01",
        MET if not cannot_fail_but_verified else UNMET,
        ("no stage reports success for a check that cannot fail"
         if not cannot_fail_but_verified else
         f"stage(s) {cannot_fail_but_verified} report verified=True for a '{_CANNOT_FAIL[0]}'-class check, "
         f"which this module documents as unable to fail — a check that cannot fail reporting success is the "
         f"W498-W500 class"),
        checkable_from="the cascade's own stages"))

    # ── M-MEAS-03 · the figure states its population ──────────────────────────────────────────────────
    assessable = v.get("assessable_stages")
    verified_n = v.get("verified_stages")
    denom_ok = isinstance(assessable, int) and assessable != len(stages) or assessable == len([
        st for st in stages if st.get("verified") is not None])
    reqs.append(_req(
        "a-count-states-its-population", "M-MEAS-03",
        (MET if isinstance(assessable, int) and isinstance(verified_n, int) and denom_ok else
         (NOT_ASSESSABLE if assessable is None else UNMET)),
        (f"the figure is {verified_n} of {assessable} ASSESSABLE stages, out of {len(stages)} run — the "
         f"denominator is what could be assessed, not what exists"
         if isinstance(assessable, int) and denom_ok else
         ("the validation figure does not state an assessable denominator, so a reader cannot tell what the "
          "ratio covers" if assessable is None else
          f"the denominator {assessable} equals the stage count {len(stages)}, so unassessable stages are "
          f"being counted as assessable")),
        checkable_from="the cascade's validation figure"))

    # ── M-DELIV-01 · a stage where a REAL check was expected and produced no verdict ──────────────────
    #
    # THE FIRST VERSION OF THIS LEG WAS ITSELF THE DEFECT, and its first run against the live cascade proved
    # it: it searched each basis for the phrases "not assessable" or "not run" and flagged three stages whose
    # bases DID explain themselves, in different words ("presence only: the Owner's Board always resolves a
    # Chief, so this check cannot fail"). A word list over prose is not a check — M-VERIF-03 — and this one
    # accused working code, which M-EXEC-01 warns of. Replaced with a condition read from FIELDS:
    #
    #   a `presence`/`none` stage returning None is correct BY CONSTRUCTION — those kinds cannot produce a
    #   verdict, and the basis requirement above already forces it to say something;
    #   a `delivery`/`decision`/`artifact` stage returning None means a check that COULD have produced a
    #   verdict produced none, which is the case a reader needs pointed out.
    _REAL_CHECK_KINDS = ("delivery", "decision", "artifact")
    expected_but_absent = [st.get("step") for st in stages
                           if st.get("verified") is None and st.get("checks") in _REAL_CHECK_KINDS]
    reqs.append(_req(
        # W508 — RENAMED to what it actually checks. It was "a-real-check-that-produced-no-verdict-is-
        # named", which reads as satisfied by naming such a stage, while the condition is that no such
        # stage exists. A requirement whose name and condition disagree misreports its own verdict.
        "every-real-check-produced-a-verdict", "M-DELIV-01",
        MET if not expected_but_absent else UNMET,
        ("no stage declaring a real check (delivery, decision or artifact) came back without a verdict"
         if not expected_but_absent else
         f"stage(s) {expected_but_absent} declare a real check kind and produced NO verdict — a check that "
         f"could have decided and did not is the case a reader most needs named, and their bases carry the "
         f"reason"),
        checkable_from="the cascade's own stages (the checks kind and the verdict, not the prose)"))

    # ── and the substance of the method, which a cascade's output cannot expose ───────────────────────
    for lid, why in (("M-VERIF-06", "whether this round's own fixes were refuted"),
                     ("M-VERIF-05", "whether each basis string was computed from state or asserted"),
                     ("M-EXEC-03", "whether every writer of a changed field was found")):
        reqs.append(_req(lid.lower(), lid, NOT_ASSESSABLE,
                         f"NOT VISIBLE in a cascade's output: {why}", checkable_from=None))

    unmet = [r for r in reqs if r["state"] == UNMET]
    na = [r for r in reqs if r["state"] == NOT_ASSESSABLE]
    return {
        "method_available": True,
        "checked_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "requirements": reqs,
        "counts": {"met": len([r for r in reqs if r["state"] == MET]), "unmet": len(unmet),
                   "not_assessable": len(na)},
        "follows_the_method_where_checkable": not unmet,
        "why_not": (None if not unmet else
                    "; ".join(f"{r['requirement']}: {r['basis']}" for r in unmet)),
        "limits": (f"{len(na)} of {len(reqs)} requirements are NOT ASSESSABLE from a cascade's output. A "
                   f"clean result here says this run's OWN ARTEFACT is consistent with the four method rules "
                   f"a cascade can be checked against — it is not a statement that the round followed the "
                   f"method."),
    }


class CascadeCheckRequest(BaseModel):
    cascade: List[Dict[str, Any]]
    validation: Optional[Dict[str, Any]] = None


@router.post("/check-cascade")
async def check_a_cascade(req: CascadeCheckRequest, user: dict | None = Depends(get_current_user)):
    """Check a transformation cascade's own output against the method. Used by the Transformation Office."""
    return {"method_check": check_cascade(req.cascade, req.validation)}


# ── HANDOVER (W509) — what survives a context, counted from the artefacts that hold it ─────────────────────

def _plan_block(name: str) -> str:
    """One generated block of the plan, verbatim. Returns "" when absent rather than inventing a summary."""
    try:
        text = (_repo_root() / "docs/FABLE_DELIVERY_PROMPT.md").read_text(encoding="utf-8")
    except OSError:
        return ""
    start = text.find(f"<!-- {name}:begin")
    end = text.find(f"<!-- {name}:end", start + 1) if start >= 0 else -1
    return text[start:end].strip() if start >= 0 and end > start else ""


def _items_without_a_bar() -> Dict[str, Any]:
    """Which plan items state NO acceptance criteria — the state that makes an item unclosable.

    This is the largest structural blocker this programme has measured: W505 found 17 of 48 open build items
    stating none, which is why no P2 item had closed in 48 rounds while rows kept closing. Counted here rather
    than remembered, because the figure ages: six of that seventeen had been barred within two rounds.
    """
    try:
        text = (_repo_root() / "docs/FABLE_DELIVERY_PROMPT.md").read_text(encoding="utf-8")
    except OSError as e:
        # W509 — the SAME SHAPE as the answer below. A refusal that omits the answer's keys makes every
        # reader raise KeyError exactly when the plan is already unreadable, which is the shape that broke a
        # guard in W508: sibling returns share a key set, and `unavailable` is ADDED, not substituted.
        return {"items_with_no_acceptance_bar": None,
                "counts": {"done": None, "barred": None, "no_bar": None},
                "why_it_matters": "not measured: the plan could not be read",
                "what_to_do": "read the plan before concluding anything about which items can close",
                "unavailable": f"the plan could not be read ({e.__class__.__name__}: {e})"}
    heads = list(re.finditer(r"(?m)^ (P[1-5]\.\d+)(?: \u2705 DONE \S+)? ", text))
    no_bar, barred, done = [], [], []
    for i, m in enumerate(heads):
        slot = m.group(1)
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        body = text[m.start():end]
        if "DONE" in body[:60]:
            done.append(slot)
        elif "ACCEPT" in body or "GUARD:" in body:
            barred.append(slot)
        else:
            no_bar.append(slot)
    return {
        "items_with_no_acceptance_bar": no_bar,
        "counts": {"done": len(done), "barred": len(barred), "no_bar": len(no_bar)},
        "why_it_matters": ("an item closes on its ACCEPT criteria. An item stating none cannot be closed "
                          "however much is built - nothing has been forgotten, there is nothing to check it "
                          "against. This is the measured reason no Phase 2 item closed in 48 rounds."),
        "what_to_do": ("an item whose body lists deliverables does not need a bar invented: the deliverables "
                       "ARE the bar, and writing them as ACCEPT is transcription plus a guard"),
        "unavailable": None,
    }


@router.get("/handover")
async def handover(user: dict | None = Depends(get_current_user)):
    """The state a successor needs, computed from the artefacts that outlive a working context.

    A conversation does not survive; docs/FOLLOWUPS.json, the plan and docs/DELIVERY_METHOD.json do. So this
    counts what they hold rather than narrating what was done.
    """
    method = _load_method()
    out: Dict[str, Any] = {
        "read_from": ["docs/FOLLOWUPS.json", "docs/FABLE_DELIVERY_PROMPT.md", "docs/DELIVERY_METHOD.json"],
        "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    # ── the register: open work, and what awaits a DECISION rather than a build ───────────────────────
    try:
        reg = json.loads((_repo_root() / "docs/FOLLOWUPS.json").read_text(encoding="utf-8"))
        items = reg.get("items", [])
        open_rows = [i for i in items if i.get("status") == "open"]
        by_item: Dict[str, int] = {}
        for r in open_rows:
            by_item[str(r.get("slot") or "(unslotted)")] = by_item.get(str(r.get("slot") or "(unslotted)"), 0) + 1
        awaiting = [{"id": r["id"], "title": r.get("title"),
                     "why_it_is_the_owners": r.get("slot_source") or "no reason recorded, which is itself a gap"}
                    for r in open_rows if r.get("owner_gated") or r.get("slot") == "OWNER"]
        out["register"] = {
            "open": len(open_rows),
            "open_by_item": dict(sorted(by_item.items())),
            "awaiting_an_owner_decision": awaiting,
            "unslotted": [r["id"] for r in open_rows if not str(r.get("slot") or "").strip()],
            "done": sum(1 for i in items if i.get("status") == "done"),
            "dropped": sum(1 for i in items if i.get("status") == "dropped"),
            "note": ("a dropped row is one measured and REFUTED, not one abandoned - two were dropped in W507 "
                     "because the code they accused did not do what they claimed"),
        }
    except Exception as e:                           # noqa: BLE001 — said, never a zero
        out["register"] = {"unavailable": f"{e.__class__.__name__}: {e}",
                           "note": "this is not a statement that there is no open work"}

    # ── the plan: what cannot be closed, and the plan's own pace with its own caveat ──────────────────
    out["unclosable_items"] = _items_without_a_bar()
    out["pace_verbatim"] = _plan_block("pace") or "the plan's pace block could not be read"
    out["plan_state_verbatim"] = _plan_block("plannow") or "the plan's state block could not be read"

    # ── the method: what no tool catches, so a successor does not assume the tooling covers it ────────
    enf = _enforcement_summary(method["lessons"])
    out["method"] = {
        **enf,
        "judgement_only_lessons": [{"id": l["id"], "rule": l["rule"], "why_no_tool": l.get("why_not_enforced")}
                                   for l in method["lessons"] if not (l.get("enforced_by") or "").strip()],
        "mechanism_limits": [{"id": m["id"], "name": m.get("name"), "known_limit": m.get("known_limit")}
                             for m in method["mechanisms"]],
    }

    out["limits"] = (
        "This counts what the artefacts HOLD. It cannot tell that something was never written down: an "
        "unrecorded decision, an unregistered finding or an unstated caveat is invisible to it by "
        "construction. That is why M-HAND-01 is a rule rather than a report - and a successor treating this "
        "as a complete picture has made the mistake it warns about.")
    return out


# ── (e) THE DEFECT CLASSES (W509) — shapes a screen can look for, not rules an operator follows ────────────

class ScreenRequest(BaseModel):
    paths: List[str]                             # repo-relative files the change touches
    classes: Optional[List[str]] = None          # limit to these class ids; default every screenable one


# Each shape is a regex over one line, plus the classes that are NOT screenable and why. A shape is written to
# be FINDABLE, not to be conclusive: `max(` over a mapping is the ordinary way to write a correct maximum too.
_SHAPES: Dict[str, List[tuple]] = {
    "D-SELECT": [
        # FU-317 (W517) - a CLAMP is excluded by the class's own definition, not by taste. `max(0.0, x)`
        # is a maximum over two SCALARS, which is not a selection over a collection; 106 of 224 candidates
        # in agentic_core were clamps, so the screen spent more than half its report on shapes its own
        # stated domain excludes. The negative lookahead drops a first argument that is a numeric literal.
        (r"\b(?:max|min)\s*\(\s*(?!-?\d+(?:\.\d+)?\s*,)",
         "a maximum or minimum taken over a collection (a clamp over a numeric literal is excluded: it is "
         "a maximum over two scalars, which this class does not cover)"),
        (r"(?:sorted\s*\(|\.sort\s*\()[^\n]*\)\s*\[\s*0\s*\]", "a sort followed by taking the first"),
        (r"\.sort\s*\([^\n]*\)[^\n]*\[\s*0\s*\]", "an in-place sort then the first element"),
    ],
    "D-THEATRE": [
        (r"Math\.random\s*\(", "a random value produced on a path a user sees"),
        (r"setTimeout\s*\([^\n]*\d{3,}", "a delay long enough to stand in for work"),
    ],
    "D-BEARER": [
        (r"<a\s[^\n]*href=\{[^\n]*(?:preview|/api/)", "a raw anchor to an API route"),
        (r"window\.open\s*\([^\n]*/api/", "a new-tab navigation to an API route"),
    ],
}
_NOT_SCREENABLE = {
    "D-FABRICATE": ("what a reader would take as measured is a judgement about the reader, not a shape in the "
                    "source. Its own sweep needed a five-area pass and an adversarial defence round."),
    "D-CONTRACT": ("it is found by a method-aware diff of every call site against every handler's method+route "
                   "pair, which is a whole-tree measurement and not a per-file screen."),
    "D-SILENT": ("an empty catch is only a defect when the action was user-visible, and whether a failure "
                 "reaches the user cannot be read from the line the catch sits on."),
}


def _method_classes() -> List[Dict[str, Any]]:
    """The classes from the register, or a refusal — never an empty list read as 'no classes'."""
    d = _load_method()
    classes = d.get("defect_classes")
    if not isinstance(classes, list) or not classes:
        raise HTTPException(status_code=503,
                            detail=f"{_METHOD_DOC} holds no defect_classes, so no shape screen can be made. "
                                   f"Nothing is reported as clear in their absence.")
    return classes


def screen_for_defect_shapes(paths: List[str], only: Optional[List[str]] = None) -> Dict[str, Any]:
    """Screen the given files for the mechanically-findable shapes. Reports CANDIDATES, never verdicts."""
    classes = _method_classes()
    by_id = {c["id"]: c for c in classes}
    wanted = [c for c in _SHAPES if (only is None or c in only)]
    root = _repo_root()

    read, unread = [], []
    texts: Dict[str, List[str]] = {}
    for rel in paths:
        p = (root / rel).resolve()
        try:
            p.relative_to(root.resolve())
        except ValueError:
            unread.append({"path": rel, "why": "outside the repository; not read"})
            continue
        try:
            texts[rel] = p.read_text(encoding="utf-8", errors="replace").splitlines()
            read.append(rel)
        except OSError as e:
            unread.append({"path": rel, "why": f"{e.__class__.__name__}: {e}"})

    candidates: List[Dict[str, Any]] = []
    for cid in wanted:
        for pattern, what in _SHAPES[cid]:
            rx = re.compile(pattern)
            for rel in read:
                for n, line in enumerate(texts[rel], 1):
                    if rx.search(line):
                        candidates.append({"defect_class": cid, "path": rel, "line": n,
                                           "shape": what, "source": line.strip()[:200]})

    screened = {cid: sum(1 for c in candidates if c["defect_class"] == cid) for cid in wanted}
    return {
        "screened_paths": read,
        "paths_not_read": unread,
        "population": (f"{len(read)} of {len(paths)} paths given, screened for "
                       f"{len(wanted)} of {len(classes)} classes"),
        "candidates": candidates,
        "candidates_by_class": screened,
        "classes_not_screenable": [{"defect_class": cid, "why": why, "state": NOT_ASSESSABLE}
                                   for cid, why in _NOT_SCREENABLE.items()
                                   if only is None or cid in only],
        "what_a_candidate_is": ("a shape occurring at a line, NOT a defect. `max(` over a collection is also "
                               "how a correct maximum is written. Each candidate is adjudicated against the "
                               "class's own exclusions, and a defended candidate is recorded as defended "
                               "rather than deleted \u2014 " + _defended_share() + " (M-VERIF-12)."),
        "what_no_candidate_is_not": ("finding no candidate of a shape is not a statement that the class is "
                                     "absent. Three of the six classes are not screenable at all, and the "
                                     "screened three are screened only in the paths listed above."),
        "adjudicated_by": [{"defect_class": cid, "not_this_class": by_id[cid].get("not_this_class")}
                           for cid in wanted if by_id.get(cid, {}).get("not_this_class")],
    }


@router.get("/defect-classes")
async def get_defect_classes(user: dict | None = Depends(get_current_user)):
    """The defect classes distilled from this repository's own ledgers, and which of them a screen can find."""
    classes = _method_classes()
    return {
        "about": _load_method()["about"].get("what_defect_classes_are"),
        "defect_classes": classes,
        "screenable": sorted(_SHAPES),
        "not_screenable": [{"defect_class": cid, "why": why} for cid, why in _NOT_SCREENABLE.items()],
        "basis": (f"{len(_SHAPES)} of {len(classes)} classes carry a shape a per-file screen can find. The "
                  f"rest need a whole-tree measurement or a judgement, and are reported NOT_ASSESSABLE rather "
                  f"than clear."),
        "screen_with": "POST /api/v1/method/screen",
    }



def _defended_share() -> str:
    """The proposed/defended counts, READ FROM THE LEDGER at call time.

    FU-305 (W515) — this sentence used to carry the two numbers as literals, nine lines below a figure the
    same dict computes with len(). A count stated in prose is not a count: it does not move when the thing it
    describes moves. It is parsed from the ledger's own header instead, and when that cannot be parsed the
    answer says so rather than falling back to the literals this change removed.
    """
    try:
        text = (_repo_root() / "docs/FABRICATION_LEDGER.md").read_text(encoding="utf-8")
    except Exception as exc:                                  # noqa: BLE001 — said, never substituted
        return f"the defended share is NOT ASSESSABLE: the ledger could not be read ({exc.__class__.__name__})"
    m = re.search(r"(\d+)\s+proposed,\s*(\d+)\s+successfully defended", text)
    if not m:
        return ("the defended share is NOT ASSESSABLE: docs/FABRICATION_LEDGER.md holds no parseable "
                "'N proposed, M successfully defended' header")
    proposed, defended = int(m.group(1)), int(m.group(2))
    return (f"{defended} of {proposed} proposals were defended on exactly these grounds in this repository's "
            f"own fabrication sweep, read live from docs/FABRICATION_LEDGER.md")

@router.post("/screen")
async def screen_a_change(req: ScreenRequest, user: dict | None = Depends(get_current_user)):
    """Screen a change's own files for the findable shapes. The agency adjudicates; this only finds."""
    if not req.paths:
        raise HTTPException(status_code=400,
                            detail="No paths given. A screen over nothing would report no candidates, which "
                                   "reads as clear.")
    return screen_for_defect_shapes(req.paths, req.classes)


# ── (f) FORECASTING (W509) — the one forecaster, plus what arithmetic cannot know ───────────────────────────

# The items the Owner's rulings hold behind other items. A schedule ordered purely by priority would work an
# item that cannot complete (M-FCAST-05), so the gate is stated rather than rediscovered. Read from the plan's
# own ruling text where it can be, and named here where the plan states it in prose.
_BLOCKED_BY_RULING = {
    "P2.11": "P3.12-P3.19", "P2.12": "P3.12-P3.19", "P2.13": "P3.12-P3.19",
    "P2.14": "P3.12-P3.19", "P2.15": "P3.12-P3.19", "P2.16": "P3.12-P3.19",
}


def _register_overstatement() -> Dict[str, Any]:
    """How wrong the open-row count has been measured to be, from the rows themselves.

    M-FCAST-02: a row may be false, or already satisfied. Both are counted here from the register's own
    `status` and closing round, so the figure moves as rounds close rather than being remembered.
    """
    try:
        reg = json.loads((_repo_root() / "docs/FOLLOWUPS.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        # W509 — the same shape as the answer below, for the same reason.
        return {"open": None, "dropped_as_refuted": None, "dropped_ids": None,
                "why_it_is_an_upper_bound": "not measured: the register could not be read",
                "the_correction": "read the register before forecasting from it",
                "unavailable": f"{e.__class__.__name__}: {e}",
                "note": "this is not a statement that the count is accurate"}
    rows = reg.get("items", [])
    dropped = [r["id"] for r in rows if r.get("status") == "dropped"]
    return {
        "open": sum(1 for r in rows if r.get("status") == "open"),
        "dropped_as_refuted": len(dropped),
        "dropped_ids": sorted(dropped),
        "why_it_is_an_upper_bound": (
            "An open row is work SUSPECTED, not work established. Measured over three consecutive rounds: two "
            "rows were dropped as factually false (the script they accused walks no such path), two were "
            "already satisfied by earlier rounds, one was three-quarters done, and five of one item's six "
            "open rows had been satisfied and never closed. Roughly nine of fifteen rows examined needed no "
            "build, so a projection from this count is biased HIGH."),
        "the_correction": ("re-read the rows. Never apply a factor: a row measured false is DROPPED with the "
                          "measurement that refutes it and a row satisfied is CLOSED, and both make the "
                          "projection more honest rather than merely shorter."),
        "unavailable": None,
        "note": None,
    }


@router.get("/forecast")
async def method_forecast(user: dict | None = Depends(get_current_user)):
    """What the plan's own pace projects, and the four things the arithmetic cannot know.

    The projection itself is NOT computed here. `agentic_core.plan_followups.forecast()` is the one forecaster
    and is also served at GET /api/v1/plan/followups; a second rate on another surface would be two records
    disagreeing about the same fact.
    """
    method = _load_method()
    out: Dict[str, Any] = {
        "projection_computed_by": "agentic_core.plan_followups.forecast()",
        "also_served_at": "/api/v1/plan/followups",
        "what_this_adds": ("the discipline around the figure: what the count over-states, what dominates the "
                          "cost of a round, and which items cannot be closed by working them"),
    }
    try:
        from agentic_core import plan_followups as _fu
        reg = _fu.load()
        prompt = (_repo_root() / "docs/FABLE_DELIVERY_PROMPT.md").read_text(encoding="utf-8")
        f = _fu.forecast(reg, prompt)
        out["projection"] = {
            "rows": {"open": f.get("open_rows"), "rate_used": f.get("rate_used"),
                     "rounds_projected": f.get("all_rows_rounds_projected")},
            "items": dict(f.get("items") or {}, rate_per_round=f.get("item_rate_per_round"),
                          rounds_projected=f.get("items_rounds_projected"),
                          with_no_row=f.get("items_with_no_row"), sized=f.get("items_sized_build")),
            "basis": f.get("items_basis"),
            "not_assessable_because": f.get("not_assessable_because"),
            "next_item": f.get("next_item"),
        }
        # M-FCAST-01: both rates, and which one measures completion — stated, not left to the reader
        # W536 (P2.17 bar (c)) — the `why` here TYPED two figures, "32 rows closed across six rounds while
        # ZERO Phase 2 items closed in forty-eight", inside the payload whose whole job is to report
        # measurement. Both were hand-written and both had gone stale. The bar says these figures are
        # computed from git and the register, never typed, so the sentence is now assembled from the two
        # rates already in this payload and states what it cannot compute instead of inventing it.
        _rows_rate = (f.get("rate_used") or {}).get("closed_per_round")
        _item_rate = f.get("item_rate_per_round")
        _rows_window = (f.get("rate_used") or {}).get("rounds") or (f.get("rate_used") or {}).get("window")
        out["which_rate_measures_completion"] = {
            "rows_per_round": _rows_rate,
            "items_per_round": _item_rate,
            "rows_closed_in_window": (round(_rows_rate * _rows_window, 1)
                                      if isinstance(_rows_rate, (int, float))
                                      and isinstance(_rows_window, (int, float)) else None),
            "rows_window_rounds": _rows_window,
            "the_lever": "items",
            "why": ("the row rate sizes a ROUND; the item rate sizes the PLAN, and only one of them moves "
                    "toward completion. "
                    + (f"Measured now: {_rows_rate} row(s) per round against {_item_rate} item(s) per round."
                       if isinstance(_rows_rate, (int, float)) and isinstance(_item_rate, (int, float))
                       else "One or both rates could not be measured, so no comparison is stated.")),
            "why_basis": ("every figure in this block is read from the generated forecast, not written here. "
                          "A count of rows closed in the window is DERIVED from the rate and the window and "
                          "is therefore approximate to the rate's rounding; it is not a tally of rows"),
        }
    except Exception as e:                            # noqa: BLE001 — said, never a fabricated rate
        out["projection"] = {"unavailable": f"{e.__class__.__name__}: {e}",
                             "note": "no rate is substituted; a forecast that cannot be measured is refused"}

    out["the_count_overstates"] = _register_overstatement()
    out["cost_of_a_round"] = {
        "dominated_by": "verification",
        "components": ["the patch (minutes)", "one full suite on the FINAL tree (about fifty minutes)",
                       "one run per blind (two rounds ran 79 and 46)",
                       "the refutation passes (six to eight, measured falling 8 -> 7 -> 6)"],
        "why_it_matters": ("a forecast built from the size of the diff is wrong by an order of magnitude, and "
                          "the lever is FEWER, LARGER rounds over one file-connected component rather than "
                          "faster patching (M-FCAST-03, M-FCAST-06)"),
        "wall_clock_is_not_work": ("git measures the median round at about 4.5 hours over a 0.2-10.9 range, a "
                                  "fifty-fold spread a median conceals; one night inside it spent four hours "
                                  "of wall clock for 355 seconds of CPU because two suite runs were destroyed "
                                  "by touching their store (M-FCAST-04, M-PREP-04)"),
    }
    # W551 — THE THIRD READER OF THIS LIST, and the one that publishes it raw. The two others derive the
    # LIVE blocked set and must exclude items a round has since closed; one of them did and one did not,
    # which is how a closed item came to be reported as held behind a gate it had already passed. This
    # one is correct to show the ruling's full content — but it is RENAMED, because "items" invited a
    # reader to treat the ruling's roster as current state, and the roster does not shrink when an item
    # closes. Whether an item is still held is answered by the reasoning faculty, which reads the plan.
    out["blocked_by_ruling"] = {
        "items_the_ruling_named": _BLOCKED_BY_RULING,
        "is_this_the_live_set": False,
        "basis": ("this is the ROSTER the ruling named, not the set still held: it does not shrink when an "
                  "item closes. The live set is in the reasoning faculty, which excludes items the plan "
                  "marks done"),
        "consequence": ("Phase 2 cannot close before a chunk of Phase 3, and no amount of row-closing inside "
                        "Phase 2 changes it. Order by what UNBLOCKS, then by vision value (M-FCAST-05)."),
    }
    out["limits"] = (
        "Arithmetic over an observed mean, in ROUNDS. Never a date and never a promise, and it moves every "
        "time a round closes or registers a row. The item projection averages over a population most of which "
        "no round has measured, which its own basis calls the weakest number on the page.")
    out["lessons"] = [{"id": l["id"], "rule": l["rule"]} for l in method["lessons"]
                      if l.get("group") == "forecasting"]
    return out


# ── (g) LEARNING (W509) — a defect becomes a rule, and a REPEAT becomes a tool ──────────────────────────────

_BREACH_STORE = "method_breaches.json"
ESCALATE_AT = 3          # the third recorded breach of a lesson nothing enforces raises a change


class BreachRequest(BaseModel):
    lesson_id: str
    round_id: str                                  # the round that broke it, e.g. "W509"
    what_happened: str                             # the measured breach, not "we forgot"
    row_id: Optional[str] = None                   # a register row, where one exists
    submit_to_change_control: bool = True


def _breach_path():
    from agentic_core.config import data_path
    return data_path(_BREACH_STORE)


def _load_breaches() -> Dict[str, List[Dict[str, Any]]]:
    """The breach ledger, or a refusal. A store that cannot be read must not read as an empty ledger."""
    p = _breach_path()
    if not p.exists():
        return {}
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise HTTPException(status_code=503,
                            detail=(f"{_BREACH_STORE} could not be read ({e.__class__.__name__}: {e}). "
                                    f"Nothing is reported as unbreached in its absence.")) from e
    return d if isinstance(d, dict) else {}


def breach_counts() -> Dict[str, int]:
    """How many breaches are RECORDED per lesson. Zero is not a statement that none happened."""
    try:
        return {k: len(v) for k, v in _load_breaches().items() if isinstance(v, list)}
    except HTTPException:
        return {}


async def record_breach(lesson_id: str, round_id: str, what_happened: str,
                        row_id: Optional[str] = None, submit: bool = True) -> Dict[str, Any]:
    """Record that a written rule was broken again, and escalate on the COUNT.

    M-LEARN-02: a rule broken after being written needs a TOOL, not a reminder. So the count is what acts,
    not the severity of any single breach — and the escalation raises a change rather than deciding one,
    because the method is amended only by the agency that holds it.
    """
    method = _load_method()
    lesson = next((l for l in method["lessons"] if l.get("id") == lesson_id), None)
    if lesson is None:
        raise HTTPException(status_code=404,
                            detail=f"No lesson {lesson_id}. A breach must name the rule it broke.")
    if not what_happened.strip():
        raise HTTPException(status_code=400,
                            detail=("what_happened must state the MEASURED breach. 'we forgot' records "
                                    "nothing a tool could be built from."))

    from agentic_core.config import atomic_write_json, store_lock
    path = _breach_path()
    entry = {"round_id": round_id, "what_happened": what_happened.strip(), "row_id": row_id,
             "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    # serialised + atomic: this store has concurrent writers, and the class of bug that loses a write here
    # has already cost this repository three separate incidents
    with store_lock(str(path)):
        led = _load_breaches()
        led.setdefault(lesson_id, []).append(entry)
        count = len(led[lesson_id])
        atomic_write_json(path, led)

    enforced = bool((lesson.get("enforced_by") or "").strip())
    escalate = (count >= ESCALATE_AT) and not enforced
    verdict = {
        "lesson_id": lesson_id,
        "rule": lesson["rule"],
        "recorded": entry,
        "breaches_recorded": count,
        "escalate_at": ESCALATE_AT,
        "enforced": enforced,
        "state": (MET if enforced else UNMET if escalate else NOT_ASSESSABLE),
        "basis": ("this lesson names an enforcer, so a breach is a gap in that enforcer rather than a missing "
                  f"one: {lesson.get('enforced_by')}" if enforced else
                  f"recorded breach {count} of a lesson nothing enforces; the {ESCALATE_AT}rd raises a change"
                  if escalate else
                  f"recorded breach {count} of {ESCALATE_AT}; below the threshold, no change is raised yet"),
        "counts_are_not_occurrences": ("nothing observes a breach, so this count is of RECORDED breaches. A "
                                       "count of zero is not a statement that a rule has never been broken."),
    }

    submitted: Dict[str, Any] = {"submitted": False, "why": "the threshold was not reached"}
    if escalate and submit:
        try:
            from agentic_core.api.change_control import SubmitChangeRequest, submit_change
            cca = await submit_change(SubmitChangeRequest(
                title=f"Give {lesson_id} an enforcer: {ESCALATE_AT} recorded breaches",
                change_type="config_minor",
                description=(f"{lesson_id} ('{lesson['rule'][:160]}') has been recorded as breached {count} "
                             f"times and nothing enforces it. Its stated reason is: "
                             f"{lesson.get('why_not_enforced') or 'none recorded, which is itself a gap'}. "
                             f"Latest breach ({round_id}): {what_happened.strip()[:400]}"),
                rationale=("M-LEARN-02: a rule broken after being written is a mechanism failure, not a "
                           "discipline failure. Either build the tool, or restate why none is possible now - "
                           "a reason written once and never revisited outlives its truth (M-LEARN-03)."),
                affected_systems=["delivery_method", "change_control"],
                submitted_by="method_learning_loop",
            ))
            submitted = {"submitted": True, "cca_id": cca.get("cca_id"), "status": cca.get("status"),
                         "asks_for": "an enforcer for this lesson, or a restated reason none is possible"}
        except Exception as e:                       # noqa: BLE001 — recorded, never swallowed
            submitted = {"submitted": False, "why": f"{e.__class__.__name__}: {e}"}
    elif escalate:
        submitted = {"submitted": False, "why": "submit_to_change_control was false; the verdict stands"}
    verdict["change_control"] = submitted
    return verdict


@router.post("/breach")
async def record_a_breach(req: BreachRequest, user: dict | None = Depends(get_current_user)):
    """Record that a written rule was broken again. The third breach of an unenforced rule raises a change."""
    return await record_breach(req.lesson_id, req.round_id, req.what_happened,
                               req.row_id, req.submit_to_change_control)


@router.get("/learning")
async def learning_state(user: dict | None = Depends(get_current_user)):
    """The loop's own state: which of this method's rules are failing, and what the platform did about it."""
    method = _load_method()
    counts = breach_counts()
    by_id = {l["id"]: l for l in method["lessons"]}
    breached = sorted(
        ({"lesson_id": lid, "breaches_recorded": n,
          "rule": by_id.get(lid, {}).get("rule", "(no such lesson — the ledger names a rule the method lost)"),
          "enforced_by": by_id.get(lid, {}).get("enforced_by"),
          "at_or_over_threshold": n >= ESCALATE_AT and not (by_id.get(lid, {}).get("enforced_by") or "").strip()}
         for lid, n in counts.items()),
        key=lambda x: -x["breaches_recorded"])
    return {
        "loop": ("a CONFIRMED defect becomes a candidate lesson (POST /derive), Change Control ratifies it, a "
                 "later breach is recorded (POST /breach), and the third breach of a lesson nothing enforces "
                 "raises a change to give it one"),
        "enforcement": _enforcement_summary(method["lessons"]),
        "breached": breached,
        "escalated": [b["lesson_id"] for b in breached if b["at_or_over_threshold"]],
        "escalate_at": ESCALATE_AT,
        "lessons_with_no_recorded_breach": sorted(set(by_id) - set(counts)),
        "what_this_cannot_see": ("nothing observes a breach. Every figure here counts RECORDED breaches, so a "
                                 "lesson with none may simply never have been checked - which is why the "
                                 "loop is a discipline with a tool inside it, not a tool."),
        "learn_from_successes_too": ("M-LEARN-04: the practice that cut refutation from eight passes to six "
                                     "came from a SUCCESS, and no defect would ever have produced it. A "
                                     "success enters through /derive with the measurement as its evidence."),
        "lessons": [{"id": l["id"], "rule": l["rule"]} for l in method["lessons"]
                    if l.get("group") == "learning"],
    }


# ── (h) DIAGNOSING (W509) — the step between a symptom and a patch ──────────────────────────────────────────

class DiagnoseRequest(BaseModel):
    failures: List[Dict[str, Any]]        # [{name, message, file?, line?}] - what was OBSERVED
    context: Optional[str] = None         # what changed, what was running


def _signature(f: Dict[str, Any]) -> str:
    """One failure's comparable signature: the first line of its message, normalised of ids and numbers.

    Normalised because two failures caused by one deleted store differ only in the id they could not find,
    and a signature that includes the id would never match anything.
    """
    msg = str(f.get("message") or "").strip().splitlines()
    head = msg[0] if msg else ""
    head = re.sub(r"[0-9a-f]{6,}", "<id>", head, flags=re.I)
    # W509 — NO word boundaries on the digit rule. The first version used a bounded digit match, and a word
    # boundary does not fall between an underscore and a digit, so a path like data/store_000.json normalised
    # to itself and TWELVE failures caused by one deleted directory came back as twelve distinct signatures.
    # The instrument failed on the exact case it was built for, and was driven against that case before it was
    # trusted (M-VERIF-01: green is evidence only if red was reachable).
    head = re.sub(r"\d+", "<n>", head)
    head = re.sub(r"['\"][^'\"]{0,120}['\"]", "<s>", head)
    return head[:200]


def diagnose_failures(failures: List[Dict[str, Any]], context: Optional[str] = None) -> Dict[str, Any]:
    """Screen a set of observed failures for the shape that says ONE cause. Never names the cause."""
    if not failures:
        raise HTTPException(status_code=400,
                            detail=("No failures given. A diagnosis over nothing would report no shared "
                                    "signature, which reads as 'these are unrelated'."))
    groups: Dict[str, List[str]] = {}
    for f in failures:
        groups.setdefault(_signature(f), []).append(str(f.get("name") or "(unnamed)"))
    biggest = max(groups.items(), key=lambda kv: len(kv[1])) if groups else ("", [])
    n, shared = len(failures), len(biggest[1])
    share = round(shared / n, 3) if n else None

    # the signature that matters: MOST of the failures reduce to one message. Two is not a pattern.
    one_cause_shape = shared >= 3 and share is not None and share >= 0.5
    files = {str(f.get("file")) for f in failures if f.get("file")}

    return {
        "failures_given": n,
        "distinct_signatures": len(groups),
        "largest_group": {"signature": biggest[0], "count": shared, "share": share,
                          "tests": sorted(biggest[1])[:25]},
        "signatures": [{"signature": k, "count": len(v)} for k, v in
                       sorted(groups.items(), key=lambda kv: -len(kv[1]))],
        "files_touched": sorted(files) or None,
        "shared_signature": one_cause_shape,
        "what_this_means": (
            ("MOST of these failures reduce to one message, which is the shape of ONE cause and not of "
             f"{n} defects. Fifty-two failures in this programme's own history were a single deleted data "
             "directory. Re-run a SAMPLE of three to five in a clean environment before changing anything: "
             "if the sample passes, the diagnosis is about the environment, not the code (M-DIAG-01).")
            if one_cause_shape else
            (f"These {n} failures reduce to {len(groups)} distinct signatures, so no single-cause shape is "
             "visible here. That is NOT a statement that they are unrelated - a shared cause can produce "
             "different messages, and this only compares the text.")),
        "rule_out_before_changing_anything": [
            "the harness: was the store, tree or bundle modified while the run was in flight (M-PREP-04)",
            "the environment: does a 3-5 test sample pass against a FRESH store (M-DIAG-01, M-VERIF-11)",
            "the reproducer's cost: find the smallest selector that shows it before iterating (M-DIAG-02)",
            "the edit: does the branch the failure names actually RUN, and did an edit create that condition "
            "(M-DIAG-03)",
            "the chokepoint: is the site the failure names where the behaviour is DECIDED (M-DIAG-04)",
        ],
        "limits": ("This compares MESSAGE TEXT after normalising ids and numbers. It cannot name a cause, it "
                   "cannot diagnose a single failure, and a shared signature is a reason to re-run a sample - "
                   "never a diagnosis (M-DIAG-05: name what is still unexplained)."),
        "context": context,
    }


@router.post("/diagnose")
async def diagnose_a_set_of_failures(req: DiagnoseRequest, user: dict | None = Depends(get_current_user)):
    """Screen observed failures for the shape of one cause, and say what to rule out first."""
    return diagnose_failures(req.failures, req.context)


# ── (i) CORRECTING (W509) — how a wrong thing is made right without moving the defect ───────────────────────

class CorrectRequest(BaseModel):
    defect: str                                  # what was wrong, measured
    measurement: Optional[str] = None            # what established it
    cause: Optional[str] = None                  # the chokepoint, not the symptom site
    prior_value_captured: Optional[bool] = None  # can this be reversed
    narrowest_action: Optional[str] = None        # close / drop / relabel / scope / build
    readers_reverified: Optional[List[str]] = None
    not_covered: Optional[str] = None
    weakened_a_check: Optional[bool] = None
    submit_to_change_control: bool = False


_NARROW_ACTIONS = ("close", "drop", "relabel", "state_a_scope", "build")


def assess_correction(c: Dict[str, Any]) -> Dict[str, Any]:
    """Assess a PROPOSED correction against the correcting rules. Three states, and never 'verified'."""
    reqs: List[Dict[str, Any]] = []

    defect = str(c.get("defect") or "").strip()
    measurement = str(c.get("measurement") or "").strip()
    reqs.append(_req("states-the-defect-and-its-measurement", "M-CORR-06",
                     MET if len(defect) >= 20 and measurement else UNMET,
                     (f"the defect is stated in {len(defect)} characters and a measurement is given"
                      if len(defect) >= 20 and measurement else
                      "a correction that does not say what it corrected, and how that was established, "
                      "leaves the next reader unable to tell a fix from a rewrite"),
                     checkable_from="the proposal"))

    cause = str(c.get("cause") or "").strip()
    reqs.append(_req("names-a-cause-not-a-site", "M-DIAG-04",
                     MET if cause else UNMET,
                     ("names a cause" if cause else
                      "no cause is named. A correction aimed at the site where a behaviour is OBSERVED rather "
                      "than where it is DECIDED will be made again - recall was fixed at the call sites twice "
                      "before the default was found"),
                     checkable_from="the proposal"))

    prior = c.get("prior_value_captured")
    reqs.append(_req("the-correction-reverses", "M-CORR-02",
                     MET if prior is True else UNMET if prior is False else NOT_ASSESSABLE,
                     ("a prior value was captured, so this can be undone" if prior is True else
                      "no prior value was captured, so this correction is irreversible by construction - a "
                      "change nobody can undo is a change nobody can afford to make" if prior is False else
                      "the proposal does not say whether a prior value was captured; not every correction "
                      "changes a stored value, so this is not assumed either way"),
                     checkable_from="the proposal"))

    action = str(c.get("narrowest_action") or "").strip().lower()
    reqs.append(_req("takes-the-narrowest-true-action", "M-CORR-03",
                     MET if action in _NARROW_ACTIONS and action != "build" else
                     NOT_ASSESSABLE if action == "build" else UNMET,
                     (f"the action is '{action}', which changes no more than the record requires"
                      if action in _NARROW_ACTIONS and action != "build" else
                      "the action is a BUILD, which is the largest available correction. Whether it is the "
                      "narrowest TRUE action cannot be read from the proposal - five of one item's six rows "
                      "were already satisfied and building any of them would have changed working code"
                      if action == "build" else
                      f"no narrowest action is stated; it must be one of {', '.join(_NARROW_ACTIONS)}"),
                     checkable_from="the proposal"))

    weakened = c.get("weakened_a_check")
    reqs.append(_req("did-not-weaken-a-check", "M-CORR-04",
                     UNMET if weakened is True else NOT_ASSESSABLE,
                     ("the proposal states that a check was weakened. A failing guard is a question, not an "
                      "instruction: if the code is right the guard is REWRITTEN to assert the right thing, "
                      "never loosened" if weakened is True else
                      "a loosened assertion and a corrected one look identical in a diff, so this cannot be "
                      "checked from a record - only the reason distinguishes them, and it lives in the commit "
                      "message"),
                     checkable_from="nothing - this is the judgement the rule exists for"))

    readers = c.get("readers_reverified") or []
    reqs.append(_req("re-verified-every-reader", "M-EXEC-03",
                     NOT_ASSESSABLE,
                     (f"the proposal names {len(readers)} re-verified reader(s): "
                      f"{', '.join(map(str, readers[:8]))}. That they were re-verified is a claim about work "
                      f"done, which no record can show" if readers else
                      "no readers are named. A truth fix is done only when every writer, the reached page and "
                      "an executing guard leg all say the new truth - and whether they do is established by "
                      "running them, not by a field"),
                     checkable_from="nothing - a guard run is the evidence"))

    states = [r["state"] for r in reqs]
    unmet = [r["requirement"] for r in reqs if r["state"] == UNMET]
    return {
        "requirements": reqs,
        "summary": {"met": states.count(MET), "unmet": len(unmet),
                    "not_assessable": states.count(NOT_ASSESSABLE), "total": len(reqs)},
        "unmet": unmet,
        # there is deliberately no `sound` field. It could only ever have been None - three of the six
        # requirements are judgements no record can expose - and a verdict that cannot come out otherwise is
        # not an assessment (the class test_w494 guards). The basis says what IS known instead.
        "verdict_basis": (
            f"{len(unmet)} requirement(s) are UNMET from the proposal itself: {', '.join(unmet)}. A correction "
            f"with an unmet checkable requirement is not ready." if unmet else
            "no checkable requirement is unmet. This is NOT a statement that the correction is sound: three of "
            "the six are judgements no record can expose, and soundness is established by a guard that was "
            "made to fail first (M-VERIF-01)."),
        "never_reported": ("this endpoint never reports a correction as VERIFIED. It assesses a PROPOSAL "
                           "against the correcting rules; the evidence is a guard, and a guard is run."),
    }


@router.post("/correct")
async def assess_a_correction(req: CorrectRequest, user: dict | None = Depends(get_current_user)):
    """Assess a proposed correction against the correcting rules, and optionally file it with the agency."""
    _load_method()                     # refuse to assess against a method that cannot be read
    out = assess_correction(req.model_dump())
    submitted: Dict[str, Any] = {"submitted": False,
                                 "why": "submit_to_change_control was false; the assessment is returned only"}
    if req.submit_to_change_control:
        try:
            from agentic_core.api.change_control import SubmitChangeRequest, submit_change
            cca = await submit_change(SubmitChangeRequest(
                title=f"Correction: {req.defect[:70]}",
                change_type="config_minor",
                description=(f"Defect: {req.defect[:500]} | Cause: {req.cause or 'NOT STATED'} | Action: "
                             f"{req.narrowest_action or 'NOT STATED'} | Not covered: "
                             f"{req.not_covered or 'not stated'}"),
                rationale=(f"Measured by: {req.measurement or 'NOT STATED - which is itself unmet'}. "
                           f"Assessed against the method's correcting rules: "
                           f"{out['summary']['unmet']} unmet, {out['summary']['not_assessable']} not "
                           f"assessable."),
                affected_systems=["delivery_method"] + [str(r) for r in (req.readers_reverified or [])][:8],
                submitted_by="method_correction",
            ))
            submitted = {"submitted": True, "cca_id": cca.get("cca_id"), "status": cca.get("status")}
        except Exception as e:                   # noqa: BLE001 — recorded, never swallowed
            submitted = {"submitted": False, "why": f"{e.__class__.__name__}: {e}"}
    out["change_control"] = submitted
    return out


# ── (j) THE APPRAISAL CELL (W510) — eight faculties, four paired axes ───────────────────────────────────────
#
# A CELL, not a list of rules: given a scope it takes eight readings and reconciles them. Neither end of an
# axis is sufficient alone — reflection without reasoning is a diary, foresight without hindsight is a
# promise, introspection without extrospection is a platform grading its own homework.

_AXES = (("reflection", "reasoning"), ("attribution", "recognition"),
         ("foresight", "hindsight"), ("introspection", "extrospection"))


def _git(*args: str) -> Optional[str]:
    """Run a read-only git command, or None. Never raises: git may be absent or the clone shallow."""
    import subprocess
    try:
        p = subprocess.run(["git", *args], cwd=str(_repo_root()), capture_output=True, text=True, timeout=25)
        return p.stdout if p.returncode == 0 else None
    except (OSError, subprocess.SubprocessError):
        return None


def _round_of(message: str) -> Optional[int]:
    """The round a commit subject declares, e.g. 'feat(W509): ...' -> 509. None when it declares none."""
    m = re.search(r"\bW(\d{2,4})\b", message or "")
    return int(m.group(1)) if m else None


def _rows_the_tree_moved_under(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """EXTROSPECTION: open rows whose files a LATER round changed than the round that found them.

    This is FU-306's instrument. It reports CANDIDATES and closes nothing: whether a row is satisfied is a
    reading of the code it names, never a diff. Measured motivation - three consecutive rounds found rows
    already satisfied or factually false, and roughly nine of fifteen rows examined needed no build at all.
    """
    log = _git("log", "--format=%H%x1f%s", "--name-only", "-n", "400")
    if not log:
        return {"state": NOT_ASSESSABLE,
                "basis": ("git history could not be read (git absent, or a shallow clone as CI uses), so no "
                          "row is reported as a candidate. This is NOT a statement that every row is current."),
                "candidates": [], "candidate_count": 0, "history_commits": None,
                # W536 — the same keys as the computed branch, because a caller indexing one shape must not
                # raise on the other. None here means NOT COMPUTED, which is different from zero: with no
                # history read, this check considered nothing at all rather than considering everything.
                "not_considered_rows": None, "not_considered_row_count": None,
                "commits_no_round_could_be_read_from": None,
                "not_considered_basis": ("no history was read, so what this check could not consider is NOT "
                                         "COMPUTED rather than nought — it considered nothing"),
                "limits": ("nothing was read, so nothing is claimed. The limits of a successful read do not "
                           "apply here because no read succeeded.")}
    # W510 — parsed SEQUENTIALLY, not by splitting on blank lines. `--name-only` prints the files AFTER a
    # blank line, so splitting on "\n\n" separated every commit header from its own file list: one block held
    # the header with no files, the next held files whose first line was read as a header and skipped for
    # naming no round. The faculty therefore returned zero candidates over the whole plan across 401 commits
    # and COULD NOT have returned anything else — a check that cannot fire, committed inside the cell built to
    # catch that class, and found only by asking whether it could fire at all (M-VERIF-01).
    # A header is identifiable: it is the only line containing the \x1f separator the format asks for.
    touched: Dict[str, int] = {}                     # file -> the highest round that changed it
    commits, current = 0, None
    for line in log.splitlines():
        if not line.strip():
            continue
        if "\x1f" in line:
            commits += 1
            current = _round_of(line.split("\x1f", 1)[1])
            continue
        if current is not None and line > "" and current > touched.get(line, 0):
            touched[line] = current
    candidates = []
    for r in rows:
        src = _round_of(str(r.get("source") or ""))
        if src is None:
            continue
        later = {f: touched[f] for f in (r.get("files") or []) if f in touched and touched[f] > src}
        if later:
            candidates.append({"id": r.get("id"), "title": r.get("title"), "found_in_round": src,
                               "files_changed_since": later,
                               "why": (f"the tree moved under this row: {len(later)} of its file(s) were "
                                       f"changed in a later round than W{src}, which found it")})
    # W536 (FU-345) — WHAT THIS CHECK CANNOT SEE, counted rather than left in a prose limit. Its own limits
    # string already said it reads 400 commits and only those whose subject declares a round, so a row naming
    # no files cannot be matched at all and a change made by an unparseable commit subject is invisible. A
    # round reading only the candidate count would take the candidates for the whole picture. Not split by
    # cause: a subject declaring no round and one declaring a sub-round this parser cannot read are different
    # facts, and this counts what no round could be read FROM without claiming which.
    _no_files = [r.get("id") for r in rows if not (r.get("files") or [])]
    _unreadable_subjects = 0
    for _line in log.splitlines():
        if "\x1f" in _line and not _round_of(_line.split("\x1f", 1)[1]):
            _unreadable_subjects += 1
    return {
        "state": MET if candidates else NOT_ASSESSABLE,
        "candidates": sorted(candidates, key=lambda c: -max(c["files_changed_since"].values()))[:40],
        "candidate_count": len(candidates),
        "not_considered_rows": sorted(_no_files),
        "not_considered_row_count": len(_no_files),
        "commits_no_round_could_be_read_from": _unreadable_subjects,
        "not_considered_basis": (
            f"{len(_no_files)} open row(s) name NO files, so this check cannot match them against any change "
            f"and they are neither candidates nor cleared — they are UNEXAMINED by it. A further "
            f"{_unreadable_subjects} of {commits} commit(s) read carry a subject this parser could not read a "
            f"round from, so whatever they changed is invisible here too. Neither number is a defect in the "
            f"rows or the commits; both are the width of this instrument, counted instead of described"),
        # counted by the SAME parse that found the candidates, not by a second expression that could agree
        # with it by coincidence — which the blank-line split did, at 401, while finding nothing
        "history_commits": commits,
        "basis": (f"{len(candidates)} open row(s) name a file that a later round changed. Each is a CANDIDATE "
                  f"for re-reading and none is closed here: whether a row is satisfied is a reading of the "
                  f"code it names, not a diff."
                  if candidates else
                  "no open row names a file changed by a later round, within the history read. A row whose "
                  "files nobody touched can still be false - two were dropped as factually wrong in W507."),
        "limits": ("It reads the last 400 commits and only commits whose subject declares a round. A row "
                   "carrying no files, or found by a round the subject does not name, is invisible to it."),
    }


def _rate_stability(reg: Any, prompt: str) -> Dict[str, Any]:
    """HINDSIGHT: is the item rate the forecaster projects from actually STABLE across the span?

    A projection applied forward from a smooth average over a discontinuity is a promise. This splits the
    rounds that closed an item into an earlier and a later half and compares.
    """
    try:
        from agentic_core import plan_followups as _fu
        items = _fu.plan_items(prompt)
    except Exception as e:                                # noqa: BLE001
        return {"state": NOT_ASSESSABLE, "items_with_a_round": None,
                "basis": f"the plan's items could not be read ({e.__class__.__name__})"}
    done = sorted(r for r in (_round_of(str(i.get("done_by") or i.get("done") or "")) for i in items)
                  if r is not None)
    if len(done) < 6:
        return {"state": NOT_ASSESSABLE, "items_with_a_round": len(done),
                "basis": (f"only {len(done)} item(s) carry a readable round, and a split needs at least six. "
                          f"No stability is claimed either way.")}
    mid = len(done) // 2
    early, late = done[:mid], done[mid:]
    er = round(len(early) / max(1, early[-1] - early[0] + 1), 3)
    lr = round(len(late) / max(1, late[-1] - late[0] + 1), 3)
    ratio = round(lr / er, 2) if er else None
    stable = ratio is not None and 0.5 <= ratio <= 2.0
    return {
        "state": MET if stable else UNMET,
        # the same key the refusal branch carries: sibling returns share a shape, and a reader that keys on it
        # to decide whether NOT_ASSESSABLE is honest must be able to read it in both cases
        "items_with_a_round": len(done),
        "earlier_half": {"rounds": f"W{early[0]}-W{early[-1]}", "items": len(early), "rate": er},
        "later_half": {"rounds": f"W{late[0]}-W{late[-1]}", "items": len(late), "rate": lr},
        "later_over_earlier": ratio,
        "basis": (f"the item rate is {er} per round over W{early[0]}-W{early[-1]} and {lr} over "
                  f"W{late[0]}-W{late[-1]} — a ratio of {ratio}. "
                  + ("Within a factor of two, so projecting from the span's average is defensible."
                     if stable else
                     "OUTSIDE a factor of two, so the span's average is a smooth line over a discontinuity "
                     "and a projection from it will be wrong in a knowable direction.")),
        "and_ask_why": ("a round that beats its projection is a finding before it is velocity: five of one "
                        "item's six rows were already satisfied in W509, so the round closed them without "
                        "doing the work the schedule assumed."),
    }


def appraise_scope_for(systems: List[str]) -> Dict[str, Any]:
    """The SLOT a set of affected systems points at, if any — for callers that hold systems, not a slot.

    Used by Change Control so a change record can carry the appraisal of the scope it declares. Returns None
    rather than guessing: a change whose systems match no item is not appraised against an item chosen for it.
    """
    try:
        from agentic_core import plan_followups as _fu
        reg = _fu.load()
    except Exception:                                    # noqa: BLE001 — no scope rather than a wrong one
        return {"slot": None, "why": "the register could not be read, so no scope is inferred"}
    want = {str(x).strip().lower() for x in (systems or []) if str(x).strip()}
    if not want:
        return {"slot": None, "why": "the change names no affected system, so there is no scope to appraise"}
    hits: Dict[str, int] = {}
    for r in (reg.get("items") or []):
        if not isinstance(r, dict) or r.get("status") != "open":
            continue
        slot = str(r.get("slot") or "")
        for f in (r.get("files") or []):
            low = str(f).lower()
            if any(w in low or low.endswith(w) for w in want):
                hits[slot] = hits.get(slot, 0) + 1
    if not hits:
        return {"slot": None,
                "why": ("no open row names a file matching this change's affected systems, so it is not "
                        "appraised against an item chosen for it")}
    best = max(hits.items(), key=lambda kv: kv[1])
    return {"slot": best[0], "matched_rows": best[1],
            "why": f"{best[1]} open row(s) on {best[0]} name a file matching this change's affected systems",
            "other_candidates": {k: v for k, v in sorted(hits.items(), key=lambda kv: -kv[1])[1:5]}}


@router.get("/appraise")
async def appraise(scope: Optional[str] = None, user: dict | None = Depends(get_current_user)):
    """Run the Appraisal Cell over a scope — a phase prefix ("P2"), an item ("P2.4"), or the whole plan."""
    method = _load_method()
    lessons = [l for l in method["lessons"] if l.get("group") == "appraisal"]
    out: Dict[str, Any] = {
        "scope": scope or "the whole plan",
        "axes": [{"axis": f"{a} → {b}", "neither_end_alone": True} for a, b in _AXES],
        "structures": {"axes": len(_AXES), "spine": 1,
                       "faculties": len(_AXES) * 2 + len(_SPINE)},
        "faculties": {},
        "what_a_cell_is": method["about"].get("what_a_cell_is"),
    }

    try:
        from agentic_core import plan_followups as _fu
        reg = _fu.load()
        prompt = (_repo_root() / "docs/FABLE_DELIVERY_PROMPT.md").read_text(encoding="utf-8")
        items = _fu.plan_items(prompt)
        rows = [r for r in (reg.get("items") or []) if isinstance(r, dict)]
    except Exception as e:                                # noqa: BLE001 — said, never a confident empty cell
        raise HTTPException(status_code=503,
                            detail=(f"the plan and the register could not be read ({e.__class__.__name__}: "
                                    f"{e}); no appraisal is made, because an appraisal of nothing reads as "
                                    f"an appraisal of something sound.")) from e

    def in_scope(slot: Any) -> bool:
        s = str(slot or "")
        return True if not scope else (s == scope or s.startswith(scope + "."))

    scoped_items = [i for i in items if in_scope(i.get("slot"))]
    open_rows = [r for r in rows if r.get("status") == "open" and in_scope(r.get("slot"))]
    if scope and not scoped_items:
        raise HTTPException(status_code=404, detail=f"No plan item matches scope '{scope}'.")

    # ── 1 REFLECTION — what was FINISHED, separated from what was touched ─────────────────────────────
    closed_rows = [r for r in rows if r.get("status") == "done" and in_scope(r.get("slot"))]
    out["faculties"]["reflection"] = {
        "items_done": sum(1 for i in scoped_items if i.get("done")),
        "items_open": sum(1 for i in scoped_items if not i.get("done")),
        "rows_closed": len(closed_rows),
        "rows_open": len(open_rows),
        "rows_dropped": sum(1 for r in rows if r.get("status") == "dropped" and in_scope(r.get("slot"))),
        "basis": ("read from the register's statuses and the plan's DONE markers. ITEMS closed is progress; "
                  "ROWS closed is motion — 32 rows closed across six rounds while zero Phase 2 items closed "
                  "in forty-eight, and reading the second as the first is the error this faculty exists for."),
    }

    # ── 2 REASONING — the order the constraints imply, and the one lever ──────────────────────────────
    # W551 — A DONE ITEM IS NOT BLOCKED, IT IS CLOSED. This filtered by scope and not by state, so an
    # item the ruling had held and a round then closed was counted BOTH in items_done and in the blocked
    # set — double-counted, which inflated the ceiling by one for every such item and broke the identity
    # this cell's own guard asserts (ceiling == items in scope minus items blocked). Found when P2.12
    # closed: the cell reported five items as held behind a gate the sixth had already passed, which is
    # the opposite of what a reader needs from a list called "blocked".
    _done_slots = {i["slot"] for i in scoped_items if i.get("done")}
    blocked = {k: v for k, v in _BLOCKED_BY_RULING.items()
               if in_scope(k) and k not in _done_slots}
    unblocked = [i["slot"] for i in scoped_items if not i.get("done") and i["slot"] not in blocked]
    out["faculties"]["reasoning"] = {
        "blocked_by_ruling": blocked,
        "closable_by_working_them": unblocked,
        "ceiling_without_clearing_the_gate": (len([i for i in scoped_items if i.get("done")]) + len(unblocked)
                                             if blocked else None),
        "basis": (f"{len(blocked)} item(s) in this scope are held behind other items by ruling, so they cannot "
                  f"be closed by working them however high they score. The ceiling above is what this scope "
                  f"can reach WITHOUT clearing its gate."
                  if blocked else
                  "no item in this scope is recorded as held behind another, so the order is free and should "
                  "follow vision value. A constraint nobody wrote down is invisible here."),
        "the_one_lever": ("verification dominates a round's cost — the suite is one full run per round, a "
                          "blind sweep is one run per blind, refutation takes six to eight passes. The single "
                          "measured lever is a worktree per blind (FU-253), because it is the only one that "
                          "reduces the dominant term rather than the small one."),
        "limits": "it reports the blocking order the plan STATES; it cannot discover a constraint nobody wrote.",
    }

    # ── 3 ATTRIBUTION — which rows can be re-measured, and which can only be believed ─────────────────
    unattributed = [r["id"] for r in open_rows if not _round_of(str(r.get("source") or ""))]
    out["faculties"]["attribution"] = {
        "rows_naming_their_source_round": len(open_rows) - len(unattributed),
        "rows_with_no_source_round": unattributed,
        "share_attributed": (round((len(open_rows) - len(unattributed)) / len(open_rows), 3)
                             if open_rows else None),
        "basis": ("a row that names the round which found it can be re-measured; one that does not can only "
                  "be believed. A row asserted '19 call sites' and the measured figure was ZERO — not "
                  "dishonest, unattributed, so nothing could age it."),
        "limits": ("it checks that a source round is NAMED. Whether the figures in a row's body were measured "
                   "that way is a reading of the body, and is the judgement half of this faculty."),
    }

    # ── 4 RECOGNITION — the mechanisms, so a round is cut by class and not by row count ───────────────
    by_file: Dict[str, List[str]] = {}
    for r in open_rows:
        for f in (r.get("files") or []):
            by_file.setdefault(f, []).append(str(r.get("id")))
    clusters = sorted(({"files": [f], "rows": ids} for f, ids in by_file.items() if len(ids) > 1),
                      key=lambda c: -len(c["rows"]))
    out["faculties"]["recognition"] = {
        "rows_sharing_a_file": clusters[:12],
        "rows_citing_no_file": [r["id"] for r in open_rows if not (r.get("files") or [])],
        "defect_classes_available": [c["id"] for c in (method.get("defect_classes") or [])],
        "basis": ("rows that share a file are candidates for ONE mechanism. Recognition is what turned twenty "
                  "Phase 2 rows into seven mechanisms — the difference between twenty rounds and four — and "
                  "what found that 25 sites of one sentence were a single class."),
        "how_to_cut_a_round": "by mechanism and file connection under ONE item, never by row count",
        "limits": ("a shared file is a hint, not a class. A row citing no file is invisible to this and is "
                   "listed above for that reason."),
    }

    # ── 5 FORESIGHT — read the ONE forecaster; compute no rate here ───────────────────────────────────
    try:
        f = _fu.forecast(reg, prompt)
        out["faculties"]["foresight"] = {
            "rounds_for_the_open_rows": f.get("all_rows_rounds_projected"),
            "rounds_for_the_open_items": f.get("items_rounds_projected"),
            "item_rate_per_round": f.get("item_rate_per_round"),
            "items_never_sized": f.get("items_with_no_row"),
            "weakest_number": f.get("items_basis"),
            "computed_by": "agentic_core.plan_followups.forecast() — the ONE forecaster",
            "basis": ("rounds, never a date, and no rate is computed in this cell: a second forecaster would "
                      "be two records disagreeing about one fact."),
        }
    except Exception as e:                                # noqa: BLE001
        out["faculties"]["foresight"] = {"state": NOT_ASSESSABLE,
                                         "basis": f"the forecaster could not run ({e.__class__.__name__}: {e});"
                                                  f" no projection is substituted."}

    # ── 6 HINDSIGHT — did the rate the projection rests on actually hold ─────────────────────────────
    out["faculties"]["hindsight"] = _rate_stability(reg, prompt)

    # ── 7 INTROSPECTION — what the record cannot see about itself ─────────────────────────────────────
    enf = _enforcement_summary(method["lessons"])
    counts = breach_counts()
    out["faculties"]["introspection"] = {
        "method_rules_nothing_enforces": enf["judgement_only"],
        "method_rules_total": enf["lessons_total"],
        "items_in_scope_with_no_row": [i["slot"] for i in scoped_items
                                       if not i.get("done") and not any(
                                           str(r.get("slot")) == i["slot"] for r in open_rows)],
        "breaches_recorded": sum(counts.values()),
        "basis": ("the unenforced share, the unsized items and the unobserved breaches, as first-class "
                  "figures. A breach count of zero means none was RECORDED - nothing observes a breach - and "
                  "an item with no row has never been sized by anything."),
        "limits": "this is the platform reading its own record. It is the half that cannot be trusted alone.",
    }

    # ── 8 EXTROSPECTION — what only the tree can tell us ─────────────────────────────────────────────
    out["faculties"]["extrospection"] = _rows_the_tree_moved_under(open_rows)

    # ── THE TEMPORAL SPINE (W512) — 9 retrospection · 10 observation · 11 prospection ─────────────────
    out["faculties"]["retrospection"] = _retrospect(
        [r for r in rows if in_scope(r.get("slot"))], reg)
    out["faculties"]["observation"] = _observe()
    out["faculties"]["prospection"] = _prospect(scoped_items, rows)
    out["spine"] = {
        "spine": " → ".join(_SPINE),
        "why_a_spine_and_not_an_axis": ("time has a MIDDLE. The four axes are dyads whose ends check each "
                                        "other; this is a triad, and its middle is the present — the faculty "
                                        "this cell was built without."),
        "neither_end_alone": ("retrospection without observation is nostalgia; prospection without observation "
                              "is fantasy; observation without either is drift."),
    }

    out["reconciliation"] = (
        "Neither end of an axis is sufficient alone. REFLECTION without REASONING is a diary and reasoning "
        "without reflection is invention; ATTRIBUTION without RECOGNITION is a list of sources and recognition "
        "without attribution is a pattern nobody can check; FORESIGHT without HINDSIGHT is a promise and "
        "hindsight without foresight is regret; INTROSPECTION without EXTROSPECTION is a platform grading its "
        "own homework and extrospection without introspection is a platform that cannot say what it does not "
        "know. Read the pairs together or the cell has not run. And the SPINE is read as a whole for the same "
        "reason: RETROSPECTION without OBSERVATION is nostalgia, PROSPECTION without OBSERVATION is fantasy, "
        "and observation without either is drift.")
    out["this_cell_never_says"] = (
        "that a scope is sound, ready, or on track. Two of its eight faculties are largely judgement and say "
        "so, and the evidence for a delivery is a guard that was made to fail first.")
    out["lessons"] = [{"id": l["id"], "axis": l.get("axis"), "faculty": l.get("faculty"), "rule": l["rule"]}
                      for l in lessons]
    return out


# ── THE TEMPORAL SPINE (W512) — retrospection ↔ observation ↔ prospection ───────────────────────────────────
#
# Time is not a dyad. The cell's four axes each have two ends that check each other; this has a MIDDLE, and the
# middle is the one the cell was built without. Retrospection without observation is nostalgia; prospection
# without observation is fantasy; observation without either is drift.

_SPINE = ("retrospection", "observation", "prospection")


def _retrospect(rows: List[Dict[str, Any]], reg: Any) -> Dict[str, Any]:
    """RETROSPECTION: the record's PATTERN, not its totals — and what the pattern means.

    A row closed because it was already SATISFIED and a row closed because it was BUILT are the same increment
    in a total, which is why forty-eight rounds of totals could not show that roughly nine of fifteen rows
    examined needed no build at all.
    """
    try:
        from agentic_core import plan_followups as _fu
        act = _fu._round_activity(reg)
    except Exception as e:                                # noqa: BLE001 — said, never an invented pattern
        # the SAME key set as the answer below: a refusal that omits the answer's keys makes every reader
        # raise KeyError exactly when the record is already unreadable (the W508 shape).
        return {"state": NOT_ASSESSABLE,
                "basis": f"the register's round record could not be read ({e.__class__.__name__}: {e})",
                "refutation_share": None, "rounds": None,
                "rows_built_or_satisfied": None, "rows_dropped_as_refuted": None,
                "rounds_that_closed_something": None, "rounds_that_only_found": None,
                "closed_total": None, "found_total": None, "backlog_growing": None,
                "what_the_pattern_means": "not measured: the round record could not be read",
                "limits": "nothing was read, so nothing is claimed about the pattern"}

    done = [r for r in rows if r.get("status") == "done"]
    dropped = [r for r in rows if r.get("status") == "dropped"]
    resolved = len(done) + len(dropped)
    share = round(len(dropped) / resolved, 3) if resolved else None

    closing = sorted(r for r, a in act.items() if a.get("closed", 0) > 0)
    finding_only = sorted(r for r, a in act.items() if a.get("closed", 0) == 0 and a.get("found", 0) > 0)
    closed_total = sum(a.get("closed", 0) for a in act.values())
    found_total = sum(a.get("found", 0) for a in act.values())

    return {
        "state": MET if resolved else NOT_ASSESSABLE,
        "basis": None,                 # the answer's meaning is in what_the_pattern_means; `basis` is the
        "rounds": None,                # refusal branch's field, carried here so the shapes match
        "rows_built_or_satisfied": len(done),
        "rows_dropped_as_refuted": len(dropped),
        "refutation_share": share,
        "rounds_that_closed_something": len(closing),
        "rounds_that_only_found": finding_only,
        "closed_total": closed_total,
        "found_total": found_total,
        "backlog_growing": (found_total > closed_total) if (closed_total or found_total) else None,
        "what_the_pattern_means": (
            (f"{len(dropped)} of {resolved} resolved rows were DROPPED as refuted rather than built, a "
             f"refutation share of {share}. A row dropped as false and a row closed because it was already "
             f"satisfied are both work the register ASKED FOR and did not need — which is why the open count "
             f"is an upper bound on the work and not a measure of it (M-FCAST-02). The totals cannot show "
             f"this, because closing a satisfied row and closing a built one are the same increment."
             if resolved else "no row has been resolved, so there is no pattern to read yet.")
            + (f" {len(finding_only)} round(s) closed nothing and only registered findings: those add work "
               f"rather than burning it, and counting them as build rounds would understate the rate."
               if finding_only else "")),
        "limits": ("this reads STATUS, not cause. It cannot tell a row closed because it was built from one "
                   "closed because it was already satisfied — that distinction lives in the closing round's "
                   "own words, and recording it is what would make this faculty sharper."),
    }


def _observe() -> Dict[str, Any]:
    """OBSERVATION: the live organism, now. The faculty the cell was built without.

    Every reading of NOW is stale the instant it is taken. And a STOPPED heartbeat is not a healthy zero: it
    means there is no organism state to read, which is a different fact and is said as one.
    """
    out: Dict[str, Any] = {"read_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    try:
        from agentic_core.organism.heartbeat import heartbeat
        st = heartbeat.status()
    except Exception as e:                                 # noqa: BLE001
        return dict(out, state=NOT_ASSESSABLE,
                    basis=(f"the organism could not be read ({e.__class__.__name__}: {e}). This is NOT a "
                           f"statement that it is idle."))
    running = bool(st.get("running"))
    out.update({
        "state": MET if running else UNMET,
        "beating": running,
        "beats": st.get("beats"),
        "circadian_phase": st.get("circadian_phase"),
        "phase_intensity": st.get("phase_intensity"),
        "last_beat": st.get("last_beat"),
        "last_actions": {k: st.get(k) for k in
                         ("last_realisation", "last_self_healing", "last_recovery", "last_heal", "last_genome")
                         if st.get(k) is not None},
        "basis": ("the organism is beating, so this is a reading of a live system" if running else
                  "THE HEARTBEAT IS STOPPED. Nothing is being operated, nothing is being screened, and the "
                  "figures above are the last ones it recorded rather than current ones. A stopped beat is not "
                  "a healthy zero."),
        "limits": ("a reading of NOW is stale the moment it is taken, and this one does not re-read. It says "
                   "when it was taken so a reader can judge that, which is the only honest thing available."),
    })
    return out


def _prospect(scoped_items: List[Dict[str, Any]], rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """PROSPECTION: the branches, each with its assumption. Ranked by nothing, ever.

    A possibility given a probability has been turned into a prediction, and this platform has exactly one
    forecaster. So this enumerates and refuses to order.
    """
    branches: List[Dict[str, Any]] = []

    blocked = {k: v for k, v in _BLOCKED_BY_RULING.items()
               if any(str(i.get("slot")) == k and not i.get("done") for i in scoped_items)}
    if blocked:
        branches.append({
            "branch": "the gate clears",
            "assumption": f"the items named in the ruling are delivered: {sorted(set(blocked.values()))}",
            "what_becomes_possible": sorted(blocked),
            "what_this_is_not": "not a claim that they will be, and not an estimate of when",
        })
        branches.append({
            "branch": "the gate does not clear",
            "assumption": "the blocking items stay open",
            "what_becomes_possible": [],
            "consequence": (f"{len(blocked)} item(s) cannot be closed by working them, so the phase's ceiling "
                            f"stands wherever the unblocked work reaches"),
        })

    owner = [r for r in rows if r.get("status") == "open"
             and (r.get("owner_gated") or str(r.get("slot")) == "OWNER")]
    for r in owner:
        branches.append({
            "branch": f"the Owner decides {r.get('id')}",
            "assumption": "a decision is recorded either way",
            "what_becomes_possible": [str(r.get("slot") or "OWNER")],
            "why_it_is_the_owners": r.get("slot_source") or "no reason recorded, which is itself a gap",
            "what_this_is_not": "not a recommendation, and not a guess at which way it goes",
        })

    unsized = [i["slot"] for i in scoped_items
               if not i.get("done") and not any(str(x.get("slot")) == i["slot"] and x.get("status") == "open"
                                                for x in rows)]
    if unsized:
        branches.append({
            "branch": "an unsized item turns out larger than the average",
            "assumption": f"{len(unsized)} item(s) in scope carry no registered row, so nothing has measured them",
            "what_becomes_possible": [],
            "consequence": ("the projection is an average over a population most of which no round has "
                            "opened — this branch is why the forecaster calls that its weakest number"),
        })

    return {
        "state": MET if branches else NOT_ASSESSABLE,
        "branches": branches,
        "count": len(branches),
        "basis": ("each branch names the ASSUMPTION it rests on. They are possibilities, not predictions."
                  if branches else
                  "no branch is readable for this scope: nothing is recorded as blocked, no decision is "
                  "awaiting the Owner, and every item carries a row. That is not a statement that the future "
                  "is certain."),
        "never": ("ranked, weighted, given a probability, or given a date. A possibility with a likelihood is "
                  "a prediction, and this platform has ONE forecaster "
                  "(agentic_core.plan_followups.forecast) — a second voice on the same question is two "
                  "records disagreeing about one fact (M-DELIV-08)."),
        "limits": ("it enumerates the branches the ARTEFACTS record — a ruling, an owner-gated row, an unsized "
                   "item. A future nobody wrote down is invisible to it, which is most of them."),
    }
