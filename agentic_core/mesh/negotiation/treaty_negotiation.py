import numpy as np
import torch
from typing import List, Dict, Any, Optional
from agentic_core.biomimicry.minimisation.core.optimal_transport import OptimalTransportRouter
from agentic_core.ueg.logger import VSBUEGLogger
class TreatyNegotiator:
    def __init__(self, node_id: str, ueg_logger: Optional[VSBUEGLogger] = None):
        self.node_id, self.ueg, self.ot_router = node_id, ueg_logger or VSBUEGLogger(), OptimalTransportRouter(epsilon=0.01)
    async def negotiate(self, my_intents: List[Dict], peer_intents: List[Dict]) -> Dict:
        n, m = len(my_intents), len(peer_intents)
        cost = np.zeros((n, m))
        for i in range(n):
            for j in range(m):
                cost[i,j] = np.linalg.norm(np.array(my_intents[i].get("profile",[0.5,0.5])) - np.array(peer_intents[j].get("profile",[0.5,0.5])))
        plan, wasserstein, info = self.ot_router.solve(torch.ones(n)/n, torch.ones(m)/m, torch.from_numpy(cost).float())
        terms = [{"local": my_intents[i].get("id"), "peer": peer_intents[int(np.argmax(plan[i,:]))].get("id")} for i in range(n)]
        res = {"proposer": self.node_id, "terms": terms, "wasserstein": float(wasserstein)}
        await self.ueg.log_minimisation_event("treaty_negotiated", res)
        return res
