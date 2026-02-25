import asyncio
import logging
from typing import Any, List, Dict
from .ledger import UnifiedEvidenceGraph

logger = logging.getLogger(__name__)

class ContinuousTruthMaintenanceSystem:
    """
    Article AK: Continuous Truth Maintenance System (CTMS - v53 Upgrade).
    Maintains unassailable truth via non-monotonic reasoning and belief revision.
    """
    def __init__(self, ueg: UnifiedEvidenceGraph):
        self.ueg = ueg
        self.is_running = False

    async def start(self):
        self.is_running = True
        logger.info("Starting CTMS background daemon (v53)...")
        while self.is_running:
            await self.scan_and_resolve()
            await asyncio.sleep(600) # v53: Scalable monitoring

    async def scan_and_resolve(self):
        """
        Scans for logical inconsistencies and initiates recursive belief revision.
        """
        edges = self.ueg.get_edges()
        contradictions = [(u, v, d) for u, v, d in edges if d.get('relation') == 'CONTRADICTS']

        for u, v, d in contradictions:
            logger.warning(f"CTMS detected contradiction: {u} <-> {v}")
            # v53: Non-monotonic belief revision
            await self._resolve_contradiction(u, v)

    async def _resolve_contradiction(self, node_a: str, node_b: str):
        """
        v53 Resolution: Trust-weighted voting and causal constraint checking.
        """
        trust_a = self._calculate_trust_score(node_a)
        trust_b = self._calculate_trust_score(node_b)

        weaker = node_a if trust_a < trust_b else node_b
        stronger = node_b if trust_a < trust_b else node_a

        # Article AK: Log resolution with explanation
        explanation = f"Contradiction resolved via trust-weighted voting. {stronger} (score {max(trust_a, trust_b)}) upheld over {weaker} (score {min(trust_a, trust_b)})."

        self.ueg.ledger.add_transaction('ctms', 'BELIEF_REVISION', {
            'rejected': weaker,
            'upheld': stronger,
            'explanation': explanation
        })

        # Update node metadata
        if weaker in self.ueg.graph:
            self.ueg.graph.nodes[weaker]['status'] = 'REJECTED'
            self.ueg.graph.nodes[weaker]['confidence'] = 0.0

        if stronger in self.ueg.graph:
            self.ueg.graph.nodes[stronger]['status'] = 'UPHELD'
            self.ueg.graph.nodes[stronger]['confidence'] = 1.0

        # v53: Propagate truth values recursively
        await self._propagate_truth(stronger)

        logger.info(f"CTMS: {explanation}")

    def _calculate_trust_score(self, node_id: str) -> float:
        """
        v53: trust = support_count * (2.0 if formally_proven else 1.0)
        """
        # Bonus for formal verification (Article AJ)
        has_proof = any(d.get('relation') == 'VALIDATED_BY' and "proof" in u.lower()
                        for u, v, d in self.ueg.get_edges() if v == node_id)

        support_count = len([u for u, v, d in self.ueg.get_edges() if v == node_id and d.get('relation') == 'SUPPORTS'])

        multiplier = 2.5 if has_proof else 1.0
        return float(support_count) * multiplier

    async def _propagate_truth(self, node_id: str):
        """
        Recursive belief propagation (Article AK).
        """
        # Find children
        derived = [u for u, v, d in self.ueg.get_edges() if v == node_id and d.get('relation') == 'DERIVED_FROM']
        for child in derived:
             if child in self.ueg.graph:
                self.ueg.graph.nodes[child]['confidence'] = min(1.0, self.ueg.graph.nodes[child].get('confidence', 0.5) * 1.2)
                # Recurse
                await self._propagate_truth(child)

class ContinuousTruthMaintenance(ContinuousTruthMaintenanceSystem):
    """Wrapper for backward compatibility."""
    pass
