"""
IDBO Cognitive Engines + MJM — HTTP Surface

W489 (sweep S2.0, C3) — SIX ENGINES EXIST AND RUN; THREE ARE DECLARED AND DO NOT.
This surface claimed nine cognitive engines, offered a nine-engine cascade, listed nine in its
registry and reported `engines_run: 9`. Six engine modules exist (aqal, hoshiyari, iman, inkashaf,
samajh, soch); the three "meta" engines (niyyah, tafakkur, tawazun) have no module at all — the
meta/ package is empty. The three meta engines are PLANNED work carried by the delivery plan under P3.13 — the claim was not
that they are unwanted, but that a plan is not a measurement: the cascade runs the six, MJM re-runs
the SAME six, so nine was never a count of anything that happened. The six themselves return fixed markers rather than
computing (see cascade_v16), which this surface now states rather than implying analysis.

Exposes the deep intelligence layer to the API:

  POST /api/v1/cognitive/cascade    — run the six-engine cascade on a problem
  POST /api/v1/cognitive/mjm        — run MJM Mushahida-Jaiza-Muaina lifecycle
  POST /api/v1/cognitive/engine     — run a single named engine
  GET  /api/v1/cognitive/engines    — list all available engines

The cascade and MJM are reached by the VSB spawn path. They are NOT a precondition of every AI
call: the four intelligence pipelines and the CEO surfaces call the gateway directly.
"""
from __future__ import annotations

import time
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from agentic_core.cognitive.cascade_v16 import UltimateCognitiveCascade
from agentic_core.mjm.mjm import MJMOrchestratorV4, ConsultationRequest

router = APIRouter(prefix="/api/v1/cognitive", tags=["cognitive-engines"])

# Singletons — instantiated once, reused across requests
_cascade = UltimateCognitiveCascade()
_mjm = MJMOrchestratorV4()

_ENGINE_REGISTRY = {
    "aqal":      {"name": "Aqal", "function": "Rational analysis and structured reasoning", "layer": "foundational"},
    "hoshiyari": {"name": "Hoshiyari", "function": "Situational awareness and context sensing", "layer": "foundational"},
    "iman":      {"name": "Iman", "function": "Values alignment and ethical grounding", "layer": "foundational"},
    "inkashaf":  {"name": "Inkashaf", "function": "Discovery, pattern recognition, insight generation", "layer": "foundational"},
    "samajh":    {"name": "Samajh", "function": "Deep comprehension and sense-making", "layer": "foundational"},
    "soch":      {"name": "Soch", "function": "Reflective thinking and deliberation", "layer": "foundational"},
    # W489 — PLANNED, NOT YET BUILT. agentic_core/cognitive/meta/ holds only __init__.py; there is no
    # niyyah, tafakkur or tawazun module, so no cascade can run them. They are REAL PLANNED WORK, not
    # an abandoned claim: the delivery plan builds them under P3.13 ("The three meta-regulative
    # engines — Tawazun, Niyyah, Tafakkur — refusal by default"). P3.12 is the neighbouring item and
    # is NOT where they are built: it carries the CONTRACT that must accept their names (FU-224) and
    # the six foundational engines. They stay listed for that reason,
    # marked as planned, and are never counted among the engines that ran.
    "niyyah":    {"name": "Niyyah", "function": "Intention alignment and purpose scoring", "layer": "meta",
                  "implemented": False, "status": "planned",
                  "note": "planned — no engine module yet; the delivery plan builds it under P3.13"},
    "tafakkur":  {"name": "Tafakkur", "function": "Deep contemplation over complex problems", "layer": "meta",
                  "implemented": False, "status": "planned",
                  "note": "planned — no engine module yet; the delivery plan builds it under P3.13"},
    "tawazun":   {"name": "Tawazun", "function": "Balance and trade-off resolution", "layer": "meta",
                  "implemented": False, "status": "planned",
                  "note": "planned — no engine module yet; the delivery plan builds it under P3.13"},
}
for _e in _ENGINE_REGISTRY.values():
    _e.setdefault("implemented", True)
    _e.setdefault("status", "built")
    # the six that exist return fixed markers rather than computing — said here, not implied away
    _e.setdefault("computes", False)
_IMPLEMENTED = [e for e, i in _ENGINE_REGISTRY.items() if i["implemented"]]


