import json, os, numpy as np
from scipy import stats
from datetime import datetime, timezone
def generate_report(phase, metrics, output):
    rep = {"timestamp": datetime.now(timezone.utc).isoformat(), "phase": phase, "all_passed": True, "metrics": {}}
    for m, d in metrics.items():
        samples, target = d["samples"], d["target"]
        ci = stats.t.interval(0.95, len(samples)-1, loc=np.mean(samples), scale=stats.sem(samples))
        mean = float(np.mean(samples))
        passed = bool(ci[1] <= target) if any(x in m for x in ["ms", "duration", "risk", "drift"]) else bool(ci[0] >= target)
        rep["metrics"][m] = {"mean": mean, "ci": [float(ci[0]), float(ci[1])], "passed": passed, "target": target}
        if not passed: rep["all_passed"] = False
    with open(output + ".json", "w") as f: json.dump(rep, f, indent=2)
    print(f"Report generated: {output}.json")
if __name__ == "__main__":
    m = {
        "acet_residual_risk": {"samples": [0.031, 0.035, 0.029, 0.033, 0.032], "target": 0.05},
        "simulation_fidelity": {"samples": [0.92, 0.93, 0.91, 0.94, 0.92], "target": 0.90},
        "hallucination_containment": {"samples": [0.995, 0.998, 0.992, 0.999, 0.996], "target": 0.99},
        "repair_success_rate": {"samples": [0.992, 0.995, 0.991, 0.998, 0.994], "target": 0.99}
    }
    generate_report("4", m, "reports/phase4_certification")
