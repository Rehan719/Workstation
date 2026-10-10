"""The Instrument Cell (plan item P3.31) — the fabric PROPOSES, CHECKS and VERIFIES; a person still decides.

Built ON the resource fabric: its registry, its outcome vocabulary, its run store and its router prefix. There
is no second registry and no second runner here. Everything this module returns is computed from the fabric's
own records at the moment of the call, and each answer says what it was decided from.

WHAT IT ADDS (each was measured absent before it was built — docs/INSTRUMENT_CELL_BRIEF_ASSESSMENT.md):
  availability   whether the fabric can run a resource's engine, read now, with the reason when it cannot
  contract       what a resource takes and what it yields, derived from the registry and refused if incomplete
  propose        the smallest available set covering STATED requirements — it saves nothing and runs nothing
  verify         each stated criterion met / unmet / not assessed against a RECORDED run

WHAT IT DOES NOT DO: generate instruments, promote anything, tune itself from past runs, or run or save
anything. An alternative is NAMED here when one is declared. Trying one belongs to the composition runner,
which does it once and only for a failed status read (Owner ruling 2026-10-10).
"""
from __future__ import annotations

import inspect
import itertools
import re
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from agentic_core.api import resource_fabric as _fab

router = APIRouter(prefix="/api/v1/resources/cell", tags=["instrument-cell"])

#  A DECLARED POLICY, NOT A MEASUREMENT. Nothing in the tree measures how many stages a run can carry, so this
#  is a ceiling chosen to stop a runaway composition and it is reported as declared wherever it is shown.
MAX_STAGES = 12
MAX_STAGES_BASIS = ("declared policy: a ceiling against a runaway composition. It is not derived from a "
                    "measurement of what the organism can carry")
#  each resource is attempted once per run; nothing in the fabric retries
ATTEMPTS_PER_RESOURCE = 1
_EXACT_UP_TO = 3            # the size up to which the smallest cover is found by exhaustive search


# ── the registry is validated where it is read ────────────────────────────────────────────────────
def registry_defects(registry: List[Dict[str, Any]]) -> List[str]:
    """Every way a registration fails to state a usable contract. Empty means none."""
    out: List[str] = []
    seen: set = set()
    for r in registry:
        rid = r.get("id")
        if not isinstance(rid, str) or not rid.strip():
            out.append(f"a registration has no id: {str(r)[:80]}")
            continue
        if rid in seen:
            out.append(f"{rid}: registered twice")
        seen.add(rid)
        if not [c for c in (r.get("capabilities") or []) if isinstance(c, str) and c.strip()]:
            out.append(f"{rid}: declares no capability, so nothing can ever select it")
        if not isinstance(r.get("reconfigurable_params"), dict):
            out.append(f"{rid}: declares no parameter table (an empty one is a statement; a missing one is not)")
        if not str(r.get("endpoint") or "").startswith("/api/"):
            out.append(f"{rid}: declares no endpoint")
        if not r.get("methods"):
            out.append(f"{rid}: declares no method for its endpoint")
    return out


_DEFECTS = registry_defects(_fab._REGISTRY)
if _DEFECTS:      # refused at import: a resource with no contract must not be selectable by accident
    raise RuntimeError("the resource registry holds registrations without a usable contract: "
                       + "; ".join(_DEFECTS))


# ── availability: read now, and said with its reason ──────────────────────────────────────────────
_RUNNER_OWNED = {"vsb_org_swarm": "run by the composition runner itself (the organisation cascade)"}


def _handler_ids() -> Optional[set]:
    """The resource ids the fabric's real-resource handler has a branch for, read from the handler.

    Read from the function's source because that is where the fact lives: the handler is an if-chain, and a
    registered id with no branch falls through and returns nothing. None when the source cannot be read, and
    then availability is reported NOT CHECKED rather than guessed."""
    return _HANDLER_IDS


def _read_handler_ids() -> Optional[set]:
    try:
        src = inspect.getsource(_fab._run_real_resource_handler)
    except (OSError, TypeError):
        return None
    ids = set(re.findall(r'rid == "([a-z_0-9]+)"', src))
    for group in re.findall(r"rid in \(([^)]*)\)", src):
        ids.update(re.findall(r'"([a-z_0-9]+)"', group))
    return ids


