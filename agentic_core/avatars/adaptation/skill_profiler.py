from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, Optional, Any
import logging

logger = logging.getLogger(__name__)

@dataclass
class SkillModel:
    """Bayesian model of user competence per domain."""
    domain: str
    p_known: float  # Prior probability user knows the skill
    p_learn: float  # Probability of learning from attempt
    attempt_count: int
    last_updated: datetime

class SkillProfiler:
    """
    Models user skill evolution using Bayesian Knowledge Tracing (BKT).
    Domains: coding, writing, data_analysis, system_administration, general_productivity.
    """
    def __init__(self, ueg_logger: Any):
        self.ueg = ueg_logger
        self.profiles: Dict[str, Dict[str, SkillModel]] = {} # user_id -> domain -> model

    async def update_skill(self, user_id: str, domain: str, success: bool):
        """Update skill model using Bayesian inference."""
        if user_id not in self.profiles:
            self.profiles[user_id] = self._initialize_default_profile()

        model = self.profiles[user_id].get(domain)
        if not model:
            return

        # Simple BKT update logic
        # P(Ln|Success) = P(Ln-1|Success) + (1 - P(Ln-1|Success)) * P(Learn)
        # For simplicity, we use a fixed update here
        p_known_prev = model.p_known
        if success:
            model.p_known = p_known_prev + (1 - p_known_prev) * model.p_learn
        else:
            model.p_known = p_known_prev * 0.9 # Slight decrease on failure

        model.attempt_count += 1
        model.last_updated = datetime.now(timezone.utc)

        await self.ueg.log_event("SKILL_PROFILE_UPDATED", {
            "user_id": user_id,
            "domain": domain,
            "p_known_before": p_known_prev,
            "p_known_after": model.p_known,
            "success": success
        })

    def get_skill_level(self, user_id: str, domain: str) -> str:
        """Map p_known to beginner/builder/mastery/recovery."""
        model = self.profiles.get(user_id, {}).get(domain)
        if not model:
            return "beginner"

        if model.p_known < 0.4:
            return "beginner"
        elif model.p_known < 0.8:
            return "builder"
        else:
            return "mastery"

    def _initialize_default_profile(self) -> Dict[str, SkillModel]:
        domains = ["coding", "writing", "data_analysis", "system_administration", "general_productivity"]
        return {
            d: SkillModel(
                domain=d,
                p_known=0.1,
                p_learn=0.1,
                attempt_count=0,
                last_updated=datetime.now(timezone.utc)
            ) for d in domains
        }
