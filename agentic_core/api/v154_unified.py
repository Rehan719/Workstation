from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from agentic_core.layers.l1_genomic.validator import validator_l1
from agentic_core.layers.l2_runtime.inference import inference_engine
from agentic_core.layers.l4_library.registry import model_registry
from agentic_core.layers.l5_recombination.merger import model_merger

router = APIRouter(prefix="/v154", tags=["Genesis API"])

@router.get("/status")
async def get_genesis_status():
    """LAYER 6: ORCHESTRATION - Real-time system vitals."""
    return {
        "entity": "Workstation Sovereign v200.0",
        "epoch": "Genesis (v154.0)",
        "layers": {
            "L1": "Active (Constitutional)",
            "L2": "Active (Edge Runtime)",
            "L3": "Standby",
            "L4": "Active (Library)",
            "L5": "Active (Recombination)",
            "L6": "Active (Orchestration)",
            "L7": "First Light"
        },
        "constitution_root": validator_l1.root_hash
    }

@router.post("/forge/recombine")
async def trigger_recombination(model_ids: List[str], strategy: str = "TIES"):
    """LAYER 6 -> LAYER 5: Trigger model recombination."""
    # Constitutional check
    if not validator_l1.validate_action("recombine", {"models": model_ids}):
        raise HTTPException(status_code=403, detail="Recombination blocked by Article 1095.")

    if strategy == "TIES":
        res = model_merger.ties_merge(model_ids, [0.5, 0.5])
    else:
        res = model_merger.dare_merge(model_ids)

    # Register result in L4
    new_agent_did = model_registry.register_composite(res)
    return {"status": "recombined", "agent_did": new_agent_did, "metadata": res}

@router.get("/library/models")
async def list_models():
    return model_registry.registry

@router.get("/constitution/articles")
async def list_articles():
    return validator_l1.genome['constitution']['articles']
