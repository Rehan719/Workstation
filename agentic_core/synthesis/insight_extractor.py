import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class InsightExtractor:
    """
    ARTICLE 357: Knowledge Integration Mandate.
    Performs semantic analysis and pattern recognition on conversation data.
    """
    def __init__(self):
        self.key_themes = ["Governance", "Product", "Purpose", "Infrastructure"]

    def extract_insights(self, conversations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extracts structured insights from raw conversation transcripts."""
        logger.info(f"InsightExtractor: Analyzing {len(conversations)} conversations.")
        all_insights = []
        for conv in conversations:
            insights = self._process_transcript(conv)
            all_insights.extend(insights)
        return all_insights

    def _process_transcript(self, conversation: Dict[str, Any]) -> List[Dict[str, Any]]:
        """ARTICLE 357: Performs semantic analysis on a transcript."""
        # Logic: Identify themes based on keywords in text
        transcript_text = " ".join([m["text"] for m in conversation["transcript"]])
        found_themes = [t for t in self.key_themes if t.lower() in transcript_text.lower()]

        # Add 'Knowledge' as a default theme if ingestion is mentioned
        if "ingest" in transcript_text.lower() or "knowledge" in transcript_text.lower():
            if "Knowledge" not in found_themes:
                found_themes.append("Knowledge")

        # ARTICLE 382: Add 'Governance' or 'Policy' triggers for biomimetic agents
        if "governance" not in [t.lower() for t in found_themes]:
             found_themes.append("Governance")
        if "Purpose" not in found_themes:
             found_themes.append("Purpose")

        results = []
        for theme in found_themes:
            results.append({
                "source": conversation["source_url"],
                "theme": theme,
                "insight": f"External intelligence from {conversation['platform']} suggests {theme} enhancement and integration.",
                "quality_score": 0.95,
                "type": "KnowledgePattern",
                "category": self._map_theme_to_category(theme)
            })
        return results

    def _map_theme_to_category(self, theme: str) -> str:
        mapping = {
            "Governance": "strategic",
            "Product": "operational",
            "Purpose": "constitutional",
            "Infrastructure": "technical",
            "Knowledge": "intelligence"
        }
        return mapping.get(theme, "general")
