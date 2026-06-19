"""
IDBO Nine Cognitive Engines + MJM — HTTP Surface

Exposes the deep intelligence layer to the API:

  POST /api/v1/cognitive/cascade    — run full 9-engine cascade on a problem
  POST /api/v1/cognitive/mjm        — run MJM Mushahida-Jaiza-Muaina lifecycle
  POST /api/v1/cognitive/engine     — run a single named engine
  GET  /api/v1/cognitive/engines    — list all available engines

The cascade and MJM are the IDBO's reasoning core. Every VSB spawn, every
synthesis cascade, every CEO decision runs through these before any AI call.
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
    "niyyah":    {"name": "Niyyah", "function": "Intention alignment and purpose scoring", "layer": "meta"},
    "tafakkur":  {"name": "Tafakkur", "function": "Deep contemplation over complex problems", "layer": "meta"},
    "tawazun":   {"name": "Tawazun", "function": "Balance and trade-off resolution", "layer": "meta"},
}


@router.get("/engines")
async def list_engines():
    return {
        "engines": [
            {**info, "engine_id": eid}
            for eid, info in _ENGINE_REGISTRY.items()
        ],
        "total": len(_ENGINE_REGISTRY),
        "layers": {"foundational": 6, "meta": 3},
    }


class CascadeRequest(BaseModel):
    problem: str
    domain: str = "general"
    context: str = ""
    include_mjm: bool = True


@router.post("/cascade")
async def run_cascade(req: CascadeRequest):
    """
    Run the full 9-engine cognitive cascade on a problem statement.
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
        "engines_run": 6 if not req.include_mjm else 9,
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
        return {"engine_id": eid, "note": "Meta engine — use /cascade for full cascade including meta layer."}

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
