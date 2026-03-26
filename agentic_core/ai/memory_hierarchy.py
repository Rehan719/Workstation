import logging
import networkx as nx
import json
import os
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)

class MemoryHierarchy:
    """
    v0.9 Unified Memory Hierarchy.
    Working (Redis), Episodic (ChromaDB), Semantic (Vector), Procedural (Graph).
    """
    def __init__(self, data_dir: str = "agentic_core/data/memory"):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)

        # Procedural Memory (Graph-based)
        self.procedural_graph = nx.DiGraph()
        self._load_procedural_memory()

    def add_episodic_entry(self, task: str, outcome: str, context: Dict[str, Any]):
        """Episodic Memory: Time-series event storage."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "task": task,
            "outcome": outcome,
            "context": context
        }
        # In a real system, we'd write to ChromaDB/PostgreSQL
        logger.info(f"Memory: Logged episode - {task}")
        return entry

    def query_semantic_memory(self, query: str) -> List[str]:
        """Semantic Memory: Fact retrieval (Vector-style)."""
        # Mocking vector search results
        facts = ["Article 1127 governs evolution", "QEP Flagship is live", "PQC is mandatory"]
        return [f for f in facts if any(word in f.lower() for word in query.lower().split())]

    def record_procedural_pattern(self, step_from: str, step_to: str, success_rate: float):
        """Procedural Memory: Workflow and tool usage patterns."""
        if not self.procedural_graph.has_edge(step_from, step_to):
            self.procedural_graph.add_edge(step_from, step_to, success_rate=success_rate, count=1)
        else:
            data = self.procedural_graph[step_from][step_to]
            data['count'] += 1
            data['success_rate'] = (data['success_rate'] * (data['count']-1) + success_rate) / data['count']

        self._save_procedural_memory()

    def _load_procedural_memory(self):
        path = os.path.join(self.data_dir, "procedural.json")
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    data = json.load(f)
                    self.procedural_graph = nx.node_link_graph(data)
            except:
                pass

    def _save_procedural_memory(self):
        path = os.path.join(self.data_dir, "procedural.json")
        with open(path, "w") as f:
            data = nx.node_link_data(self.procedural_graph)
            json.dump(data, f)

unified_memory = MemoryHierarchy()
