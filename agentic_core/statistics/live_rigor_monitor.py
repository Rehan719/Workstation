import math

import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, UTC
from scipy import stats
from agentic_core.ueg.logger import VSBUEGLogger as UEGLogger


class LiveRigorMonitor:
    """Statistical validation of an accumulated metric series: 95% t-interval CI + one-sample t-test.

    W437 — three §4.5-class defects lived here, proved live before the rewrite:
      · `power` was `n/100 + 0.5` — a call counter wearing a statistics label. No power analysis
        existed, and the "power gate" it fed froze `significant` at false for the first 29 calls
        regardless of evidence (a real p-value of 1.5e-24 was reported "not significant"). Deleted,
        not renamed: there is no quantity here for the name to describe.
      · The first call on any metric returned `p_value: 1.0` and `ci_95: [v, v]` — numbers that
        were never computed, in the same shape as real ones, with no way to tell. Unmeasured is
        now unmeasured: `p_value: null` / `ci_95: null` with the reason stated.
      · A zero-variance series made scipy return NaN, which crashed JSON serialization with a 500 —
        AFTER the UEG provenance write, sealing a NaN "validation" into the chain for a response no
        caller ever received. The NaN is now caught before both.

    `significant` is tri-state: true/false only when the t-test actually ran, null when it could not.
    """

    def __init__(self, ueg: UEGLogger):
        self.ueg = ueg
        self.ci_level = 0.95
        self.metric_history: Dict[str, List[float]] = {}

    async def validate_metric(self, metric_name: str, current_value: float, baseline: float) -> Dict[str, Any]:
        series = self.metric_history.setdefault(metric_name, [])
        series.append(current_value)
        n = len(series)

        ci = self._compute_ci(series)
        # W437 refuter catch: the first version of this gate tested set-equality, but the math
        # degenerates whenever the standard error is 0.0 — including DISTINCT values whose variance
        # underflows — and a non-finite observation (NaN/inf, now also refused at the request model)
        # sailed through to a p=nan that compared False and was sealed into the UEG chain before the
        # response 500'd. The gate is now the actual degeneracy condition, and a non-finite p is
        # caught after the test as well.
        sem_zero = n >= 2 and float(stats.sem(series)) == 0.0

        p_value: Optional[float] = None
        reason: Optional[str] = None
        if n < 3:
            reason = (f"n={n} — below this monitor's minimum of 3 observations for a t-test "
                      f"(a policy floor, not a mathematical limit); nothing was tested")
            if sem_zero:
                reason += "; the interval is zero-width because the series has zero variance so far"
        elif sem_zero:
            reason = (f"zero variance (or variance underflowed to zero) across {n} observations — "
                      f"the t-statistic is undefined, so no test ran")
        else:
            _, p = stats.ttest_1samp(series, baseline)
            p = float(p)
            if math.isfinite(p):
                p_value = p
            else:
                reason = (f"the t-test degenerated to a non-finite p over {n} observations — "
                          f"no verdict can be supported")

        significant: Optional[bool] = (p_value < 0.05) if p_value is not None else None

        result = {
            "metric": metric_name,
            "value": current_value,
            "baseline": baseline,
            "n": n,
            "ci_95": ci,
            "p_value": p_value,
            "significant": significant,
            "basis": (reason if reason is not None else
                      f"one-sample t-test of {n} observations against baseline {baseline}: "
                      f"p={p_value:.4g} {'<' if significant else '>='} 0.05"),
            "timestamp": datetime.now(UTC).isoformat(),
        }

        await self.ueg.log_event("STATISTICAL_VALIDATION", result)
        return result

    def _compute_ci(self, data: List[float]) -> Optional[Tuple[float, float]]:
        """95% t-interval, or None when one point cannot support an interval (or the math degenerates)."""
        if len(data) < 2:
            return None
        mean = float(np.mean(data))
        sem = float(stats.sem(data))
        if sem == 0.0:
            return (mean, mean)   # zero variance — a genuinely zero-width interval, flagged via basis
        half = sem * float(stats.t.ppf((1 + self.ci_level) / 2, len(data) - 1))
        lo, hi = mean - half, mean + half
        if not (math.isfinite(lo) and math.isfinite(hi)):
            return None   # a non-finite interval is not an interval — never serialise NaN/inf
        return (lo, hi)
