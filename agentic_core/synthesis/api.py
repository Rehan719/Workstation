import logging
import json
import re
import os
from typing import List, Dict, Any, Optional, AsyncIterator
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
import datetime
import uuid

from config.paths import DATA_DIR
from agentic_core.ai.gateway import gateway
from agentic_core.synthesis.presentation import presentation_gen
from agentic_core.synthesis.business_model import business_simulator

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/synthesis", tags=["Synthesis Studio"])


class SynthesisRequest(BaseModel):
    content_ids: List[str]
    output_type: str
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
        self.history: List[Dict[str, Any]] = []

    # ── Context resolution ──────────────────────────────────────────────────────

    def _resolve_context(self, content_ids: List[str]) -> tuple:
        """Looks up extracted text for the selected file IDs from the ingestion registry."""
        from agentic_core.ingestion.api import ingestion_manager  # lazy import — avoids circular

        parts: List[str] = []
        topic_candidates: List[str] = []
        for cid in content_ids:
            for entry in ingestion_manager.registry:
                if entry["file_id"] == cid:
                    text = entry.get("extracted_text", "")
                    parts.append(f"[Source: {entry['filename']}]\n{text}")
                    topic_candidates.append(
                        entry["filename"].rsplit(".", 1)[0].replace("_", " ").replace("-", " ").title()
                    )
                    break

        context = "\n\n---\n\n".join(parts)
        inferred_topic = " · ".join(topic_candidates[:2]) if topic_candidates else "Comprehensive Analysis"
        return context, inferred_topic

    # ── AI helpers ──────────────────────────────────────────────────────────────

    async def _query(self, prompt: str, tag: str) -> str:
        return await gateway.query(prompt, agent=f"synthesis:{tag}")

    @staticmethod
    def _extract_json_array(text: str) -> Optional[list]:
        m = re.search(r'\[[\s\S]*?\]', text, re.DOTALL)
        if m:
            try:
                return json.loads(m.group())
            except json.JSONDecodeError:
                pass
        return None

    @staticmethod
    def _extract_json_object(text: str) -> Optional[dict]:
        # Prefer outermost complete object
        m = re.search(r'\{[\s\S]*\}', text, re.DOTALL)
        if m:
            try:
                return json.loads(m.group())
            except json.JSONDecodeError:
                pass
        return None

    # ── Main generation entry point ──────────────────────────────────────────────

    async def generate_output(self, request: SynthesisRequest) -> Dict[str, Any]:
        output_id = str(uuid.uuid4())
        timestamp = datetime.datetime.utcnow().isoformat()
        otype = request.output_type

        context, inferred_topic = self._resolve_context(request.content_ids)
        instructions = request.instructions.strip()
        topic = instructions or inferred_topic

        ctx_block = f"\n\nKnowledge base:\n{context[:4000]}" if context else ""

        content = ""
        metadata: Dict[str, Any] = {"type": otype}
        if instructions:
            metadata["instructions"] = instructions

        # ── Document types ───────────────────────────────────────────────────────
        if otype in ("report", "review", "analysis", "dissertation", "dossier"):
            label_map = {
                "report": "Report",
                "review": "Scientific Review",
                "analysis": "Analysis",
                "dissertation": "Dissertation",
                "dossier": "Intelligence Dossier",
            }
            doc_label = label_map[otype]
            prompt = (
                f'You are a world-class analyst. Write a thorough professional {doc_label} on: "{topic}".{ctx_block}\n\n'
                f"Format as clean markdown:\n# {doc_label}: {topic}\n## Abstract\n## Introduction\n"
                f"## Analysis\n## Discussion\n## Conclusion\n\n"
                f"Be specific and cite knowledge base content where relevant."
            )
            content = await self._query(prompt, otype)
            if not content.strip().startswith("#"):
                content = f"# {doc_label}: {topic}\n\n{content}"
            metadata.update(format="md", title=f"{doc_label}: {topic}")

        # ── Presentation / Video ─────────────────────────────────────────────────
        elif otype in ("presentation", "video"):
            prompt = (
                f'Create a 10-slide executive presentation on: "{topic}".{ctx_block}\n\n'
                "Return ONLY a JSON array of exactly 10 slide objects, each with keys: "
                'id (int), title (str), content (str), narration (str). '
                "No markdown, no explanation — only the JSON array."
            )
            raw = await self._query(prompt, "presentation")
            slides = self._extract_json_array(raw)
            if not slides:
                slides = presentation_gen.generate_presentation(topic)
            for i, s in enumerate(slides):
                s.setdefault("id", i + 1)
                s.setdefault("animation", ["fade-in", "slide-left", "zoom-in"][i % 3])
            content = json.dumps(slides, indent=2)
            metadata.update(format="json", slides_count=len(slides), title=f"Presentation: {topic}")

        # ── Audiobook ────────────────────────────────────────────────────────────
        elif otype == "audiobook":
            prompt = (
                f'Create a 10-chapter audiobook on: "{topic}".{ctx_block}\n\n'
                "Return ONLY a JSON array of 10 chapter objects with keys: "
                "id (int), title (str), narration (str, 4-6 sentences), duration_sec (int). "
                "No markdown, no explanation — only the JSON array."
            )
            raw = await self._query(prompt, "audiobook")
            chapters = self._extract_json_array(raw)
            if not chapters:
                chapters = presentation_gen.generate_audiobook(topic)
            content = json.dumps(chapters, indent=2)
            metadata.update(format="json", chapters_count=len(chapters), title=f"Audiobook: {topic}")

        # ── Website ──────────────────────────────────────────────────────────────
        elif otype == "website":
            prompt = (
                f'Write a complete single-page HTML5 website about: "{topic}".{ctx_block}\n\n'
                "Use inline CSS. Dark theme: background #0b0f19, accent #64ffda, text #e2e8f0. "
                "Include: hero section with headline, key findings, features grid, call-to-action button. "
                "Return full HTML only — no markdown fencing, no explanation."
            )
            raw = await self._query(prompt, "website")
            raw = raw.strip()
            if not raw.startswith("<!"):
                content = (
                    f'<!DOCTYPE html><html><head><meta charset="utf-8"><title>{topic}</title>'
                    f'<style>body{{background:#0b0f19;color:#e2e8f0;font-family:system-ui;'
                    f'max-width:860px;margin:0 auto;padding:2rem}}'
                    f'h1,h2{{color:#64ffda}}</style></head>'
                    f'<body>{raw}</body></html>'
                )
            else:
                content = raw
            metadata.update(format="html", title=f"Website: {topic}")

        # ── Buildable artifacts ──────────────────────────────────────────────────
        elif otype in ("app", "agent", "product", "service"):
            label_map = {
                "app": "Application Specification",
                "agent": "AI Agent Blueprint",
                "product": "Product Brief",
                "service": "Service Definition",
            }
            doc_label = label_map[otype]
            prompt = (
                f'Generate a detailed {doc_label} JSON for: "{topic}".{ctx_block}\n\n'
                f"Return ONLY a JSON object with keys: title, description, key_features (array of strings), "
                f"technical_stack (array of strings), value_proposition, target_audience, "
                f"implementation_phases (array of {{phase, milestone, timeline}}), status. "
                f"Be specific and detailed. No markdown — only the JSON object."
            )
            raw = await self._query(prompt, otype)
            artifact = self._extract_json_object(raw)
            if not artifact:
                artifact = {
                    "title": f"{doc_label}: {topic}",
                    "description": raw[:600] if raw else f"Specification for {topic}",
                    "status": "Generated — ready for development",
                }
            artifact.setdefault("title", f"{doc_label}: {topic}")
            artifact["timestamp"] = timestamp
            content = json.dumps(artifact, indent=2)
            metadata.update(format="json", title=artifact["title"])

        # ── Business Model Canvas ────────────────────────────────────────────────
        elif otype == "business_model":
            prompt = (
                f'Generate a comprehensive Business Model Canvas for: "{topic}".{ctx_block}\n\n'
                "Return ONLY a JSON object with keys: title, value_proposition, "
                "customer_segments (array), channels (array), customer_relationships, "
                "revenue_streams (array), key_resources (array), key_activities (array), "
                "key_partners (array), cost_structure (array), market_opportunity, "
                "competitive_advantage. No markdown — only the JSON object."
            )
            raw = await self._query(prompt, "business_model")
            canvas = self._extract_json_object(raw)
            if not canvas:
                canvas = business_simulator.generate_business_model_canvas(topic)
            canvas.setdefault("title", f"Business Model Canvas: {topic}")
            canvas["timestamp"] = timestamp
            content = json.dumps(canvas, indent=2)
            metadata.update(format="json", title=canvas["title"])

        # ── Simulation ───────────────────────────────────────────────────────────
        elif otype == "simulation":
            prompt = (
                f'Generate a detailed market simulation JSON for: "{topic}".{ctx_block}\n\n'
                "Return ONLY a JSON object with keys: "
                "title, market_summary, projections ({{year_1, year_3, year_5}} as USD numbers), "
                "roi_analysis (string), "
                "sim_results (object with ese_adoption, aro_efficiency, bto_roadmap, drad_resilience — "
                "matching the structure: ese_adoption has early_adopter/fast_follower/laggard each with revenue+market_share, "
                "aro_efficiency has resource_optimization_gain+cost_reduction_per_patient, "
                "bto_roadmap has implementation_speed_multiplier+milestone_confidence, "
                "drad_resilience has compliance_score+adaptation_latency_ms). "
                "No markdown — only the JSON object."
            )
            raw = await self._query(prompt, "simulation")
            model = self._extract_json_object(raw)
            if not model:
                model = business_simulator.generate_model(context[:2000] or topic, topic)
            model.setdefault("title", f"Simulation: {topic}")
            model["timestamp"] = timestamp
            # Ensure BusinessModelDashboard has the required sim_results shape
            if "sim_results" not in model or not isinstance(model.get("sim_results"), dict):
                fallback = business_simulator.generate_model(context[:500] or topic, topic)
                model["sim_results"] = fallback["sim_results"]
            if "projections" not in model:
                model["projections"] = {"year_1": 4.5e7, "year_3": 2.1e8, "year_5": 8.4e8}
            content = json.dumps(model, indent=2)
            metadata.update(format="json", title=model["title"])

        else:
            content = json.dumps({"title": f"{otype.title()}: {topic}", "status": "Generated", "timestamp": timestamp}, indent=2)
            metadata.update(format="json", title=f"{otype.title()}: {topic}")

        # ── Persist to disk ──────────────────────────────────────────────────────
        ext = metadata.get("format", "json")
        output_path = self.output_dir / f"{output_id}.{ext}"
        with open(output_path, "w", encoding="utf-8") as fh:
            fh.write(content)

        result: Dict[str, Any] = {
            "output_id": output_id,
            "output_url": f"/api/v1/synthesis/download/{output_id}",
            "content": content,
            "metadata": metadata,
            "timestamp": timestamp,
        }
        self.history.append(result)
        logger.info("Synthesis complete: type=%s id=%s", otype, output_id)
        return result