#  READ ONCE, AT IMPORT. `inspect.getsource` slices the file ON DISK by the loaded function's line numbers, so
#  on a running process whose source file was edited underneath it the slice is some other text entirely: the
#  first live read of this module, on a server started before an edit, reported 40 of 41 resources as having
#  no handler. At import the file and the loaded code are the same thing; afterwards they need not be.
_HANDLER_IDS = _read_handler_ids()


def _served(app) -> Optional[Dict[str, set]]:
    """path -> methods the application serves; None when there is no application to read."""
    if app is None:
        return None
    table: Dict[str, set] = {}
    for route in getattr(app, "routes", []) or []:
        path = getattr(route, "path", None)
        if path:
            table.setdefault(path, set()).update(getattr(route, "methods", None) or set())
    return table


def availability(rid: str, app=None) -> Dict[str, Any]:
    """available | prompt_stage_only | not_checked — with the reason, and what was NOT checked."""
    base = _fab._BY_ID[rid]
    handlers = _handler_ids()
    served = _served(app)
    declared_methods = set(base.get("methods") or [])
    if served is None:
        endpoint_state, endpoint_basis = "not_checked", "no application was available to read the route table from"
    else:
        on_path = served.get(base["endpoint"])
        if on_path is None:
            endpoint_state = "not_served"
            endpoint_basis = f"the registry declares {base['endpoint']} and the application serves no such path"
        elif not (declared_methods & on_path):
            endpoint_state = "method_mismatch"
            endpoint_basis = (f"the registry declares {sorted(declared_methods)} on {base['endpoint']} and the "
                              f"application serves {sorted(m for m in on_path if m not in ('HEAD', 'OPTIONS'))}")
        else:
            endpoint_state, endpoint_basis = "served", "the declared endpoint and method are in the route table"
    if handlers is None:
        state, reason = "not_checked", "the handler's source could not be read, so no branch could be looked for"
    elif rid in handlers:
        state, reason = "available", "the fabric's real-resource handler has a branch for it"
    elif rid in _RUNNER_OWNED:
        state, reason = "available", _RUNNER_OWNED[rid]
    else:
        state = "prompt_stage_only"
        reason = ("registered, and the fabric's real-resource handler has no branch for it: composing it adds "
                  "a prompt stage to the swarm and does not run its engine")
    return {"id": rid, "state": state, "reason": reason,
            "endpoint_state": endpoint_state, "endpoint_basis": endpoint_basis,
            "not_checked": ("whether its engine succeeds on a real input - that is known only by running it, "
                            "and a run records it as its outcome")}


# ── contract: derived from the registry, never typed beside it ────────────────────────────────────
def equivalents(rid: str) -> List[str]:
    """Resources that DECLARE the same thing: the same endpoint, the same kind, and that kind a status read.

    Computed, not listed. Two registrations that read the same platform state through the same route are the
    only case the registry itself establishes as interchangeable; anything broader would be a judgement."""
    base = _fab._BY_ID[rid]
    if _fab._resource_kind(rid) != "status_read":
        return []
    return sorted(o["id"] for o in _fab._REGISTRY
                  if o["id"] != rid and o["endpoint"] == base["endpoint"]
                  and _fab._resource_kind(o["id"]) == "status_read")


_WHEN_RUN = {
    "status_read": "when run, it reads platform state that is already there; no facility runs",
    "query": "when run, it assesses against records and live state already there; it produces and persists nothing",
    "blueprint": "when run, it composes a design blueprint from the catalogue; it provisions and activates nothing",
    "facility_run": "when run, it runs its engine and produces an output",
}


