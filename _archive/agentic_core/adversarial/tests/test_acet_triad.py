import pytest
from agentic_core.adversarial.acet_triad import ACETAdversarialTriad
from agentic_core.ueg.logger import VSBUEGLogger

@pytest.mark.asyncio
async def test_acet_residual_risk_target():
    ueg = VSBUEGLogger()
    triad = ACETAdversarialTriad(ueg)

    res = await triad.run_episode()
    # Constraint 8: residual risk <= 5%
    assert res["residual_risk"] <= 0.05
    assert res["status"] == "STABLE"

@pytest.mark.asyncio
async def test_acet_continuous_campaign():
    triad = ACETAdversarialTriad()
    results = await triad.continuous_campaign(episodes=10)
    assert len(results) == 10
    for r in results:
        assert r["residual_risk"] <= 0.05
