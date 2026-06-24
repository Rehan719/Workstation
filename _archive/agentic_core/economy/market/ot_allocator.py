import numpy as np
import torch
from typing import List, Dict, Any, Optional
from agentic_core.biomimicry.minimisation.core.optimal_transport import OptimalTransportRouter
from agentic_core.ueg.logger import VSBUEGLogger

class ResourceMarketAllocator:
    """
    OT-based resource allocation across the mesh.
    Minimises transport cost subject to supply/demand constraints.
    """
    def __init__(self, ueg_logger: Optional[Any] = None):
        self.ot = OptimalTransportRouter(epsilon=0.01)
        self.ueg = ueg_logger or VSBUEGLogger()

    async def allocate(self, supply: List[Dict[str, Any]], demand: List[Dict[str, Any]]) -> Dict[str, Any]:
        n, m = len(supply), len(demand)
        supply_vec = torch.tensor([s['available'] for s in supply]).float()
        demand_vec = torch.tensor([d['required'] for d in demand]).float()

        # Build cost matrix based on distance/latency (Simulated)
        cost_matrix = torch.ones((n, m)) * 0.1

        plan, wasserstein, info = self.ot.solve(supply_vec, demand_vec, cost_matrix)

        allocations = []
        for i in range(n):
            for j in range(m):
                if plan[i, j] > 1e-5:
                    allocations.append({
                        "from": supply[i]["peer_id"],
                        "to": demand[j]["peer_id"],
                        "amount": float(plan[i, j]),
                        "resource": supply[i]["resource"]
                    })

        result = {
            "allocations": allocations,
            "wasserstein": float(wasserstein),
            "status": "optimized"
        }
        await self.ueg.log_minimisation_event("resource_allocation_complete", result)
        return result
