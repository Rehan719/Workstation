import logging
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import datetime
import uuid
import json
import os

from config.paths import DATA_DIR
from agentic_core.synthesis.scientific_review import review_generator
from agentic_core.synthesis.presentation import presentation_gen
from agentic_core.synthesis.business_model import business_simulator

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/synthesis", tags=["Synthesis Studio"])

class SynthesisRequest(BaseModel):
    content_ids: List[str]
    output_type: str # 'report', 'presentation', 'website', 'simulation'
    instructions: str = ""
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

    def _generate_artifact(self, kind: str, topic: str) -> Dict[str, Any]:
        templates = {
            "app": {
                "title": f"App Scaffold: {topic}",
                "platform": "Web + Mobile (React Native bridge)",
                "core_features": [f"{topic} dashboard", "Real-time sync via Sovereign Mesh", "Role-based access control"],
                "tech_stack": ["React", "FastAPI", "WebSocket", "Zustand"],
                "status": "Scaffolded — ready for Agent Forge composition"
            },
            "agent": {
                "title": f"AI Agent/Model Spec: {topic}",
                "role": f"Autonomous specialist for {topic}",
                "model_architecture": "L12 Multi-Modal Fabric orchestration with constitutional guardrails",
                "capabilities": ["Context retrieval", "Multi-step reasoning", "Tool invocation", "Self-evaluation"],
                "guardrails": ["Constitutional AI veto layer", "GaaS compliance checks"],
                "status": "Spec generated — deployable via Agent Forge"
            },
            "product": {
                "title": f"Product Brief: {topic}",
                "value_proposition": f"Solves {topic} via sovereign, AI-orchestrated automation.",
                "target_market": "Enterprise R&D and regulatory teams",
                "pricing_model": "Tiered subscription + usage-based API",
                "status": "Brief generated — ready for Business Model Canvas"
            },
            "service": {
                "title": f"Service Definition: {topic}",
                "category": "Managed AI Orchestration",
                "delivery_model": "API + white-label dashboard",
                "sla": "99.9% uptime, <200ms mesh latency",
                "pricing_model": "Per-seat + consumption-based",
                "status": "Definition generated — ready for onboarding"
            }
        }
        artifact = dict(templates.get(kind, {"title": f"{kind.title()}: {topic}", "status": "Generated"}))
        artifact["timestamp"] = datetime.datetime.utcnow().isoformat()
        return artifact

    async def generate_output(self, request: SynthesisRequest) -> Dict[str, Any]:
        output_id = str(uuid.uuid4())
        timestamp = datetime.datetime.utcnow().isoformat()

        # 1. Gather Content (Simulation: reference ingestion registry or ChromaDB)
        # For this demo, we use the selected content IDs as context
        instructions = request.instructions.strip()
        topic = instructions or "Patient Safety in Advanced Therapies"
        context_summary = f"Synthesizing {len(request.content_ids)} knowledge nodes"
        if instructions:
            context_summary += f" per instructions: {instructions}"
        context_summary += "..."

        # 2. Logic based on Output Type
        content = ""
        metadata = {"type": request.output_type}
        if instructions:
            metadata["instructions"] = instructions

        if request.output_type == "report":
            review = review_generator.generate_review(topic, context_summary)
            content = review["markdown"]
            metadata["format"] = "md"
            metadata["title"] = review["title"]
        elif request.output_type in ("review", "analysis", "dissertation", "dossier"):
            doc_type = request.output_type.capitalize()
            review = review_generator.generate_review(topic, context_summary, doc_type=doc_type)
            content = review["markdown"]
            metadata["format"] = "md"
            metadata["title"] = review["title"]
        elif request.output_type in ("presentation", "video"):
            slides = presentation_gen.generate_presentation(topic)
            content = json.dumps(slides, indent=2)
            metadata["format"] = "json"
            metadata["slides_count"] = len(slides)
        elif request.output_type == "audiobook":
            chapters = presentation_gen.generate_audiobook(topic)
            content = json.dumps(chapters, indent=2)
            metadata["format"] = "json"
            metadata["chapters_count"] = len(chapters)
        elif request.output_type == "website":
            content = f"<!DOCTYPE html><html><body style='background:#0b0f19;color:#64ffda;'><h1>{topic}</h1><p>{context_summary}</p></body></html>"
            metadata["format"] = "zip"
        elif request.output_type in ("app", "agent", "product", "service"):
            artifact = self._generate_artifact(request.output_type, topic)
            content = json.dumps(artifact, indent=2)
            metadata["format"] = "json"
            metadata["title"] = artifact["title"]
        elif request.output_type == "business_model":
            canvas = business_simulator.generate_business_model_canvas(topic)
            content = json.dumps(canvas, indent=2)
            metadata["format"] = "json"
            metadata["title"] = canvas["title"]
        elif request.output_type == "simulation":
            model = business_simulator.generate_model(context_summary, instructions or "Long-Term Safety Assurance (LTSA)")
            content = json.dumps(model, indent=2)
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
    """v1.0: Endpoint to download synthesized output files with path traversal protection."""
    # Sanitize output_id to ensure it's just a filename, not a path
    clean_id = os.path.basename(output_id)

    # Search for any file matching the clean_id (regardless of extension)
    files = list(synthesis_manager.output_dir.glob(f"{clean_id}.*"))
    if not files:
        raise HTTPException(status_code=404, detail="Output file not found")

    file_path = files[0]
    # Final check: Ensure the resolved path is actually within the output directory
    if not str(file_path.resolve()).startswith(str(synthesis_manager.output_dir.resolve())):
        raise HTTPException(status_code=403, detail="Forbidden: Path traversal detected")

    return FileResponse(path=file_path, filename=file_path.name)
