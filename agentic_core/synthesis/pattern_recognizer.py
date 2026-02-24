from typing import List, Dict, Any

class PatternRecognizer:
    """Extracts optimal patterns from historical insights."""

    def extract_patterns(self, insights: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        patterns = []
        for insight in insights:
            if "key_terms" in insight:
                patterns.append({
                    "concept": insight["key_terms"],
                    "relevance": 1.0 if insight["type"] == "doc" else 0.8
                })
        return patterns
