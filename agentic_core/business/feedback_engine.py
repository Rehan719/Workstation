import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class FeedbackEngine:
    """
    ARTICLE 202: Market Feedback Integration.
    Collects NPS/CSAT and usage analytics to optimize service delivery.
    """
    def __init__(self):
        self.surveys = []
        self.usage_stats = {}

    def record_feedback(self, client_id: str, survey_data: Dict[str, Any]):
        self.surveys.append({"client_id": client_id, "data": survey_data})
        logger.info(f"FEEDBACK: Recorded survey from {client_id}. NPS: {survey_data.get('nps')}")

    def track_usage(self, client_id: str, service: str):
        self.usage_stats[client_id] = self.usage_stats.get(client_id, [])
        self.usage_stats[client_id].append(service)
        logger.debug(f"ANALYTICS: Client {client_id} used {service}.")

    def get_market_sentiment(self) -> float:
        if not self.surveys: return 0.0
        nps_scores = [s["data"].get("nps", 0) for s in self.surveys]
        return sum(nps_scores) / len(nps_scores)
