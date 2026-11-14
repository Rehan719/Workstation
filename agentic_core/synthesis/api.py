import logging
import json
import re
import os
from typing import List, Dict, Any, Optional, AsyncIterator
from fastapi import APIRouter, Depends, HTTPException
from agentic_core.auth.core import get_current_user, user_can_access     # W886 (FU-995, FU-1061)
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
import datetime
import uuid

from agentic_core.store_paths import DATA_DIR
from agentic_core.ai.gateway import gateway
#  W1020 - the two template modules, synthesis/presentation.py and synthesis/business_model.py, are removed: their
#  last callers were the audiobook's and the canvas's fallbacks below, which handed a template over as the topic's
#  content when the model's reply did not parse
from agentic_core.api._ai_provenance import (reply_evidence as _reply_evidence)   # W727
from agentic_core.api._ai_provenance import wrap_material as _wrap_material886      # W886 (FU-995)


def _owner887(user) -> Optional[str]:
    """W887 - the name an output is kept under: the signed-in person, or the single-user owner label."""
    from agentic_core.auth.core import request_owner_id
    return request_owner_id(user if isinstance(user, dict) else None)


REGISTRY_PREVIEW_CHARS886 = 1000      # what the upload registry keeps of each file's text (ingestion/api.py)


def _knowledge_base886(context: str, at_limit: Optional[List[str]] = None) -> tuple:
    """W886 (FU-995) - the selected files' text, handed over as data through the shared material boundary (the cut
    recorded, a delimiter inside it defused), or nothing at all when there is none. Each file is what the upload
    registry keeps of it - its first 1,000 characters - and a file that reached that is said to be possibly longer."""
    if not context:
        return "", None
    block, record = _wrap_material886(context, label="KNOWLEDGE BASE", limit=4000)
    if at_limit:
        record["files_at_the_registry_preview_limit"] = list(at_limit)
        record["basis"] += (f"; each file is the first {REGISTRY_PREVIEW_CHARS886:,} characters the upload registry keeps "
                            f"of its text, and {len(at_limit)} reached that limit ({', '.join(at_limit[:5])}), so their "
                            f"text may be longer than what was handed over")
    return f"\n\nKnowledge base (the files the person selected, handed over as data):\n{block}", record

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
    # W490 (refutation) — the /stream done frame has carried provenance since W451; this
    # non-streaming twin recorded NONE, and the page's fallback path then badged its output
    # "structured floor" whatever had served it. The model strips extras, so the field has to
    # exist here for the truth to reach the reader at all.
    served_by: Optional[str] = None
    is_external: bool = False
    #  W659 - what was withheld from the composed text, and why (declared, or the model strips it)
    faith_content: Optional[Dict[str, Any]] = None
    owner_id: Optional[str] = None          # W887 - who asked for it; None on rows written before


#  the output types generate_output has a branch for; a guard keeps this set and the branches in step
_GENERATED_OUTPUT_TYPES = frozenset({
    "report", "review", "analysis", "dissertation", "dossier", "presentation", "video", "audiobook", "website",
    "app", "agent", "product", "service", "business_model", "simulation"})
#  W1019 - the output types composed whole and never streamed: /stream refuses them, and the studio asks /generate
_COMPOSED_WHOLE_TYPES = frozenset({"simulation"})


