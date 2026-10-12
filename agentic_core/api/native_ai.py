"""
Native AI Fabric API — Workstation's OWN AI resources, exposed.

Surfaces the in-house AI control plane (W1): the model-resource registry (owned native
engine + self-hosted local model + optional external accelerants), the orchestrator
(in-house-first completion), and the swarm engine (bespoke, reusable agent-cascade trees).
Everything is honest about which resource served and whether any external provider was used.
"""
from __future__ import annotations

import os
from typing import Any, Dict, List, Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from agentic_core.ai.native import orchestrator, registry
from agentic_core.ai.native.model_resource import external_allowed

router = APIRouter(prefix="/api/v1/native-ai", tags=["native-ai-fabric"])


# -- P3.32 clause 3 - EACH SURFACE THAT DESCRIBES A MODEL STATES ITS OWN LEVEL, IN ITS OWN ANSWER ------------
#  The level and what it rests on are read from ONE place - `_EVIDENCE_SURFACES`, further down - at the moment
#  the route answers. Nothing is typed beside a route. A route marked here and missing from that table answers
#  "NOT PLACED" instead of borrowing a level. The level is the SURFACE's (the kind of statement the route
#  makes); it is not a judgement of the particular answer.
_LEVEL_STATED: set = set()


def _level_statement(path: str) -> Dict[str, Any]:
    placed = _EVIDENCE_SURFACES.get(path)
    if placed is None:
        return {"evidence_level": None, "evidence_level_number": None,
                "evidence_basis": (f"NOT PLACED: {router.prefix}{path} is in no evidence table, so no level is "
                                   f"stated for it")}
    level, rests_on = placed
    return {"evidence_level": level, "evidence_level_number": (1 if level == "behaviour" else None),
            "evidence_basis": (f"{rests_on}. "
                               + ("Level 1 - inputs and outputs only; the highest level anything here reaches"
                                  if level == "behaviour" else
                                  "Configuration - what is configured, declared or reachable; below level 1 and "
                                  "not a statement about behaviour"))}


def _states_level(path: str):
    """Mark a route of this router so its answer carries its own evidence level. A dict answer gains the three
    fields (a field the handler set itself is kept); any other answer is returned as it is."""
    import functools
    _LEVEL_STATED.add(path)

    def _mark(fn):
        @functools.wraps(fn)
        async def _answer(*args, **kwargs):
            res = await fn(*args, **kwargs)
            if isinstance(res, dict):
                return {**_level_statement(path), **res}
            return res
        _answer._states_level = path
        return _answer
    return _mark


@router.get("/status")
@_states_level("/status")
async def native_status():
    resources = registry.available()
    owned = [r for r in resources if not r["is_external"] and r["available"]]
    order = registry.select()
    # HONEST active-resolution: the resource that will actually serve the next completion, and whether that
    # is a REAL model (local Ollama / external accelerant) or the deterministic native FLOOR (is_model=False,
    # structured reasoning — not an LLM). Surfaced so the Owner can see, at a glance, exactly what is serving.
    active = order[0] if order else "native"
    is_real_model = active != "native"
    active_row = next((r for r in resources if r["name"] == active), None)
    # §6 (W323) — MEASURED serving mode beside the prediction: the selection head can list a model
    # that keeps failing while the floor actually serves — `mode` now follows what the learning
    # loop MEASURED on the most recent recorded work, never just the optimistic prediction.
    # W458 (P1.10, ledger 1.10 · R4.7) — measured from the most recent SUCCESSFUL completion. The
    # per-model aggregate had no notion of "the newest row failed": one config-disabled local
    # attempt made `measured` = ollama and `mode` = real_model while the floor served everything.
    measured = None
    _last_at = None
    _failed_since = 0
    try:
        from agentic_core.api.operational_excellence import last_successful_server
        _last = last_successful_server()
        measured = _last.get("served_by")
        _last_at = _last.get("at")
        _failed_since = int(_last.get("attempts_since") or 0)
    except Exception:
        pass
    mode_predicted = "real_model" if is_real_model else "deterministic_floor"
    mode_measured = ("unmeasured" if measured is None
                     else ("deterministic_floor" if measured == "native" else "real_model"))
    return {
        "posture": "in-house-first",
        "external_allowed": external_allowed(),
        "owned_resources_available": [r["name"] for r in owned],
        "selection_order": order,
        "active_model": active,
        "active_model_label": (active_row or {}).get("model", active),
        "is_real_model": is_real_model,
        "mode": mode_measured if mode_measured != "unmeasured" else mode_predicted,
        "mode_predicted": mode_predicted,
        "mode_measured": mode_measured,
        "measured_recent_server": measured,
        "mode_note": ("mode follows the most recent completion that actually SERVED (a successful "
                      "recorded row) when history exists, prediction only until then — the two disagree "
                      "when a listed model keeps failing, or is disabled by configuration and skipped"),
        # §6 (W424, corrected W458) — `floor_active` answers "what served last", NOT "what is serving
        # now": it is derived from ONE row, and since W458 that row is the most recent SUCCESSFUL
        # completion (a failed or never-attempted resource no longer counts as having served). The row
        # travels with the verdict in `floor_active_basis`, so the claim is checkable on screen.
        "floor_active": (mode_measured == "deterministic_floor" if mode_measured != "unmeasured"
                         else not is_real_model),
        "floor_active_basis": (
            ("most recent SUCCESSFUL recorded completion was served by " + str(measured)
             + " (one row, at " + str(_last_at) + ")"
             + (f"; {_failed_since} failed attempt(s) recorded since" if _failed_since else "")
             + " — this is history, not a live probe; a resource disabled by configuration is skipped, not counted")
            if measured is not None else
            "no successful completion has been recorded yet; predicted from whether a real model is listed"),
        "floor_note": (None if is_real_model else
                       "The deterministic native floor is serving — honest structured reasoning, NOT an LLM. "
                       "Run a local Ollama model (or enable an external accelerant) for generative prose."),
        "guarantee": "Workstation always produces a real, structured result from its OWN resources "
                     "with NO external dependency; external providers are optional accelerants "
                     "(flag-gated by AI_ALLOW_EXTERNAL).",
        "resources": resources,
    }


@router.get("/homeostasis")
async def native_homeostasis():
    """§8→§6: the live biomimetic homeostatic posture governing the native AI fabric — how the living
    organism's state (immune · circadian · metabolic ATP · composite health) currently modulates how much
    cognitive work the swarm/tree will admit. Real organism state; cognition also feeds ATP back (closed loop)."""
    from agentic_core.ai.native.homeostasis import homeostasis
    return homeostasis.snapshot()


@router.get("/resources")
@_states_level("/resources")
async def native_resources():
    return {"resources": registry.available(), "selection_order": registry.select()}


@router.get("/inventory")
@_states_level("/inventory")
async def native_inventory():
    """FU-618 — WHAT RESOURCES EXIST AND WHAT STATE EACH IS IN, in one read-only answer.

    Composed from the producers that already exist; nothing is stored or recomputed here. Each block names
    what KIND of statement it is (measured now / declared by the registry / simulated / not known), because
    the optimizer's capacity baseline is a labelled simulation and the machine block is a measurement, and a
    reader must not take one for the other. A producer that cannot answer is `known: False` with the reason:
    not known is not the same as none.
    """
    def _block(kind: str, basis: str, produce):
        try:
            return {"known": True, "basis_kind": kind, "basis": basis, "data": produce()}
        except Exception as exc:                                    # noqa: BLE001 - said, never swallowed
            return {"known": False, "basis_kind": "not_known", "data": None,
                    "basis": f"NOT KNOWN - this producer could not answer ({type(exc).__name__}: "
                             f"{str(exc)[:120]}). Not the same as none."}

    from agentic_core.ai.native import tiers as _tiers

    def _fabric():
        from agentic_core.api.resource_fabric import _REGISTRY
        classes: Dict[str, int] = {}
        for r in _REGISTRY:
            classes[r["resource_class"]] = classes.get(r["resource_class"], 0) + 1
        return {"total": len(_REGISTRY), "by_class": classes}

    def _optimizer():
        from agentic_core.optimizer.fabric import DynamicResourceFabric
        return DynamicResourceFabric().get_inventory_status()

    def _homeostasis():
        from agentic_core.ai.native.homeostasis import homeostasis
        return homeostasis.snapshot()

    return {
        "machine": _block("measured", "read from this machine at call time; each field carries its own "
                          "source in the data", _tiers.machine),
        "tiers": _block("measured", "each tier's `runnable here` is decided from the machine block above and "
                        "the local model runtime, at call time", _tiers.registry),
        "models": _block("declared", "the model resource registry: what is configured and reachable; "
                         "`available` is checked at call time, the model names are configuration",
                         lambda: {"resources": registry.available(), "selection_order": registry.select()}),
        "fabric": _block("declared", "the Resource Fabric's registered resources, counted by class; a count "
                         "of what is registered, not of what has run", _fabric),
        "homeostasis": _block("measured", "the organism's current admission posture for cognitive work",
                              _homeostasis),
        "optimizer_baseline": _block("simulated", "a single-node SIMULATED capacity baseline with no real "
                                     "quota behind it - not a measurement of this machine; the machine "
                                     "block is", _optimizer),
        "read_only": True,
        "note": ("composed from existing producers; this route stores nothing and allocates nothing. People "
                 "are not a resource class here."),
    }


@router.get("/tiers")
@_states_level("/tiers")
async def native_tiers():
    """The five declared tiers, each with whether it is RUNNABLE HERE and the MEASURED reason (P3.20).

    The machine is measured at call time rather than recorded: a figure typed into a file would go stale
    the day the hardware changes and would then be a claim about a machine nobody re-measured. A tier
    that is not runnable carries what it needs, what this machine has, and the difference — and it holds
    NO resources, because listing a model the machine cannot run is the same defect as a leaderboard
    nothing scored.
    """
    from agentic_core.ai.native.tiers import registry as _tier_registry
    return _tier_registry()


@router.get("/route")
@_states_level("/route")
async def native_route(domain: str = "", risk: str = "normal"):
    """Which tier would serve this, and WHY — including every tier rejected on the way down.

    The walk starts at the tier the request WANTS and descends to the deterministic floor, which always
    terminates it. So this refuses a TIER, never the request, and the rejections are the useful half of
    the answer: a caller can see that a grave domain was not routed to a model, or that a tier was
    skipped because this machine is 4.31 GB short of what it needs.
    """
    from agentic_core.ai.native.tiers import route as _route
    return _route(domain, risk)


