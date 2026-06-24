import pytest
from agentic_core.hallucination.sandbox import HallucinationSandbox
from agentic_core.ueg.logger import VSBUEGLogger

@pytest.mark.asyncio
async def test_hallucination_containment_logic():
    ueg = VSBUEGLogger()
    sandbox = HallucinationSandbox(ueg)

    draft = "The capital fund generated 15% ROI in 2 hours."
    context = {"domain": "finance"}

    res = await sandbox.validate_and_refine(draft, context)

    # In hardened version, result must have passed=True or be refined.
    # If it passed, it must show 100% containment.
    if res.get("passed"):
        assert res["containment_efficacy"] == 1.0
        assert res["algorithm"] == "spatial_quadtree_gradient_descent"
    else:
        # If it didn't pass initially, it would have been refined.
        # VRPR outputs don't have 'passed' field directly usually,
        # but my refined sandbox re-validates.
        assert res.get("passed") is True # Sandbox ensures it eventually passes or loops
