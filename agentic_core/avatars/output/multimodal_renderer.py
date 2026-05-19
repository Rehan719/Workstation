import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class AvatarRenderer:
    """
    Visual body of the avatar.
    Supports MetaHuman/NVIDIA ACE with a default 2D/SVG fallback.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.renderer_type = config.get("type", "2d") # 2d, metahuman, nvidia_ace
        self.current_expression = "neutral"

    async def set_expression(self, expression: str):
        """Map cognitive/emotional state to visual expression."""
        self.current_expression = expression
        logger.info(f"Renderer ({self.renderer_type}): Setting expression to {expression}")

        if self.renderer_type == "metahuman":
            await self._update_metahuman(expression)
        elif self.renderer_type == "nvidia_ace":
            await self._update_ace(expression)
        else:
            # 2D fallback: In a web interface, this would emit a WebSocket event
            logger.debug(f"2D Renderer: expression {expression} updated.")

    async def show_overlay(self, overlay_type: str, data: Dict[str, Any]):
        """Render UI overlays (checklists, highlights)."""
        logger.info(f"Renderer: Showing {overlay_type} overlay")

    async def _update_metahuman(self, expression: str):
        """Metahuman Bridge (Advanced Tier)."""
        logger.info(f"Metahuman: Updating expression to {expression}")

    async def _update_ace(self, expression: str):
        """NVIDIA ACE Bridge (Advanced Tier)."""
        logger.info(f"NVIDIA ACE: Updating expression to {expression}")

class MultimodalRenderer:
    """Synchronizes Voice, Visual, and Text output."""
    def __init__(self, voice_engine: Any, avatar_renderer: Any):
        self.voice = voice_engine
        self.renderer = avatar_renderer

    async def render(self, text: str, expression: str, overlays: Optional[List[Dict]] = None):
        """Emits multimodal output."""
        # 1. Update visual expression
        await self.renderer.set_expression(expression)

        # 2. Show overlays if any
        if overlays:
            for o in overlays:
                await self.renderer.show_overlay(o["type"], o.get("data", {}))

        # 3. Speak the text (usually the longest operation)
        await self.voice.speak(text)

        # 4. Text output is handled by the frontend interface
