import json
import os
import hashlib
import time
from typing import Dict, Any

class UEGLogger:
    def __init__(self, log_dir: str = "outputs/ueg"):
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        self.log_file = os.path.join(self.log_dir, f"ueg_log_{int(time.time())}.jsonl")

    def log_event(self, domain: str, event_type: str, details: Dict[str, Any]):
        """
        Logs an event to the Unified Event Graph with SHA-3-512 hashing.
        """
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        event_id = hashlib.sha3_256(f"{timestamp}{domain}{event_type}".encode()).hexdigest()[:16]

        log_entry = {
            "event_id": event_id,
            "timestamp": timestamp,
            "domain": domain,
            "event_type": event_type,
            "details": details
        }

        # Calculate SHA-3-512 of the entry for integrity
        entry_str = json.dumps(log_entry, sort_keys=True)
        integrity_hash = hashlib.sha3_512(entry_str.encode()).hexdigest()
        log_entry["integrity_hash"] = integrity_hash

        with open(self.log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

        # Also log to sovereign metrics for sovereignctl
        self._log_to_sovereign_metrics(domain, event_type, details)

    def _log_to_sovereign_metrics(self, domain: str, event_type: str, details: Dict[str, Any]):
        sovereign_log = "outputs/sovereign_metrics.jsonl"
        metric_entry = {
            "layer": f"GrandOps-v6-{domain}",
            "metric": event_type,
            "value": 1,
            "status": "PASS" if not details.get("violations") else "FAIL",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        with open(sovereign_log, "a") as f:
            f.write(json.dumps(metric_entry) + "\n")
