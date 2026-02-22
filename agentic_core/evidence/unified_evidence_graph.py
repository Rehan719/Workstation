from typing import Dict, Any, List, Optional
import networkx as nx
from datetime import datetime
import copy

class UnifiedEvidenceGraph:
    """
    v52.0 Article BA: Robust Unified Evidence Graph (UEG).
    Integrates formal proofs, Bayesian uncertainty, multi-modal embeddings,
    and system-wide versioning/rollback for autonomous mutations.
    """
    def __init__(self):
        self.graph = nx.DiGraph()
        self.version = "52.0"
        self.history: List[Dict[str, Any]] = []

    def commit_version(self, description: str):
        """Creates a snapshot of the current graph for rollback support."""
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "description": description,
            "version": self.version,
            "graph_data": copy.deepcopy(self.graph)
        }
        self.history.append(snapshot)
        if len(self.history) > 100: # Limit history size
            self.history.pop(0)

    def rollback(self, steps: int = 1):
        """Rolls back the graph state by a specified number of steps."""
        if len(self.history) >= steps:
            target = self.history[-steps]
            self.graph = target["graph_data"]
            self.version = target["version"]
            # Remove rolled back history
            self.history = self.history[:-steps]
            return True
        return False

    def add_evidence(self, source_id: str, target_id: str, relation: str, metadata: Optional[Dict[str, Any]] = None):
        """Adds a directional evidence link."""
        self.graph.add_edge(source_id, target_id,
                            relation=relation,
                            timestamp=datetime.now().isoformat(),
                            **(metadata or {}))

    def mark_claim_verified(self, claim_id: str, proof_receipt: Dict[str, Any]):
        """Marks a node as formally verified by a theorem prover."""
        if claim_id not in self.graph:
            self.graph.add_node(claim_id)
        self.graph.nodes[claim_id]['proof_status'] = "VERIFIED"
        self.graph.nodes[claim_id]['proof_details'] = proof_receipt

    def set_uncertainty(self, node_id: str, bayesian_stats: Dict[str, float]):
        """Attaches Bayesian uncertainty parameters to an evidence node."""
        if node_id in self.graph:
            self.graph.nodes[node_id].update(bayesian_stats)

    def add_causal_link(self, cause_id: str, effect_id: str, mechanism: str, strength: float):
        self.graph.add_edge(cause_id, effect_id,
                            relation="CAUSALLY_INFLUENCES",
                            mechanism=mechanism,
                            causal_strength=strength,
                            timestamp=datetime.now().isoformat())

    def link_blockchain_receipt(self, node_id: str, receipt: Dict[str, Any]):
        if node_id in self.graph:
            self.graph.nodes[node_id]['blockchain_anchor'] = receipt

    def store_symbolic_knowledge(self, rule_id: str, rule_metadata: Dict[str, Any]):
        self.graph.add_node(rule_id, type="SYMBOLIC_RULE", **rule_metadata)

    def record_quantum_metrics(self, job_id: str, metrics: Dict[str, Any]):
        if job_id not in self.graph:
            self.graph.add_node(job_id)
        self.graph.nodes[job_id]['quantum_metrics'] = metrics

    def log_xai_trace(self, decision_id: str, xai_metadata: Dict[str, Any]):
        if decision_id not in self.graph:
            self.graph.add_node(decision_id)
        self.graph.nodes[decision_id]['xai_trace'] = xai_metadata

    def get_highest_confidence_path(self, goal: str) -> List[str]:
        return list(nx.topological_sort(self.graph)) if nx.is_directed_acyclic_graph(self.graph) else []

    def get_nodes(self) -> List[str]:
        return list(self.graph.nodes)

    def get_edges(self) -> List[tuple]:
        return list(self.graph.edges)
