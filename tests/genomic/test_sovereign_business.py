import sys
from types import ModuleType

# Mock missing modules globally
for mod_name in ['shap', 'jwt', 'casbin', 'alembic', 'pygit2', 'sigstore']:
    if mod_name not in sys.modules:
        mock = ModuleType(mod_name)
        sys.modules[mod_name] = mock

import pytest
from agentic_core.governance.command_dispatch import AICommander, AIDispatcher
from agentic_core.governance.adaptive_profiles import IndustryAdaptiveGovernance, IndustryType
from agentic_core.business.pipelines import BusinessPipeline

@pytest.mark.asyncio
async def test_commander_dispatcher():
    commander = AICommander()
    dispatcher = AIDispatcher()

    objective = await commander.define_objective("Increase market share", {"region": "global"})
    assert objective["priority"] == "HIGH"

    task_id = await dispatcher.dispatch_task(objective, {"compute": 10})
    assert task_id.startswith("task_")
    assert len(dispatcher.active_tasks) == 1

def test_adaptive_governance():
    gov = IndustryAdaptiveGovernance()
    profile = gov.apply_profile(IndustryType.HEALTH)
    assert profile["phi_protection"] is True
    assert profile["compliance"] == "HIPAA"

@pytest.mark.asyncio
async def test_business_pipelines():
    res = await BusinessPipeline.run_p2p({"vendor": "Acme"})
    assert res["status"] == "PAID"

    res = await BusinessPipeline.run_o2c({"order": "A1"})
    assert res["revenue"] == 1500.0
