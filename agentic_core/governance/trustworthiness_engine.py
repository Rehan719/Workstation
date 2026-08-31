import logging
from typing import Dict, Any, List, Optional
import numpy as np

logger = logging.getLogger(__name__)

class TrustworthinessEngine:
    """
    ARTICLE 100: Bias detection, fairness metrics, explainability scoring.
    Unified governance for generated apps and cognitive outputs.
    """
    def __init__(self, fairness_threshold: float = 0.9, bias_sensitivity: float = 0.5):
        self.fairness_threshold = fairness_threshold
        self.bias_sensitivity = bias_sensitivity
        self.trust_scores: Dict[str, float] = {}

    def analyze_fairness(self, output: Any, demographic_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Measure the supplied demographic distribution, or say nothing was measured.

        W409 — this set fairness_score = 1.0, or the literal 0.95 whenever ANY demographic_data
        dict was passed (truthiness was the whole "analysis"), and returned status "COMPLIANT" on
        both paths. `output` was never read. Executed on
        ('Only hire men. Reject all women applicants.', {'gender': {'m': 100, 'f': 0}}) it
        returned {'fairness_score': 0.95, 'is_fair': True, 'status': 'COMPLIANT'} — a fairness
        certificate for a total exclusion, from a body commented "# Placeholder".

        The docstring already named the real method, so the real method now runs: the four-fifths
        (disparate impact) ratio min(group)/max(group) over the supplied counts, worst attribute
        deciding. With no usable demographic_data nothing can be measured and the result says
        NOT_ASSESSED instead of 1.0. The `output` text is still not analysed — this deployment has
        no text-fairness analyser — and the result now says so rather than implying otherwise.
        """
        def _numeric(mapping: Dict[str, Any]) -> Dict[str, float]:
            return {str(g): float(v) for g, v in mapping.items()
                    if isinstance(v, (int, float)) and not isinstance(v, bool)}

        buckets: Dict[str, Dict[str, float]] = {}
        if isinstance(demographic_data, dict):
            nested = {k: v for k, v in demographic_data.items() if isinstance(v, dict)}
            if nested:
                for attribute, counts in nested.items():
                    buckets[str(attribute)] = _numeric(counts)
            else:
                buckets["overall"] = _numeric(demographic_data)

        ratios: Dict[str, float] = {}
        for attribute, counts in buckets.items():
            if len(counts) < 2:
                continue
            highest = max(counts.values())
            if highest <= 0:
                continue
            ratios[attribute] = min(counts.values()) / highest

        if not ratios:
            logger.info("TrustworthinessEngine: fairness NOT assessed — no usable demographic data.")
            return {
                "fairness_score": None,
                "is_fair": None,
                "status": "NOT_ASSESSED",
                "detail": ("No fairness measurement was made. Supply demographic_data as "
                           "{attribute: {group: count}} with at least two numeric groups. The "
                           "`output` itself is not analysed — this deployment has no "
                           "text-fairness analyser."),
            }

        worst_attribute = min(ratios, key=lambda a: ratios[a])
        fairness_score = round(ratios[worst_attribute], 4)
        is_fair = fairness_score >= self.fairness_threshold

        logger.info(f"TrustworthinessEngine: Analyzed fairness. Score: {fairness_score:.2f}, Is Fair: {is_fair}")
        return {
            "fairness_score": fairness_score,
            "is_fair": is_fair,
            "status": "COMPLIANT" if is_fair else "VIOLATION",
            "method": "four-fifths disparate-impact ratio (min group / max group)",
            "ratios": {a: round(r, 4) for a, r in ratios.items()},
            "worst_attribute": worst_attribute,
            "note": ("Measured from the supplied demographic_data only; the `output` argument is "
                     "not analysed."),
        }

    def detect_bias(self, output: Any, sensitivity: float = 0.5) -> Dict[str, Any]:
        """Report that no bias detection ran, instead of handing back a clean bill of health.

        W409 — the body was `# Placeholder` + `bias_score = 0.05`, so every call returned
        {'bias_score': 0.05, 'is_biased': False, 'status': 'NO_BIAS'}, including
        detect_bias('Women are worse engineers than men.'). `output` was never read, and the
        literal sat below the default sensitivity of 0.5, so BIASED was structurally unreachable —
        no input could ever contradict the verdict.

        No bias detector exists in this repo. The §11 screen (api/compliance) is a
        haram/legal/EHS/ethics screen, not a bias measurement, so reporting its verdict as a bias
        score would relabel one claim as another. Absence is reported instead of a number.
        """
        logger.info("TrustworthinessEngine: bias NOT assessed — no bias detector is implemented.")
        return {
            "bias_score": None,
            "is_biased": None,
            "status": "NOT_ASSESSED",
            "sensitivity": sensitivity,
            "detail": ("No bias detection ran, so no bias verdict is given. Nothing in this "
                       "deployment analyses the supplied output for bias."),
        }

    def generate_explainability_report(self, task_id: str, reasoning_chain: List[str]) -> Dict[str, Any]:
        """Record the reasoning chain; do not score a transparency nothing measured.

        W409 — this returned "transparency_score": 0.95 and "interpretability": "HIGH" for every
        task, whatever the reasoning_chain was — an empty chain scored 0.95 exactly as a full one
        did. Both were literals in the dict; nothing inspected the steps. The rest of the report
        (task_id, steps, timestamp) is real and is kept as it was.
        """
        report = {
            "task_id": task_id,
            "steps": reasoning_chain,
            "step_count": len(reasoning_chain or []),
            "transparency_score": None,
            "interpretability": "NOT_SCORED",
            "note": ("No transparency or interpretability score is computed — nothing in this "
                     "deployment scores a reasoning chain. The recorded steps are the whole of "
                     "the report."),
            "timestamp": np.datetime64('now')
        }

        logger.info(f"TrustworthinessEngine: Generated explainability report for task {task_id}.")
        return report

    def update_trust_score(self, component_id: str, new_score: float):
        """
        Updates the trust score for a specific system component.
        """
        self.trust_scores[component_id] = new_score
        logger.info(f"TrustworthinessEngine: Trust score for {component_id} updated to {new_score:.2f}")

    def get_system_trust_index(self) -> Optional[float]:
        """Return the mean of the RECORDED trust scores, or None when none were ever recorded.

        W409 — the empty case returned 1.0: a perfect system-wide trust index computed from zero
        observations, indistinguishable from a genuine 1.0 earned by components that had actually
        been scored. None says "no component has been scored yet". The averaging branch below was
        always real and is unchanged.
        """
        if not self.trust_scores:
            return None
        return sum(self.trust_scores.values()) / len(self.trust_scores)
