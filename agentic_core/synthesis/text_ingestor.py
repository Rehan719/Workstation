import os
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class TextIngestor:
    """ARTICLE 356: Expanded Knowledge Ingestion (Text & History)."""

    def ingest_background(self, paths: List[str]) -> List[Dict[str, Any]]:
        """Ingests background text files, introspection data, and history for v125.0."""
        logger.info(f"TextIngestor: Ingesting knowledge from {len(paths)} paths.")
        results = []
        for path in paths:
            if os.path.isfile(path) and path.endswith(".txt"):
                content = self._read_source(path)
                results.append({
                    "source": path,
                    "type": "background_text",
                    "content": content,
                    "metadata": {
                        "length": len(content),
                        "filename": os.path.basename(path),
                        "ingested_at": "v125.0_ingestion_pipeline"
                    }
                })
        return results

    def _read_source(self, path: str) -> str:
        try:
            with open(path, 'r', errors='ignore') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to read source {path}: {e}")
            return ""
