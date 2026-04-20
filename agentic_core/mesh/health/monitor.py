import time, asyncio
from typing import Dict, Optional
from agentic_core.ueg.logger import VSBUEGLogger
class MeshHealthMonitor:
    def __init__(self, heartbeat_interval=5.0, ueg_logger=None):
        self.heartbeat_interval, self.ueg, self.peer_heartbeats = heartbeat_interval, ueg_logger or VSBUEGLogger(), {}
    async def start_heartbeat(self):
        while True:
            await self.ueg.log_minimisation_event("mesh_heartbeat_sent", {"timestamp": time.time()})
            await asyncio.sleep(self.heartbeat_interval)
    def get_reputation(self, peer_id):
        last_seen = self.peer_heartbeats.get(peer_id, 0)
        diff = time.time() - last_seen
        return max(0.0, 1.0 - (diff / 30.0)) if diff < 30.0 else 0.0