@router.get("/engines")
async def list_engines():
    # W520 — THIS PAGE'S OWN LIST IS NOT EVIDENCE ABOUT THE ENGINES. `_ENGINE_REGISTRY` above is a table kept
    # by hand; the object a consumer actually resolves an engine through is CognitiveEngineRegistry. That is
    # not a hypothetical divergence: FU-221 was exactly this gap, with the registry holding ZERO engines while
    # this route reported six, for as long as nobody compared them. So the counts below are COMPUTED from the
    # table rather than written as literals, the registry is asked for its own report, and a disagreement
    # between the two is reported rather than resolved silently in favour of whichever is cheaper to read.
    from agentic_core.cognitive.registry import CognitiveEngineRegistry as _Reg

    _layers: dict[str, int] = {}
    _layers_impl: dict[str, int] = {}
    for _eid, _i in _ENGINE_REGISTRY.items():
        _layers[_i["layer"]] = _layers.get(_i["layer"], 0) + 1
        if _i["implemented"]:
            _layers_impl[_i["layer"]] = _layers_impl.get(_i["layer"], 0) + 1

    _rep = _Reg.report()
    _registered = _rep.get("registered") or []
    _disagree = sorted(set(_IMPLEMENTED) ^ set(_registered))

    return {
        "engines": [
            {**info, "engine_id": eid}
            for eid, info in _ENGINE_REGISTRY.items()
        ],
        "total": len(_ENGINE_REGISTRY),
        "implemented_total": len(_IMPLEMENTED),
        "layers": {k: _layers.get(k, 0) for k in ("foundational", "meta")},
        "layers_implemented": {k: _layers_impl.get(k, 0) for k in ("foundational", "meta")},
        "basis": (f"{len(_IMPLEMENTED)} of the {len(_ENGINE_REGISTRY)} engines exist as modules and run; the "
                  f"{len(_ENGINE_REGISTRY) - len(_IMPLEMENTED)} meta engines are PLANNED (no module yet — the "
                  "delivery plan builds them under P3.13). No engine computes yet: each of the "
                  f"{len(_IMPLEMENTED)} returns a fixed marker, which P3.12 also carries."),
        # The registry's own answer, so this route stops being the only witness to its own claim.
        "registry": {
            "registered": _registered,
            "registered_count": len(_registered),
            "engine_type_declares": _rep.get("engine_type_declares"),
            "declared_but_absent": _rep.get("declared_but_absent") or [],
            "declared_but_absent_basis": _rep.get("declared_but_absent_basis") or {},
            "unavailable": _rep.get("unavailable") or {},
            "bootstrap_failed": _rep.get("bootstrap_failed"),
            "basis": _rep.get("basis"),
            # W523 (Owner ruling 2026-09-30) — the denominator is 23 in five tiers. This page's own table
            # lists NINE because it was written against the twelve-engine architecture's first two tiers,
            # so `total: 9` below is this table's size and NOT a claim about how many engines exist. The
            # two are different questions and the page now answers both rather than letting one stand in
            # for the other.
            "by_tier": _rep.get("by_tier") or {},
            "tiers_declared": _rep.get("tiers_declared") or [],
            "what_the_denominator_means": _rep.get("what_the_denominator_means"),
            "why_this_pages_total_is_smaller": (
                "`total` is the size of this page's hand-kept table (the foundational and meta tiers). "
                "`registry.engine_type_declares` is what the architecture declares across all five tiers. "
                "A reader comparing them is comparing a table to an architecture, not finding a defect"),
            "what_registration_does_not_mean": _rep.get("what_registration_does_not_mean"),
            "this_pages_list_agrees": not _disagree,
            "disagreement": _disagree,
            "disagreement_basis": (
                "this page's hand-kept table and the registry name different engines: "
                f"{_disagree}. Trust NEITHER count until they are reconciled — a consumer resolves engines "
                "through the registry, so the registry is what a caller will actually get"
                if _disagree else
                "this page's hand-kept table and the registry name the same engines"),
        },
    }


class CascadeRequest(BaseModel):
    problem: str
    domain: str = "general"
    context: str = ""
    include_mjm: bool = True


