import logging
import time
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

#  W543 — THE PROCESS'S OWN START, so the uptime this module reports is a measurement of something.
#  What stood here was `random.randint(3600, 86400)`: a plausible uptime between an hour and a day,
#  redrawn on every call, served to the AI CEO as a registered tool and therefore reportable to a user
#  as a fact. The honest figure is narrower than the fabricated one — this is how long THIS PROCESS has
#  been running, not how long the fabric has been up — and saying so is the point.
_PROCESS_STARTED = time.monotonic()

class DynamicReactiveAdaptiveFabric:
    """
    QEP - DRAD: Dynamic Reactive Adaptive Fabric.
    Continuously monitors user interactions and system performance,
    adjusting the behaviour of the QEP engines in real time.
    """
    def __init__(self):
        #  W543 — None, not a flattering default. These four started as 0.0 latency, 0.0 error rate, 1.0
        #  USER SATISFACTION and 0.0 utilisation, and nothing wrote any of them until a caller supplied
        #  telemetry — which no live caller does. So a fabric nobody had measured reported no errors and
        #  total user satisfaction, and the defaults were indistinguishable from a genuinely perfect
        #  reading. A platform's claim about its users' satisfaction is the one figure it must never
        #  invent: the only real signal of that kind this repository has is a support confirmation, which
        #  a user writes themselves (agentic_core/support/tickets.py, W541-W542).
        self.performance_metrics: Dict[str, Any] = {
            "latency": None,
            "error_rate": None,
            "user_satisfaction": None,
            "qep_utilization": None
        }
        #  whether anything has ever reported telemetry to this instance — the difference between
        #  "measured and fine" and "never measured", which the defaults above used to erase
        self._telemetry_received = False
        self.adaptations = []

    def monitor(self, system_telemetry: Dict[str, Any]) -> Dict[str, Any]:
        """Monitors and updates internal performance state.

        W543 — the two thresholds below used `.get(key, 0)`, so an UNREPORTED metric was compared as a
        zero and therefore never breached. That is the same defect in the opposite direction from the
        status line: an absent figure that cannot trigger an adaptation, inside a fabric whose whole claim
        is that it adapts. Both are now compared only when a number actually arrived.
        """
        if system_telemetry:
            self.performance_metrics.update(system_telemetry)
            self._telemetry_received = True

        _lat = self.performance_metrics.get("latency")
        if isinstance(_lat, (int, float)) and _lat > 200:   # ms
            self.adaptations.append({
                "timestamp": datetime.utcnow().isoformat(),
                "action": "TRIGGER_ARO_OPTIMIZATION",
                "reason": "High Latency Detected"
            })

        _err = self.performance_metrics.get("error_rate")
        if isinstance(_err, (int, float)) and _err > 0.05:  # 5%
            self.adaptations.append({
                "timestamp": datetime.utcnow().isoformat(),
                "action": "TRIGGER_LSTM_SELF_HEALING",
                "reason": "High Error Rate Detected"
            })

        #  THREE STATES WHERE THERE WERE TWO. `NOMINAL if error_rate < 0.05 else CRITICAL` over a default
        #  of 0.0 meant an unmeasured fabric was always NOMINAL — the reassuring answer was the one that
        #  required no evidence.
        if not isinstance(_err, (int, float)):
            _status, _basis = "NOT_ASSESSED", (
                "no error rate has been reported to this fabric, so it is neither nominal nor critical. "
                "A fabric nobody has measured is not a healthy one")
        elif _err < 0.05:
            _status, _basis = "NOMINAL", f"error rate {_err} is below the 0.05 threshold"
        else:
            _status, _basis = "CRITICAL", f"error rate {_err} is at or above the 0.05 threshold"

        return {
            "engine": "DRAD",
            "timestamp": datetime.utcnow().isoformat(),
            "status": _status,
            "status_basis": _basis,
            "metrics": self.performance_metrics,
            "active_adaptations": self.adaptations[-5:] # Last 5 adaptations
        }

    def get_fabric_health(self) -> Dict[str, Any]:
        """Health metrics for the adaptive fabric — measured, or stated as unmeasured.

        W543 — THIS IS SERVED TO THE AI CEO AS A REGISTERED TOOL (agentic_core/api/v138/ceo.py's
        ToolRegistry entry `check_qep_fabric_health`), so whatever it returns can be reported to a user as
        a fact in conversation. What it returned was `random.uniform(0.9, 1.0)` as the health score and
        `random.randint(3600, 86400)` as the uptime: two numbers drawn from a generator, redrawn on every
        call, in a plausible range. A fabricated figure that is PLAUSIBLE and VARIES is harder to catch
        than a constant, because it survives the two checks a reader actually makes — it is not a round
        number and it is not the same twice.
        """
        _score = self.performance_metrics.get("error_rate")
        return {
            "fabric_version": "v0.8.0-QEP",
            #  a real measurement, and named for what it actually measures
            "process_uptime_seconds": round(time.monotonic() - _PROCESS_STARTED, 1),
            "adaptation_count": len(self.adaptations),
            "telemetry_received": self._telemetry_received,
            #  three-state: a score only where something was reported to compute it from
            "current_health_score": (round(1.0 - float(_score), 4)
                                     if isinstance(_score, (int, float)) else None),
            "health_basis": (
                f"computed as 1 - error_rate from the last reported error rate ({_score})"
                if isinstance(_score, (int, float)) else
                "NOT ASSESSED: no telemetry has been reported to this fabric, so there is no error rate "
                "to compute a health score from. This is not a low score and it is certainly not a high "
                "one — nothing has measured it"),
            "uptime_basis": ("the elapsed monotonic time of THIS PROCESS, not of the fabric or of any "
                             "deployment: a restart resets it"),
        }

drad_instance = DynamicReactiveAdaptiveFabric()

def get_drad_instance() -> DynamicReactiveAdaptiveFabric:
    return drad_instance