class SynthesisManager:
    def __init__(self):
        self.output_dir = DATA_DIR / "synthesis_outputs"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.history: List[Dict[str, Any]] = []
        # W490 — None until a call actually serves something; never defaulted to a floor claim
        self._last_served_by: Optional[str] = None
        self._last_is_external: bool = False

    # ── Context resolution ──────────────────────────────────────────────────────

    def _resolve_context(self, content_ids: List[str], user: Optional[dict] = None) -> tuple:
        """Looks up extracted text for the selected file IDs from the ingestion registry."""
        from agentic_core.ingestion.api import ingestion_manager  # lazy import — avoids circular

        parts: List[str] = []
        topic_candidates: List[str] = []
        # W495 (FU-124) — this pasted every selected file's `extracted_text` into the prompt as
        # "Knowledge base", and before this round that field held INVENTED text for every type but
        # .txt/.md: a constant for pdf/docx, a filename-pattern lookup for audio (including a scripture
        # rendering), a sentence for everything else. A file the platform could not read contributes
        # nothing to a prompt, and the skipped ones are named rather than silently thinning the context.
        skipped: List[str] = []
        not_found: List[str] = []
        for cid in content_ids:
            for entry in ingestion_manager.registry:
                if entry["file_id"] == cid:
                    #  W886 (FU-1061) - a file the caller may not see is not found, never composed into their output
                    if not user_can_access(user if isinstance(user, dict) else None, entry.get("owner_id")):
                        not_found.append(cid)
                        break
                    text = (entry.get("extracted_text") or "").strip()
                    if entry.get("status") != "EXTRACTED" or not text:
                        skipped.append(f"{entry['filename']} ({entry.get('status') or 'NOT_EXTRACTED'})")
                        break
                    parts.append(f"[Source: {entry['filename']}]\n{text}")
                    topic_candidates.append(
                        entry["filename"].rsplit(".", 1)[0].replace("_", " ").replace("-", " ").title()
                    )
                    break
        self._last_context_skipped = skipped
        self._last_context_not_found = not_found                 # W886 (FU-1061)
        self._last_context_at_limit = [e["filename"] for cid in content_ids for e in ingestion_manager.registry
                                       if e.get("file_id") == cid and e.get("status") == "EXTRACTED"
                                       and cid not in not_found
                                       and len(e.get("extracted_text") or "") >= REGISTRY_PREVIEW_CHARS886]
        if skipped:
            logger.warning("synthesis context: %d selected file(s) contributed nothing because the "
                           "platform has not read them: %s", len(skipped), "; ".join(skipped))

        context = "\n\n---\n\n".join(parts)
        inferred_topic = " · ".join(topic_candidates[:2]) if topic_candidates else "Comprehensive Analysis"
        return context, inferred_topic

    # ── AI helpers ──────────────────────────────────────────────────────────────

    def _provenance_note(self) -> str:
        """One sentence naming what served this output — or saying nothing is recorded."""
        sb = getattr(self, "_last_served_by", None)
        if not sb:
            return "no call is recorded as having composed this output"
        if getattr(self, "_last_is_external", False):
            return f"served by an external accelerant (via {sb}) — opt-in"
        if sb in ("native", "template"):
            return ("structured floor — not model analysis: composed by the deterministic native "
                    "structured engine, which arranges the headings it was asked for and does not "
                    "supply analysis")
        return f"composed in-house by {sb}"

    def _with_provenance(self, content: str, ext: str) -> str:
        note = self._provenance_note()
        if ext == "json":
            try:
                obj = json.loads(content)
                if isinstance(obj, dict):
                    obj["provenance"] = note
                    return json.dumps(obj, indent=2)
            except Exception:
                pass
            return content
        if ext in ("md", "markdown", "txt"):
            return f"> Provenance: {note}\n\n{content}"
        if ext in ("html", "htm"):
            return f"<!-- Provenance: {note} -->\n{content}"
        return content

    async def _query(self, prompt: str, tag: str, said: Optional[str] = None) -> str:
        """W490 (refutation) — `gateway.query` discards served_by, so every output this manager
        produced was unlabelled at the source. The last call's provenance is recorded for the
        response; a composition of several calls reports the last one that served it."""
        #  W646 - `said` is the person's own instructions for this output. The TOPIC is not passed as theirs:
        #  with no instructions it is inferred from the knowledge base, which they did not write.
        meta = await gateway.query_meta(prompt, agent=f"synthesis:{tag}", augment=False, user_text=(said or None))
        self._last_served_by = meta.get("served_by", "native")
        self._last_is_external = bool(meta.get("is_external"))
        return meta.get("output", "")

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

    async def generate_output(self, request: SynthesisRequest, user: Optional[dict] = None) -> Dict[str, Any]:
        output_id = str(uuid.uuid4())
        timestamp = datetime.datetime.utcnow().isoformat()
        otype = request.output_type
        #  W645 (FU-647, ledger v14 R4) - AN OUTPUT TYPE NOTHING HERE PRODUCES IS REFUSED. The fall-through
        #  below wrote {"status": "Generated"} for any string at all - a podcast, a typo - saved it to disk and
        #  filed it in the history as an output. Refused before anything is resolved, written or recorded.
        if otype not in _GENERATED_OUTPUT_TYPES:
            raise HTTPException(status_code=422, detail=(
                f"output_type {otype!r} is not one this route generates. It generates: "
                f"{', '.join(sorted(_GENERATED_OUTPUT_TYPES))}. Nothing was generated or saved."))

        context, inferred_topic = self._resolve_context(request.content_ids, user)
        instructions = request.instructions.strip()
        topic = instructions or inferred_topic

        ctx_block, _kb886 = _knowledge_base886(context, self._last_context_at_limit)   # W886 (FU-995)

        content = ""
        metadata: Dict[str, Any] = {"type": otype}
        if _kb886:
            metadata["knowledge_base_handed_over"] = _kb886
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
                f'Write a thorough {doc_label} on: "{topic}".{ctx_block}\n\n'
                f"Format as clean markdown:\n# {doc_label}: {topic}\n## Abstract\n## Introduction\n"
                f"## Analysis\n## Discussion\n## Conclusion\n\n"
                f"Be specific and cite knowledge base content where relevant."
            )
            content = await self._query(prompt, otype, said=instructions)
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
            raw = await self._query(prompt, "presentation", said=instructions)
            slides = self._extract_json_array(raw)
            if not slides:
                # W414 — this substituted presentation_gen.generate_presentation(), which returns a
                # FIXED 10-slide deck about advanced-therapy safety (AAV, CAR-T, mRNA) whatever the
                # topic, using `topic` only in slide 1's title. Slide 2 cites "Wu et al. 2025:
                # Integration risks higher than estimated" — an invented academic citation presented
                # as a research finding. Asking for a deck on any subject returned that.
                slides = [{
                    "id": 1,
                    "title": f"Presentation: {topic}",
                    "content": ("The model did not return a usable slide deck for this topic, so "
                                "none is shown."),
                    "narration": "",
                    "generated": False,
                }]
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
            raw = await self._query(prompt, "audiobook", said=instructions)
            chapters = self._extract_json_array(raw)
            narrated = bool(chapters)
            if not chapters:
                # W1020 - this substituted presentation_gen.generate_audiobook(), which narrated the FIXED deck W414
                # took off the presentation path: whatever the topic, ten chapters on AAV, CAR-T and mRNA safety citing
                # three papers that do not exist ("Wu et al 2025", "Chazarin et al 2026", "Gifford et al 2025")
                # and a market figure nothing derived. An audiobook on a bakery cooperative was narrated that.
                chapters = [{
                    "id": 1,
                    "title": f"Audiobook: {topic}",
                    "narration": "",
                    "generated": False,
                    "detail": ("The model did not return a usable audiobook for this topic, so none is narrated. "
                               "A fixed template on another subject was previously substituted here."),
                }]
            content = json.dumps(chapters, indent=2)
            #  W1020 - the count is of chapters narrated: the one that says none came back is not a chapter
            metadata.update(format="json", chapters_count=len(chapters) if narrated else 0, title=f"Audiobook: {topic}")

        # ── Website ──────────────────────────────────────────────────────────────
        elif otype == "website":
            prompt = (
                f'Write a complete single-page HTML5 website about: "{topic}".{ctx_block}\n\n'
                "Use inline CSS. Dark theme: background #0b0f19, accent #64ffda, text #e2e8f0. "
                "Include: hero section with headline, key findings, features grid, call-to-action button. "
                "Return full HTML only — no markdown fencing, no explanation."
            )
            raw = await self._query(prompt, "website", said=instructions)
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
            raw = await self._query(prompt, otype, said=instructions)
            artifact = self._extract_json_object(raw)
            if not artifact:
                # W1020 - this said the reply's first 600 characters as the specification's description, cut without
                # a word, and stamped it "Generated — ready for development": with no model, the floor's own headings
                # were offered as a specification ready to build, and with no reply the description was made up.
                artifact = {
                    "generated": False,
                    "detail": (f"The model did not return a parseable {doc_label.lower()} for this topic, so none "
                               "is shown, and nothing here is ready for development."),
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
            raw = await self._query(prompt, "business_model", said=instructions)
            canvas = self._extract_json_object(raw)
            if not canvas:
                # W1020 - this substituted business_simulator.generate_business_model_canvas(), one FIXED canvas that
                # used the topic in two strings: every business got the same segments ("Enterprise R&D teams",
                # "Regulatory bodies"), channels, partners and revenue streams, and the platform's own engines as its
                # key resources, with nothing marking it as a template.
                canvas = {
                    "generated": False,
                    "detail": ("The model did not return a parseable business model canvas for this topic, so none "
                               "is shown. A fixed template was previously substituted here."),
                }
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
                "drad_resilience has adaptation_latency_ms). "
                "No markdown — only the JSON object."
            )
            raw = await self._query(prompt, "simulation", said=instructions)
            model = self._extract_json_object(raw)
            if not model:
                # W407 — this substituted business_simulator.generate_model(), a FIXED template whose
                # figures ($4.2B market, 28% "gain via SciPy", 2.4x "faster via AI Swarms", 0.99
                # compliance) are literals and whose `data` argument is ignored entirely. Handing
                # that back when the model produced nothing presents invention as simulation.
                model = {
                    "title": f"Simulation: {topic}",
                    "generated": False,
                    "detail": ("The model did not return a parseable simulation for this topic, so "
                               "none is shown. A template was previously substituted here."),
                }
            model.setdefault("title", f"Simulation: {topic}")
            model["timestamp"] = timestamp
            # W407 — this used to GRAFT fabricated figures onto a real model result: when the AI
            # reply lacked sim_results it copied them from business_simulator (a fixed template),
            # and when it lacked projections it injected the literals
            #     {"year_1": 4.5e7, "year_3": 2.1e8, "year_5": 8.4e8}.
            # The output was then a blend of genuine model reasoning and invented financials with
            # nothing marking which was which — the consumer could not tell them apart, and the UI
            # rendered both identically. Real mixed with fabricated is worse than either alone.
            #
            # Absence is now reported as absence. The dashboard shows what the model produced and
            # says plainly when it produced no simulation.
            if not isinstance(model.get("sim_results"), dict) or not model.get("sim_results"):
                model["sim_results"] = None
                model["sim_results_note"] = ("The model did not return simulation results. None are "
                                             "shown, because any shown here would be invented.")
            if not model.get("projections"):
                model["projections"] = None
                model["projections_note"] = ("The model did not return financial projections. None "
                                             "are shown.")
            content = json.dumps(model, indent=2)
            metadata.update(format="json", title=model["title"])

        else:   # unreachable while the refusal above and the branches agree; if they ever disagree, SAY SO
            raise HTTPException(status_code=500, detail=(
                f"output_type {otype!r} is listed as generated and no branch produces it. Nothing was generated."))

        # ── Persist to disk ──────────────────────────────────────────────────────
        #  W659 - Arabic script in what was COMPOSED is withheld before the text is written, stored or returned
        from agentic_core.religious_domain.composed_text import withhold_arabic as _withhold659
        content, _faith659 = _withhold659(content)
        ext = metadata.get("format", "json")
        output_path = self.output_dir / f"{output_id}.{ext}"
        # W490 (refutation) — the DOWNLOADED file is served straight off disk, so a provenance line
        # rendered in the browser never reaches it. The file now carries what composed it, in the same
        # words as everywhere else; a JSON output carries it as a field rather than a comment.
        with open(output_path, "w", encoding="utf-8") as fh:
            fh.write(self._with_provenance(content, ext))

        result: Dict[str, Any] = {**_reply_evidence(getattr(self, '_last_served_by', None)), 
            "output_id": output_id,
            "output_url": f"/api/v1/synthesis/download/{output_id}",
            "content": content,
            "metadata": metadata,
            "timestamp": timestamp,
            "faith_content": _faith659,
            # W490 — None when no call served this output; the page renders that as "not recorded"
            "served_by": getattr(self, "_last_served_by", None),
            "is_external": bool(getattr(self, "_last_is_external", False)),
            "owner_id": _owner887(user),           # W887 - who asked for it
        }
        self.history.append(result)
        logger.info("Synthesis complete: type=%s id=%s", otype, output_id)
        return result