@router.get("/models")
@_states_level("/models")
async def native_models():
    """The OWNED model resources, with the local models actually discovered on the Ollama server — each
    selectable by name (model='ollama:<name>'). The native deterministic floor is always available."""
    from agentic_core.ai.native.model_resource import local_models
    discovered = local_models()
    tiers = [{"id": "auto", "label": "Auto (in-house-first)", "kind": "policy"},
             {"id": "native", "label": "Native floor (deterministic)", "kind": "native"}]
    if discovered:
        tiers.append({"id": "local", "label": "Local model (default)", "kind": "local"})
        tiers += [{"id": f"ollama:{m}", "label": m, "kind": "local"} for m in discovered]
    from agentic_core.ai.native.model_resource import effective_default_local, lifecycle_state
    _st = lifecycle_state()
    return {"local_models": discovered,
            "default_local": effective_default_local() if discovered else None,
            "promoted_default": _st.get("default_local"), "retired": _st.get("retired") or [],
            "tiers": tiers,
            "store_incomplete": _st.get("store_incomplete"),          # W577 (FU-298)
            "retired_is_incomplete": bool(_st.get("store_incomplete")),
            "note": "Owned models. Route a completion to any with model=<id>. External providers are opt-in "
                    "accelerants (AI_ALLOW_EXTERNAL); the native floor is always available."}


# ── Owned-model LIFECYCLE (W276) — evaluate · promote · retire · reinstate ──────────────────────
class LifecycleModelRequest(BaseModel):
    model: str


def _ueg_lifecycle(action: str, model: str, extra: Dict[str, Any] | None = None) -> None:
    try:
        from agentic_core.gaas.v5 import UEGLogger
        UEGLogger().log({"type": f"native_ai.model.{action}", "model": model, **(extra or {})})
    except Exception:
        pass


def _lifecycle_for_write() -> Dict[str, Any]:
    """The lifecycle record read STRICTLY, for the four routes that write it back.

    W577 (FU-395) — all four took the TOLERANT read and handed it to `save_lifecycle`. A tolerant
    read returns the store's first complete JSON value and discards the rest, so a write on that base
    persists the prefix. On this particular record the consequence is sharp: `retire_model` appends to
    `st["retired"]` and saves, so a dropped prefix would have UN-RETIRED every other model while
    reporting that one had been retired. Refusing is the only answer that cannot lose a retirement.
    """
    from fastapi import HTTPException
    from agentic_core.ai.native.model_resource import lifecycle_state
    from agentic_core.config import StoreUnavailable
    try:
        return lifecycle_state(strict=True)
    except StoreUnavailable as e:
        raise HTTPException(
            status_code=503,
            detail=f"{e}; the model lifecycle was NOT changed, so no promotion, retirement or "
                   f"evaluation already recorded has been lost") from None


def _serving_basis(effective, promoted, configured, estate) -> str:
    """W492 - what serves, and why, from the two names and the estate that were actually read."""
    if effective:
        return (f"{effective} is installed and serves local calls"
                + (" (promoted)" if effective == promoted else " (from OLLAMA_MODEL)"))
    absent = [n for n in (promoted, configured) if n and n not in set(estate or [])]
    if not estate:
        return ("no local model is installed, so the deterministic native floor serves"
                + (f"; {', '.join(absent)} configured but absent" if absent else
                   "; none is configured either"))
    return ("the native floor serves: "
            + (f"{', '.join(absent)} is named but not in the installed estate "
               f"({', '.join(estate)})" if absent else
               f"no default is named, though {', '.join(estate)} is installed"))


@router.get("/lifecycle")
@_states_level("/lifecycle")
async def model_lifecycle():
    """§6 (W276) — the owned-model estate's lifecycle state: the promoted serving default, retired
    models, the active estate default orchestration draws on, and recent evaluations."""
    from agentic_core.ai.native.model_resource import (lifecycle_state, effective_default_local,
                                                       configured_default_local,
                                                       active_local_models, local_models)
    st = lifecycle_state()
    _eff = effective_default_local()
    _estate = active_local_models()
    # W492 (FU-183) — /models already guarded this ("default_local" only when something is discovered);
    # /lifecycle did not, so it published the OLLAMA_MODEL fallback NAME as the serving default with an
    # empty estate. What is configured and what serves are two facts, and the answer says which is which.
    return {"promoted_default": st.get("default_local"),
            "effective_default": _eff,
            "configured_default": configured_default_local(),
            "serves": ("local_model" if _eff else "native_floor"),
            # W492 (refutation) - this asserted "<model> is installed and serves" for a PROMOTED model
            # that had been uninstalled, and said "no local model is installed" when the estate was
            # non-empty but neither the promoted nor the configured name was in it. Both facts are read.
            "serving_basis": _serving_basis(_eff, st.get("default_local"),
                                            configured_default_local(), _estate),
            "retired": st.get("retired") or [],
            "discovered": local_models(), "active_estate": _estate,
            "evaluations": (st.get("evaluations") or [])[-10:],
            # W577 (FU-298) — an empty `retired` and an UNREADABLE record of retirements render the
            # same. That matters here more than on a listing: a reader concluding "no model has been
            # retired" may reinstate or route to one that was. The direction is stated, because the
            # retirements that could not be read are the ones missing from the list.
            "store_incomplete": st.get("store_incomplete"),
            "retired_is_incomplete": bool(st.get("store_incomplete")),
            "retired_basis": ("the lifecycle record could not be read whole, so a model that WAS "
                              "retired may be absent from this list"
                              if st.get("store_incomplete")
                              else "every retirement in the lifecycle record")}


#  W641 (P3.32) - THE PROBE SET IS A NAMED, VERSIONED THING. It was three tuples typed inside the handler, so
#  an evaluation carried no statement of WHAT it had been run against and a changed probe was invisible: two
#  results months apart looked comparable and need not have been. A change here is a NEW VERSION, never an
#  edit - the digest below is stored on every evaluation and a guard pins version to digest.
_EVAL_PROBE_SET_VERSION = "2"
_EVAL_PROBES = [
    {"id": "structure", "control": False, "marker": "## Risks",
     "prompt": "Reply with exactly two sections:\n## Summary\n## Risks\nTopic: a halal meal-kit venture."},
    {"id": "instruction", "control": False, "marker": "-",
     "prompt": "List exactly three bullet points, each under 10 words, on safe data handling."},
    {"id": "reasoning", "control": False, "marker": "60",
     "prompt": "A VSB earns 100 WST and its costs are 40 WST. State the surplus and ONE prudent use for it.\n## Answer"},
    #  THE CONTROL: a reply to this must NOT contain the structure probe's marker. A model that echoes its
    #  prompt, or sprays headings on everything, hits every marker above and fails here - which is the only
    #  thing in this set that can tell a marker hit from a model that says the marker regardless.
    {"id": "control", "control": True, "marker": "## Risks",
     "prompt": "Reply with the single word: ready"},
]


def _eval_probe_digest() -> str:
    import hashlib as _h
    import json as _j
    return _h.sha256(_j.dumps(_EVAL_PROBES, sort_keys=True).encode("utf-8")).hexdigest()[:16]


#  P3.32 (round 8) - A VERSION IS PINNED TO ITS DIGEST, HERE, AND THE TABLE IS APPEND-ONLY. The comment above
#  said "a guard pins version to digest"; the guard recomputed the digest from the probes it was checking, so
#  a probe edited WITHOUT a new version number stayed green and two records under one version were no longer
#  comparable. A change to the set is a new key in this table. An entry already here is never altered: the
#  guard holds each recorded version to the digest written beside it. (Version "1" was three tuples typed in
#  the handler; its digest was never recorded and is not invented here.)
_EVAL_PROBE_SET_HISTORY = {
    "2": "4917359cd4051532",
}


def _probe_set_state() -> Dict[str, Any]:
    """Whether the probe set in memory IS the set its version number names. Read at each call."""
    ver, now = _EVAL_PROBE_SET_VERSION, _eval_probe_digest()
    pinned = _EVAL_PROBE_SET_HISTORY.get(ver)
    if pinned is None:
        return {"ok": False, "version": ver, "digest": now, "pinned": None,
                "why": (f"probe set version {ver} has no pinned digest, so a record under it would name a "
                        f"set nothing can check. Add the version and its digest to the history table.")}
    if pinned != now:
        return {"ok": False, "version": ver, "digest": now, "pinned": pinned,
                "why": (f"the probe set was edited under version {ver}: its digest is now {now} and the "
                        f"digest pinned for that version is {pinned}. A changed case set is a new version, "
                        f"never an edit.")}
    return {"ok": True, "version": ver, "digest": now, "pinned": pinned, "why": None}


def _require_pinned_probe_set() -> Dict[str, Any]:
    st = _probe_set_state()
    if not st["ok"]:
        raise HTTPException(status_code=409, detail=st["why"] + " Nothing was run and nothing was recorded.")
    return st


#  P3.32 (round 8; Owner ruling 2026-10-11) - THE HELD-OUT CASES. "Held-out" means never shown in any prompt
#  or document: they live in their own file, are read from it at each call, and are pinned by version to a
#  digest exactly as the public set is. No route returns a held-out PROMPT; a baseline record carries the
#  case id, the reply and the verdict. Nothing reads a held-out result to decide anything (promotion,
#  routing and selection do not open the baseline store).
_HELDOUT_HISTORY = {
    "1": "763a1d22466ec97b",
}


def _heldout_path():
    import pathlib as _pl
    return _pl.Path(__file__).resolve().parents[1] / "ai" / "native" / "heldout_cases.json"


def _heldout_digest(cases) -> str:
    import hashlib as _h
    import json as _j
    return _h.sha256(_j.dumps(cases, sort_keys=True).encode("utf-8")).hexdigest()[:16]


