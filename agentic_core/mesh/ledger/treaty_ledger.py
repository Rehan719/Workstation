import hashlib, time, json
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from agentic_core.biomimicry.minimisation.core.schrodinger_bridge import SchrödingerBridgeEngine
from agentic_core.ueg.logger import VSBUEGLogger
import torch

@dataclass
class Treaty:
    id: str
    proposer: str
    counterparty: str
    terms: Dict[str, Any]
    sb_kl_divergence: float
    timestamp: str
    status: str = "proposed"
    signatures: List[str] = None
    def dict(self): return asdict(self)

class TreatyLedger:
    def __init__(self, node_id: str, ueg_logger: Optional[VSBUEGLogger] = None):
        self.node_id, self.ueg, self.treaties = node_id, ueg_logger or VSBUEGLogger(), {}
    async def propose_treaty(self, counterparty: str, terms: Dict[str, Any], remote_caps: Optional[Dict] = None) -> Treaty:
        sb = SchrödingerBridgeEngine()
        s_dist = torch.tensor([0.4, 0.3, 0.2, 0.1]).float()
        t_dist = torch.tensor([0.1, 0.2, 0.3, 0.4]).float()
        cost = torch.eye(4)*0.1 + (1.0-torch.eye(4))
        plan, kl_div, info = sb.compute_bridge(s_dist, t_dist, cost)
        tid = hashlib.sha3_512(f"{self.node_id}:{counterparty}:{time.time()}".encode()).hexdigest()
        treaty = Treaty(tid, self.node_id, counterparty, terms, float(kl_div), datetime.utcnow().isoformat(), signatures=[])
        self.treaties[tid] = treaty
        await self.ueg.log_minimisation_event("treaty_proposed", treaty.dict())
        return treaty
    async def sign_treaty(self, tid: str, sig: str) -> bool:
        if tid not in self.treaties: return False
        t = self.treaties[tid]
        if sig not in t.signatures: t.signatures.append(sig)
        if len(t.signatures) >= 2:
            t.status = "ratified"
            await self.ueg.log_minimisation_event("treaty_ratified", {"id": tid})
            return True
        return False
