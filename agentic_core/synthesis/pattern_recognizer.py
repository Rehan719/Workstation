import logging
from typing import List, Dict, Any
from collections import Counter

logger = logging.getLogger(__name__)

class PatternRecognizer:
    """
    DD: Conserved Pattern Discovery.
    Analyzes historical data and operational logs to find successful patterns.
    """
    def __init__(self):
        self.history = []

    def ingest_data(self, data: Dict[str, Any]):
        self.history.append(data)

    def discover_patterns(self) -> List[Dict[str, Any]]:
        """
        Identifies recurring themes in history.
        """
        logger.info("PATTERN: Starting pattern discovery across history.")

        if not self.history:
            return []

        # Simple frequency analysis of keys/values
        all_actions = [item.get('action') for item in self.history if 'action' in item]
        counts = Counter(all_actions)

        patterns = []
        for action, count in counts.items():
            if count > 2: # Threshold for a 'pattern'
                patterns.append({
                    "pattern": action,
                    "frequency": count,
                    "confidence": min(0.99, count * 0.1)
                })

        logger.info(f"PATTERN: Discovered {len(patterns)} conserved patterns.")
        return patterns