def contract(rid: str) -> Dict[str, Any]:
    base = _fab._BY_ID[rid]
    kind = _fab._resource_kind(rid)
    side = _fab._READ_SIDE_EFFECTS.get(rid)
    if side:
        persists, persists_basis = "side_effect", side
    elif kind in ("status_read", "query", "blueprint"):
        persists, persists_basis = "nothing", _WHEN_RUN[kind]
    else:
        persists = "not_declared"
        persists_basis = ("this resource runs an engine, and the registry does not record what the engine "
                          "persists; read its run record to see what it did")
    params = dict(base.get("reconfigurable_params") or {})
    return {"id": rid, "inputs": params,
            "inputs_basis": ("the registry's declared parameters, each with its declared type or example; "
                             "which of them the engine REQUIRES is not declared"),
            "takes_no_input": not params,
            #  W640 - a contract describes what a resource WOULD do. The fabric's own kind phrases are written
            #  for a run that happened ("ran its engine and produced this output"), and the first live proposal
            #  printed that sentence over a resource nothing had run. So: its own wording, in the conditional.
            "yields": kind, "when_run": _WHEN_RUN[kind],
            "persists": persists, "persists_basis": persists_basis,
            "capabilities": list(base.get("capabilities") or []),
            "usable_in": list(base.get("usable_in") or []),
            "equivalents": equivalents(rid),
            "equivalents_basis": ("registrations declaring the same endpoint as a status read; empty means "
                                  "the registry establishes no interchangeable resource")}


# ── requirements and selection ────────────────────────────────────────────────────────────────────
def _norm(s: Any) -> str:
    return " ".join(str(s or "").lower().split())


def _covers(requirement: str, resource: Dict[str, Any]) -> Optional[str]:
    """The capability tag by which `resource` covers `requirement`, or None. Equality first, then containment
    on whole words either way; nothing fuzzier, because a near-match that is wrong selects the wrong engine."""
    want = _norm(requirement)
    if not want:
        return None
    tags = [_norm(c) for c in resource.get("capabilities") or []]
    for t in tags:
        if t == want:
            return t
    for t in tags:
        if re.search(rf"(?<![a-z0-9]){re.escape(want)}(?![a-z0-9])", t) or \
                re.search(rf"(?<![a-z0-9]){re.escape(t)}(?![a-z0-9])", want):
            return t
    return None


def suggest_requirements(objective: str) -> List[Dict[str, str]]:
    """Capability tags that appear, as whole words, in the objective. A SUGGESTION for a person to confirm."""
    text = _norm(objective)
    out: Dict[str, str] = {}
    for r in _fab._REGISTRY:
        for c in r.get("capabilities") or []:
            t = _norm(c)
            if t and t not in out and re.search(rf"(?<![a-z0-9]){re.escape(t)}(?![a-z0-9])", text):
                out[t] = r["id"]
    return [{"capability": t, "first_declared_by": rid} for t, rid in sorted(out.items())]


def select(requirements: List[str], app=None, usage_area: Optional[str] = None) -> Dict[str, Any]:
    """The smallest set of AVAILABLE resources covering the stated requirements, and everything it left out."""
    reqs = [r for r in dict.fromkeys(_norm(x) for x in requirements) if r]
    covers: Dict[str, Dict[str, str]] = {}          # rid -> {requirement: tag}
    excluded: List[Dict[str, Any]] = []
    for r in _fab._REGISTRY:
        hit = {q: tag for q in reqs for tag in [_covers(q, r)] if tag}
        if not hit:
            continue
        av = availability(r["id"], app)
        if av["state"] != "available":
            excluded.append({"id": r["id"], "would_cover": sorted(hit), "because": f"{av['state']}: {av['reason']}"})
            continue
        if usage_area and usage_area not in (r.get("usable_in") or []):
            excluded.append({"id": r["id"], "would_cover": sorted(hit),
                             "because": f"does not declare the usage area '{usage_area}'"})
            continue
        covers[r["id"]] = hit
    coverable = sorted({q for h in covers.values() for q in h})
    uncovered = [q for q in reqs if q not in coverable]

    def _key(combo):                                   # deterministic: most specific first, then by id
        return (sum(len(_fab._BY_ID[i]["capabilities"]) for i in combo), combo)

    chosen: List[str] = []
    method = "nothing to cover"
    if coverable:
        pool = sorted(covers)
        found = None
        for size in range(1, min(_EXACT_UP_TO, len(pool)) + 1):
            fits = [c for c in itertools.combinations(pool, size)
                    if set(coverable) <= {q for i in c for q in covers[i]}]
            if fits:
                found = min(fits, key=_key)
                method = (f"exhaustive: no set of fewer than {size} available resource(s) covers the coverable "
                          f"requirements, and among sets of {size} the one declaring the fewest capabilities "
                          f"was taken")
                break
        if found is None:
            left, greedy = set(coverable), []
            while left:
                best = max(pool, key=lambda i: (len(left & set(covers[i])), -len(_fab._BY_ID[i]["capabilities"]), i))
                gain = left & set(covers[best])
                if not gain:
                    break
                greedy.append(best)
                left -= gain
            found = tuple(greedy)
            method = (f"greedy: no set of {_EXACT_UP_TO} or fewer covers the requirements, so resources were "
                      f"added by how many uncovered requirements each takes. NOT proven to be the smallest set")
        chosen = list(found)
    return {"requirements": reqs, "selected": [
                {"id": i, "name": _fab._BY_ID[i]["name"], "covers": sorted(covers[i]),
                 "by_capability": covers[i], "contract": contract(i), "availability": availability(i, app)}
                for i in chosen],
            "uncovered": uncovered,
            "uncovered_basis": ("no AVAILABLE registered resource declares a capability matching these; a "
                                "requirement left here is not met by widening the match"),
            "excluded": excluded, "method": method}


