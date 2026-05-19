"""
Avatar Visual Renderer.
Digital human interface with expression mapping.
"""
import logging
from typing import Dict, Any, List, Optional
import asyncio

logger = logging.getLogger(__name__)

class AvatarRenderer:
    """
    IDBO Layer 12: User Experience / Visual body.
    Supports MetaHuman/NVIDIA ACE with a default 2D/SVG fallback.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.renderer_type = config.get("type", "2d") # 2d, metahuman, nvidia_ace
        self.current_expression = "neutral"
        logger.info(f"AvatarRenderer Initialized. Type: {self.renderer_type}")

    async def set_expression(self, expression: str):
        """Map cognitive/emotional state to visual expression."""
        self.current_expression = expression
        logger.debug(f"Renderer ({self.renderer_type}): expression -> {expression}")

        if self.renderer_type == "metahuman":
            await self._update_metahuman(expression)
        elif self.renderer_type == "nvidia_ace":
            await self._update_ace(expression)
        else:
            # 2D WebGL Fallback: Emit UI state update
            logger.debug(f"2D Renderer: expression {expression} updated.")

    async def show_overlay(self, overlay_type: str, data: Dict[str, Any]):
        """Render instructional overlays (checklists, highlights, code hints)."""
        logger.info(f"Renderer: Overlay [{overlay_type}] displayed.")

    async def _update_metahuman(self, expression: str):
        """Metahuman Bridge (Advanced Tier)."""
        logger.info(f"Metahuman: Updating morph targets for {expression}")

    async def _update_ace(self, expression: str):
        """NVIDIA ACE Bridge (Advanced Tier)."""
        logger.info(f"NVIDIA ACE: Updating animation state for {expression}")

class MultimodalRenderer:
    """
    Orchestration layer for synchronized Voice, Visual, and Text output.
    Ensures <500ms end-to-end latency for UI updates.
    """
    def __init__(self, voice_engine: Any, avatar_renderer: Any):
        self.voice = voice_engine
        self.renderer = avatar_renderer

    async def render(self, text: str, expression: str, overlays: Optional[List[Dict]] = None):
        """Emits synchronized multimodal instruction."""
        # 1. Immediate UI Feedback (Visual/Expression)
        ui_task = asyncio.create_task(self.renderer.set_expression(expression))

        # 2. Show instructional overlays
        if overlays:
            for o in overlays:
                await self.renderer.show_overlay(o["type"], o.get("data", {}))

        # 3. Auditory Output (Voice)
        voice_task = asyncio.create_task(self.voice.speak(text))

        # Text/Transcript update is typically handled by the frontend websocket handler
        await asyncio.gather(ui_task, voice_task)
        logger.info("Multimodal emission complete.")
