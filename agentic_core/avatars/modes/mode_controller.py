from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

class AvatarMode(Enum):
    INSTRUCTOR = "instructor"   # Step-by-step teaching
    COPILOT = "copilot"         # Real-time collaboration
    INSPECTOR = "inspector"     # Audit quality & correctness
    COACH = "coach"             # Motivation & progress tracking
    EXPLORER = "explorer"       # Ideation & discovery
    EMERGENCY = "emergency"     # Crisis recovery

@dataclass
class ModeConfig:
    mode: AvatarMode
    tone: str
    explanation_depth: str  # simple, detailed, technical
    pacing: str  # slow, moderate, fast
    vrpr_threshold: float
    cognitive_weights: Dict[str, float]

class AvatarModeManager:
    """
    Manages avatar mode transitions and configurations.
    """
    def __init__(self, ueg_logger: Any):
        self.ueg = ueg_logger
        self.current_mode = AvatarMode.INSTRUCTOR

        self.mode_configs = {
            AvatarMode.INSTRUCTOR: ModeConfig(
                mode=AvatarMode.INSTRUCTOR,
                tone="supportive_mentor",
                explanation_depth="detailed",
                pacing="moderate",
                vrpr_threshold=0.95,
                cognitive_weights={"aqal": 0.4, "samajh": 0.3, "iman": 0.3}
            ),
            AvatarMode.COPILOT: ModeConfig(
                mode=AvatarMode.COPILOT,
                tone="collaborative_partner",
                explanation_depth="technical",
                pacing="fast",
                vrpr_threshold=0.92,
                cognitive_weights={"aqal": 0.3, "soch": 0.4, "inkashaf": 0.3}
            ),
            AvatarMode.INSPECTOR: ModeConfig(
                mode=AvatarMode.INSPECTOR,
                tone="rigorous_auditor",
                explanation_depth="technical",
                pacing="moderate",
                vrpr_threshold=0.98,
                cognitive_weights={"hoshiyari": 0.5, "aqal": 0.3, "tawazun": 0.2}
            ),
            AvatarMode.COACH: ModeConfig(
                mode=AvatarMode.COACH,
                tone="inspiring_coach",
                explanation_depth="simple",
                pacing="slow",
                vrpr_threshold=0.90,
                cognitive_weights={"iman": 0.4, "tafakkur": 0.4, "samajh": 0.2}
            ),
            AvatarMode.EXPLORER: ModeConfig(
                mode=AvatarMode.EXPLORER,
                tone="curious_explorer",
                explanation_depth="detailed",
                pacing="moderate",
                vrpr_threshold=0.88,
                cognitive_weights={"soch": 0.5, "inkashaf": 0.3, "aqal": 0.2}
            ),
            AvatarMode.EMERGENCY: ModeConfig(
                mode=AvatarMode.EMERGENCY,
                tone="decisive_operator",
                explanation_depth="simple",
                pacing="fast",
                vrpr_threshold=0.99,
                cognitive_weights={"hoshiyari": 0.6, "aqal": 0.3, "tafakkur": 0.1}
            )
        }

    async def switch_mode(self, new_mode: AvatarMode, reason: str):
        """Switches the active mode with UEG logging."""
        old_mode = self.current_mode
        self.current_mode = new_mode

        await self.ueg.log_event("AVATAR_MODE_TRANSITION", {
            "from_mode": old_mode.value,
            "to_mode": new_mode.value,
            "reason": reason
        })
        logger.info(f"Avatar Mode switched from {old_mode.name} to {new_mode.name}")

    def get_current_config(self) -> ModeConfig:
        return self.mode_configs[self.current_mode]