# ── criteria: met / unmet / not assessed, each with the evidence it was read from ─────────────────
def assess(criteria: List[Any], run: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    by_resource = {x.get("resource"): x for x in ((run or {}).get("real_resources") or [])}
    for c in criteria or []:
        row: Dict[str, Any] = {"criterion": c}
        if run is None:
            row.update(state="not_assessed", evidence=None, basis="nothing has run, so there is nothing to read")
        elif isinstance(c, dict) and c.get("kind") == "resource_outcome":
            got = by_resource.get(c.get("resource"))
            if got is None:
                row.update(state="not_assessed", evidence=None,
                           basis=f"resource {c.get('resource')!r} was not attempted in this run")
            else:
                row.update(state="met" if got.get("outcome") == c.get("is") else "unmet",
                           evidence={"resource": got.get("resource"), "outcome": got.get("outcome"),
                                     "error": got.get("error")},
                           basis="read from the run's own record of what that resource did")
        elif isinstance(c, dict) and c.get("kind") == "quality_gate":
            gate = run.get("qms_gate_passed")
            if gate is None:
                row.update(state="not_assessed", evidence={"qms_gate_passed": None},
                           basis="the quality gate recorded that it could not assess this run")
            else:
                row.update(state="met" if gate else "unmet", evidence={"qms_gate_passed": gate},
                           basis="read from the run's recorded quality-gate verdict")
        else:
            row.update(state="not_assessed", evidence=None,
                       basis=("a criterion in free text: nothing here can read a run against a sentence. State "
                              "it as a resource_outcome or a quality_gate criterion, or assess it yourself"))
        rows.append(row)
    counts = {s: sum(1 for r in rows if r["state"] == s) for s in ("met", "unmet", "not_assessed")}
    return {"criteria": rows, "counts": counts,
            #  not assessed is never met: an empty list, or one with anything unassessed, is not "all met"
            "all_met": bool(rows) and counts["met"] == len(rows),
            "all_met_basis": "true only when every stated criterion was assessed AND met; none stated is not met"}


# ── routes ────────────────────────────────────────────────────────────────────────────────────────
@router.get("/availability")
async def cell_availability(request: Request):
    rows = [{**availability(r["id"], request.app), "name": r["name"]} for r in _fab._REGISTRY]
    counts: Dict[str, int] = {}
    for x in rows:
        counts[x["state"]] = counts.get(x["state"], 0) + 1
    return {"resources": rows, "counts": counts, "total": len(rows),
            "declaration_defects": [{"id": x["id"], "endpoint_state": x["endpoint_state"],
                                     "basis": x["endpoint_basis"]}
                                    for x in rows if x["endpoint_state"] in ("not_served", "method_mismatch")],
            "basis": ("read at this call from the fabric's handler and the application's route table. "
                      "'available' means the fabric can run the resource's engine; it does not mean the engine "
                      "will succeed")}


@router.get("/contract/{resource_id}")
async def cell_contract(resource_id: str, request: Request):
    if resource_id not in _fab._BY_ID:
        raise HTTPException(status_code=404, detail=f"Resource {resource_id} is not registered.")
    return {**contract(resource_id), "availability": availability(resource_id, request.app)}


class ProposeRequest(BaseModel):
    objective: str
    required_capabilities: List[str] = []
    acceptance_criteria: List[Any] = []
    usage_area: Optional[str] = None
    max_stages: int = MAX_STAGES


@router.post("/propose")
async def cell_propose(req: ProposeRequest, request: Request):
    """A PROPOSAL. It saves nothing and runs nothing; a person composes and runs what they accept."""
    if not str(req.objective or "").strip():
        raise HTTPException(status_code=422, detail="an objective is required")
    if not 1 <= req.max_stages <= MAX_STAGES:
        raise HTTPException(status_code=422, detail=(
            f"max_stages must be between 1 and {MAX_STAGES} ({MAX_STAGES_BASIS})"))
    limits = {"max_stages": req.max_stages, "ceiling": MAX_STAGES, "ceiling_basis": MAX_STAGES_BASIS,
              "attempts_per_resource": ATTEMPTS_PER_RESOURCE,
              "attempts_basis": "each resource is attempted once per run; the fabric retries nothing"}
    common = {"objective": req.objective.strip(), "saved": False, "ran": False,
              "what_this_is": "a proposal: nothing was saved and nothing was run", "limits": limits}
    stated = [c for c in req.required_capabilities if _norm(c)]
    if not stated:
        return {**common, "requirements_confirmed": False, "selection": None,
                "suggested_requirements": suggest_requirements(req.objective),
                "suggestion_basis": ("capability tags that appear as whole words in the objective. A tag match, "
                                     "not an understanding of the objective: confirm, change or replace them and "
                                     "send them back as required_capabilities"),
                "criteria": assess(req.acceptance_criteria, None)}
    sel = select(stated, request.app, req.usage_area)
    if len(sel["selected"]) > req.max_stages:
        raise HTTPException(status_code=422, detail=(
            f"covering these requirements takes {len(sel['selected'])} resources and the limit for this "
            f"proposal is {req.max_stages}. Nothing was proposed; narrow the requirements or raise the limit "
            f"(ceiling {MAX_STAGES})."))
    return {**common, "requirements_confirmed": True, "selection": sel,
            "alternatives": {s["id"]: [{"id": e, "availability": availability(e, request.app)["state"]}
                                       for e in s["contract"]["equivalents"]] for s in sel["selected"]},
            "alternatives_basis": ("declared equivalents are NAMED here; a proposal tries nothing. At RUN time the "
                                   "fabric tries one declared equivalent, once, when a status read fails "
                                   "(Owner ruling 2026-10-10) - never for a resource that runs an engine or "
                                   "writes, and never a second one"),
            "criteria": assess(req.acceptance_criteria, None)}


class VerifyRequest(BaseModel):
    run_id: str
    criteria: List[Any]


@router.post("/verify")
async def cell_verify(req: VerifyRequest, user: dict | None = Depends(_fab.get_current_user)):
    """Read stated criteria against a RECORDED composition run."""
    from agentic_core.config import StoreUnavailable, read_json_strict
    try:
        runs = read_json_strict(_fab.data_path("composition_runs.json"), list, expect=list)
    except StoreUnavailable as e:
        raise HTTPException(status_code=503, detail=f"the run store could not be read, so nothing was assessed: {e}")
    run = next((r for r in runs if r.get("run_id") == req.run_id), None)
    if run is None:
        raise HTTPException(status_code=404, detail=f"run {req.run_id} is not in the run store")
    _fab._require_design_access(run, user, "Composition run", req.run_id)
    return {"run_id": req.run_id, "composition_id": run.get("composition_id"), **assess(req.criteria, run)}
