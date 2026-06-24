import numpy as np
from scipy import stats
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass

@dataclass
class StatisticalReport:
    mean: float
    confidence_interval: Tuple[float, float]
    p_value: Optional[float] = None
    power: Optional[float] = None
    passed: bool = True

class StatisticalValidator:
    """
    Enforces 95% Confidence Intervals and Power Analysis for all system metrics.
    Ensures Digital Biomimicry of Minimisation is statistically sound.
    """
    def __init__(self, confidence_level: float = 0.95):
        self.confidence_level = confidence_level

    def validate_metric(self, data: List[float], baseline: Optional[float] = None) -> StatisticalReport:
        if len(data) < 2:
            return StatisticalReport(np.mean(data) if data else 0, (0, 0), passed=False)

        mean = np.mean(data)
        sem = stats.sem(data)
        ci = stats.t.interval(self.confidence_level, len(data)-1, loc=mean, scale=sem)

        p_value = None
        passed = True
        if baseline is not None:
            t_stat, p_value = stats.ttest_1samp(data, baseline)
            passed = p_value < (1 - self.confidence_level)

        return StatisticalReport(mean, ci, p_value, passed=passed)

    def power_analysis(self, effect_size: float, alpha: float = 0.05, power: float = 0.8) -> int:
        """Calculate required sample size for given effect size."""
        # Simplified power analysis for bootstrap
        from statsmodels.stats.power import TTestIndPower
        analysis = TTestIndPower()
        sample_size = analysis.solve_power(effect_size=effect_size, alpha=alpha, power=power)
        return int(np.ceil(sample_size))
