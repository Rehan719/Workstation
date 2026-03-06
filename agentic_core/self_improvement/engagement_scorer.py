from typing import Dict, Any

class UserEngagementScorer:
    """CQ-III: User Engagement Scoring."""

    def score(self, signals: Dict[str, Any]) -> float:
        # Scale: -1 to +1
        # Target: dwell time > 8.2s (+1), correction rate > 17% (-1)
        dwell_time = signals.get("dwell_time", 5.0)
        correction_rate = signals.get("correction_rate", 0.1)

        score = 0.0
        if dwell_time > 8.2:
            score += 0.5
        if correction_rate > 0.17:
            score -= 0.5

        return max(-1.0, min(1.0, score))
