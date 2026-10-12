"""The Instrument Cell (plan item P3.31) — the fabric PROPOSES, CHECKS and VERIFIES; a person still decides.

Built ON the resource fabric: its registry, its outcome vocabulary, its run store and its router prefix. There
is no second registry and no second runner here. Everything this module returns is computed from the fabric's
own records at the moment of the call, and each answer says what it was decided from.

WHAT IT ADDS (each was measured absent before it was built — docs/INSTRUMENT_CELL_BRIEF_ASSESSMENT.md):
  availability   whether the fabric can run a resource's engine, read now, with the reason when it cannot
  contract       what a resource takes and what it yields, derived from the registry and refused if incomplete
  propose        the smallest available set covering STATED requirements — it saves nothing and runs nothing
  verify         each stated criterion met / unmet / not assessed against a RECORDED run
  specification  what a proposal IS in the shape the fabric keeps, its digest, and a re-check of a
                 kept one against the registry now. Computed here; the FABRIC keeps it

WHAT IT DOES NOT DO: generate instruments, promote anything, tune itself from past runs, or run or save
anything. An alternative is NAMED here when one is declared. Trying one belongs to the composition runner,
which does it once and only for a failed status read (Owner ruling 2026-10-10).
"""
from __future__ import annotations

import hashlib
import inspect
import itertools
import json
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
_EXACT_REQUIREMENTS = 16    # W674 - above three: an exact search over subsets of the requirements, up to this many


def _smallest_cover(coverable: List[str], covers: Dict[str, Dict[str, str]], weight) -> Optional[tuple]:
    """W674 (P3.31 clause 4) - THE SMALLEST SET, FOUND AND NOT GUESSED. For each subset of the coverable
    requirements, the best set of resources that covers at least that subset: fewest resources first, then the
    fewest declared capabilities, then by id - the same order the exhaustive step uses. Every subset is
    reached from a smaller one by adding one resource, so the full set's entry is a smallest cover. None when
    there are more requirements than this search is bounded to."""
    if len(coverable) > _EXACT_REQUIREMENTS:
        return None
    bit = {q: 1 << k for k, q in enumerate(coverable)}
    masks = {i: sum(bit[q] for q in h if q in bit) for i, h in covers.items()}
    full = (1 << len(coverable)) - 1
    best: Dict[int, tuple] = {0: ()}

    def _rank(combo):
        return (len(combo), sum(weight(i) for i in combo), combo)
    for mask in range(full + 1):                       # ascending: a superset mask is always the larger number
        have = best.get(mask)
        if have is None:
            continue
        for i, m in masks.items():
            if not m & ~mask:
                continue                               # this resource adds no requirement the set lacks
            nxt = mask | m
            cand = tuple(sorted(have + (i,)))
            if nxt not in best or _rank(cand) < _rank(best[nxt]):
                best[nxt] = cand
    return best.get(full)
#  P3.31 clause 1 - the kinds of need a registration may declare (resource_fabric._need_*). `model` is a
#  served model above the floor (the completion kind counts the floor as met); `none` is a stated "nothing".
_NEED_KINDS = ("module", "completion", "config", "package", "model", "none")


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
        #  P3.31 clauses 1 and 2 - EVERY REGISTRATION DECLARES WHAT IT NEEDS. An ABSENT declaration is a
        #  defect, so the registry is refused at import with the resource named. An empty list and a `none`
        #  need are statements; a missing `needs` is not one. A present declaration must be one the check reads.
        needs = r.get("needs")
        if needs is None:
            out.append(f"{rid}: declares no needs (an empty declaration or a 'none' need is a statement; "
                       f"a missing one is not)")
        elif not isinstance(needs, list):
            out.append(f"{rid}: declares needs that are not a list")
        else:
            for n in needs:
                kind = n.get("kind") if isinstance(n, dict) else None
                if kind not in _NEED_KINDS:
                    out.append(f"{rid}: declares a need of a kind the check cannot read ({kind!r})")
                elif kind == "module" and not (n.get("module") and n.get("attr")):
                    out.append(f"{rid}: declares a module need without naming the module and what it takes from it")
                elif kind == "package" and not n.get("package"):
                    out.append(f"{rid}: declares a package need without naming the package")
                elif kind == "config" and n.get("param") not in (r.get("reconfigurable_params") or {}):
                    out.append(f"{rid}: declares that it requires the parameter {n.get('param')!r}, "
                               f"which its own parameter table does not hold")
                elif kind == "none" and not str(n.get("read") or "").strip():
                    out.append(f"{rid}: declares that it needs nothing without saying what was read to conclude it")
                elif kind == "none" and len(needs) != 1:
                    out.append(f"{rid}: declares that it needs nothing beside {len(needs) - 1} other need(s)")
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