synthesis_manager = SynthesisManager()


@router.post("/generate", response_model=SynthesisOutput)
async def generate_synthesis(request: SynthesisRequest, user: dict | None = Depends(get_current_user)):
    """AI-powered multi-modal synthesis from knowledge base content."""
    #  W659 - the person's instructions, before anything is composed
    from agentic_core.religious_domain.composed_text import refuse_faith_ruling as _refuse_ruling659
    _refuse_ruling659(request.instructions, "synthesis request")
    return await synthesis_manager.generate_output(request, user if isinstance(user, dict) else None)


@router.post("/stream")
async def stream_synthesis(request: SynthesisRequest, user: dict | None = Depends(get_current_user)):
    """
    Server-Sent Events endpoint that streams the synthesis token-by-token.
    On completion emits a final JSON event with the full output_id and download URL.
    """
    #  W659 - refused HERE, before the generator exists: a refusal raised inside a stream arrives after a 200
    from agentic_core.religious_domain.composed_text import refuse_faith_ruling as _refuse_ruling659
    _refuse_ruling659(request.instructions, "synthesis request")
    #  W1019 - A SIMULATION IS COMPOSED WHOLE. This route fell through to its markdown prompt for one and saved the
    #  reply as a .json file, so the studio's dashboard, which parses the simulation, drew nothing on the path the
    #  studio tries first, and the download was markdown under a .json name, without the provenance a parsed
    #  simulation's download carries. /generate asks the model for the simulation's structure and says when none came
    #  back. Refused before anything is asked, written or recorded, and after the ruling check, as /generate refuses.
    if request.output_type in _COMPOSED_WHOLE_TYPES:
        raise HTTPException(status_code=422, detail=(
            f"output_type {request.output_type!r} is composed whole, not streamed: POST /api/v1/synthesis/generate "
            "asks the model for its structure and says when none came back. Nothing was generated or saved."))
    context, inferred_topic = synthesis_manager._resolve_context(request.content_ids,
                                                                 user if isinstance(user, dict) else None)
    instructions = request.instructions.strip()
    topic = instructions or inferred_topic
    ctx_block, _kb886 = _knowledge_base886(context, synthesis_manager._last_context_at_limit)   # W886 (FU-995)
    otype = request.output_type

    label_map = {
        "report": "Report", "review": "Scientific Review", "analysis": "Analysis",
        "dissertation": "Dissertation", "dossier": "Intelligence Dossier",
    }

    if otype in label_map:
        doc_label = label_map[otype]
        prompt = (
            f'Write a thorough {doc_label} on: "{topic}".{ctx_block}\n\n'
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
    from agentic_core.auth.core import request_owner_id as _rqo886
    _stream_owner886 = _rqo886(user if isinstance(user, dict) else None)   # W886 - the stream records under its caller

    async def event_stream() -> AsyncIterator[str]:
        fin: dict = {}
        #  W659 - a run of Arabic script can be split across tokens; the filter keeps the state between them
        from agentic_core.religious_domain.composed_text import ArabicStreamFilter as _Filter659
        from agentic_core.religious_domain.composed_text import withhold_arabic as _withhold659
        _flt659 = _Filter659()
        # W451 — stream_meta: the done frame discloses who served it and whether the profile shaped it
        # P2.2 (W511) — stated, not inherited. This was one of the 29 call sites W489 found carrying
        # another request's content when the default was True.
        async for ev in gateway.stream_meta(prompt, agent=f"synthesis:stream:{otype}", augment=False,
                                            user_text=(instructions or None),   # W646
                                            owner_id=_stream_owner886):         # W886
            if "token" in ev:
                _tok659 = _flt659.feed(ev["token"])
                collected.append(_tok659)
                safe = _tok659.replace("\n", "\\n").replace("\r", "")
                yield f"data: {json.dumps({'token': safe})}\n\n"
            elif ev.get("done"):
                fin = ev

        # Persist full content (the guardrail's replacement, never a violation — as query_meta persists)
        if fin.get("guardrail_passed") is not False:
            content, _faith659 = "".join(collected), _flt659.record()
        else:
            content, _faith659 = _withhold659(fin.get("output") or "")
        ext = "html" if otype == "website" else ("json" if otype in ("presentation", "video", "audiobook", "business_model", "simulation") else "md")
        output_path = synthesis_manager.output_dir / f"{output_id}.{ext}"
        # W490 (refutation) — the STREAM path persists its own file too; it carries the provenance the
        # done frame already reports, so the downloaded copy says what the screen said.
        synthesis_manager._last_served_by = fin.get("served_by") or None
        synthesis_manager._last_is_external = bool(fin.get("is_external"))
        output_path.write_text(synthesis_manager._with_provenance(content, ext), encoding="utf-8")
        synthesis_manager.history.append({**_reply_evidence(fin.get('served_by') or None), 
            "output_id": output_id,
            "output_url": f"/api/v1/synthesis/download/{output_id}",
            "content": content,
            "owner_id": _owner887(user),           # W887 - who asked for it
            "metadata": {"type": otype, "format": ext, "title": topic,
                         **({"knowledge_base_handed_over": _kb886} if _kb886 else {})},     # W886 (FU-995)
            "timestamp": timestamp,
            #  W645 (FU-647) - the stream's history row carries what served it, as the done frame does. Without
            #  these the response model filled is_external False by default, whatever had actually served.
            "served_by": fin.get("served_by") or None,
            "is_external": bool(fin.get("is_external")),
            "faith_content": _faith659,
        })

        # W494 (FU-148 refutation) - the done frame sent no `format` and no `slides_count`, so the
        # studio page invented `format: 'md'` for every streamed type and its slides_count branch was
        # dead. Both are computed here already (`ext`, and the content for a slide deck is the JSON the
        # player parses), so the stream reports them instead of leaving the page to guess. slides_count
        # is omitted rather than defaulted when the content does not parse to a deck.
        _slides_n = None
        if otype in ("presentation", "video"):
            try:
                _parsed = json.loads(content)
                if isinstance(_parsed, list):
                    _slides_n = len(_parsed)
                elif isinstance(_parsed, dict) and isinstance(_parsed.get("slides"), list):
                    _slides_n = len(_parsed["slides"])
            except Exception:
                _slides_n = None
        _done = {**_reply_evidence(fin.get('served_by')), 'done': True, 'output_id': output_id,
                 'download_url': f'/api/v1/synthesis/download/{output_id}', 'timestamp': timestamp,
                 'format': ext,
                 'served_by': fin.get('served_by'), 'is_external': bool(fin.get('is_external')),
                 'profile_applied': bool(fin.get('profile_applied')),
                 'faith_content': _faith659,
                 'model_tokens': fin.get('model_tokens'), 'model_tokens_basis': fin.get('model_tokens_basis')}   # W776
        if _slides_n is not None:
            _done['slides_count'] = _slides_n
        yield f"data: {json.dumps(_done)}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream", headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@router.get("/history", response_model=List[SynthesisOutput])
async def get_synthesis_history(user: dict | None = Depends(get_current_user)):
    """Returns the synthesis outputs generated in this server session that the caller may see. W887 - with sign-in
    on this listed every person's outputs, whole."""
    u = user if isinstance(user, dict) else None
    return [r for r in reversed(synthesis_manager.history) if user_can_access(u, r.get("owner_id"))]


@router.get("/download/{output_id}")
async def download_output(output_id: str, user: dict | None = Depends(get_current_user)):
    """Downloads a synthesized output file. Protected against path traversal. W887 - another person's output is not
    found; a file with no history row has no owner to match, so under sign-in it is an administrator's."""
    clean_id = os.path.basename(output_id)
    _row887 = next((r for r in synthesis_manager.history if r.get("output_id") == clean_id), None)
    if not user_can_access(user if isinstance(user, dict) else None, (_row887 or {}).get("owner_id")):
        raise HTTPException(status_code=404, detail="Output file not found")
    files = list(synthesis_manager.output_dir.glob(f"{clean_id}.*"))
    if not files:
        raise HTTPException(status_code=404, detail="Output file not found")
    file_path = files[0]
    if not str(file_path.resolve()).startswith(str(synthesis_manager.output_dir.resolve())):
        raise HTTPException(status_code=403, detail="Forbidden")
    return FileResponse(path=file_path, filename=file_path.name)
