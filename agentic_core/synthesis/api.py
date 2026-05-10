import logging
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import datetime
import uuid
import json
import os

from agentic_core.config.paths import DATA_DIR
from agentic_core.synthesis.scientific_review import review_generator
from agentic_core.synthesis.presentation import presentation_gen
from agentic_core.synthesis.business_model import business_simulator

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/synthesis", tags=["Synthesis Studio"])

class SynthesisRequest(BaseModel):
    content_ids: List[str]
    output_type: str # 'report', 'presentation', 'website', 'simulation'
    parameters: Dict[str, Any] = {}

class SynthesisOutput(BaseModel):
    output_id: str
    output_url: str
    content: str
    metadata: Dict[str, Any]
    timestamp: str

class SynthesisManager:
    def __init__(self):
        self.output_dir = DATA_DIR / "synthesis_outputs"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.history = []

    async def generate_output(self, request: SynthesisRequest) -> Dict[str, Any]:
        output_id = str(uuid.uuid4())
        timestamp = datetime.datetime.utcnow().isoformat()

        # 1. Gather Content (Simulation: reference ingestion registry or ChromaDB)
        # For this demo, we use the selected content IDs as context
        context_summary = f"Synthesizing {len(request.content_ids)} knowledge nodes..."

        # 2. Logic based on Output Type
        content = ""
        metadata = {"type": request.output_type}

        if request.output_type == "report":
            review = review_generator.generate_review("Patient Safety in Advanced Therapies", context_summary)
            content = review["markdown"]
            metadata["format"] = "md"
            metadata["title"] = review["title"]
        elif request.output_type == "presentation":
            slides = presentation_gen.generate_presentation("Patient Safety in Advanced Therapies")
            content = json.dumps(slides)
            metadata["format"] = "json"
            metadata["slides_count"] = len(slides)
        elif request.output_type == "website":
            content = "<!DOCTYPE html><html><body style='background:#0b0f19;color:#64ffda;'><h1>Sovereign Web Node</h1><p>Active and Secure.</p></body></html>"
            metadata["format"] = "zip"
        elif request.output_type == "simulation":
            model = business_simulator.generate_model(context_summary)
            content = json.dumps(model)
            metadata["format"] = "json"
            metadata["title"] = model["title"]
        else:
            content = "Autonomous process results compiled."
            metadata["format"] = "json"

        output_path = self.output_dir / f"{output_id}.{metadata['format']}"
        with open(output_path, "w") as f:
            f.write(content)

        result = {
            "output_id": output_id,
            "output_url": f"/api/v1/synthesis/download/{output_id}",
            "content": content,
            "metadata": metadata,
            "timestamp": timestamp
        }
        self.history.append(result)
        return result

synthesis_manager = SynthesisManager()

@router.post("/generate", response_model=SynthesisOutput)
async def generate_synthesis(request: SynthesisRequest):
    """v1.0: Synthesis Studio Generation Endpoint."""
    return await synthesis_manager.generate_output(request)

@router.get("/history", response_model=List[SynthesisOutput])
async def get_synthesis_history():
    return synthesis_manager.history

@router.get("/download/{output_id}")
async def download_output(output_id: str):
    # Logic to return file response
