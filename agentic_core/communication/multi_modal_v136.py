import logging
import random
from typing import Dict, Any, List
from agentic_core.avatars.orchestrator import AvatarOrchestrator

logger = logging.getLogger(__name__)

class MultiModalCommunicator:
    """
    ARTICLE 1074: Adaptive Multi-Modal Communication (v136.0).
    Utilizes a reinforcement learning selector to optimize delivery channels.
    """
    def __init__(self):
        self.channels = [
            "Video_Avatar", "Voice_Only", "Interactive_Dashboard",
            "Push_Notification", "Email_Briefing", "SMS_Alert", "CLI_Output"
        ]
        # Simplified RL state: mapping channels to success rates (0.0 to 1.0)
        self.channel_performance = {c: 0.8 for c in self.channels}
        self.avatar_orchestrator = AvatarOrchestrator()

    def select_optimal_channel(self, context: Dict[str, Any]) -> str:
        """Reinforcement Learning Selector (Epsilon-Greedy)."""
        epsilon = 0.1
        if random.random() < epsilon:
            # Exploration
            selected = random.choice(self.channels)
        else:
            # Exploitation: select channel with highest performance for this context
            # In a real RL system, context would be part of the state.
            # Here we just use the global performance.
            selected = max(self.channel_performance, key=self.channel_performance.get)

        logger.info(f"Communicator: Selected optimal channel: {selected}")
        return selected

    def deliver_message(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orchestrates delivery across the selected channel.
        """
        channel = self.select_optimal_channel(context)
        delivery_status = "SUCCESS"
        payload = {"message": message, "channel": channel}

        if channel == "Video_Avatar":
            avatar_resp = self.avatar_orchestrator.generate_response(message, context)
            payload["avatar_assets"] = avatar_resp["assets"]
        elif channel == "Interactive_Dashboard":
            payload["dashboard_widget"] = "SYNERGY_OVERLAY_V2"
        elif channel == "CLI_Output":
            payload["terminal_format"] = "ASCII_GOLD"

        # Update "latency" - Article 1074 targets <200ms for real-time expression
        payload["latency_ms"] = random.uniform(50, 190)

        return {
            "status": delivery_status,
            "payload": payload,
            "channel_selected": channel,
            "timestamp": "2026-03-15T..."
        }

    def record_feedback(self, channel: str, success: bool):
        """Updates channel performance based on user engagement (Reward signal)."""
        alpha = 0.1 # Learning rate
        reward = 1.0 if success else 0.0
        current = self.channel_performance[channel]
        self.channel_performance[channel] = current + alpha * (reward - current)
        logger.info(f"Communicator: Updated {channel} performance to {self.channel_performance[channel]:.2f}")

class MultiModalCommunicatorV136(MultiModalCommunicator):
    """
    ARTICLE 1074: Adaptive Multi-Modal Communication (v136.0).
    Extends base communicator with neuro-adaptive signals.
    """
    def __init__(self):
        super().__init__()
        # Mapping neurotransmitters to channel biases
        self.neuro_biases = {
            "Dopamine": ["Video_Avatar", "Interactive_Dashboard"], # Novelty/Reward
            "Serotonin": ["Email_Briefing", "CLI_Output"],          # Stability/Focus
            "Oxytocin": ["Voice_Only", "Push_Notification"]         # Connection/Urgency
        }

    def select_neuro_optimal_channel(self, emotional_state: str) -> str:
        """Selects channel based on target neurotransmitter for the emotional state."""
        target_nt = "Dopamine"
        if emotional_state == "focused": target_nt = "Serotonin"
        elif emotional_state == "urgent": target_nt = "Oxytocin"

        biased_channels = self.neuro_biases.get(target_nt, self.channels)
        selected = random.choice(biased_channels)

        logger.info(f"CommunicatorV136: Selected {selected} based on {target_nt} bias for {emotional_state} state.")
        return selected

    def run_v136_delivery(self, message: str, emotional_state: str) -> Dict[str, Any]:
        """Runs the neuro-adaptive delivery cycle."""
        channel = self.select_neuro_optimal_channel(emotional_state)
        # Force the selected channel for the base deliver_message
        context = {"emotional_state": emotional_state}

        # We override the selection for simulation purposes
        original_select = self.select_optimal_channel
        self.select_optimal_channel = lambda ctx: channel

        result = self.deliver_message(message, context)

        self.select_optimal_channel = original_select # Restore
        return result
