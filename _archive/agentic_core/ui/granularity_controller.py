import logging
import time
from typing import Dict, Any, List
from agentic_core.transition.graduated_transition_manager import GraduatedTransitionManager

logger = logging.getLogger(__name__)

class GranularityController:
    """
    ARTICLE 135: Behavior-Driven Granularity.
    Adapts cognitive detail based on multi-objective utility (System Load, Confidence, Telemetry).
    """
    def __init__(self, transition_mgr: GraduatedTransitionManager = None):
        self.modes = ["summary", "detailed", "expert"]
        self.current_mode = "detailed"
        self.transition_mgr = transition_mgr or GraduatedTransitionManager()
        self.telemetry_history = []
        self.confidence_threshold = 0.82

    def evaluate_granularity(self, system_metrics: Dict[str, Any]) -> str:
        """
        Multi-objective utility function for granularity adjustment.
        Utility = (Confidence * 0.4) - (SystemLoad * 0.3) + (UserEngagement * 0.3)
        """
        confidence = system_metrics.get("cognitive_confidence", 0.5)
        load = system_metrics.get("system_load", 0.1)
        engagement = system_metrics.get("user_engagement", 0.5)

        utility = (confidence * 0.4) - (load * 0.3) + (engagement * 0.3)

        logger.info(f"Granularity Utility Score: {utility:.2f}")

        if utility > 0.85:
            target_mode = "expert"
        elif utility > 0.50:
            target_mode = "detailed"
        else:
            target_mode = "summary"

        if target_mode != self.current_mode:
            logger.info(f"Adapting granularity: {self.current_mode} -> {target_mode}")
            self.current_mode = target_mode

            # Feed back into Transition Protocol (Article 135/77)
            # If in 'summary' mode (low utility), slow down transition rebalancing
            if target_mode == "summary":
                logger.warning("Low utility detected. Throttling transition rebalancing.")
                # Logic to influence transition speed would go here

        return self.current_mode

    def process_signal(self, signal_type: str, value: Any):
        """Processes interaction signals and updates state."""
        self.telemetry_history.append({"type": signal_type, "val": value, "time": time.time()})

        # Map signals to system_metrics for evaluation
        metrics = {
            "cognitive_confidence": 0.9, # Mocked for now
            "system_load": 0.1,
            "user_engagement": 0.5
        }

        if signal_type == "pause_duration":
            metrics["user_engagement"] = 1.0 / (1.0 + value) # Inverse engagement
        elif signal_type == "edit_frequency":
            metrics["user_engagement"] = min(1.0, value / 10.0)

        self.evaluate_granularity(metrics)

    def get_output_filter(self) -> Dict[str, bool]:
        """Returns filter settings based on current mode."""
        filters = {
            "show_raw_logs": self.current_mode == "expert",
            "show_reasoning_trace": self.current_mode in ["detailed", "expert"],
            "summarize_results": self.current_mode == "summary",
            "active_mode": self.current_mode
        }
        return filters

if __name__ == "__main__":
    ctrl = GranularityController()
    print(f"Initial: {ctrl.current_mode}")
    ctrl.process_signal("pause_duration", 25.0)
    print(f"Post-Long-Pause: {ctrl.current_mode}")
    ctrl.process_signal("edit_frequency", 12.0)
    print(f"Post-Frequent-Edits: {ctrl.current_mode}")
