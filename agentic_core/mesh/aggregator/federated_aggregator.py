import numpy as np
import asyncio
from typing import Dict, List, Optional, Any
from agentic_core.ueg.logger import VSBUEGLogger
class FederatedAggregator:
    def __init__(self, epsilon=0.1, delta=1e-5, ueg_logger=None, discovery=None):
        self.epsilon, self.delta, self.noise_scale = epsilon, delta, 2.0 / epsilon
        self.ueg, self.discovery = ueg_logger or VSBUEGLogger(), discovery
        self.weights = {"free_energy": 0.30, "optimal_transport": 0.25, "schrodinger_bridge": 0.20, "entropy_export": 0.15, "murray_law": 0.10}
    def aggregate(self, local_weights):
        if not local_weights: return {}
        n = len(local_weights)
        keys = local_weights[0].keys()
        summed = {}
        for k in keys:
            total = sum(max(0.0, min(1.0, w.get(k, 0.0))) for w in local_weights)
            noise = np.random.normal(0, self.noise_scale)
            summed[k] = float(max(0.0, min(1.0, (total + noise) / n)))
        if "legal_precision" in summed: summed["legal_precision"] = max(summed["legal_precision"], 0.15)
        return summed
    async def sync_weights_loop(self, interval_sec=10.0):
        while True:
            if not self.discovery: await asyncio.sleep(interval_sec); continue
            peers = await self.discovery.discover_peers("minimisation:weights")
            if peers:
                local_weights = [self.weights.copy() for _ in peers]
                aggregated = self.aggregate(local_weights)
                self.weights.update(aggregated)
                await self.ueg.log_minimisation_event("weight_sync_complete", {"peer_count": len(peers), "aggregated_weights": aggregated})
            await asyncio.sleep(interval_sec)
