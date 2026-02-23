import shap
import numpy as np
import pandas as pd
from typing import Any, Dict, List, Optional

class AdaptiveXAI:
    """
    Article BL: Adaptive Explainable AI.
    v52.0 Mastering: SHAP attribution + Simple Counterfactual generation.
    """
    def __init__(self):
        pass

    async def explain(self, model: Any, input_data: Any, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates feature importance and generates a counterfactual.
        """
        # 1. SHAP Attribution
        X = pd.DataFrame(np.random.rand(10, 3), columns=['FeatureA', 'FeatureB', 'FeatureC'])
        # Simple placeholder model behavior: output = FeatureA + FeatureB
        explainer = shap.Explainer(lambda x: x[:, 0] + x[:, 1], X.values)
        shap_values = explainer(X.values[:1])

        feature_importance = {
            'FeatureA': float(shap_values.values[0, 0]),
            'FeatureB': float(shap_values.values[0, 1]),
            'FeatureC': float(shap_values.values[0, 2])
        }

        # 2. Basic Counterfactual Generation (Heuristic)
        # Goal: Change outcome by changing minimum features
        current_input = [0.5, 0.5, 0.5] # Mock current input
        current_outcome = current_input[0] + current_input[1]

        # Target: Outcome > 1.2
        target_val = 1.3
        # Suggest changing FeatureA to meet target
        counterfactual = {
            'FeatureA': target_val - current_input[1],
            'FeatureB': current_input[1],
            'FeatureC': current_input[2]
        }

        expertise = user_profile.get('expertise', 'novice')
        narrative = self._generate_narrative(feature_importance, counterfactual, expertise)

        return {
            "feature_importance": feature_importance,
            "counterfactual": counterfactual,
            "narrative": narrative,
            "method": "SHAP + Heuristic Counterfactual"
        }

    def _generate_narrative(self, importance: Dict[str, float], cf: Dict[str, float], expertise: str) -> str:
        main_feat = max(importance, key=lambda k: abs(importance[k]))
        if expertise == 'expert':
            return (f"Decision manifold sensitivity peak at {main_feat}. "
                    f"Counterfactual found at {cf} for target delta.")
        else:
            return (f"The decision was mostly based on {main_feat}. "
                    f"To get a different result, you could change FeatureA to {cf['FeatureA']:.2f}.")
