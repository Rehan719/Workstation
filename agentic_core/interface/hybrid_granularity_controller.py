from typing import Any, Dict, List, Optional
from datetime import datetime
from collections import defaultdict
from .implicit_signal_detector import ImplicitSignalDetector
from .explicit_mode_selector import ExplicitModeSelector
from .decision_engine import DecisionEngine
from .granularity_learning import GranularityLearningModule

class HybridGranularityController:
    """
    Combines implicit signals and explicit feedback to adapt information density (Article S).
    """
    def __init__(self):
        self.implicit_signal_detector = ImplicitSignalDetector()
        self.explicit_mode_selector = ExplicitModeSelector()
        self.decision_engine = DecisionEngine()
        self.learning_module = GranularityLearningModule()
        self.adaptation_log = []

    async def process_interaction(self, user_id: str, interaction: Dict[str, Any]) -> str:
        """Process user interaction and adapt granularity."""
        implicit_state = await self.implicit_signal_detector.analyze(user_id, interaction)
        explicit_mode = await self.explicit_mode_selector.get_current_mode(user_id)

        action = await self.decision_engine.decide(user_id, implicit_state, explicit_mode)

        if action != 'no_change':
            self.adaptation_log.append({
                'timestamp': datetime.utcnow().isoformat(),
                'user_id': user_id,
                'implicit_state': implicit_state,
                'explicit_mode': explicit_mode,
                'action': action
            })

        return action

    async def handle_explicit_change(self, user_id: str, new_mode: str):
        """Handle user's explicit mode change and learn from context."""
        await self.explicit_mode_selector.set_mode(user_id, new_mode)
        recent_context = await self.implicit_signal_detector.get_recent_context(user_id)
        await self.learning_module.learn_from_explicit(user_id, recent_context, new_mode)
