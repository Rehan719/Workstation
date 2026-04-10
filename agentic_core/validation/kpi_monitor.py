import time
import json
import logging
import os
from typing import Dict, Any

class KPIMonitor:
    """
    Monitors runtime metrics against target KPIs and flags regressions.
    """
    def __init__(self, log_path: str = "outputs/sovereign_metrics.jsonl"):
        self.log_path = log_path
        self.targets = {
            "latency_ms": 10.0,
            "energy_efficiency_ratio": 10.0,
            "module_query_ms": 50.0,
            "gaas_compliance_rate": 1.0,
            "grn_precision": 0.80
        }

        # Ensure directory exists
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

    def log_metric(self, layer: str, metric_name: str, value: float):
        """
        Logs a metric and checks against target.
        """
        target = self.targets.get(metric_name)
        status = "PASS"

        if target is not None:
            # For latency and query time, lower is better
            if "ms" in metric_name or "time" in metric_name:
                if value > target: status = "FAIL"
            # For efficiency and precision, higher is better
            else:
                if value < target: status = "FAIL"

        entry = {
            "timestamp": time.time(),
            "layer": layer,
            "metric": metric_name,
            "value": value,
            "target": target,
            "status": status
        }

        with open(self.log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")

        if status == "FAIL":
            logging.warning(f"KPI REGRESSION: {metric_name} in {layer} | Value: {value} | Target: {target}")

        return status

if __name__ == "__main__":
    monitor = KPIMonitor()
    monitor.log_metric("Hardware", "latency_ms", 4.5)
    monitor.log_metric("Hardware", "latency_ms", 12.0)
    monitor.log_metric("Regulation", "grn_precision", 0.85)
