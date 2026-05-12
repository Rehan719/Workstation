import asyncio
import pytest
from agentic_core.cognitive.registry import CognitiveEngineRegistry, EngineType
from agentic_core.cognitive.foundational.aqal_engine import AqalEngine
from agentic_core.cognitive.meta.niyyah_engine import NiyyahEngine
from agentic_core.cognitive.meta.tafakkur_engine import TafakkurEngine
from agentic_core.consultation.mushawara_bridge import MushawaraBridge, ConsultationQuery
from agentic_core.validation.omni_enforcement_pattern_supreme import OmniEnforcementPatternSupreme

@pytest.mark.asyncio
async def test_phase1_cognitive_cascade():
    # 1. Setup
    ueg = None # Stub logger
    enforcement = OmniEnforcementPatternSupreme({"fail_on_missing_validator": False}, {})
    registry = CognitiveEngineRegistry()

    # 2. Register Engines
    aqal = AqalEngine(ueg)
    niyyah = NiyyahEngine(ueg)
    tafakkur = TafakkurEngine(ueg)
    registry.register(EngineType.AQAL, aqal)
    registry.register(EngineType.NIYYAH, niyyah)
    registry.register(EngineType.TAFAKKUR, tafakkur)

    bridge = MushawaraBridge(registry, ueg, enforcement)

    # 3. Execute Consultation
    query = ConsultationQuery(
        id="test_decision_001",
        payload={"action": "rebalance_swf", "aum_pct": 0.05},
        context={"user_tier": "advanced", "domain": "capital"}
    )

    result = await bridge.sync_consult(
        query=query,
        required_engines=[EngineType.AQAL, EngineType.NIYYAH, EngineType.TAFAKKUR]
    )

    # 4. Verify Success Gates
    assert result.latency_ms < 500
    assert result.vrpr_confidence >= 0.95
    assert len(result.engine_attestations) == 3
    assert "Certified Strategic Outcome" in result.recommendation
    assert result.constitutional_articles == list(set(aqal.constitutional_binding + niyyah.constitutional_binding + tafakkur.constitutional_binding))

    print(f"✅ Phase 1 Cascade Successful. Latency: {result.latency_ms:.2f}ms")

if __name__ == "__main__":
    asyncio.run(test_phase1_cognitive_cascade())
