import logging
import glob
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class TelemetryAnalyser:
    """v101.0: Ingests system logs for self-reflection."""
    def analyse(self, log_dir: str = "meta") -> List[Dict[str, Any]]:
        opportunities = []
        logs = glob.glob(f"{log_dir}/*.log")
        for log in logs:
            with open(log, 'r') as f:
                content = f.read()
                if "waste" in content.lower():
                    opportunities.append({"type": "ARO_REFINEMENT", "detail": "Waste threshold alert."})
        return opportunities
