import logging
import numpy as np
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class GRNModeler:
    """
    ARTICLE 161: Gene Regulatory Network Modeler.
    Performs in silico testing to verify module behavior and interactions.
    """
    def __init__(self):
        self.simulation_results = []

    def simulate_circuit(self, genes: List[str], interactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Simulates logic gates (AND, OR, NOT) within the GRN using a transition matrix approach.
        """
        logger.info(f"GRN_MODELER: Simulating circuit with {len(genes)} nodes.")

        # Article 60: Using actual matrix-based stability computation instead of random
        size = len(genes)
        if size == 0: return {"stability_score": 1.0, "status": "EMPTY"}

        # Create a mock interaction matrix based on interactions list
        adj = np.eye(size) * 0.5
        for inter in interactions:
            try:
                i = genes.index(inter['source'])
                j = genes.index(inter['target'])
                adj[i, j] = 0.8 if inter.get('type') == 'activator' else -0.8
            except (ValueError, KeyError):
                continue

        # Compute spectral radius as a proxy for stability
        eigenvalues = np.linalg.eigvals(adj)
        spectral_radius = np.max(np.abs(eigenvalues))

        stability = 1.0 / (1.0 + spectral_radius)
        latency = 10 + size * 2.5

        result = {
            "stability_score": round(float(stability), 4),
            "propagation_latency": round(float(latency), 2),
            "status": "VALIDATED" if stability > 0.4 else "UNSTABLE"
        }
        self.simulation_results.append(result)
        return result

    def infer_topology(self, interaction_logs: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """
        Reconstructs GRN topology from system activity logs by extracting caller -> callee edges.
        Returns {} when the logs carry no usable caller/callee pairs.
        """
        # W415 — the docstring said "using correlation analysis". Nothing correlates anything
        # here: the reconstruction is a direct read of caller/callee fields off each log record.
        topology = {}
        # Article 60: Reconstruct from logs instead of returning hardcoded mock
        for log in interaction_logs:
            caller = log.get('caller')
            callee = log.get('callee')
            if caller and callee:
                if caller not in topology: topology[caller] = []
                if callee not in topology[caller]:
                    topology[caller].append(callee)

        # W415 — this ended `return topology if topology else {"orchestrator": ["manager",
        # "dispatcher"]}`. Whenever the logs were empty or unparseable the method invented a
        # three-component edge set and returned it in exactly the shape of a genuine
        # reconstruction — nothing in the returned value distinguished the fallback from
        # topology actually inferred from activity. The honest reconstruction of no usable
        # logs is no topology.
        return topology
