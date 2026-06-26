import json
import random
from datetime import datetime
import os

class XAIEngine:
    def __init__(self, xai_path="outputs/Religion/QuranEducation/observatory/xai_reports.jsonl"):
        self.xai_path = xai_path
        os.makedirs(os.path.dirname(self.xai_path), exist_ok=True)

    def generate_explanation(self, model_id, decision_id, input_features, output_decision, method="shap"):
        explanation = {
            "timestamp": str(datetime.now()),
            "model_id": model_id,
            "decision_id": decision_id,
            "method": method,
            "input_features": input_features,
            "output_decision": output_decision,
            "explanations": self._mock_explanation(method, input_features),
            "counterfactuals": self._generate_counterfactuals(input_features, output_decision)
        }
        with open(self.xai_path, 'a') as f:
            f.write(json.dumps(explanation) + "\n")
        return explanation

    def _mock_explanation(self, method, features):
        if method == "shap":
            # Generate random SHAP values for features
            return {f: random.uniform(-1, 1) for f in features}
        elif method == "lime":
            # Generate simplified local explanation
            top_feature = random.choice(list(features.keys())) if features else "none"
            return f"Decision was primarily influenced by feature: {top_feature}"
        return "Explanation not available for selected method."

    def _generate_counterfactuals(self, features, decision):
        # Generate what-if scenarios
        if not features:
            return []

        feature_to_change = random.choice(list(features.keys()))
        modified_features = features.copy()
        modified_features[feature_to_change] = "modified_value"

        return [
            {
                "change": f"If {feature_to_change} was different...",
                "potential_outcome": f"Decision for {decision} might have changed."
            }
        ]

    def generate_consistency_report(self, module_id, consistency_score):
        report = {
            "timestamp": str(datetime.now()),
            "module_id": module_id,
            "consistency_score": consistency_score,
            "theological_validation": "pass" if consistency_score > 0.9 else "fail",
            "justification": f"Consistency check complete for {module_id} with score {consistency_score}."
        }
        report_path = f"outputs/Religion/QuranEducation/observatory/consistency_{module_id}.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        return report
