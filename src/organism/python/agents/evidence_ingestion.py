import hashlib
import logging
import os
import json
from pathlib import Path
from typing import List, Dict, Any
from src.organism.python.ai_gateway import gateway
from src.organism.python.evidence.graph_schema import EvidenceGraph, LegalEvent
from src.organism.python.ai_gateway.middleware.cache import SemanticCache

logger = logging.getLogger(__name__)

class EvidenceIngestionAgent:
    """
    Autonomously processes new evidence files.
    Leverages DeepSeek for long-context parsing and semantic caching.
    """
    def __init__(self, inbox_path: str, graph: EvidenceGraph, cache: SemanticCache):
        self.inbox = Path(inbox_path)
        self.graph = graph
        self.cache = cache
        os.makedirs(self.inbox, exist_ok=True)

    async def scan_and_ingest(self):
        """Scans the inbox for new documents."""
        files = list(self.inbox.glob("*.txt")) # Supporting .txt for initial demo
        logger.info(f"EvidenceAgent: Found {len(files)} files to process.")

        for file in files:
            await self._process_file(file)

    async def _process_file(self, file_path: Path):
        content = file_path.read_text()
        file_hash = hashlib.sha256(content.encode()).hexdigest()
        cache_key = f"evidence_parse:{file_hash}"

        # 1. Check Semantic Cache
        cached = await self.cache.get(cache_key, "deepseek")
        if cached:
            logger.info(f"EvidenceAgent: Cache hit for {file_path.name}")
            events_data = json.loads(cached)
        else:
            # 2. Extract with DeepSeek
            prompt = [
                {"role": "system", "content": "Extract legal events as JSON. Include 'date', 'description', 'parties', 'tags'."},
                {"role": "user", "content": f"Document: {content}"}
            ]

            response = await gateway.execute_completion("deepseek", prompt)
            events_data = self._clean_json(response["content"])

            # Cache the result
            await self.cache.set(cache_key, json.dumps(events_data), "deepseek")

        # 3. Update Evidence Graph
        for idx, item in enumerate(events_data):
            event = LegalEvent(
                id=f"{file_hash[:8]}_{idx}",
                date=item.get("date", "2026-01-01"),
                description=item.get("description", "No description"),
                source_document=file_path.name,
                related_parties=item.get("parties", []),
                legal_tags=item.get("tags", []),
                confidence=0.9
            )
            self.graph.add_event(event)

        logger.info(f"EvidenceAgent: Ingested {len(events_data)} events from {file_path.name}")

    def _clean_json(self, raw: str) -> List[Dict[str, Any]]:
        """Extracts JSON list from LLM response."""
        try:
            # Simple extraction
            start = raw.find("[")
            end = raw.rfind("]") + 1
            return json.loads(raw[start:end])
        except Exception:
            return []
