import asyncio
import logging
from typing import Any, List, Dict
from .ledger import UnifiedEvidenceGraph

logger = logging.getLogger(__name__)

class ContinuousTruthMaintenance:
    """
    v52.0 Article AK: Continuous Truth Maintenance System (CTMS).
    v52.0 Mastering: Non-monotonic reasoning triggers and dependency tracking.
    """
    def __init__(self, ueg: UnifiedEvidenceGraph):
        self.ueg = ueg
        self.is_running = False

    async def start(self):
        self.is_running = True
        logger.info("Starting CTMS background daemon...")
        while self.is_running:
            await self.scan_and_resolve()
            await asyncio.sleep(300) # Every 5 mins for demo

    async def scan_and_resolve(self):
        """
        Scans for CONTRADICTS relations and initiates belief revision.
        """
        edges = self.ueg.get_edges()
        contradictions = [(u, v, d) for u, v, d in edges if d.get('relation') == 'CONTRADICTS']

        for u, v, d in contradictions:
            logger.warning(f"CTMS detected contradiction: {u} <-> {v}")
            # Non-monotonic revision: choose the one with lower evidentiary support
            await self._resolve_contradiction(u, v)

    async def _resolve_contradiction(self, node_a: str, node_b: str):
        """
        Heuristic: The node with fewer SUPPORTS edges is downgraded.
        """
        support_a = len([e for e in self.ueg.get_edges() if e[1] == node_a and e[2].get('relation') == 'SUPPORTS'])
        support_b = len([e for e in self.ueg.get_edges() if e[1] == node_b and e[2].get('relation') == 'SUPPORTS'])

        weaker_node = node_a if support_a < support_b else node_b

        # Log resolution to ledger
        self.ueg.ledger.add_transaction('ctms', 'BELIEF_REVISION', {
            'downgraded_node': weaker_node,
            'reason': f"Contradiction found; weaker support ({min(support_a, support_b)} vs {max(support_a, support_b)})"
        })

        # Update node metadata in graph
        self.ueg.graph.nodes[weaker_node]['status'] = 'REJECTED'
        self.ueg.graph.nodes[weaker_node]['confidence'] = 0.0

        logger.info(f"CTMS Resolved contradiction by rejecting {weaker_node}")
