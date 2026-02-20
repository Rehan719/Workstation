from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict

class ImplicitSignalDetector:
    """
    Detects real-time user interaction signals like pause duration, edit frequency, typing patterns (Article S).
    """
    def __init__(self):
        self.signal_buffer = defaultdict(list)
        self.signal_thresholds = {
            'pause_duration': 5.0,  # seconds
            'edit_frequency': 0.5,   # edits per second
            'typing_speed': 3.0,     # chars per second
        }

    async def analyze(self, user_id: str, interaction: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze interaction and return detected signals."""
        signals = {}
        now = interaction.get('timestamp', datetime.utcnow())

        # Simple analysis logic
        if self.signal_buffer[user_id]:
            last_interaction = self.signal_buffer[user_id][-1]
            pause = (now - last_interaction['timestamp']).total_seconds()
            signals['pause_duration'] = pause
            signals['pause_detected'] = pause > self.signal_thresholds['pause_duration']

        self.signal_buffer[user_id].append({
            'timestamp': now,
            'type': interaction.get('type'),
            'signals': signals
        })

        # Buffer management
        if len(self.signal_buffer[user_id]) > 100:
            self.signal_buffer[user_id] = self.signal_buffer[user_id][-100:]

        return signals

    async def get_recent_context(self, user_id: str, seconds: int = 30) -> Dict[str, Any]:
        """Aggregate recent context."""
        cutoff = datetime.utcnow() - timedelta(seconds=seconds)
        recent = [e for e in self.signal_buffer[user_id] if e['timestamp'] > cutoff]

        if not recent: return {}

        return {
            'avg_pause': sum(e['signals'].get('pause_duration', 0) for e in recent) / len(recent),
            'interaction_count': len(recent)
        }