synthesis_manager = SynthesisManager()


@router.post("/generate", response_model=SynthesisOutput)
async def generate_synthesis(request: SynthesisRequest):
    """AI-powered multi-modal synthesis from knowledge base content."""
    return await synthesis_manager.generate_output(request)


@router.post("/stream")
async def stream_synthesis(request: SynthesisRequest):
    """
    Server-Sent Events endpoint that streams the synthesis token-by-token.
    On completion emits a final JSON event with the full output_id and download URL.
    """
    context, inferred_topic = synthesis_manager._resolve_context(request.content_ids)
    instructions = request.instructions.strip()
    topic = instructions or inferred_topic
    ctx_block = f"\n\nKnowledge base:\n{context[:4000]}" if context else ""
    otype = request.output_type

    label_map = {
        "report": "Report", "review": "Scientific Review", "analysis": "Analysis",
        "dissertation": "Dissertation", "dossier": "Intelligence Dossier",
    }

    if otype in label_map:
        doc_label = label_map[otype]
        prompt = (
            f'You are a world-class analyst. Write a thorough professional {doc_label} on: "{topic}".{ctx_block}\n\n'
            f"Format as clean markdown with sections: Abstract, Introduction, Analysis, Discussion, Conclusion. "
            f"Be specific and cite knowledge base content where relevant."
        )
    elif otype in ("presentation", "video"):
        prompt = (
            f'Create a 10-slide executive presentation on: "{topic}".{ctx_block}\n\n'
            "Return a JSON array of 10 slide objects, each with: id (int), title (str), content (str), narration (str)."
        )
    elif otype == "website":
        prompt = (
            f'Write a complete single-page HTML5 website about: "{topic}".{ctx_block}\n\n'
            "Dark theme: background #0b0f19, accent #64ffda, text #e2e8f0. "
            "Include: hero, key findings, features grid, CTA. Return full HTML only."
        )
    elif otype == "business_model":
        prompt = (
            f'Generate a comprehensive Business Model Canvas for: "{topic}".{ctx_block}\n\n'
            "Return a JSON object with: title, value_proposition, customer_segments, channels, "
            "revenue_streams, key_resources, key_activities, key_partners, cost_structure, "
            "market_opportunity, competitive_advantage."
        )
    else:
        prompt = (
            f'Generate a detailed {otype} document on: "{topic}".{ctx_block}\n\n'
            "Return clean markdown."
        )

    output_id = str(uuid.uuid4())
    timestamp = datetime.datetime.utcnow().isoformat()
    collected: list[str] = []

    async def event_stream() -> AsyncIterator[str]:
        async for token in gateway.stream(prompt, agent=f"synthesis:stream:{otype}"):
            collected.append(token)
            safe = token.replace("\n", "\\n").replace("\r", "")
            yield f"data: {json.dumps({'token': safe})}\n\n"

        # Persist full content
        content = "".join(collected)
        ext = "html" if otype == "website" else ("json" if otype in ("presentation", "video", "audiobook", "business_model", "simulation") else "md")
        output_path = synthesis_manager.output_dir / f"{output_id}.{ext}"
        output_path.write_text(content, encoding="utf-8")
        synthesis_manager.history.append({
            "output_id": output_id,
            "output_url": f"/api/v1/synthesis/download/{output_id}",
            "content": content,
            "metadata": {"type": otype, "format": ext, "title": topic},
            "timestamp": timestamp,
        })

        yield f"data: {json.dumps({'done': True, 'output_id': output_id, 'download_url': f'/api/v1/synthesis/download/{output_id}', 'timestamp': timestamp})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream", headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@router.get("/history", response_model=List[SynthesisOutput])
async def get_synthesis_history():
    """Returns all synthesis outputs generated in this server session."""
    return list(reversed(synthesis_manager.history))


@router.get("/download/{output_id}")
async def download_output(output_id: str):
    """Downloads a synthesized output file. Protected against path traversal."""
    clean_id = os.path.basename(output_id)
    files = list(synthesis_manager.output_dir.glob(f"{clean_id}.*"))
    if not files:
        raise HTTPException(status_code=404, detail="Output file not found")
    file_path = files[0]
    if not str(file_path.resolve()).startswith(str(synthesis_manager.output_dir.resolve())):
        raise HTTPException(status_code=403, detail="Forbidden")
    return FileResponse(path=file_path, filename=file_path.name)