@router.post("/cascade")
async def run_cascade(req: CascadeRequest):
    """
    Run the six-engine cognitive cascade on a problem statement (the three meta engines are planned
    under P3.13 and cannot run; each of the six returns a fixed marker rather than computing).
    Optionally follows with MJM lifecycle for meta-judgement.
    Returns structured analysis from each engine stage.
    """
    problem_input = {
        "problem": req.problem,
        "domain": req.domain,
        "context": req.context,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    started = time.monotonic()

    try:
        cascade_result = await _cascade.execute_cascade(problem_input)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cascade failed: {e}")

    mjm_result = None
    if req.include_mjm:
        try:
            mjm_result = await _mjm.run_lifecycle(cascade_result)
        except Exception as e:
            mjm_result = {"error": str(e), "status": "mjm_failed_cascade_ok"}

    elapsed = round(time.monotonic() - started, 3)

    return {
        "problem": req.problem,
        "domain": req.domain,
        "cascade": cascade_result,
        "mjm": mjm_result,
        # W489 — six ran. MJM does not add three: it re-runs the SAME six (mjm.jaiza → the cascade).
        "engines_run": 6,
        "engines_run_basis": ("the six implemented engines"
                              + (" — MJM re-ran the same six, it does not add engines"
                                 if req.include_mjm else "")),
        "engines_compute": False,
        "elapsed_seconds": elapsed,
        "status": "complete",
    }


class MJMRequest(BaseModel):
    query: str
    context: dict = {}


@router.post("/mjm")
async def run_mjm(req: MJMRequest):
    """
    Run MJM (Mushahida-Jaiza-Muaina) lifecycle:
    Observe → Analyse → Act. Returns evaluated result with compliance score.
    """
    consultation = ConsultationRequest(query=req.query, context=req.context)
    try:
        response = await _mjm.consult(consultation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"MJM consultation failed: {e}")

    return {
        "query": req.query,
        "engine": response.engine,
        "answer": response.answer,
        "confidence": response.confidence,
        "constitutional_validation": {
            "passed": response.constitutional_validation.passed,
        },
        "reasoning_trace": response.reasoning_trace,
        "status": "complete",
    }


class SingleEngineRequest(BaseModel):
    engine_id: str
    input: Any
    domain: str = "general"


@router.post("/engine")
async def run_single_engine(req: SingleEngineRequest):
    """Run a single named cognitive engine on an input."""
    eid = req.engine_id.lower()
    if eid not in _ENGINE_REGISTRY:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown engine '{eid}'. Available: {list(_ENGINE_REGISTRY.keys())}"
        )

    # W489 — a PLANNED engine is answered as planned, not as a missing thing. It is named in the
    # registry because the design names it and the delivery plan builds it under P3.13; a bare 404
    # ("not in cascade") told the caller nothing about which of those it was.
    if not _ENGINE_REGISTRY[eid].get("implemented", True):
        return {"engine_id": eid, "status": "planned", "ran": False, "result": None,
                "note": ("This engine is PLANNED, not yet built — no module exists, so nothing ran. "
                         "The delivery plan builds the meta layer under P3.13; /cascade runs the six "
                         "implemented engines only.")}

    engine_obj = getattr(_cascade, eid, None)
    if engine_obj is None:
        raise HTTPException(status_code=404, detail=f"Engine '{eid}' not in cascade.")

    # Map engine → its primary method
    _METHOD_MAP = {
        "aqal":      ("reason", {"goals": req.input}, {}),
        "hoshiyari": ("detect_anomalies", req.input, None),
        "iman":      ("validate_values", req.input, None),
        "inkashaf":  ("unveil_patterns", req.input, None),
        "samajh":    ("comprehend", req.input, None),
        "soch":      ("reflect", str(req.input), None),
    }

    if eid not in _METHOD_MAP:
        return {"engine_id": eid, "status": "planned", "ran": False,
                "note": ("Meta engine — PLANNED, not yet built (no module). The delivery plan builds the "
                         "meta layer under P3.13; /cascade runs the six implemented engines only.")}

    method_name, arg1, arg2 = _METHOD_MAP[eid]
    method = getattr(engine_obj, method_name)
    try:
        if arg2 is not None:
            result = await method(arg1, arg2)
        else:
            result = await method(arg1)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Engine {eid} failed: {e}")

    return {
        "engine_id": eid,
        "engine_name": _ENGINE_REGISTRY[eid]["name"],
        "input": str(req.input)[:200],
        "result": result,
        "status": "complete",
    }