# ── declared needs: read from the registration, checked now ───────────────────────────────────────
#  Three seams, so a guard can drive each need both ways without uninstalling anything.
def _import_attr(module: str, attr: str):
    import importlib
    return getattr(importlib.import_module(module), attr)


def _completion_order() -> List[str]:
    from agentic_core.ai.native.model_resource import registry as _models
    return list(_models.select())


def _package_present(name: str) -> bool:
    import importlib.util
    return importlib.util.find_spec(name) is not None


def needs_check(rid: str, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """What `rid` DECLARES it needs, each need checked at this call: not_declared | met | unmet | not_checked.

    not_declared  the registration says nothing. NOTHING WAS CHECKED - this is not "needs nothing".
    met           every need that must hold does (an optional package may be absent; a parameter the
                  resource requires is listed under `per_run` when no configuration was given to read)
    unmet         a need that must hold does not; `basis` names it
    not_checked   a need could not be read either way (the check itself failed)
    """
    base = _fab._BY_ID[rid]
    declared = base.get("needs")
    if declared is None:
        return {"declared": False, "state": "not_declared", "needs": [], "per_run": [],
                "narrowed": [], "declared_none": False,
                "basis": ("this registration declares no needs, so nothing was checked beyond whether the "
                          "fabric has a handler for it. NOT DECLARED is not the same as needing nothing")}
    placeholders = base.get("reconfigurable_params") or {}
    rows: List[Dict[str, Any]] = []
    per_run: List[str] = []
    for n in declared:
        kind = n.get("kind")
        row: Dict[str, Any] = {"kind": kind, "optional": bool(n.get("optional")), "why": n.get("why")}
        if kind == "module":
            row["needs"] = f"{n.get('module')}.{n.get('attr')}"
            try:
                _import_attr(n.get("module"), n.get("attr"))
                row.update(met=True, basis="imported at this call")
            except (ImportError, AttributeError) as exc:
                row.update(met=False, basis=f"could not be imported ({type(exc).__name__}: {str(exc)[:120]})")
            except Exception as exc:                      # noqa: BLE001 - said, never guessed either way
                row.update(met=None, basis=f"the import could not be tried ({type(exc).__name__})")
        elif kind == "completion":
            row["needs"] = "an owned completion tier"
            try:
                order = _completion_order()
                owned = [x for x in order if x not in ("anthropic", "openai")]
                row.update(met=bool(owned), served_first=(order[0] if order else None),
                           basis=((f"{owned[0]} is the first owned tier in the selection order read at this call"
                                   + ("; that is the deterministic floor, so this need is met WITHOUT a model"
                                      if owned[0] == "native" else
                                      "; the deterministic floor is behind it" if "native" in owned else ""))
                                  if owned else "no owned completion tier is in the selection order"))
            except Exception as exc:                      # noqa: BLE001
                row.update(met=None, served_first=None,
                           basis=f"the selection order could not be read ({type(exc).__name__})")
        elif kind == "package":
            row["needs"] = f"the package {n.get('package')}"
            try:
                present = _package_present(n.get("package"))
                row.update(met=present, basis="installed" if present else "not installed")
            except Exception as exc:                      # noqa: BLE001
                row.update(met=None, basis=f"could not be looked for ({type(exc).__name__})")
        elif kind == "model":
            #  A MODEL, NOT THE FLOOR. Read from the same selection order the completion need reads; any tier
            #  in it other than the deterministic floor is a model, and an external one is named as external.
            row["needs"] = "a served model above the deterministic floor"
            try:
                order = _completion_order()
                models = [x for x in order if x != "native"]
                row.update(met=bool(models), served_first=(order[0] if order else None),
                           basis=((f"{models[0]} is in the selection order read at this call"
                                   + (" (an external provider)" if models[0] in ("anthropic", "openai") else ""))
                                  if models else
                                  ("no model is served: only the deterministic floor is in the selection order "
                                   "read at this call") if order else
                                  "nothing is in the selection order read at this call"))
            except Exception as exc:                      # noqa: BLE001
                row.update(met=None, served_first=None,
                           basis=f"the selection order could not be read ({type(exc).__name__})")
        elif kind == "none":
            row["needs"] = "nothing"
            row.update(met=True, basis=f"declared, from what was read: {n.get('read')}")
        elif kind == "config":
            param = n.get("param")
            row["needs"] = f"the parameter '{param}' set to a value"
            if config is None:
                per_run.append(param)
                row.update(met=None, per_run=True,
                           basis="per run: it is read from a configuration, and none was given to this check")
            else:
                v = config.get(param)
                ok = v not in (None, "", [], {}) and v != placeholders.get(param)
                row.update(met=ok, per_run=True,
                           basis=("set in this configuration" if ok else
                                  "not set in this configuration; without it the handler runs nothing"))
        else:
            row.update(needs=str(kind), met=None, basis="a need of a kind this check cannot read")
        rows.append(row)
    must = [r for r in rows if not r["optional"]]
    unmet = [r for r in must if r["met"] is False]
    unread = [r for r in must if r["met"] is None and not (r.get("per_run") and config is None)]
    absent = [r for r in rows if r["optional"] and r["met"] is False]
    if unmet:
        state = "unmet"
        basis = "; ".join(f"{r['needs']}: {r['basis']}" for r in unmet)
    elif unread:
        state = "not_checked"
        basis = "; ".join(f"{r['needs']}: {r['basis']}" for r in unread)
    elif rows and all(r["kind"] == "none" for r in rows):
        state = "met"
        basis = f"declares that it needs nothing - {rows[0]['basis']}"
    else:
        state = "met"
        basis = (f"{len(must) - len(per_run)} declared need(s) checked at this call and met"
                 + (f"; {', '.join(per_run)} must be set in a configuration and was not checked here" if per_run else "")
                 + (f"; optional and absent: {', '.join(r['needs'] for r in absent)}" if absent else ""))
    #  WHAT AN ABSENT OPTIONAL NEED COSTS, in the registration's own words. The resource is still available;
    #  what it cannot do HERE goes with it to the proposal and the page instead of staying in the registry.
    narrowed = [{"needs": r["needs"], "kind": r["kind"], "why": r["why"], "basis": r["basis"]} for r in absent]
    return {"declared": True, "state": state, "needs": rows, "per_run": per_run, "basis": basis,
            "narrowed": narrowed,
            "declared_none": bool(rows) and all(r["kind"] == "none" for r in rows)}


_CHECKED_WORD = {"met": "available", "unmet": "unavailable", "not_declared": "not_checked",
                 "not_checked": "not_checked"}


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
    #  P3.31 clause 1 (round 10) - `state` above KEEPS ITS MEANING (the fabric has a handler for it). What the
    #  resource DECLARES it needs is said beside it, and `checked` is the clause's own three words: a resource
    #  is "available" there only when it has a handler AND its declared needs were checked and met. One that
    #  declares nothing is "not_checked" - none is available by default.
    need = needs_check(rid)
    if state == "available":
        checked = _CHECKED_WORD[need["state"]]
        checked_basis = (need["basis"] if need["state"] != "met" else
                         f"the fabric has a handler for it, and {need['basis']}")
    else:
        checked = "unavailable" if state == "prompt_stage_only" else "not_checked"
        checked_basis = reason
    return {"id": rid, "state": state, "reason": reason,
            "needs_declared": need["declared"], "needs_state": need["state"], "needs": need["needs"],
            "needs_per_run": need["per_run"], "needs_basis": need["basis"],
            "needs_narrowed": need["narrowed"], "needs_declared_none": need["declared_none"],
            "checked": checked, "checked_basis": checked_basis,
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
    "narrative": "when run, it writes a scenario narrative from a persona prompt; no simulator or engine runs",
    "facility_run": "when run, it runs its engine and produces an output",
}


def contract(rid: str) -> Dict[str, Any]:
    base = _fab._BY_ID[rid]
    kind = _fab._resource_kind(rid)
    side = _fab._READ_SIDE_EFFECTS.get(rid)
    if side:
        persists, persists_basis = "side_effect", side
    elif kind in ("status_read", "query", "blueprint", "narrative"):
        persists, persists_basis = "nothing", _WHEN_RUN[kind]
    elif rid in _fab._FACILITY_PERSISTS:
        #  P3.31 clause 2 - declared where the engine was READ. A facility run that is not in the fabric's
        #  table still reads "not_declared" below: nobody has read what its engine writes
        persists, persists_basis = _fab._FACILITY_PERSISTS[rid]
    else:
        persists = "not_declared"
        persists_basis = ("this resource runs an engine, and the registry does not record what the engine "
                          "persists; read its run record to see what it did")
    params = dict(base.get("reconfigurable_params") or {})
    #  P3.31 clause 2 (round 10) - WHAT IT REQUIRES, where the registration declares it
    declared = base.get("needs")
    required = [n.get("param") for n in declared if n.get("kind") == "config"] if declared is not None else None
    return {"id": rid, "inputs": params,
            "inputs_basis": ("the registry's declared parameters, each with its declared type or example; "
                             + ("`required` lists the ones without which the fabric's handler runs nothing"
                                if declared is not None else
                                "which of them the engine REQUIRES is not declared")),
            "takes_no_input": not params,
            "required": required,
            "required_basis": ("declared by the registration: the handler runs nothing unless these are set"
                               if required else
                               "declared by the registration: no parameter is required to start it"
                               if declared is not None else
                               "NOT DECLARED: this registration states no needs, so which parameters it "
                               "requires is not known from the registry"),
            "needs": (list(declared) if declared is not None else None),
            "needs_declared": declared is not None,
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
        #  P3.31 clause 1 (round 10) - A DECLARED NEED THAT IS UNMET MAKES IT UNAVAILABLE: never proposed, and
        #  the reason is the need. A resource that declares nothing is NOT excluded here (see the return).
        if av["needs_state"] == "unmet":
            excluded.append({"id": r["id"], "would_cover": sorted(hit),
                             "because": f"unavailable: a declared need is not met - {av['needs_basis']}"})
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
            exact = _smallest_cover(coverable, covers, lambda i: len(_fab._BY_ID[i]["capabilities"]))
            if exact is not None:
                found = exact
                method = (f"exact: every subset of the {len(coverable)} coverable requirement(s) was searched; no "
                          f"set of fewer than {len(exact)} available resource(s) covers them, and among sets of "
                          f"{len(exact)} the one declaring the fewest capabilities was taken")
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
            method = (f"greedy: there are {len(coverable)} coverable requirements, more than the "
                      f"{_EXACT_REQUIREMENTS} an exact search is bounded to, and no set of {_EXACT_UP_TO} or fewer "
                      f"covers them, so resources were added by how many uncovered requirements each takes. "
                      f"NOT proven to be the smallest set")
        chosen = list(found)
    return {"requirements": reqs, "selected": [
                {"id": i, "name": _fab._BY_ID[i]["name"], "covers": sorted(covers[i]),
                 "by_capability": covers[i], "contract": contract(i), "availability": availability(i, app)}
                for i in chosen],
            "uncovered": uncovered,
            "uncovered_basis": ("no AVAILABLE registered resource declares a capability matching these; a "
                                "requirement left here is not met by widening the match"),
            "excluded": excluded, "method": method,
            #  P3.31 clause 1 (round 10) - a proposed resource whose needs nobody declared is NAMED. It is
            #  proposed on the strength of its handler alone, and the proposal says so rather than letting
            #  "selected" read as "checked".
            "needs_not_declared": [i for i in chosen if _fab._BY_ID[i].get("needs") is None],
            "needs_not_declared_basis": ("these are proposed because the fabric has a handler for each; none "
                                         "declares what it needs, so nothing else about them was checked")}


# ── an assembly specification: a proposal a person chose to KEEP (P3.31) ─────────────────────────
#  COMPUTED HERE, KEPT BY THE FABRIC. This module still saves nothing and runs nothing: it says what a
#  proposal for stated requirements IS at this call, in the shape that is kept; the digest of that content;
#  and, for a kept one, what is true of its resources NOW. The store, its lock and its routes are the fabric's.
SPEC_CONTENT_FIELDS = ("objective", "required_capabilities", "acceptance_criteria", "usage_area",
                       "max_stages", "proposed", "selection_rule", "uncovered")


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)


def registration_digest(rid: str) -> Optional[str]:
    """A digest of what the registry declares for `rid` NOW; None when it is not registered.

    The registry declares NO contract version: nothing in a registration says "this is contract N". So what
    is kept beside a proposed resource is this digest of its whole registration, computed, and a later
    re-check can say the registration is no longer the one that was proposed. It is not a version."""
    base = _fab._BY_ID.get(rid)
    if base is None:
        return None
    return hashlib.sha256(_canonical(base).encode("utf-8")).hexdigest()


def specification_digest(content: Dict[str, Any]) -> str:
    """The digest of a specification's CONTENT: the fields in SPEC_CONTENT_FIELDS and nothing else. Who kept
    it, when, its id and its place in a line of versions are not content - the same content has the same
    digest whoever keeps it and whenever."""
    return hashlib.sha256(
        _canonical({k: content.get(k) for k in SPEC_CONTENT_FIELDS}).encode("utf-8")).hexdigest()


def specification_content(objective: str, required_capabilities: List[str], acceptance_criteria: List[Any],
                          usage_area: Optional[str], max_stages: int, app=None) -> Dict[str, Any]:
    """What a proposal for these stated requirements IS at this call, in the shape that is kept.

    The proposed resources come from `select` - the same selection /propose returns - so a kept
    specification never holds a resource somebody typed."""
    sel = select([c for c in required_capabilities if _norm(c)], app, usage_area)
    return {"objective": str(objective or "").strip(),
            "required_capabilities": list(sel["requirements"]),
            "acceptance_criteria": list(acceptance_criteria or []),
            "usage_area": usage_area or None,
            "max_stages": int(max_stages),
            "proposed": [{"id": s["id"], "covers": list(s["covers"]),
                          "registration_digest": registration_digest(s["id"])} for s in sel["selected"]],
            "selection_rule": sel["method"],
            "uncovered": list(sel["uncovered"])}


def recheck(spec: Dict[str, Any], app=None) -> List[Dict[str, Any]]:
    """Each PROPOSED resource of a kept specification, read against the registry and the fabric NOW.

    `available` is decided by the two tests `select` makes before it proposes a resource - the fabric has a
    handler for it, and no declared need is unmet - so a resource that would not be proposed today reads
    unavailable here. Nothing is tried and nothing is put in its place: a declared equivalent is NAMED."""
    out: List[Dict[str, Any]] = []
    for p in spec.get("proposed") or []:
        rid = p.get("id") if isinstance(p, dict) else None
        if rid not in _fab._BY_ID:
            out.append({"id": rid, "registered": False, "available": False,
                        "because": "it is no longer in the resource registry",
                        "state": None, "needs_state": None, "registration_changed": None, "equivalents": []})
            continue
        av = availability(rid, app)
        if av["state"] != "available":
            ok, because = False, f"{av['state']}: {av['reason']}"
        elif av.get("needs_state") == "unmet":
            ok, because = False, f"unavailable: a declared need is not met - {av.get('needs_basis')}"
        else:
            ok, because = True, av["reason"]
        out.append({"id": rid, "registered": True, "available": ok, "because": because,
                    "state": av["state"], "needs_state": av.get("needs_state"),
                    "registration_changed": registration_digest(rid) != p.get("registration_digest"),
                    "equivalents": equivalents(rid)})
    return out


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
                                     "error": got.get("error"),
                                     #  P3.31 (round 9) - a stand-in's row is evidence about the STAND-IN
                                     **({"alternative_for": got["alternative_for"]}
                                        if got.get("alternative_for") else {}),
                                     **({"alternative": got["alternative"]} if got.get("alternative") else {})},
                           basis=("read from the run's own record of what that resource did"
                                  + (f". {got.get('resource')} ran here as a STAND-IN for "
                                     f"{got['alternative_for']}; this is not evidence about {got['alternative_for']}"
                                     if got.get("alternative_for") else "")))
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
    needs_counts: Dict[str, int] = {}
    checked_counts: Dict[str, int] = {}
    for x in rows:
        needs_counts[x["needs_state"]] = needs_counts.get(x["needs_state"], 0) + 1
        checked_counts[x["checked"]] = checked_counts.get(x["checked"], 0) + 1
    _declared = sum(1 for x in rows if x["needs_declared"])
    _narrowed = sum(1 for x in rows if x["needs_narrowed"])
    return {"resources": rows, "counts": counts, "total": len(rows),
            #  P3.31 clause 1 (round 10) - beside `counts`, which keeps its meaning (handler branches)
            "needs_counts": needs_counts, "checked_counts": checked_counts, "needs_declared": _declared,
            "needs_basis": (f"{_declared} of {len(rows)} registration(s) declare what they need, and each "
                            f"declared need was checked at this call. "
                            + ((f"The other {len(rows) - _declared} declare nothing: for those only the handler "
                                f"was looked for, and they are counted 'not_checked', never 'available'")
                               if _declared != len(rows) else
                               ("None is without a declaration: a registration that declares nothing is refused "
                                "when the registry is read at import"))
                            + ((f". {_narrowed} start here with less than they declare: an optional need is "
                                f"absent, and each says what that costs") if _narrowed else "")),
            "needs_narrowed_count": _narrowed,
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
    #  P3.31 - None (not sent) on a run made from a specification means: read it against the criteria
    #  kept with that specification. A list, even an empty one, keeps its meaning: these criteria.
    criteria: Optional[List[Any]] = None


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
    #  P3.31 clause 7 (round 9) - ATTEMPTED VERSUS NOT ATTEMPTED, read from the run's own record. A row is an
    #  attempt; a composed resource with no row was a prompt stage only, or its handler declined for want of
    #  configuration. A stand-in is listed apart: it was attempted, and it was not composed.
    rows = [x for x in (run.get("real_resources") or []) if isinstance(x, dict)]
    attempted = [x.get("resource") for x in rows if not x.get("alternative_for")]
    stand_ins = [{"for": x.get("alternative_for"), "resource": x.get("resource"), "outcome": x.get("outcome"),
                  "label": x.get("stand_in_label") or (
                      f"STAND-IN: {x.get('resource')} is not a resource this composition holds. The fabric "
                      f"tried it once in place of {x.get('alternative_for')}")}
                 for x in rows if x.get("alternative_for")]
    composed = run.get("composed")
    known = isinstance(composed, list)
    #  P3.31 - A RUN MADE FROM A SPECIFICATION IS READ AGAINST THAT SPECIFICATION'S CRITERIA. The run's record
    #  names the specification and the digest it had; the criteria are read from the kept record, and only
    #  when that record's content still has that digest. `criteria` in the answer keeps its meaning (the
    #  criteria that were assessed) and `criteria_source` says whose they were.
    link = run.get("specification") if isinstance(run.get("specification"), dict) else None
    spec_rec, spec_problem = None, None
    if link:
        try:
            spec_rec = _fab._find_specification(link.get("specification_id"))
        except StoreUnavailable as e:
            spec_problem = f"the specification store could not be read: {e}"
        else:
            if spec_rec is None:
                spec_problem = f"specification {link.get('specification_id')} is not in the specification store"
            elif specification_digest(spec_rec) != link.get("specification_digest"):
                spec_rec = None
                spec_problem = (f"the record of specification {link.get('specification_id')} no longer has the "
                                f"digest this run recorded, so its criteria were not used")
    if req.criteria is None:
        if not link:
            raise HTTPException(status_code=422, detail=(
                "criteria are required: this run names no specification, so there are no kept criteria to "
                "read it against. Nothing was assessed."))
        if spec_rec is None:
            raise HTTPException(status_code=409, detail=f"{spec_problem}. Nothing was assessed.")
    own = assess(req.criteria if req.criteria is not None else (spec_rec.get("acceptance_criteria") or []), run)
    spec_view = None
    if link:
        spec_view = {"specification_id": link.get("specification_id"),
                     "specification_digest": link.get("specification_digest"), "version": link.get("version"),
                     "criteria_read": spec_rec is not None,
                     "basis": (spec_problem if spec_rec is None else
                               "the criteria kept with the specification this run names, read from the kept "
                               "record after its content was found to have the digest the run recorded"),
                     **(assess(spec_rec.get("acceptance_criteria") or [], run) if spec_rec is not None else
                        {"criteria": None, "counts": None, "all_met": None, "all_met_basis": None}),
                     "executed": link.get("executed"), "not_attempted": link.get("not_attempted"),
                     "not_in_specification": link.get("not_in_specification")}
    return {"run_id": req.run_id, "composition_id": run.get("composition_id"), **own,
            "criteria_source": "request" if req.criteria is not None else "specification",
            "criteria_source_basis": (
                ("the criteria stated in this request. " + (
                    "This run names a specification: what its own kept criteria say is under `specification`"
                    if link else "This run names no specification"))
                if req.criteria is not None else
                f"no criteria were stated in the request, so the criteria kept with specification "
                f"{link.get('specification_id')} (the one this run names) were read"),
            "specification": spec_view,
            "attempted": attempted,
            "not_attempted": [c for c in composed if c not in attempted] if known else None,
            "stand_ins": stand_ins,
            "attempt_basis": (
                ("attempted: the fabric ran this resource's handler on this run and recorded what it did. "
                 "Not attempted: it was composed and no handler ran for it on this run")
                if known else
                ("attempted: the fabric ran this resource's handler on this run. NOT KNOWN which composed "
                 "resources were not attempted: this run was recorded before the composed list was kept "
                 "with it"))}
