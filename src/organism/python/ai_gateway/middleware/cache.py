import logging
import hashlib
import json
from typing import Dict, Any, Optional, List
import chromadb
from chromadb.utils import embedding_functions

logger = logging.getLogger(__name__)

class SemanticCache:
    """
    Semantic Caching Layer using ChromaDB.
    Avoids redundant API calls by caching semantically similar prompts.
    """
    def __init__(self, persist_directory: str = "data/organism/cache"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        # Use default embedding function (all-MiniLM-L6-v2) for efficiency
        self.emb_fn = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_or_create_collection(
            name="llm_cache",
            embedding_function=self.emb_fn
        )

    async def get(self, prompt: str, model: str, threshold: float = 0.95) -> Optional[str]:
        """
        Retrieves a cached response if a semantically similar prompt exists.
        """
        try:
            results = self.collection.query(
                query_texts=[prompt],
                n_results=1,
                where={"model": model}
            )

            if results["ids"] and results["ids"][0]:
                distance = results["distances"][0][0]
                # Cosine distance: lower is more similar.
                # default Chroma distance is l2. For semantic sim, we check threshold.
                if distance < (1 - threshold) * 10: # Rough l2 scaling for similarity
                    logger.info(f"SemanticCache: Hit for model {model} (dist: {distance:.4f})")
                    return results["documents"][0][0]
        except Exception as e:
            logger.error(f"SemanticCache: Query error: {e}")

        return None

    async def set(self, prompt: str, response: str, model: str, task_type: str = "general"):
        """
        Stores a response in the semantic cache.
        """
        doc_id = hashlib.sha256(f"{model}:{prompt}".encode()).hexdigest()
        try:
            self.collection.add(
                ids=[doc_id],
                documents=[response],
                metadatas=[{"model": model, "task_type": task_type, "prompt": prompt[:500]}]
            )
            logger.info(f"SemanticCache: Stored result for {model}")
        except Exception as e:
            logger.error(f"SemanticCache: Store error: {e}")
