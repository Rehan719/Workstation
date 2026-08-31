import pytest
from agentic_core.genetic_immune.unified_defense import UnifiedDefenseOrchestrator
from agentic_core.ueg.logger import VSBUEGLogger

@pytest.mark.asyncio
async def test_unified_defense_orchestration():
    ueg = VSBUEGLogger()
    orchestrator = UnifiedDefenseOrchestrator(ueg)

    # 1. Low threat
    signal_low = {"perplexity": 10.0}
    res_low = await orchestrator.scan_and_defend(signal_low, {})
    assert res_low["status"] == "DEFENDED"
    assert res_low["threat_score"] < 0.5

    # 2. High threat (triggers topology warning and repair logic)
    signal_high = {"perplexity": 100.0}
    res_high = await orchestrator.scan_and_defend(signal_high, {})
    assert res_high["threat_score"] > 0.9
    assert res_high["status"] in ["DEFENDED", "QUARANTINED"]
