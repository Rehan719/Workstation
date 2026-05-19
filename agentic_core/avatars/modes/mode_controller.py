"""
Avatar Mode Controller (vΩ∞-CONVERGED).
Dynamic Phenotype Switching and Cognitive Weight Balancing.
"""
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
    interruption_policy: str # always, when_confused, never

class AvatarModeManager:
    """
    IDBO Layer 9/12: Orchestration & UX.
    Manages avatar mode transitions and configurations.
    Enforces mode-specific cognitive load balancing.
    """
    def __init__(self, ueg_logger: Any):
        self.ueg = ueg_logger
        self.current_mode = AvatarMode.INSTRUCTOR

        self.mode_configs = {
            AvatarMode.INSTRUCTOR: ModeConfig(
                mode=AvatarMode.INSTRUCTOR,
                tone="patient_mentor",
                explanation_depth="detailed",
                pacing="moderate",
                vrpr_threshold=0.95,
                cognitive_weights={"aqal": 0.4, "samajh": 0.3, "iman": 0.3},
                interruption_policy="when_confused"
            ),
            AvatarMode.COPILOT: ModeConfig(
                mode=AvatarMode.COPILOT,
                tone="collaborative_partner",
                explanation_depth="technical",
                pacing="fast",
                vrpr_threshold=0.92,
                cognitive_weights={"soch": 0.3, "aqal": 0.3, "iman": 0.2, "inkashaf": 0.2},
                interruption_policy="always"
            ),
            AvatarMode.INSPECTOR: ModeConfig(
                mode=AvatarMode.INSPECTOR,
                tone="precise_auditor",
                explanation_depth="technical",
                pacing="moderate",
                vrpr_threshold=0.98,
                cognitive_weights={"hoshiyari": 0.5, "aqal": 0.3, "tawazun": 0.2},
                interruption_policy="when_confused"
            ),
            AvatarMode.COACH: ModeConfig(
                mode=AvatarMode.COACH,
                tone="inspiring_coach",
                explanation_depth="simple",
                pacing="slow",
                vrpr_threshold=0.90,
                cognitive_weights={"iman": 0.4, "tawazun": 0.3, "hoshiyari": 0.2, "samajh": 0.1},
                interruption_policy="always"
            ),
            AvatarMode.EXPLORER: ModeConfig(
                mode=AvatarMode.EXPLORER,
                tone="curious_explorer",
                explanation_depth="detailed",
                pacing="moderate",
                vrpr_threshold=0.88,
                cognitive_weights={"soch": 0.5, "inkashaf": 0.3, "samajh": 0.2},
                interruption_policy="always"
            ),
            AvatarMode.EMERGENCY: ModeConfig(
                mode=AvatarMode.EMERGENCY,
                tone="decisive_operator",
                explanation_depth="simple",
                pacing="fast",
                vrpr_threshold=0.99,
                cognitive_weights={"hoshiyari": 0.6, "aqal": 0.3, "niyyah": 0.1},
                interruption_policy="never"
            )
        }

    async def switch_mode(self, new_mode: AvatarMode, reason: str):
        """Switches phenotypic mode with UEG logging."""
        old_mode = self.current_mode
        self.current_mode = new_mode

        await self.ueg.log_event("AVATAR_PHENOTYPE_SWITCH", {
            "from": old_mode.value,
            "to": new_mode.value,
            "reason": reason,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        logger.info(f"Avatar switched to {new_mode.name} phenotype.")

    def get_current_config(self) -> ModeConfig:
        return self.mode_configs[self.current_mode]
