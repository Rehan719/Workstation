"""
Digital Twin & Simulation API — AI-powered system modelling and scenario testing.

  POST /api/v1/twin/model      — generate a digital twin model for a system
  POST /api/v1/twin/simulate   — run a simulation scenario against a model
  POST /api/v1/twin/optimise   — AI optimisation pass on a model
  GET  /api/v1/twin/models     — list all stored twin models
  GET  /api/v1/twin/models/{id} — retrieve a model
"""
from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from agentic_core.config import data_path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from agentic_core.ai.gateway import gateway
from agentic_core.organism.biobus import biobus

router = APIRouter(prefix="/api/v1/twin", tags=["digital-twin"])

_TWIN_STORE = data_path("digital_twins")
_TWIN_STORE.mkdir(parents=True, exist_ok=True)


def _twin_path(model_id: str) -> Path:
    return _TWIN_STORE / f"{model_id}.json"


def _load_twin(model_id: str) -> dict | None:
    p = _twin_path(model_id)
    return json.loads(p.read_text()) if p.exists() else None


def _save_twin(model: dict) -> None:
    _twin_path(model["model_id"]).write_text(json.dumps(model, indent=2))


@router.get("/models")
async def list_models():
    models = []
    for p in sorted(_TWIN_STORE.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
        try:
            m = json.loads(p.read_text())
            models.append({
                "model_id": m["model_id"],
                "system_name": m.get("system_name", ""),
                "domain": m.get("domain", ""),
                "model_type": m.get("model_type", ""),
                "created_at": m.get("created_at", ""),
            })
        except Exception:
            pass
    return {"models": models, "total": len(models)}


@router.get("/models/{model_id}")
async def get_model(model_id: str):
    m = _load_twin(model_id)
    if not m:
        raise HTTPException(status_code=404, detail=f"Model {model_id} not found.")
    return m


class ModelRequest(BaseModel):
    system_name: str
    system_description: str
    domain: str = "general"
    model_type: str = "process"  # process | biological | economic | physical | organisational
    complexity: str = "standard"  # simple | standard | complex


@router.post("/model")
async def generate_twin_model(req: ModelRequest):
    """
    Generate a digital twin model specification for a real-world system.
    """
    complexity_spec = {
        "simple": "Focus on 3-5 key components and the primary feedback loop.",
        "standard": "Model 6-10 components with multiple feedback loops and state variables.",
        "complex": "Model 10+ components, emergent behaviours, stochastic elements, and multi-scale dynamics.",
    }.get(req.complexity, "Model 6-10 components with multiple feedback loops.")

    prompt = (
        f"You are a systems engineer and digital twin architect. "
        f"Design a comprehensive digital twin model.\n\n"
        f"System: {req.system_name}\n"
        f"Description: {req.system_description}\n"
        f"Domain: {req.domain}\n"
        f"Model type: {req.model_type}\n"
        f"Complexity: {req.complexity}\n\n"
        f"{complexity_spec}\n\n"
        "Produce:\n"
        "## System Boundary (what is inside and outside the model)\n"
        "## Components (table: Component | Type | State Variables | Parameters)\n"
        "## Feedback Loops (positive and negative — describe each)\n"
        "## Inputs and Outputs (what enters and leaves the system)\n"
        "## State Variables (what changes over time and how)\n"
        "## Key Equations or Relationships (describe the governing dynamics)\n"
        "## Data Requirements (what data feeds the model, at what frequency)\n"
        "## Simulation Time Step and Duration\n"
        "## Validation Strategy (how to verify the model reflects reality)\n"
        "## Failure Modes (what could go wrong in the real system)\n"
        "## Key Metrics Output (what the simulation measures)\n"
    )

    biobus.fire_signal("cognitive", "twin.model", f"Digital twin: {req.system_name}", 0.6)
    model_spec = await gateway.query(prompt, agent="digital_twin_modeller")

    model_id = f"twin-{uuid.uuid4().hex[:10]}"
    model = {
        "model_id": model_id,
        "system_name": req.system_name,
        "system_description": req.system_description,
        "domain": req.domain,
        "model_type": req.model_type,
        "complexity": req.complexity,
        "model_spec": model_spec,
        "simulations": [],
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    _save_twin(model)
    biobus.record_operation("twin_model", "twin.model", success=True, payload=req.system_name)

    return {"model_id": model_id, "system_name": req.system_name, "model_spec": model_spec}


class SimulateRequest(BaseModel):
    model_id: str
    scenario_name: str
    scenario_description: str
    parameters: dict = {}
    time_horizon: str = "90 days"


@router.post("/simulate")
async def run_simulation(req: SimulateRequest):
    """
    Run a simulation scenario against an existing digital twin model.
    """
    model = _load_twin(req.model_id)
    if not model:
        raise HTTPException(status_code=404, detail=f"Model {req.model_id} not found.")

    model_summary = model["model_spec"][:800]
    params_text = json.dumps(req.parameters) if req.parameters else "Default parameters"

    prompt = (
        f"You are a simulation engineer running a digital twin scenario.\n\n"
        f"System: {model['system_name']}\n"
        f"Model summary:\n{model_summary}\n\n"
        f"Scenario: {req.scenario_name}\n"
        f"Description: {req.scenario_description}\n"
        f"Parameters: {params_text}\n"
        f"Time horizon: {req.time_horizon}\n\n"
        "Run the simulation and provide:\n"
        "## Simulation Setup (initial conditions, parameters used)\n"
        "## Phase 1: Early Dynamics (first third of time horizon)\n"
        "## Phase 2: Mid-Point State (middle third)\n"
        "## Phase 3: End State (final third)\n"
        "## Key Metrics Over Time (table: Metric | Start | Mid | End | Trend)\n"
        "## Emergent Behaviours Observed\n"
        "## Failure Modes Triggered (if any)\n"
        "## Sensitivity Analysis (which parameters had most impact)\n"
        "## Conclusions and Recommendations\n"
    )

    biobus.fire_signal("cognitive", "twin.simulate", f"Simulation: {req.scenario_name}", 0.7)
    simulation_result = await gateway.query(prompt, agent="digital_twin_simulator")

    sim_id = uuid.uuid4().hex[:8]
    simulation = {
        "simulation_id": sim_id,
        "scenario_name": req.scenario_name,
        "scenario_description": req.scenario_description,
        "parameters": req.parameters,
        "time_horizon": req.time_horizon,
        "result": simulation_result,
        "run_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    model["simulations"].append({k: v for k, v in simulation.items() if k != "result"})
    _save_twin(model)
    biobus.record_operation("twin_simulate", "twin.simulate", success=True, payload=req.scenario_name)

    return {"simulation_id": sim_id, "model_id": req.model_id, **simulation}


class OptimiseRequest(BaseModel):
    model_id: str
    optimisation_objective: str
    constraints: list[str] = []


@router.post("/optimise")
async def optimise_model(req: OptimiseRequest):
    """
    AI optimisation pass — find best parameter configuration for an objective.
    """
    model = _load_twin(req.model_id)
    if not model:
        raise HTTPException(status_code=404, detail=f"Model {req.model_id} not found.")

    constraints_text = "\n".join(f"- {c}" for c in req.constraints) if req.constraints else "No hard constraints specified."

    prompt = (
        f"You are an optimisation engineer working with a digital twin.\n\n"
        f"System: {model['system_name']}\n"
        f"Model:\n{model['model_spec'][:600]}\n\n"
        f"Optimisation objective: {req.optimisation_objective}\n"
        f"Constraints:\n{constraints_text}\n\n"
        "Provide:\n"
        "## Optimisation Problem Formulation (objective function, decision variables)\n"
        "## Recommended Algorithm (why this approach fits the problem)\n"
        "## Optimal Configuration (recommended parameter values)\n"
        "## Expected Performance Improvement vs Baseline\n"
        "## Trade-offs Made\n"
        "## Sensitivity to Parameter Variation\n"
        "## Validation Approach\n"
        "## Implementation Steps\n"
    )

    biobus.fire_signal("cognitive", "twin.optimise", f"Optimise: {req.optimisation_objective[:60]}", 0.7)
    result = await gateway.query(prompt, agent="digital_twin_optimiser")
    biobus.record_operation("twin_optimise", "twin.optimise", success=True, payload=model["system_name"])

    return {
        "optimisation_id": uuid.uuid4().hex[:8],
        "model_id": req.model_id,
        "objective": req.optimisation_objective,
        "result": result,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
