import sys
import os

# Ultra-Mocking to bypass agentic_core.__init__ issues
sys.modules['agentic_core.layers.ueg'] = type('module', (), {'ueg': type('obj', (), {'log_event': lambda *a, **k: None, 'merkle_root': '0x'})()})
sys.modules['agentic_core.layers.l11_civilisation.civilisation'] = type('module', (), {'mycelial_stack': type('obj', (), {'peers': []})})

# Define classes inline or import from file without triggering parent package init if possible
# But agentic_core init is triggered. Let's try to mock the failing imports before they are called.
sys.modules['shap'] = type('module', (), {})
sys.modules['matplotlib'] = type('module', (), {'pyplot': type('module', (), {})})
sys.modules['seaborn'] = type('module', (), {})
sys.modules['plotly'] = type('module', (), {'graph_objects': type('module', (), {})})
sys.modules['scipy'] = type('module', (), {'stats': type('module', (), {})})
sys.modules['sklearn'] = type('module', (), {'cluster': type('module', (), {})})
sys.modules['pyro'] = type('module', (), {})
sys.modules['ray'] = type('module', (), {'init': lambda **k: None})
sys.modules['web3'] = type('module', (), {})
sys.modules['z3'] = type('module', (), {})
sys.modules['qiskit'] = type('module', (), {})
sys.modules['pennylane'] = type('module', (), {})

from agentic_core.ai_ceo.memory_v01 import memory_v01, meeting_log
from agentic_core.layers.l1_identity.genome_engine import genome_engine
from agentic_core.reactor.domains.weaver import domain_weaver
from agentic_core.reactor.ecosystem.marketplace import marketplace
from agentic_core.layers.l5_resilience.resilience import resilience_manager

async def main():
    print("Verifying v0.1 Logic...")

    memory_v01.add_exchange("Hello", "Hi")
    assert len(memory_v01.query("Hello")) > 0
    print("✓ Memory Verified")

    meeting_log.post_argument("CEvO", "Args", "APPROVE")
    assert "CEvO" in meeting_log.get_recent_debate()
    print("✓ Meeting Log Verified")

    genome_engine.genome["constitution"]["articles"].append({"id": 42, "content": "transparency rigid"})
    assert genome_engine.get_behavioral_params()["temperature"] == 0.4
    print("✓ Evolution Params Verified")

    res = await domain_weaver.synthesize("test", ["science"])
    assert "test" in res["query"]
    print("✓ Weaver Verified")

    mid = marketplace.publish_agent({"n": "a"}, "u")
    assert len(marketplace.list_agents()) > 0
    print("✓ Marketplace Verified")

    for _ in range(5): resilience_manager.handle_failure("c", "E", {})
    assert resilience_manager.predict_failure("c") is True
    print("✓ Resilience Verified")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
