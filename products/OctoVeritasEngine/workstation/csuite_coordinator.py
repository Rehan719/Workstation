import json
import os
from typing import Dict, Any, List

class AgentPreference:
    def __init__(self, role: str, default_weights: Dict[str, float]):
        self.role = role
        self.weights = default_weights
        self._load_config()

    def _load_config(self):
        config_path = f"configs/csuite/preferences_{self.role}.json"
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.weights.update(json.load(f))

class CSuiteCoordinator:
    def __init__(self):
        self.agents = {
            "CFO": AgentPreference("CFO", {"cost_weight": 0.8, "speed_weight": 0.2}),
            "CMO": AgentPreference("CMO", {"engagement_weight": 0.9, "quality_weight": 0.5}),
            "CTO": AgentPreference("CTO", {"reliability_weight": 0.7, "security_weight": 0.9}),
            "CHO": AgentPreference("CHO", {"ethics_weight": 0.95, "compliance_weight": 1.0}),
            "COO": AgentPreference("COO", {"resilience_weight": 0.8, "efficiency_weight": 0.6})
        }

    def get_aggregated_preferences(self) -> Dict[str, float]:
        aggregated = {}
        for role, agent in self.agents.items():
            for key, val in agent.weights.items():
                aggregated[key] = max(aggregated.get(key, 0.0), val)
        return aggregated

class COEGatekeeper:
    def __init__(self):
        self.coes = ["Data Science", "UX", "Security", "AI Ethics", "DevOps"]

    def approve_plan(self, plan: Any) -> Dict[str, Any]:
        results = {}
        for coe in self.coes:
            # Simulate high-fidelity mock logic
            approved = True
            feedback = "Approved by CoE gatekeeper."

            if coe == "UX" and not getattr(plan, 'accessibility', True):
                approved = False
                feedback = "UX CoE rejection: Accessibility standards not met."
            elif coe == "Security" and not getattr(plan, 'hashed', True):
                approved = False
                feedback = "Security CoE rejection: Asset integrity hash missing."

            results[coe] = {"approved": approved, "feedback": feedback}

        return results
