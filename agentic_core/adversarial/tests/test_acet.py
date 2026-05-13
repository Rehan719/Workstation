import pytest
from agentic_core.adversarial.acet_triad import ACETAdversarialTriad
from agentic_core.ueg.logger import VSBUEGLogger

@pytest.mark.asyncio
async def test_acet_residual_risk():
    ueg = VSBUEGLogger()
    triad = ACETAdversarialTriad(ueg)

    res = await triad.run_episode()
    assert res["residual_risk"] <= 0.05
    assert res["status"] == "STABLE"

@pytest.mark.asyncio
async def test_continuous_campaign():
    triad = ACETAdversarialTriad()
    results = await triad.continuous_campaign(episodes=5)
    assert len(results) == 5
    assert all(r["residual_risk"] <= 0.05 for r in results)
