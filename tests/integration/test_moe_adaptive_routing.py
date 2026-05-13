import pytest, numpy as np
from agentic_core.recirculation.moe.fabric import MoEFabric
from agentic_core.cognitive.bootstrap import bootstrap_engines
def test_moe_routing():
    reg = bootstrap_engines()
    moe = MoEFabric(reg)
    assert len(moe.route(np.array([1,0,0,0,0,0]), {"tier": "advanced"}, top_k=5)) == 5
    assert len(moe.route(np.array([1,0,0,0,0,0]), {"tier": "free"}, top_k=5)) == 2
