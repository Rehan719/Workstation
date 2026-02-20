from typing import Any, Dict, List, Optional
from datetime import datetime
from collections import defaultdict

class GranularityLearningModule:
    """
    Learns from explicit feedback to improve future predictions (Article S).
    """
    def __init__(self):
        self.training_data = defaultdict(list)

    async def learn_from_explicit(self, user_id: str, context: Dict[str, Any], chosen_mode: str):
        """Record the correlation between context and choice."""
        self.training_data[user_id].append({
            'context': context,
            'chosen_mode': chosen_mode,
            'timestamp': datetime.utcnow().isoformat()
        })
        # In a real implementation, this would trigger model retraining
