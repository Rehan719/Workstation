import logging
import time
from typing import Dict, Any, List
from .pathway_registry import PathwayRegistry

logger = logging.getLogger(__name__)

class SignalTransductionEngine:
    """
    DA: Hierarchical Signal Transduction Engine.
    Simulates the flow of signals from receptors through transduction cascades.
    """
    def __init__(self):
        self.registry = PathwayRegistry()
        self.active_signals = []

    def receive_signal(self, signal_type: str, intensity: float, metadata: Dict[str, Any]):
        """
        Receives an extracellular signal and initiates transduction.
        """
        logger.info(f"SIGNALING: Received extracellular signal: {signal_type} (intensity={intensity})")

        # Match signal to pathway
        if signal_type == "GrowthFactor":
            self.transduce("MAPK", intensity, metadata)
        elif signal_type == "Cytokine":
            self.transduce("JAK-STAT", intensity, metadata)
        elif signal_type == "NutrientLevel":
            self.transduce("PI3K-Akt", intensity, metadata)
        else:
            logger.warning(f"SIGNALING: Unknown signal type {signal_type}. Routing to default cascade.")
            self.transduce("MAPK", intensity * 0.5, metadata)

    def transduce(self, pathway_name: str, intensity: float, metadata: Dict[str, Any]):
        pathway = self.registry.get_pathway(pathway_name)
        if not pathway:
            return

        logger.info(f"SIGNALING: Initiating {pathway_name} cascade: {pathway['description']}")

        current_intensity = intensity
        for stage in pathway['stages']:
            # Simulate attenuation and transformation at each stage
            time.sleep(0.01) # Simulate biological delay (very small for agent context)
            current_intensity *= 0.95 # Some signal loss during transduction
            logger.debug(f"SIGNALING: {pathway_name} stage {stage} completed. Current intensity: {current_intensity:.4f}")

        logger.info(f"SIGNALING: {pathway_name} reached target: {pathway['target']}")
        self.active_signals.append({
            "pathway": pathway_name,
            "final_intensity": current_intensity,
            "target": pathway['target'],
            "timestamp": time.time()
        })

    def get_nuclear_signals(self) -> List[Dict[str, Any]]:
        """
        Returns signals that have reached the 'nucleus' (transcriptional layer).
        """
        return self.active_signals
