import os
import json
import yaml
import re
from datetime import datetime

class AdvancedAnalyticsEngineV10:
    """
    Law Grand Operation v10.0-PLATINUM Advanced Analytics Engine.
    Implements pattern recognition, heuristic sentiment analysis,
    and predictive risk modeling for legal intelligence.
    """

    def __init__(self, config_path):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        self.version = self.config['analytics_engine']['version']
        self.name = self.config['analytics_engine']['name']
        self.risk_matrix = self.config['predictive_risk_matrix']
        self.granularity = self.config['extraction_granularity']
        self.analytics_logs = []

    def analyze_text_patterns(self, text, source_id):
        """
        Analyzes text for specific legal patterns and contradictions.
        """
        insights = []

        # Heuristic Contradiction Detection (Mock Logic for Sandbox)
        if "satisfactory" in text.lower() and "dismissal" in text.lower():
            insights.append({
                "type": "potential_contradiction",
                "severity": "Critical",
                "description": "Text mentions 'satisfactory' performance alongside 'dismissal' context.",
                "relevance": "Supports pretextual dismissal argument (94% punctuality vs. performance claim)."
            })

        # Sentiment Analysis (Heuristic)
        positive_terms = ["excellent", "consistently", "achieved", "met", "satisfactory"]
        negative_terms = ["unacceptable", "failure", "poor", "disciplinary", "concerns"]

        pos_count = sum(1 for word in positive_terms if word in text.lower())
        neg_count = sum(1 for word in negative_terms if word in text.lower())

        sentiment = "Neutral"
        if pos_count > neg_count: sentiment = "Positive/Performance-Aligned"
        elif neg_count > pos_count: sentiment = "Negative/Adverse"

        insights.append({
            "type": "sentiment_analysis",
            "score": f"{pos_count}/{neg_count}",
            "summary": sentiment
        })

        return insights

    def calculate_predictive_risk(self, historical_events):
        """
        Predicts litigation risk based on a sequence of events.
        """
        risk_score = 0
        risk_factors = []

        for event in historical_events:
            event_type = event.get('type')
            if event_type == 'disclosure_delay' and event.get('days', 0) > self.risk_matrix['disclosure_delay']['threshold_days']:
                risk_score += 30
                risk_factors.append(f"Disclosure Delay ({event.get('days')} days) - Level: {self.risk_matrix['disclosure_delay']['risk_level']}")

            if event_type == 'contradiction':
                risk_score += 50
                risk_factors.append(f"Contradiction Detected - Level: {self.risk_matrix['contradiction_detected']['risk_level']}")

        status = "Low"
        if risk_score > 70: status = "Critical"
        elif risk_score > 40: status = "High"

        return {
            "risk_score": risk_score,
            "status": status,
            "factors": risk_factors
        }

    def generate_precedent_velocity(self, case_citations):
        """
        Simulates precedent velocity tracking (frequency and recency).
        """
        velocity_report = {}
        for citation in case_citations:
            # Mock velocity calculation
            velocity_report[citation] = {
                "velocity_index": 0.95, # High usage in recent tribunals
                "trend": "Increasing",
                "authority_weight": "Binding (EAT/Court of Appeal)"
            }
        return velocity_report

    def sentence_level_extract(self, text):
        """
        Splits text into sentences for high-granularity forensic tracing.
        """
        # Simple regex for sentence splitting
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
        return [{"index": i, "content": s.strip()} for i, s in enumerate(sentences) if s.strip()]

    def log_analytical_event(self, facility, action, outcome):
        event = {
            "timestamp": datetime.now().isoformat(),
            "facility": facility,
            "action": action,
            "outcome": outcome,
            "engine_version": self.version
        }
        self.analytics_logs.append(event)
        return event

if __name__ == "__main__":
    # Test instance
    engine = AdvancedAnalyticsEngineV10("configs/Law/EmploymentTribunal/v10/analytics_config.yaml")
    test_text = "Rehan Minhas consistently achieved 94% punctuality, which was satisfactory. However, the dismissal was based on performance concerns."
    print(json.dumps(engine.analyze_text_patterns(test_text, "test_source"), indent=2))
