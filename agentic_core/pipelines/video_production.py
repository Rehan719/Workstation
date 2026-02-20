from typing import Dict, Any, List
import asyncio
from ..orchestrator import Orchestrator

class ScientificVideoPipeline:
    """
    Radical v31.0 Pipeline: Transforms a scientific topic into a narrated video.
    Chains: Research -> Writing -> Slides -> Animation -> Audio -> Video.
    """
    def __init__(self, orchestrator: Orchestrator):
        self.orchestrator = orchestrator

    async def produce_video(self, topic: str) -> Dict[str, Any]:
        """
        Executes the full end-to-end production workflow.
        """
        print(f"🎬 Starting Radical Video Production for: {topic}")

        # 1. Deep Research (PaperQA2)
        research_task = {"id": "research", "type": "advanced_research", "goal": f"Deep dive into {topic}"}
        research_results = await self.orchestrator.execute(research_task)

        # 2. Manuscript Synthesis (LaTeX Architect)
        writing_task = {"id": "writing", "type": "scientific_publication", "goal": "Write summary manuscript", "data": research_results}
        manuscript = await self.orchestrator.execute(writing_task)

        # 3. Slide Maestro (Reveal.js / Beamer)
        slide_task = {"id": "slides", "type": "presentation_generation", "goal": "Generate slide deck", "content": manuscript}
        slides = await self.orchestrator.execute(slide_task)

        # 4. Multimedia Synthesis (Manim + TTS + Video Weaver)
        video_task = {
            "id": "video",
            "type": "video_presentation",
            "goal": "Narrate and animate",
            "slides": slides,
            "enable_audio_description": True, # Article P
            "enable_whisperx_diarization": True # Advanced Audio
        }
        final_video = await self.orchestrator.execute(video_task)

        # 5. Accessibility Layer (Article P)
        if video_task.get("enable_audio_description"):
            ad_task = {"id": "audio_description", "type": "agent_direct", "assigned_agent": "audio.accessibility.v31", "video": final_video}
            final_video["accessibility"] = await self.orchestrator.execute(ad_task)

        print("✅ Production Complete.")
        return {
            "status": "success",
            "video_path": "/content/published/final_production_v31.mp4",
            "provenance_ledger": "/content/projects/latest/provenance/ledger.jsonl",
            "accessibility_meta": final_video.get("accessibility")
        }
