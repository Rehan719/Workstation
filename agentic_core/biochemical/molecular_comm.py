import logging
import time
import math
from typing import Dict, Any, List, Optional
from enum import Enum

logger = logging.getLogger(__name__)

class Neurotransmitter(Enum):
    OXYTOCIN = "OXYTOCIN"   # Trust boost
    SEROTONIN = "SEROTONIN" # Mood/Stability
    DOPAMINE = "DOPAMINE"   # Reward/Motivation

class MolecularSignalingFramework:
    """
    ARTICLE 611: Molecular Communication Architecture.
    Simulates neurotransmitter-mediated signaling pathways between agents.
    Uses fractional-order diffusion approximations for propagation modeling.
    """
    def __init__(self, diffusion_coeff: float = 0.45, decay_rate: float = 0.05):
        self.diffusion_coeff = diffusion_coeff
        self.decay_rate = decay_rate
        self.active_signals: List[Dict[str, Any]] = []

    def emit_signal(self, transmitter: Neurotransmitter, concentration: float, source_agent: str):
        """Emission of a molecular signal into the shared medium."""
        signal = {
            "type": transmitter.value,
            "initial_concentration": concentration,
            "source": source_agent,
            "emitted_at": time.time(),
            "decay_factor": self.decay_rate
        }
        self.active_signals.append(signal)
        logger.info(f"MOLECULAR: {source_agent} emitted {concentration} units of {transmitter.value}")

    def get_local_concentration(self, target_agent: str, current_time: float) -> Dict[str, float]:
        """
        Calculates local concentration based on fractional-order diffusion logic.
        Concentration = Sum(Initial * exp(-decay * dt) / (diffusion * dt^alpha))
        """
        concentrations = {t.value: 0.0 for t in Neurotransmitter}

        for signal in self.active_signals:
            dt = current_time - signal["emitted_at"]
            if dt <= 0: continue

            # Simulated fractional-order diffusion (alpha=0.8)
            alpha = 0.8
            decay = math.exp(-signal["decay_factor"] * dt)
            diffusion = self.diffusion_coeff * math.pow(dt, alpha)

            local_conc = (signal["initial_concentration"] * decay) / (1 + diffusion)
            concentrations[signal["type"]] += local_conc

        return concentrations

class MolecularCommunicationSDK:
    """Enterprise-grade SDK for bio-integrated signaling."""
    def __init__(self, framework: MolecularSignalingFramework):
        self.framework = framework

    def modulate_agent_trust(self, agent_id: str, base_trust: float) -> float:
        concs = self.framework.get_local_concentration(agent_id, time.time())
        oxytocin_boost = concs.get("OXYTOCIN", 0.0) * 0.2
        return min(1.0, base_trust + oxytocin_boost)

    def modulate_swarm_motivation(self, swarm_id: str) -> float:
        concs = self.framework.get_local_concentration(swarm_id, time.time())
        dopamine_level = concs.get("DOPAMINE", 0.0)
        return dopamine_level # Returns motivation factor
