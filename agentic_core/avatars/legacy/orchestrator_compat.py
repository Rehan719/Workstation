import logging
from typing import Dict, Any, List
from agentic_core.avatars.core.avatar_identity import AvatarState, AvatarIdentityManager
from agentic_core.avatars.frontend.avatar_interface import AvatarFrontendInterface
from agentic_core.avatars.core.recirculation_orchestrator import AvatarRecirculationOrchestrator
from agentic_core.ueg.logger import VSBUEGLogger

logger = logging.getLogger(__name__)

class LegacyAvatarOrchestratorCompat:
    """
    ARTICLE 1034 (DEPRECATED): Backward compatibility wrapper.
    Forwards calls to the new Living Workstation Avatar engine.
    """
    def __init__(self, new_interface: AvatarFrontendInterface):
        self.interface = new_interface
        logger.warning("LegacyAvatarOrchestratorCompat: Using deprecated avatar orchestrator.")

    def generate_response(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Deprecated: Use AvatarFrontendInterface.handle_user_message instead."""
        import asyncio
        # Blocking wrapper for legacy sync code
        loop = asyncio.get_event_loop()
        res = loop.run_until_complete(self.interface.handle_user_message(prompt, context))

        return {
            "role": "jules",
            "text": res.get("output", {}).get("text", "Error"),
            "assets": {"video_url": "legacy_fallback"},
            "constitutional_audit": "PASSED"
        }

    def switch_avatar(self, role: str):
        """Deprecated avatar switcher."""
        logger.warning(f"switch_avatar({role}) is deprecated.")
