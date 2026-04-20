import time
from agentic_core.mesh.health.monitor import MeshHealthMonitor
def test_health():
    m = MeshHealthMonitor()
    m.peer_heartbeats["p1"] = time.time()
    assert m.get_reputation("p1") > 0.9
