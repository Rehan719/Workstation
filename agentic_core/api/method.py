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
    return {
        "about": d["about"],
        "groups": d["about"].get("groups", []),
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