def _load_heldout() -> Dict[str, Any]:
    """The held-out set, read now: {ok, version, digest, cases} or {ok: False, why}. Never a partial set."""
    import json as _j
    try:
        doc = _j.loads(_heldout_path().read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {"ok": False, "version": None, "digest": None, "cases": [],
                "why": "the held-out case file is not present, so no held-out case can be run"}
    except (OSError, ValueError) as e:
        return {"ok": False, "version": None, "digest": None, "cases": [],
                "why": f"the held-out case file could not be read ({e.__class__.__name__})"}
    ver = str((doc or {}).get("version") or "") if isinstance(doc, dict) else ""
    cases = (doc or {}).get("cases") if isinstance(doc, dict) else None
    well_formed = (isinstance(cases, list) and cases and all(
        isinstance(c, dict) and all(isinstance(c.get(k), str) and c.get(k).strip() for k in ("id", "marker", "prompt"))
        for c in cases) and len({c["id"] for c in cases}) == len(cases))
    if not ver or not well_formed:
        return {"ok": False, "version": ver or None, "digest": None, "cases": [],
                "why": "the held-out case file does not hold a version and a list of {id, marker, prompt} cases"}
    now, pinned = _heldout_digest(cases), _HELDOUT_HISTORY.get(ver)
    if pinned is None:
        return {"ok": False, "version": ver, "digest": now, "cases": [],
                "why": f"held-out set version {ver} has no pinned digest"}
    if pinned != now:
        return {"ok": False, "version": ver, "digest": now, "cases": [],
                "why": (f"the held-out set was edited under version {ver}: its digest is now {now} and the "
                        f"digest pinned for that version is {pinned}. A changed case set is a new version, "
                        f"never an edit.")}
    return {"ok": True, "version": ver, "digest": now, "cases": cases, "why": None}


def _require_heldout() -> Dict[str, Any]:
    held = _load_heldout()
    if not held["ok"]:
        raise HTTPException(status_code=409, detail=held["why"] + " Nothing was run and nothing was recorded.")
    return held


_EXPOSURE_SKIP_DIRS = frozenset({".git", "node_modules", "__pycache__", "venv", ".venv", "dist", "build",
                                 ".pytest_cache", ".mypy_cache"})
_EXPOSURE_SUFFIXES = (".py", ".md", ".txt", ".json", ".ts", ".tsx", ".js", ".jsx", ".yaml", ".yml", ".html",
                      ".toml", ".cfg", ".ini", ".j2", ".jinja", ".prompt", ".csv", ".rst")
_EXPOSURE_MAX_BYTES = 32 * 1024 * 1024


def heldout_exposure(roots, cases=None, return_paths: bool = False) -> Dict[str, Any]:
    """Every text file under `roots` that contains a held-out case's prompt. AN INSTRUMENT, WITH ITS SCOPE.

    A case is "contained" when the file's text, lower-cased and with runs of whitespace collapsed, holds the
    whole prompt or its opening or closing 48 characters treated the same way. The held-out file itself is
    excluded by path and named under `excluded`. What this does NOT see: a paraphrase, a translation, a
    prompt split across files, a file whose suffix is not in the list, a file over the size limit (named
    under `skipped`), and anything outside `roots`. Zero hits means "none of these cases was found in N
    files"; it is not a statement about files this did not open."""
    import os as _os
    import pathlib as _pl

    def _n(s: str) -> str:
        return " ".join(str(s).lower().split())

    if cases is None:
        cases = _load_heldout().get("cases") or []
    needles = []
    for c in cases:
        p = _n(c.get("prompt", ""))
        if len(p) < 24:
            continue                      # too short to search for without matching ordinary prose
        for frag in {p, p[:48], p[-48:]}:
            needles.append((c.get("id"), frag))
    own = _heldout_path().resolve()
    examined, hits, skipped, excluded, paths = 0, [], [], [], []
    for root in roots:
        root = _pl.Path(root)
        walker = ([(str(root.parent), [], [root.name])] if root.is_file() else _os.walk(root))
        for dirpath, dirnames, filenames in walker:
            dirnames[:] = [d for d in dirnames if d not in _EXPOSURE_SKIP_DIRS]
            for fn in filenames:
                fp = _pl.Path(dirpath) / fn
                if not fn.lower().endswith(_EXPOSURE_SUFFIXES):
                    continue
                try:
                    if fp.resolve() == own:
                        excluded.append(str(fp))
                        continue
                    if fp.stat().st_size > _EXPOSURE_MAX_BYTES:
                        skipped.append({"file": str(fp), "why": "over the size limit"})
                        continue
                    text = _n(fp.read_text(encoding="utf-8", errors="replace"))
                except OSError as e:
                    skipped.append({"file": str(fp), "why": e.__class__.__name__})
                    continue
                examined += 1
                if return_paths:
                    paths.append(str(fp))
                found = sorted({cid for cid, frag in needles if frag in text})
                for cid in found:
                    hits.append({"file": str(fp), "case": cid})
    out = {"files_examined": examined, "cases_searched": len({cid for cid, _ in needles}),
           "hits": hits, "skipped": skipped, "excluded": excluded,
           "scope": [str(r) for r in roots],
           "basis": (f"{len(hits)} occurrence(s) of a held-out prompt in {examined} text file(s) under the "
                     f"stated roots; {len(skipped)} file(s) could not be examined. A paraphrase is not seen.")}
    if return_paths:
        out["paths"] = paths
    return out


_EVAL_BASIS = ("a marker hit means the reply CONTAINS a marker string - it is not a judgement that the reply is "
               "correct. One run per probe, no held-out probe, and the probes are public in the source, so this "
               "is a smoke check of behaviour (evidence level 1: inputs and outputs). Nothing here inspects or "
               "compares a model's internal state.")


@router.post("/lifecycle/evaluate")
async def evaluate_model(req: LifecycleModelRequest):
    """§6 (W276) — run a bounded, HONEST evaluation of a named local model: three small probes
    routed explicitly to it. Scored only on what genuinely happened (did the target actually
    serve · non-empty output · requested structure present · latency); when the model cannot
    serve, that is the result — never a fabricated score. Attempts feed the W275 health window."""
    import time as _t
    _require_pinned_probe_set()            # P3.32 - a set edited under its version is refused, nothing asked
    probes = [(p["id"], p["prompt"], p["marker"]) for p in _EVAL_PROBES if not p["control"]]
    results = []
    served_target = 0
    for pid, prompt, marker in probes:
        _p0 = _t.time()
        r = await orchestrator.complete(prompt, agent=f"eval:{req.model}",
                                        prefer=f"ollama:{req.model}", timeout=20.0)
        on_target = r.get("served_by") == f"ollama:{req.model}"
        served_target += 1 if on_target else 0
        results.append({"probe": pid, "served_by": r.get("served_by"), "on_target": on_target,
                        "non_empty": bool((r.get("output") or "").strip()),
                        "structure_hit": marker.lower() in (r.get("output") or "").lower(),
                        #  P3.32 - THE REPLY IS KEPT, so a probe that missed can be re-read
                        **_reply_record(r.get("output")),
                        "ms": int((_t.time() - _p0) * 1000)})
    can_serve = served_target == len(probes)
    score = (round(sum(1.0 for x in results if x["structure_hit"]) / len(results), 2)
             if can_serve else None)   # honest: no score when the target never served
    #  W641 - the control runs only when the target can serve (otherwise the floor would answer it), and its
    #  result is its own field: `score` keeps the meaning its two readers know.
    control = None
    if can_serve:
        _c = next(p for p in _EVAL_PROBES if p["control"])
        _cr = await orchestrator.complete(_c["prompt"], agent=f"eval:{req.model}",
                                          prefer=f"ollama:{req.model}", timeout=20.0)
        _on = _cr.get("served_by") == f"ollama:{req.model}"
        control = {"probe": _c["id"], "on_target": _on,
                   "marker_absent": (_c["marker"].lower() not in (_cr.get("output") or "").lower()) if _on else None,
                   **_reply_record(_cr.get("output")),
                   "basis": ("the reply must NOT contain the structure probe's marker; a model that says it "
                             "regardless fails here" if _on else
                             "the target did not serve the control, so it says nothing either way")}
    from agentic_core.ai.native.model_resource import save_lifecycle
    st = _lifecycle_for_write()                              # W577 (FU-395)
    evaluation = {"model": req.model, "can_serve": can_serve, "score": score,
                  #  W641 - what the number is, what it was run against, and what it does not establish
                  "marker_hits": sum(1 for x in results if x["structure_hit"]) if can_serve else None,
                  "probes_total": len(results), "control": control,
                  "probe_set": {"version": _EVAL_PROBE_SET_VERSION, "digest": _eval_probe_digest()},
                  #  P3.32 - beside it, never inside it: `probe_set` keeps the two keys its readers compare
                  "probe_set_pinned": True,
                  "serving": _serving_identity(f"ollama:{req.model}"),
                  "evidence_level": "behaviour", "basis": _EVAL_BASIS,
                  "probes": results, "at": __import__("time").strftime("%Y-%m-%dT%H:%M:%SZ",
                                                                       __import__("time").gmtime())}
    st["evaluations"].append(evaluation)
    save_lifecycle(st)
    _ueg_lifecycle("evaluated", req.model, {"can_serve": can_serve, "score": score})
    return evaluation


# -- P3.32 (round 8) - THE BEHAVIOURAL BASELINE: PER SERVING TIER, ON DEMAND, A RECORD THAT CAN BE RE-READ --
#  What it is: the public probe set and the held-out set put to ONE owned serving tier, each reply kept with
#  its hash, each case ending passed / failed / not read, the whole thing stored with the case-set versions
#  and whatever identity the tier has. What it is not: a judgement that a reply is correct, a comparison of
#  two models, or anything about a model's insides. OWNER (2026-10-11): it runs when a person asks for it and
#  at no other time - nothing in the organism's beat, the startup path or a read route calls it.
_BASELINE_TIMEOUT_S = 20.0
_BASELINE_REPLY_KEEP = 600
_BASELINE_BASIS = ("one run per case against one serving tier. 'passed' means the reply CONTAINS the case's "
                   "marker string (for the control: does NOT contain it) - it is not a judgement that the "
                   "reply is correct. A case the tier did not serve is 'not read' and counts as neither. "
                   "Evidence level 1: inputs and outputs only. Run on demand; nothing schedules it.")


def _read_floor_identity():
    #  READ ONCE, AT IMPORT (the lesson of instrument_cell._HANDLER_IDS): at import the file on disk and the
    #  loaded engine are the same thing; on a long-running process they need not be.
    try:
        import hashlib as _h
        from agentic_core.ai.native import engine as _engine
        with open(_engine.__file__, "rb") as _f:
            return _h.sha256(_f.read().replace(b"\r\n", b"\n")).hexdigest()[:16]
    except Exception:                                    # noqa: BLE001 - said on the record as not recorded
        return None


_FLOOR_IDENTITY = _read_floor_identity()


def _local_model_digest(name: str):
    """The digest the local runtime reports for a pulled model name, or None. Read, never guessed."""
    if os.getenv("AI_DISABLE_LOCAL", "").lower() in ("1", "true", "yes"):
        return None
    try:
        import httpx
        from agentic_core.ai.native.model_resource import _ollama_base
        r = httpx.get(f"{_ollama_base()}/api/tags", timeout=1.0)
        if r.status_code != 200:
            return None
        for m in (r.json().get("models") or []):
            n = str(m.get("name") or "")
            if n == name or n == f"{name}:latest":
                return m.get("digest") or None
    except Exception:                                    # noqa: BLE001
        return None
    return None


def _serving_identity(tier: str) -> Dict[str, Any]:
    """WHAT a run was served by, as far as that can be known. A name is not an identity: a local tag can be
    pulled again to a different build, so a run that records only the name cannot be reproduced from it."""
    settings = {"prefer": tier, "timeout_s": _BASELINE_TIMEOUT_S,
                "sampling": "not set by this route: the runtime's own defaults apply and are not recorded"}
    if tier == "native":
        return {"tier": tier, "kind": "deterministic_floor", "identity": _FLOOR_IDENTITY,
                "identity_kind": "source_sha256" if _FLOOR_IDENTITY else None,
                "identity_basis": ("the sha256 of the floor engine's own source file as loaded when this "
                                   "process started (line endings normalised). It does not cover modules "
                                   "that file imports" if _FLOOR_IDENTITY else
                                   "IDENTITY NOT RECORDED: the floor engine's source could not be read"),
                "settings": {**settings, "sampling": "none: the floor samples nothing"}}
    dg = _local_model_digest(tier.split(":", 1)[1])
    return {"tier": tier, "kind": "local_model", "identity": dg,
            "identity_kind": "runtime_digest" if dg else None,
            "identity_basis": ("the digest the local runtime reported for this model name at the time of the run"
                               if dg else
                               "MODEL IDENTITY NOT RECORDED: the local runtime reported no digest for this "
                               "name, so this run names a model and not a build of it. A later run under the "
                               "same name is not known to be the same model"),
            "settings": settings}


def _reply_record(text) -> Dict[str, Any]:
    """A reply KEPT: a bounded excerpt, its full length, and the hash of the whole of it."""
    import hashlib as _h
    t = text if isinstance(text, str) else ""
    return {"reply_excerpt": t[:_BASELINE_REPLY_KEEP], "reply_chars": len(t),
            "reply_truncated": len(t) > _BASELINE_REPLY_KEEP,
            "reply_sha256": _h.sha256(t.encode("utf-8")).hexdigest()}


def _withheld_if_repeats(set_name: str, prompt: str, reply) -> Dict[str, Any]:
    """A HELD-OUT case stays held out even when the tier repeats it back. A reply that contains the case's
    prompt (whole, or its opening or closing 48 characters, case and spacing ignored) is kept as its hash and
    length only; the excerpt is withheld and the record says so. A public case's reply is always kept."""
    if set_name != "heldout":
        return {}

    def _n(s) -> str:
        return " ".join(str(s or "").lower().split())
    p, r = _n(prompt), _n(reply)
    if p and (p in r or p[:48] in r or p[-48:] in r):
        return {"reply_excerpt": "",
                "reply_withheld": ("the reply repeats the held-out prompt, so its text is not kept here; its "
                                   "hash and length are. Showing it would show the case")}
    return {}


def _baseline_store():
    from agentic_core.config import data_path
    return data_path("model_baselines.json")


def _baselines_for_write() -> List[Dict[str, Any]]:
    from agentic_core.config import StoreUnavailable, read_json_strict
    try:
        return read_json_strict(_baseline_store(), list, expect=list)
    except StoreUnavailable as e:
        raise HTTPException(status_code=503,
                            detail=f"{e}; no baseline was run and no baseline record was changed") from None


def _baseline_tier(tier: str) -> str:
    t = str(tier or "").strip()
    if t == "native" or (t.startswith("ollama:") and t.split(":", 1)[1].strip()):
        return t
    raise HTTPException(status_code=422, detail=(
        "a baseline is run against an OWNED serving tier: 'native' (the deterministic floor) or "
        "'ollama:<name>' (a local model). 'auto' and 'local' name a policy rather than a tier, and an "
        "external provider is never baselined here. Nothing was run."))


def _case_sets(held: Dict[str, Any]) -> Dict[str, Any]:
    return {"public": {"version": _EVAL_PROBE_SET_VERSION, "digest": _eval_probe_digest(),
                       "cases": len(_EVAL_PROBES)},
            "heldout": {"version": held["version"], "digest": held["digest"], "cases": len(held["cases"])}}


async def _baseline_record(tier: str, held: Dict[str, Any], serving: Dict[str, Any]) -> Dict[str, Any]:
    import time as _t
    import uuid as _u
    rows: List[Dict[str, Any]] = []
    for set_name, cases in (("public", _EVAL_PROBES), ("heldout", held["cases"])):
        for c in cases:
            _p0 = _t.time()
            r = await orchestrator.complete(c["prompt"], agent=f"baseline:{tier}", prefer=tier,
                                            timeout=_BASELINE_TIMEOUT_S)
            reply = r.get("output") or ""
            on = r.get("served_by") == tier
            present = str(c["marker"]).lower() in reply.lower()
            is_control = bool(c.get("control"))
            rows.append({"case": c["id"], "set": set_name, "control": is_control,
                         "served_by": r.get("served_by"), "on_target": on,
                         "non_empty": bool(reply.strip()), "marker_present": present,
                         "passed": ((not present) if is_control else present) if on else None,
                         "passed_basis": (("the control: its reply must NOT contain the marker" if is_control
                                           else "its reply must contain the marker") if on else
                                          f"not read: {r.get('served_by')} answered this case, not {tier}, "
                                          f"so the reply says nothing about {tier}"),
                         **_reply_record(reply), **_withheld_if_repeats(set_name, c["prompt"], reply),
                         "ms": int((_t.time() - _p0) * 1000)})
    counts = {"passed": sum(1 for x in rows if x["passed"] is True),
              "failed": sum(1 for x in rows if x["passed"] is False),
              "not_read": sum(1 for x in rows if x["passed"] is None)}
    served_target = bool(rows) and all(x["on_target"] for x in rows)
    others = sorted({str(x["served_by"]) for x in rows if not x["on_target"]})
    return {"run_id": f"bl-{_u.uuid4().hex[:10]}",
            "at": _t.strftime("%Y-%m-%dT%H:%M:%SZ", _t.gmtime()), "trigger": "on_demand",
            "tier": tier, "serving": serving, "case_sets": _case_sets(held),
            "cases": rows, "served_target": served_target, "counts": counts,
            "established": ((f"what {tier} replied to {len(rows)} case(s) on this run: {counts['passed']} "
                             f"passed their marker rule and {counts['failed']} did not")
                            if served_target else
                            (f"NOT ESTABLISHED for {tier}: {counts['not_read']} of {len(rows)} case(s) were "
                             f"answered by {', '.join(others) or 'nothing'}. Those replies are kept and say "
                             f"nothing about {tier}")),
            "evidence_level": "behaviour", "basis": _BASELINE_BASIS}


def _baseline_append(record: Dict[str, Any]) -> None:
    from agentic_core.config import atomic_write_json, store_lock
    with store_lock(_baseline_store()):
        rows = _baselines_for_write()
        rows.append(record)
        atomic_write_json(_baseline_store(), rows)       # nothing is dropped: a baseline is evidence


class BaselineRequest(BaseModel):
    tier: str = "native"


@router.post("/baseline/run")
async def run_baseline(req: BaselineRequest):
    """Run the behavioural baseline against ONE owned serving tier, now, because a person asked.

    Refused before anything is asked of a model: a tier that is not owned (422), a case set edited under
    its version (409), a held-out file that is missing or edited (409), a baseline store that cannot be
    read whole (503). A tier that does not SERVE is not a refusal: the run is recorded with every case
    'not read', because that the tier could not answer is itself the result."""
    tier = _baseline_tier(req.tier)
    _require_pinned_probe_set()
    held = _require_heldout()
    _baselines_for_write()                               # refuse BEFORE spending a call on a store we cannot write
    record = await _baseline_record(tier, held, _serving_identity(tier))
    _baseline_append(record)
    _ueg_lifecycle("baseline_run", tier, {"run_id": record["run_id"], "served_target": record["served_target"],
                                          "counts": record["counts"]})
    return record


@router.get("/baseline")
async def list_baselines(tier: str | None = None, limit: int = 20):
    """The baseline records, newest first, and - per owned serving tier - whether one exists at all.
    A read: it runs nothing."""
    from agentic_core.ai.native.model_resource import local_models
    from agentic_core.config import read_json_reported
    _all, _why = read_json_reported(_baseline_store(), [])
    rows = [r for r in (_all if isinstance(_all, list) else []) if isinstance(r, dict)]
    owned = ["native"] + [f"ollama:{m}" for m in local_models()]
    known = owned + sorted({str(r.get("tier")) for r in rows if r.get("tier") and r.get("tier") not in owned})
    tiers = []
    for t in known:
        mine = [r for r in rows if r.get("tier") == t]
        _tried = [r for r in mine if isinstance(r.get("reproduction"), dict)]
        _same = [r for r in _tried if r["reproduction"].get("reproduced") is True]
        tiers.append({"tier": t, "serves_now": t in owned, "runs": len(mine),
                      "reproduction_attempts": len(_tried), "reproduced_runs": len(_same),
                      "reproducibility": (
                          (f"SHOWN {len(_same)} time(s) for this tier: a re-run from the recorded versions gave "
                           f"byte-identical replies"
                           + (f"; {len(_tried) - len(_same)} other re-run(s) did not" if len(_tried) > len(_same) else ""))
                          if _same else
                          (f"NOT SHOWN for this tier: {len(_tried)} re-run(s) were made and none gave "
                           f"byte-identical replies") if _tried else
                          "NOT SHOWN for this tier: no baseline of it has been run again"),
                      "latest_run_id": mine[-1].get("run_id") if mine else None,
                      "basis": ((f"{len(mine)} baseline run(s) recorded; the latest is "
                                 f"{mine[-1].get('run_id')} at {mine[-1].get('at')}") if mine else
                                "NO BASELINE has been run for this tier")
                               + ("" if t in owned else ". This tier is not discovered now")})
    shown = [r for r in rows if tier is None or r.get("tier") == tier]
    held = _load_heldout()
    _rep_for = [t["tier"] for t in tiers if t["reproduced_runs"]]
    return {"runs": list(reversed(shown[-max(1, min(int(limit), 100)):])), "total": len(shown), "tiers": tiers,
            "store_incomplete": _why, "listing_is_incomplete": bool(_why),
            "listing_basis": ("the baseline store could not be read whole, so runs may be MISSING from this "
                              "list" if _why else "every baseline run in the store"),
            "case_sets_now": {"public": _probe_set_state(),
                              "heldout": {k: held.get(k) for k in ("ok", "version", "digest", "why")}},
            "trigger": "on demand only: POST /api/v1/native-ai/baseline/run. Nothing schedules a baseline.",
            #  P3.32 ACCEPT - WHERE REPRODUCIBILITY HAS BEEN SHOWN, read from the stored re-runs at this call
            "reproducibility_shown_for": _rep_for,
            "reproducibility_basis": (
                ((f"reproducibility has been shown for {', '.join(_rep_for)} and for no other tier"
                  + (" - that is the deterministic floor only; no model's baseline has been reproduced here"
                     if _rep_for == ["native"] else ""))
                 if _rep_for else
                 "reproducibility has been shown for no tier: no stored re-run gave byte-identical replies")
                + ". A baseline record supports a re-run; only a stored re-run shows one"
                + ("; the store could not be read whole, so re-runs may be missing from this count" if _why else "")),
            "evidence_level": "behaviour", "basis": _BASELINE_BASIS}


@router.get("/baseline/{run_id}")
async def get_baseline(run_id: str):
    """One baseline record whole - every case with the reply that was given, so a failed case can be re-read."""
    from agentic_core.config import read_json_reported
    _all, _why = read_json_reported(_baseline_store(), [])
    rec = next((r for r in (_all if isinstance(_all, list) else [])
                if isinstance(r, dict) and r.get("run_id") == run_id), None)
    if rec is None:
        raise HTTPException(status_code=404, detail=(
            f"no baseline run {run_id}" + ("; the store could not be read whole, so it may exist and be "
                                           "unreadable" if _why else "")))
    return rec


@router.post("/baseline/{run_id}/reproduce")
async def reproduce_baseline(run_id: str):
    """Run a recorded baseline AGAIN from the versions it recorded, and say case by case whether the reply
    was the same. Refused - with nothing run - when it cannot be run from those versions: the case sets in
    the code are no longer the ones recorded, the record names no serving identity, or the tier's identity
    now differs. The comparison is of reply hashes; "the same" means byte-identical text."""
    rec = next((r for r in _baselines_for_write() if isinstance(r, dict) and r.get("run_id") == run_id), None)
    if rec is None:
        raise HTTPException(status_code=404, detail=f"no baseline run {run_id}")
    tier = _baseline_tier(rec.get("tier"))
    _require_pinned_probe_set()
    held = _require_heldout()
    if rec.get("case_sets") != _case_sets(held):
        raise HTTPException(status_code=409, detail=(
            f"baseline {run_id} recorded case sets {rec.get('case_sets')} and the code now holds "
            f"{_case_sets(held)}. It can be reproduced only from the versions it recorded. Nothing was run."))
    was = (rec.get("serving") or {}).get("identity")
    serving = _serving_identity(tier)
    if not was:
        raise HTTPException(status_code=409, detail=(
            f"REPRODUCIBILITY CANNOT BE ESTABLISHED for baseline {run_id}: it recorded no serving identity "
            f"for {tier}, so a second run is not known to be of the same thing. Nothing was run."))
    if serving.get("identity") != was:
        raise HTTPException(status_code=409, detail=(
            f"baseline {run_id} was served by identity {was} and {tier} now reports "
            f"{serving.get('identity') or 'no identity'}. A run now would be of a different thing. "
            f"Nothing was run."))
    record = await _baseline_record(tier, held, serving)
    then = {(c.get("set"), c.get("case")): c for c in (rec.get("cases") or []) if isinstance(c, dict)}
    cmp_rows = []
    for c in record["cases"]:
        old = then.get((c["set"], c["case"])) or {}
        cmp_rows.append({"case": c["case"], "set": c["set"],
                         "same_reply": old.get("reply_sha256") == c["reply_sha256"],
                         "same_verdict": old.get("passed") == c["passed"]})
    different = [x["case"] for x in cmp_rows if not x["same_reply"]]
    record["reproduction_of"] = run_id
    record["reproduction"] = {
        "of": run_id, "reproduced": not different, "cases": cmp_rows, "different": different,
        "basis": ((f"all {len(cmp_rows)} replies are byte-identical to those of {run_id}") if not different else
                  (f"{len(different)} of {len(cmp_rows)} replies differ from those of {run_id}: "
                   f"{', '.join(different)}. Same case sets and same recorded identity; the tier did not "
                   f"give the same text"))}
    _baseline_append(record)
    _ueg_lifecycle("baseline_reproduced", tier, {"run_id": record["run_id"], "of": run_id,
                                                 "reproduced": not different})
    return record


# -- P3.32 clause 3 - WHICH LEVEL OF EVIDENCE EACH SURFACE HERE RESTS ON; NONE ABOVE THE FIRST ---------------
#  Two levels exist on this platform and no third: "configuration" (what is configured, declared or
#  reachable - not a statement about behaviour) and "behaviour" (what came back for an input). Every route
#  of this router is in exactly one of the two tables below; a route added without being placed in one is
#  reported by `_unclassified_routes()` and fails the guard.
_EVIDENCE_SURFACES = {
    "/status": ("configuration", "which resource is listed first and which one served the last recorded completion"),
    "/resources": ("configuration", "the model resources configured and whether each is reachable"),
    "/inventory": ("configuration", "what is registered and measured about this machine; each block names its own kind"),
    "/tiers": ("configuration", "the declared tiers and whether this machine can run each"),
    "/route": ("configuration", "which tier a request would be sent to, by rule"),
    "/models": ("configuration", "the local model names the runtime lists"),
    "/lifecycle": ("configuration", "the promoted default and retired names; its `evaluations` are behaviour records"),
    "/lifecycle/promote": ("configuration", "a named model is made the default; nothing about it is measured"),
    "/lifecycle/retire": ("configuration", "a named model is removed from the active list"),
    "/lifecycle/reinstate": ("configuration", "a named model is returned to the active list"),
    "/capabilities": ("configuration", "a catalogue of what is built"),
    "/selfcheck": ("configuration", "whether each backing module imports"),
    "/lifecycle/evaluate": ("behaviour", "replies to the public probe set, by marker"),
    "/baseline/run": ("behaviour", "replies to the public and held-out case sets, by marker"),
    "/baseline": ("behaviour", "the stored baseline records"),
    "/baseline/{run_id}": ("behaviour", "one stored baseline record with its replies"),
    "/baseline/{run_id}/reproduce": ("behaviour", "whether a second run gave byte-identical replies"),
    "/complete": ("behaviour", "one reply and which resource gave it"),
    "/ensemble": ("behaviour", "several replies and which resource gave each"),
    "/swarm": ("behaviour", "a chain of replies and which resource gave each"),
    "/tree": ("behaviour", "a tree of replies and which resource gave each"),
}
_NOT_A_MODEL_STATEMENT = {
    "/homeostasis": "the organism's admission posture, not a statement about a model",
    "/transduce": "arithmetic on a number the caller supplies (a Hill function); its `activation` field is that function's value, not a reading of a model",
    "/topology": "graph arithmetic on caller-supplied nodes and edges",
    "/entropy": "a hash of caller-supplied metadata",
    "/quorum": "threshold arithmetic over a catalogue count",
    "/intent": "a regular-expression classifier",
    "/entailment": "a word-overlap measure",
    "/consensus": "a vote tally over caller-supplied votes",
    "/rigor": "statistics over a caller-supplied series",
    "/validate": "a text-similarity measure against a caller-supplied reference",
    "/decide": "maximin arithmetic over caller-supplied utilities",
    "/evidence-levels": "this inventory",
}
#  P3.32 clause 3 - these five answer with a RECORD (just made, or stored) that carries its own level
_LEVEL_IN_RECORD = frozenset({"/lifecycle/evaluate", "/baseline/run", "/baseline", "/baseline/{run_id}",
                              "/baseline/{run_id}/reproduce"})


def _surfaces_not_stating() -> List[str]:
    """Model-describing routes whose OWN ANSWER does not carry its evidence level. Empty means none."""
    return sorted(p for p in _EVIDENCE_SURFACES if p not in _LEVEL_STATED and p not in _LEVEL_IN_RECORD)


def _unclassified_routes(paths=None) -> List[str]:
    """Routes of this router that are in NEITHER table, and routes that are in both. Empty means none."""
    if paths is None:
        paths = sorted({r.path[len(router.prefix):] for r in router.routes if getattr(r, "path", "")})
    return sorted([p for p in paths if (p in _EVIDENCE_SURFACES) == (p in _NOT_A_MODEL_STATEMENT)])


@router.get("/evidence-levels")
async def evidence_levels():
    """Which level of evidence each surface of this router rests on. Read-only."""
    return {"levels": {"configuration": "what is configured, declared or reachable; not a statement about behaviour",
                       "behaviour": "what came back for an input (level 1). The highest level anything here reaches"},
            "surfaces": [{"path": router.prefix + p, "level": lv, "rests_on": why,
                          "stated_in_its_own_answer": p in _LEVEL_STATED or p in _LEVEL_IN_RECORD}
                         for p, (lv, why) in sorted(_EVIDENCE_SURFACES.items())],
            "not_stating_their_level": [router.prefix + p for p in _surfaces_not_stating()],
            "not_model_statements": [{"path": router.prefix + p, "why": why}
                                     for p, why in sorted(_NOT_A_MODEL_STATEMENT.items())],
            "unclassified": _unclassified_routes(),
            "highest_level": "behaviour",
            #  THE WORDING CHECK, AND WHAT ITS TWO RESULTS MEAN. A phrase list has no third result.
            "claims_check": {"result_words": ["flagged", "nothing matched"],
                             "where": ("a phrase scan the test suite runs over the API, the AI modules and the "
                                       "web app's source. This route does not run it"),
                             "basis": ("a phrase list can FLAG a sentence shaped like a claim about a model's "
                                       "insides. When it flags none the result is 'nothing matched' in the "
                                       "files examined, which does not establish that no surface over-claims")},
            "boundary": ("Level 1 only. The study of a model's insides is not built and not scheduled "
                         "(Owner, 2026-10-10); no route here does it."),
            "scope": "the routes of /api/v1/native-ai. Other routers that mention a model are not inventoried here."}


@router.post("/lifecycle/promote")
@_states_level("/lifecycle/promote")
async def promote_model(req: LifecycleModelRequest):
    """§6 (W276) — promote a DISCOVERED local model to the persisted serving default (the 'ollama'
    resource + gateway serve with it; env OLLAMA_MODEL becomes the fallback). Honest: promoting an
    undiscovered model is refused, not pretended."""
    from fastapi import HTTPException
    from agentic_core.ai.native.model_resource import local_models, lifecycle_state, save_lifecycle
    if req.model not in local_models():
        raise HTTPException(status_code=409, detail=f"Model '{req.model}' is not discovered on the "
                            "local server — pull it first; promotion never pretends.")
    st = _lifecycle_for_write()                              # W577 (FU-395)
    st["default_local"] = req.model
    st["retired"] = [m for m in (st.get("retired") or []) if m != req.model]
    save_lifecycle(st)
    _ueg_lifecycle("promoted", req.model)
    return {"promoted": req.model, "effective_default": req.model}


@router.post("/lifecycle/retire")
@_states_level("/lifecycle/retire")
async def retire_model(req: LifecycleModelRequest):
    """§6 (W276) — retire a local model from the ACTIVE estate: default orchestration (ensemble,
    'ollama' default routing) stops drawing on it; explicit ollama:<name> routing remains the
    user's explicit choice. Reversible via /lifecycle/reinstate."""
    from agentic_core.ai.native.model_resource import lifecycle_state, save_lifecycle
    st = _lifecycle_for_write()                              # W577 (FU-395)
    if req.model not in (st.get("retired") or []):
        st["retired"].append(req.model)
    if st.get("default_local") == req.model:
        st["default_local"] = None            # a retired model cannot stay the promoted default
    save_lifecycle(st)
    _ueg_lifecycle("retired", req.model)
    return {"retired": st["retired"], "promoted_default": st.get("default_local")}


@router.post("/lifecycle/reinstate")
@_states_level("/lifecycle/reinstate")
async def reinstate_model(req: LifecycleModelRequest):
    """§6 (W276) — return a retired model to the active estate."""
    from agentic_core.ai.native.model_resource import lifecycle_state, save_lifecycle
    st = _lifecycle_for_write()                              # W577 (FU-395)
    st["retired"] = [m for m in (st.get("retired") or []) if m != req.model]
    save_lifecycle(st)
    _ueg_lifecycle("reinstated", req.model)
    return {"retired": st["retired"]}


# Catalogue of Workstation's OWN AI capabilities — each backed by a REAL, integrated agentic_core module
# (the integration sweep; see docs/AGENTIC_CORE_INTEGRATION_AUDIT.md). Discoverability for the fabric.
_CAPABILITIES = [
    {"name": "Workflow tree", "endpoint": "POST /api/v1/native-ai/tree", "kind": "orchestration",
     "source": "ai.native.orchestrator", "in_house": True,
     "description": "Autonomously decompose a goal into a dependency DAG and run it in-house-first with parallel branches, biomimetically governed + logged."},
    {"name": "Agent swarm cascade", "endpoint": "POST /api/v1/native-ai/swarm", "kind": "orchestration",
     "source": "ai.native.orchestrator", "in_house": True,
     "description": "Run a bespoke linear agent-cascade over owned resources."},
    {"name": "In-house completion", "endpoint": "POST /api/v1/native-ai/complete", "kind": "orchestration",
     "source": "ai.native.orchestrator", "in_house": True,
     "description": "In-house-first completion with health-based resource selection + the always-available native floor."},
    {"name": "Minimax decision", "endpoint": "POST /api/v1/native-ai/decide", "kind": "decision",
     "source": "cognition.minimax_optimizer", "in_house": True,
     "description": "Maximin over caller-supplied per-action utilities under worst-case stressors; without action_utilities every action ties and NO winner is invented."},
    {"name": "Validation", "endpoint": "POST /api/v1/native-ai/validate", "kind": "validation",
     "source": "validation.accuracy_validator", "in_house": True,
     "description": "Real difflib semantic-similarity / numerical-tolerance / code-presence checks against a reference."},
    {"name": "Statistical rigor", "endpoint": "POST /api/v1/native-ai/rigor", "kind": "analysis",
     "source": "statistics.live_rigor_monitor", "in_house": True,
     "description": "Real scipy 95% CI + one-sample t-test over an accumulated metric series — reports n, and returns null (with the reason) when the data cannot support a test."},
    {"name": "Swarm consensus", "endpoint": "POST /api/v1/native-ai/consensus", "kind": "swarm",
     "source": "swarm.conflict_resolution", "in_house": True,
     "description": "Real threshold vote-tally — the STRONGEST clearing choice wins, ties are disclosed, and the tally travels with the verdict."},
    {"name": "Signal transduction", "endpoint": "POST /api/v1/native-ai/transduce", "kind": "biomimetic",
     "source": "signaling.empirical_transduction", "in_house": True,
     "description": "Hill saturation transform (K50=0.5) — where a signal sits on a sigmoidal dose-response curve. Nothing is timed; supra-threshold means input ≥ K50."},
    {"name": "Quorum threshold", "endpoint": "POST /api/v1/native-ai/quorum", "kind": "biomimetic",
     "source": "quorum.sensing", "in_house": True,
     "description": "Threshold model over the platform's defined agent catalog (or a supplied population, echoed as such) — arithmetic density × threshold, not an observation of behaviour."},
    {"name": "Intent inference", "endpoint": "POST /api/v1/native-ai/intent", "kind": "nlp",
     "source": "nlp.nli_engine", "in_house": True,
     "description": "Real regex keyword-pattern intent classification (deterministic, not LLM)."},
    {"name": "Entailment", "endpoint": "POST /api/v1/native-ai/entailment", "kind": "nlp",
     "source": "nlp.nli_engine", "in_house": True,
     "description": "Real word-overlap natural-language inference (ENTAILED / PARTIAL / NEUTRAL)."},
    {"name": "Seed derivation", "endpoint": "POST /api/v1/native-ai/entropy", "kind": "crypto",
     "source": "crypto.entropy_pool", "in_house": True,
     "description": "SHA3-512 + XOR deterministic seed derivation over caller-supplied metadata — reproducible seeding; reads NO system entropy, never for keys/nonces/tokens."},
    {"name": "Graph topology", "endpoint": "POST /api/v1/native-ai/topology", "kind": "topology",
     "source": "topology.defense", "in_house": True,
     "description": "Real Betti numbers — β₀ components (union-find) + β₁ cycles over APPLIED edges; discarded edges and the β₁ threshold are disclosed in the payload."},
    {"name": "VBS governance", "endpoint": "POST /api/v1/vbs/*", "kind": "governance",
     "source": "vbs", "in_house": True,
     "description": "Real QMS quality gates + DCMS SHA3-512 versioning + BMS unit-economics + EMS + Mycelial backbone."},
    {"name": "UEG provenance", "endpoint": "GET /api/v1/ueg/verify", "kind": "provenance",
     "source": "ueg.logger", "in_house": True,
     "description": "Real hash-chained SHA3-512 Merkle-DAG audit ledger with full-chain verify_chain()."},
    {"name": "Degradation detection", "endpoint": "GET /api/v1/operations/degradation", "kind": "analysis",
     "source": "self_improvement.degradation_detector", "in_house": True,
     "description": "Real telemetry degradation detection (latency rise / accuracy drop) over the learning loop."},
]


@router.get("/capabilities")
@_states_level("/capabilities")
async def native_capabilities():
    """Catalogue of Workstation's OWN AI capabilities — each backed by a REAL, integrated agentic_core
    module (no external dependency). The fabric's breadth, discoverable."""
    return {"posture": "in-house-first", "count": len(_CAPABILITIES),
            "note": "Every capability is backed by a real, integrated agentic_core module — see "
                    "docs/AGENTIC_CORE_INTEGRATION_AUDIT.md for the full real-vs-mock sweep.",
            "capabilities": _CAPABILITIES}


@router.get("/selfcheck")
@_states_level("/selfcheck")
async def native_selfcheck():
    """Fabric integrity check: actually IMPORT each integrated capability's source module and report
    which are live. Guards the whole integration arc — if any owned capability's backing module breaks,
    this flips all_live to false (honest, real import probe — not a static claim)."""
    import importlib
    sources = sorted({c["source"] for c in _CAPABILITIES})
    modules = []
    for src in sources:
        try:
            importlib.import_module(f"agentic_core.{src}")
            modules.append({"source": src, "live": True})
        except Exception as e:
            modules.append({"source": src, "live": False, "error": type(e).__name__})
    live = sum(1 for m in modules if m["live"])
    return {"posture": "in-house-first", "total": len(modules), "live": live,
            "all_live": live == len(modules), "modules": modules}


class CompleteRequest(BaseModel):
    prompt: str
    agent: str = "assistant"
    prefer_external: bool = False
    timeout: float = 30.0
    model: str = "auto"   # §6 model-tier preference: auto | native (force floor) | local (require Ollama)


class EnsembleRequest(BaseModel):
    prompt: str
    agent: str = "ensemble"
    models: List[str] = []      # tier ids (e.g. ["ollama:llama3.2","ollama:llama2","native"]); empty = all owned
    synthesize: bool = True


@router.post("/ensemble")
@_states_level("/ensemble")
async def native_ensemble(req: EnsembleRequest):
    """§6 — run a prompt across MULTIPLE owned models in parallel, then synthesise a consensus. Owned
    orchestration as a composable resource; every member reports which owned resource served it."""
    #  W627 (FU-531) - the same constitutional pre-gate and response checkpoint /complete and /swarm carry
    from agentic_core.ai.gateway import console_pre_gate, console_post_gate
    _halt = console_pre_gate(req.agent)
    if _halt:
        return {"agent": req.agent, "members": [], "synthesis": None, "refused": True,
                "final": f"[CONSTITUTIONAL REFUSAL] {_halt.get('refused_reason')}", "governance_checkpoint": _halt}
    res = await orchestrator.ensemble(req.prompt, agent=req.agent,
                                      models=req.models or None, synthesize=req.synthesize)
    #  W642 (FU-646, ledger v14 R4) - THE CHECKPOINT SCREENS WHAT THE CALLER RECEIVES. With no synthesis this
    #  screened an empty string and returned post_checked and post_compliant true over member outputs it had
    #  never read. It screens the synthesis when there is one, the member outputs when there is not, and when
    #  there is nothing to screen it says nothing was checked.
    _syn = str((res.get("synthesis") or {}).get("output") or "")
    _member_text = "\n\n".join(str(m.get("output") or "") for m in (res.get("members") or []) if m.get("output"))
    _screened = _syn or _member_text
    chk = console_post_gate(req.agent, _screened)
    chk["covers"] = ("the consensus synthesis" if _syn else
                     "the member outputs (no synthesis ran)" if _member_text else
                     "nothing: no member produced output")
    if not _screened:
        chk["post_checked"] = False
        chk["post_compliant"] = None
        chk["basis"] = "no output was produced, so nothing was screened; an empty string is not a checked answer"
    res["governance_checkpoint"] = chk
    return res


@router.post("/complete")
@_states_level("/complete")
async def native_complete(req: CompleteRequest):
    # W619 (FU-496) — the console reaches the orchestrator directly, so it gets the gateway's gates here
    from agentic_core.ai.gateway import console_pre_gate, console_post_gate
    _halt = console_pre_gate(req.agent)
    if _halt:
        return {"output": f"[CONSTITUTIONAL REFUSAL] {_halt.get('refused_reason')}",
                "served_by": "constitutional_policy_gate", "is_external": False, "resources_tried": [],
                "governance_checkpoint": _halt}
    res = await orchestrator.complete(req.prompt, agent=req.agent, timeout=req.timeout,
                                      prefer_external=req.prefer_external, prefer=req.model,
                                      user_text=(req.prompt or None))   # W651 (FU-675) - the console's own text
    res["governance_checkpoint"] = console_post_gate(req.agent, res.get("output", ""))
    return res


class SwarmStage(BaseModel):
    role: str
    instruction: str


class SwarmRequest(BaseModel):
    agent: str = "swarm"
    context: str = ""
    prefer_external: bool = False
    stages: List[SwarmStage] = []


@router.post("/swarm")
@_states_level("/swarm")
async def native_swarm(req: SwarmRequest):
    stages: List[Dict[str, str]] = [{"role": s.role, "instruction": s.instruction} for s in req.stages]
    #  W674 (P3.31 clause 6) - THE STAGE CEILING APPLIES HERE TOO. It was enforced where a composition or a
    #  saved cascade runs and not on this console, which runs whatever list it is sent. Refused before the
    #  gate and before any model is asked; nothing is truncated.
    from agentic_core.api.instrument_cell import MAX_STAGES as _max_stages, MAX_STAGES_BASIS as _max_basis
    if len(stages) > _max_stages:
        from fastapi import HTTPException
        raise HTTPException(status_code=422, detail=(
            f"this run names {len(stages)} stages and a run attempts at most {_max_stages} ({_max_basis}). "
            f"Nothing was run."))
    if not stages:
        stages = [
            {"role": "analyst", "instruction": "Analyse the objective and key factors."},
            {"role": "designer", "instruction": "Design the approach from the analysis."},
            {"role": "synthesiser", "instruction": "Synthesise the final recommendation."},
        ]
    from agentic_core.ai.gateway import console_pre_gate, console_post_gate
    _halt = console_pre_gate(req.agent)
    if _halt:
        return {"agent": req.agent, "stages": 0, "trace": [], "any_external": False, "homeostasis": None,
                "final": f"[CONSTITUTIONAL REFUSAL] {_halt.get('refused_reason')}", "governance_checkpoint": _halt}
    #  P3.30 (ledger v16 R4.17) - the context field is what the person typed on this console; the stage
    #  instructions may be the page's defaults and are not passed as theirs
    res = await orchestrator.swarm(req.agent, stages, context=req.context, prefer_external=req.prefer_external,
                                   user_text=((req.context or "").strip() or None))
    res["governance_checkpoint"] = console_post_gate(req.agent, str(res.get("final") or ""))
    return res


class TreeRequest(BaseModel):
    goal: str
    context: str = ""
    max_parallel: int = 4
    prefer_external: bool = False
    timeout: float = 30.0


class TransduceRequest(BaseModel):
    input_signal: float = Field(ge=0.0, allow_inf_nan=False)   # a Hill transform of a negative concentration has no referent
    hill: float = Field(default=4.5, gt=0.0, le=100.0, allow_inf_nan=False)
    include_curve: bool = False


@router.post("/transduce")
async def native_transduce(req: TransduceRequest):
    """Owned Hill saturation transform (agentic_core/signaling): where a signal sits on a sigmoidal
    dose-response curve — activation = s^h / (K50^h + s^h), K50 = 0.5, disclosed in the payload.

    W437 — this endpoint used to report `latency_s` (nothing was timed — a constant formula wearing
    a unit) and echo a `frequency` parameter that provably never entered the result, under the method
    string "Hill-equation pulsatile cascade". Both are DELETED, not renamed; `propagated` became
    `supra_threshold`, stated for what it is (input_signal >= K50), and the basis travels with it."""
    from agentic_core.signaling.empirical_transduction import EmpiricalSignalTransduction
    r = EmpiricalSignalTransduction(hill=req.hill).transform(req.input_signal)
    out = {"input_signal": req.input_signal, "activation": r["activation"],
           "supra_threshold": r["supra_threshold"], "k50": r["k50"], "hill": r["hill"],
           "basis": r["basis"], "method": "Hill saturation transform (owned signaling)"}
    if req.include_curve:
        out["dose_response"] = r["dose_response"]
        out["dose_response_domain"] = r["dose_response_domain"]
    return out


class TopologyRequest(BaseModel):
    nodes: List[Any] = []
    edges: List[Any] = []     # each edge: [u, v] (or {source, target})


@router.post("/topology")
async def native_topology(req: TopologyRequest):
    """Owned graph-topology analysis (agentic_core/topology.TopologyDefense): REAL Betti numbers of the
    1-complex — β₀ = connected components (union-find), β₁ = E−V+β₀ = independent cycles, computed over
    the edges the union-find actually APPLIED. A tree → β₁=0; a cycle → β₁≥1; disconnection raises β₀.

    W437 — β₁ used to count the RAW edge list while validation quietly discarded malformed/dangling
    edges (junk edges reported as "structural holes"), and "SPIKE_DETECTED" asserted a temporal rise
    against a baseline that never existed, using an undisclosed 3.0 cutoff that ignored β₀ entirely.
    Now the discard is disclosed, the threshold is in the payload, and the verdict fields say only
    what one measurement can say: fragmented (β₀>1) and beta1_over_threshold."""
    from agentic_core.topology.defense import TopologyDefense
    res = await TopologyDefense().compute_persistent_homology({"nodes": req.nodes, "edges": req.edges})
    return {"beta0_components": res["beta0"], "beta1_cycles": res["beta1"],
            "fragmented": res["fragmented"], "beta1_threshold": res["beta1_threshold"],
            "beta1_over_threshold": res["beta1_over_threshold"],
            "nodes_submitted": res["nodes_submitted"], "nodes_distinct": res["nodes_distinct"],
            "nodes_discarded": res["nodes_discarded"], "edges_submitted": res["edges_submitted"],
            "edges_applied": res["edges_applied"], "edges_discarded": res["edges_discarded"],
            "basis": res["basis"],
            "method": "graph Betti numbers via Euler characteristic (owned topology)"}


class EntropyRequest(BaseModel):
    sources: List[Dict[str, Any]] = []   # each: {size, source, content_hash, timestamp}


@router.post("/entropy")
async def native_entropy(req: EntropyRequest):
    """Owned deterministic seed derivation (agentic_core/crypto.EntropyPool): SHA3-512 + XOR mixing over
    the caller-supplied source metadata — same sources (fixed timestamps) ⇒ same seed, which is the
    point: reproducible in-house seeding. NO system entropy is read anywhere.

    W437 — this endpoint used to report `bits_harvested` (a fixed +128 per source that never examined
    a byte — five empty dicts "harvested" 640 bits into a 512-bit register) and a `pool_integrity`
    digest that was byte-identical to the seed, so it could never disagree with the value it claimed
    to attest. The counter is now what it always was (mixing_rounds), the digest is a disjoint slice
    of the pool hash, and the response says plainly what this seed must never be used for."""
    from agentic_core.crypto.entropy_pool import EntropyPool
    pool = EntropyPool()
    for s in req.sources:
        pool.add_entropy(s)
    return {"seed": pool.get_seed(), "mixing_rounds": pool.mixing_rounds,
            "pool_digest": pool.pool_digest(), "sources_mixed": len(req.sources),
            "algo": "sha3_512 + XOR mixing", "method": "deterministic seed derivation (owned crypto)",
            "basis": ("deterministic derivation over caller-supplied metadata; no system, hardware or "
                      "physical entropy is read — do NOT use this seed as a key, nonce, or token"
                      + ("; no sources were supplied, so this is the fixed genesis-constant seed "
                         "(identical in every deployment)" if not req.sources else "")
                      + (f"; {pool.timestamps_defaulted} source(s) carried no timestamp — a fixed 0 "
                         f"was used for each (the derivation stays deterministic)"
                         if pool.timestamps_defaulted else ""))}


class QuorumRequest(BaseModel):
    agents: int | None = Field(default=None, ge=0, le=1_000_000_000)   # None → the platform's agent catalog is counted
    secretion: float = Field(default=10.0, ge=0.0, allow_inf_nan=False)   # AI-2 analog secreted per agent
    threshold: float = Field(default=50.0, gt=0.0, allow_inf_nan=False)


@router.post("/quorum")
async def native_quorum(req: QuorumRequest):
    """Owned quorum threshold model (agentic_core/quorum.QuorumSensing) over the platform's defined
    agent catalog — or an explicitly supplied population, echoed as such.

    W437 — this endpoint claimed "sensing", a "shared field" and "real threshold kinetics" while
    computing agents × secretion > threshold over numbers the caller typed in. It also rounded the
    reported concentration but compared the unrounded one, so a payload could display
    50.0 > 50.0 = true. Now the population defaults to the platform's agent catalog with
    population_source disclosing which was used — and the refuter pass corrected the first version
    of this fix, which called that catalog "live_roster": _AGENTS is a static definition that never
    changes at runtime, and naming a constant a live observation is the same defect class. The
    reported concentration is the exact product the verdict derives from (a single multiplication,
    not a float-summing loop the basis would misdescribe as ×)."""
    from agentic_core.quorum.sensing import QuorumSensing
    from agentic_core.api.swarm import _AGENTS
    if req.agents is None:
        population, source, source_desc = len(_AGENTS), "agent_catalog", \
            "the platform's defined agent catalog — a static definition, not a runtime observation"
    else:
        population, source, source_desc = req.agents, "caller_supplied", "caller-supplied population"
    q = QuorumSensing("swarm", threshold=req.threshold)
    q.secrete_ai2(population * req.secretion)
    concentration = q.ai2_concentration   # exact — the verdict below derives from THIS value
    mode = q.get_behavior_mode()
    return {"agents": population, "population_source": source,
            "concentration": concentration, "threshold": req.threshold,
            "behavior_mode": mode, "cooperative": mode == "COOPERATIVE",
            "basis": (f"{population} agents ({source_desc}) × secretion {req.secretion} = "
                      f"{concentration} vs threshold {req.threshold} — an arithmetic threshold "
                      f"check, not an observation of live behaviour"),
            "method": "quorum threshold model (owned biomimetic swarm)"}


class IntentRequest(BaseModel):
    text: str


@router.post("/intent")
async def native_intent(req: IntentRequest):
    """Owned NLP intent inference (agentic_core/nlp.NLIEngine): REAL regex keyword-pattern scoring over
    the text — deterministic, not LLM. Returns the best intent + confidence + all per-intent scores."""
    from agentic_core.nlp.nli_engine import NLIEngine
    return NLIEngine().infer_intent(req.text)


class EntailmentRequest(BaseModel):
    premise: str
    hypothesis: str


@router.post("/entailment")
async def native_entailment(req: EntailmentRequest):
    """Owned NLP entailment (agentic_core/nlp.NLIEngine) — LEXICAL word-overlap inference.

    W431: returns the deciding number and the limits of the method, not a bare verdict. It used to
    report ENTAILED for "The sky is not blue" -> "The sky is blue", because a negator sits in the
    PREMISE and overlap only counts hypothesis tokens found there. Asymmetric negation now yields
    CONTRADICTION — the label this docstring always promised and the code never returned.
    ENTAILED | PARTIAL_ENTAILMENT | NEUTRAL | CONTRADICTION | UNDECIDABLE. Deterministic, and
    lexical: it does not read word order, quantifiers, or role inversion."""
    from agentic_core.nlp.nli_engine import NLIEngine
    detail = NLIEngine().entailment_detail(req.premise, req.hypothesis)
    # The ratio and the limits travel WITH the verdict: a label that makes a logical claim on lexical
    # evidence must show the evidence, or the caller has no way to judge it.
    return {"premise": req.premise, "hypothesis": req.hypothesis, **detail}


class Vote(BaseModel):
    voter: str
    choice: str


class ConsensusRequest(BaseModel):
    proposal_id: str = "proposal"
    votes: List[Vote] = []
    total_nodes: int = Field(default=0, ge=0)     # 0 → use the number of DISTINCT voters
    threshold: float = Field(default=0.66, gt=0.0, le=1.0)   # W437: was unbounded — -1.0 "reached consensus"


@router.post("/consensus")
async def native_consensus(req: ConsensusRequest):
    """Owned swarm consensus (agentic_core/swarm.ConsensusEngine): REAL threshold vote-tally — the
    STRONGEST choice clearing the threshold wins; an exact top tie is disclosed, never resolved by
    input order (W431). The tally, shares and basis travel with the verdict so a caller can check it.

    W437 — the W431 engine fix existed but this handler still called the old single-value path,
    dropping the tally/tie/basis it computes; total_nodes still counted the RAW ballot list although
    votes are keyed by voter and later ballots overwrite earlier ones (three entries from one voter
    reported as a 3-vote ballot); and threshold accepted any float — -1.0 returned a "reached"
    consensus that is meaningless by construction. All three closed."""
    from agentic_core.swarm.conflict_resolution import ConsensusEngine
    ce = ConsensusEngine(threshold=req.threshold)
    for v in req.votes:
        ce.record_vote(req.proposal_id, v.voter, v.choice)
    distinct = len(ce.votes.get(req.proposal_id) or {})
    total = req.total_nodes or distinct
    detail = ce.consensus_detail(req.proposal_id, total)
    return {"reached": detail["reached"], "choice": detail["choice"], "tied": detail["tied"],
            "tied_choices": detail["tied_choices"], "tally": detail["tally"],
            "shares": detail["shares"], "threshold": req.threshold,
            "total_nodes": total, "ballots_submitted": len(req.votes),
            "distinct_voters": detail["distinct_voters"], "basis": detail["basis"],
            "method": "threshold consensus (owned swarm)"}


class RigorRequest(BaseModel):
    metric_name: str
    # W437: NaN/inf observations are refused at the door — a NaN used to reach scipy, compare
    # False as "not significant", get sealed into the UEG chain, and then 500 the response
    value: float = Field(allow_inf_nan=False)
    baseline: float = Field(default=0.0, allow_inf_nan=False)


# Shared statistical-rigor monitor — real scipy CI + t-tests over a live metric series; logs each
# validation to the owned UEG provenance chain. Stateful (accumulates per-metric history) by design.
def _rigor_monitor():
    from agentic_core.statistics.live_rigor_monitor import LiveRigorMonitor
    from agentic_core.ueg.registry import ueg_ledger
    global _RIGOR
    try:
        return _RIGOR
    except NameError:
        _RIGOR = LiveRigorMonitor(ueg=ueg_ledger)
        return _RIGOR


@router.post("/rigor")
async def native_rigor(req: RigorRequest):
    """Owned statistical-rigor capability (agentic_core/statistics.LiveRigorMonitor): REAL scipy 95%
    t-interval CI + one-sample t-test over the accumulated per-metric series. Tri-state and honest:
    when the test could not run (n<3, or zero variance), p_value and significant are null with the
    reason in `basis` — never a fabricated 1.0.

    W437 — the old response carried `power` (a call counter: n/100 + 0.5, no power analysis existed)
    whose gate froze `significant` at false for 29 calls regardless of evidence — a live p-value of
    1.5e-24 was reported "not significant". First calls returned p_value 1.0 and a zero-width CI that
    were never computed, and a zero-variance series 500'd AFTER sealing a NaN into the UEG chain."""
    res = await _rigor_monitor().validate_metric(req.metric_name, req.value, req.baseline)
    return {"metric": res["metric"], "value": res["value"], "baseline": res["baseline"],
            "n": res["n"],
            "ci_95": list(res["ci_95"]) if res["ci_95"] is not None else None,
            "p_value": res["p_value"], "significant": res["significant"], "basis": res["basis"],
            "method": "scipy t-interval CI + one-sample t-test (owned statistics)"}


class ValidateRequest(BaseModel):
    prediction: Any
    actual: Any
    # W437: a validated enum — an unknown value used to fall silently into the equality branch while
    # the hardcoded method string claimed difflib ran
    task_type: Literal["SEMANTIC", "NUMERICAL", "APP_CODE", "GENERIC"] = "SEMANTIC"


_VALIDATE_METHODS = {
    "SEMANTIC": "difflib SequenceMatcher ratio vs 0.8 (owned validation)",
    "NUMERICAL": "absolute error vs 1% tolerance (owned validation)",
    "APP_CODE": "syntax-token presence check — not a correctness measure (owned validation)",
    "GENERIC": "exact equality — binary, no confidence gradient (owned validation)",
}


@router.post("/validate")
async def native_validate(req: ValidateRequest):
    """Owned validation capability (agentic_core/validation.AccuracyValidator): reference comparison
    per task type, with the confidence basis travelling alongside — not LLM self-grading.

    W437 — the W432 engine fix (confidence: null where nothing computes one, with confidence_basis)
    existed but THIS handler still cast `float(confidence)`, which 500'd on every GENERIC/APP_CODE
    call, dropped the basis, and stamped one hardcoded "(difflib, real)" method string on all four
    branches. The method now names the branch that actually ran."""
    from agentic_core.validation.accuracy_validator import AccuracyValidator
    res = AccuracyValidator().validate_output(req.prediction, req.actual, task_type=req.task_type)
    return {"is_accurate": bool(res["is_accurate"]),
            "confidence": (None if res["confidence"] is None else float(res["confidence"])),
            "confidence_basis": res["confidence_basis"], "task_type": res["task_type"],
            "method": _VALIDATE_METHODS[req.task_type]}


class DecideRequest(BaseModel):
    state: Dict[str, Any] = {}
    actions: List[str] = []
    # W437: the only way this endpoint can genuinely decide. The default utility never reads the
    # action, so without per-action utilities every 2+ action call ties — disclosed, never invented.
    action_utilities: Dict[str, float] | None = None


@router.post("/decide")
async def native_decide(req: DecideRequest):
    """In-house minimax (maximin) over candidate actions under worst-case stressors — the OWNED
    cognition capability (agentic_core/cognition).

    W437 refuter catch on the W431 fix: the tie disclosure was honest but made the endpoint a
    PERMANENT refusal — the default utility ignores the action, so no reachable input could ever
    discriminate, while the docstring advertised "when no custom utility is provided" for a
    parameter that did not exist. `action_utilities` now exists: supply a base utility per action
    and the maximin genuinely ranks them; omit it and the all-tie refusal stands, stated as such."""
    from agentic_core.cognition.minimax_optimizer import MinimaxOptimizer, default_utility_func
    actions = req.actions or ["proceed", "refine", "hold"]
    state = req.state or {"base_stability": 0.9}
    if req.action_utilities is not None:
        missing = [a for a in actions if a not in req.action_utilities]
        if missing:
            raise HTTPException(status_code=422,
                                detail=f"action_utilities must cover every action; missing: {missing} "
                                       f"(a partial table would silently hand missing actions a default)")
        au = dict(req.action_utilities)

        def _utility(state_: Dict[str, Any], action: str, stressor: str) -> float:
            base = float(au[action])
            if stressor == "hypoxia":
                base -= 0.3
            if stressor == "high_load":
                base -= 0.1
            return max(0.0, base)

        util, util_source = _utility, "caller-supplied per-action utilities"
    else:
        util, util_source = default_utility_func, (
            "default survival utility — it does NOT read the action, so with 2+ actions every "
            "candidate ties and no winner is invented; supply action_utilities to rank")
    res = MinimaxOptimizer().evaluate_strategy(state, actions, util)
    return {"posture": "in-house", "method": "minimax adversarial (owned cognition)",
            "actions": actions, "utility_source": util_source,
            "stressor_note": ("two of the four stressors subtract nothing, so the binding worst case "
                              "is always hypoxia (−0.3); stressors shift all actions equally and never "
                              "change the ranking"),
            **res}


@router.post("/tree")
@_states_level("/tree")
async def native_tree(req: TreeRequest):
    """Autonomous workflow-TREE orchestration: the native swarm decomposes the goal into a dependency
    tree and runs it in-house-first with PARALLEL branches — the living-organism cascade (immune-throttled
    parallelism + biobus signals + learning loop). Every node reports the OWNED resource that served it."""
    #  W627 (FU-531) - gated as /complete and /swarm are; the orchestrator itself applies no policy
    from agentic_core.ai.gateway import console_pre_gate, console_post_gate
    _halt = console_pre_gate("tree")
    if _halt:
        return {"goal": req.goal, "nodes": [], "refused": True,
                "final": f"[CONSTITUTIONAL REFUSAL] {_halt.get('refused_reason')}", "governance_checkpoint": _halt}
    res = await orchestrator.orchestrate_tree(
        req.goal, context=req.context, max_parallel=req.max_parallel,
        prefer_external=req.prefer_external, timeout=req.timeout)
    res["governance_checkpoint"] = console_post_gate("tree", str(res.get("final") or ""))
    return res
