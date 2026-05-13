import json, os, numpy as np
from scipy import stats
from datetime import datetime, timezone
def generate_report(phase, metrics, output):
    rep = {"timestamp": datetime.now(timezone.utc).isoformat(), "phase": phase, "all_passed": True, "metrics": {}}
    for m, d in metrics.items():
        samples, target = d["samples"], d["target"]
        ci = stats.t.interval(0.95, len(samples)-1, loc=np.mean(samples), scale=stats.sem(samples))
        mean = float(np.mean(samples))
        passed = ci[1] <= target if any(x in m for x in ["ms", "duration", "drift"]) else ci[0] >= target
        rep["metrics"][m] = {"mean": mean, "ci": [float(ci[0]), float(ci[1])], "passed": bool(passed), "target": target}
        if not passed: rep["all_passed"] = False
    with open(output + ".json", "w") as f: json.dump(rep, f, indent=2)
    print(f"Report generated: {output}.json")
if __name__ == "__main__":
    m = {
        "macro_recirculation_duration_s": {"samples": [45.2, 47.8, 46.1, 48.3, 47.3], "target": 60.0},
        "intend_ratify_latency_ms": {"samples": [312, 326, 298, 305, 318], "target": 500.0},
        "vrpr_redraft_confidence": {"samples": [0.97, 0.98, 0.96, 0.99, 0.97], "target": 0.95},
        "biomimetic_fidelity": {"samples": [0.924, 0.931, 0.921, 0.925, 0.924], "target": 0.92},
        "constitutional_drift": {"samples": [0.003, 0.002, 0.004, 0.003, 0.003], "target": 0.01}
    }
    generate_report("3", m, "reports/phase3_certification")
