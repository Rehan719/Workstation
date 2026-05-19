"""
Skill Profiler & Adaptive Pedagogy.
Models user skill evolution using Bayesian Knowledge Tracing (BKT).
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)

@dataclass
class SkillModel:
    """Bayesian model of user competence per domain."""
    domain: str
    p_known: float  # Probability user knows the skill [0.0, 1.0]
    p_learn: float  # Probability of learning from attempt
    p_guess: float  # Probability of correct guess despite not knowing
    p_slip: float   # Probability of mistake despite knowing
    attempt_count: int
    last_updated: datetime

class SkillProfiler:
    """
    IDBO Layer 8: Recombination / Skill Adaptation.
    Tracks user competence across Workstation domains:
    - coding, writing, data_analysis, system_administration, general_productivity.
    """
    def __init__(self, ueg_logger: Any):
        self.ueg = ueg_logger
        self.profiles: Dict[str, Dict[str, SkillModel]] = {} # user_id -> domain -> model

    async def update_skill(self, user_id: str, domain: str, success: bool):
        """
        Update skill model using Bayesian Knowledge Tracing.
        Enforces online learning from every user interaction.
        """
        if user_id not in self.profiles:
            self.profiles[user_id] = self._initialize_default_profile(user_id)

        model = self.profiles[user_id].get(domain)
        if not model:
            # Domain not tracked yet
            model = self._create_domain_model(user_id, domain)
            self.profiles[user_id][domain] = model

        p_known_old = model.p_known

        # 1. Bayesian Update: P(Ln|Action)
        if success:
            # P(Ln|Correct) = (P(Ln-1)*(1-P(slip))) / (P(Ln-1)*(1-P(slip)) + (1-P(Ln-1))*P(guess))
            p_correct = (p_known_old * (1 - model.p_slip)) + ((1 - p_known_old) * model.p_guess)
            p_known_given_action = (p_known_old * (1 - model.p_slip)) / p_correct
        else:
            # P(Ln|Incorrect) = (P(Ln-1)*P(slip)) / (P(Ln-1)*P(slip) + (1-P(Ln-1))*(1-P(guess)))
            p_incorrect = (p_known_old * model.p_slip) + ((1 - p_known_old) * (1 - model.p_guess))
            p_known_given_action = (p_known_old * model.p_slip) / p_incorrect

        # 2. Transition Update: P(Ln+1) = P(Ln|Action) + (1-P(Ln|Action))*P(learn)
        model.p_known = p_known_given_action + (1 - p_known_given_action) * model.p_learn

        model.attempt_count += 1
        model.last_updated = datetime.now(timezone.utc)

        await self.ueg.log_event("AVATAR_SKILL_UPDATED", {
            "user_id": user_id,
            "domain": domain,
            "p_known": model.p_known,
            "success": success,
            "attempts": model.attempt_count
        })

    def get_skill_level(self, user_id: str, domain: str) -> str:
        """Map BKT p_known to phenotypic mode: beginner, builder, mastery, recovery."""
        model = self.profiles.get(user_id, {}).get(domain)
        if not model: return "beginner"

        pk = model.p_known
        if pk < 0.4: return "beginner"
        if pk < 0.75: return "builder"
        return "mastery"

    def _initialize_default_profile(self, user_id: str) -> Dict[str, SkillModel]:
        domains = ["coding", "writing", "data_analysis", "system_administration", "general_productivity"]
        return {d: self._create_domain_model(user_id, d) for d in domains}

    def _create_domain_model(self, user_id: str, domain: str) -> SkillModel:
        return SkillModel(
            domain=domain,
            p_known=0.2, # Prior
            p_learn=0.1,
            p_guess=0.2,
            p_slip=0.1,
            attempt_count=0,
            last_updated=datetime.now(timezone.utc)
        )
