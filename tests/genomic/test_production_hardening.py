import sys
from types import ModuleType

# Mock missing modules globally
for mod_name in ['shap', 'jwt', 'casbin', 'alembic', 'pygit2', 'sigstore']:
    if mod_name not in sys.modules:
        mock = ModuleType(mod_name)
        sys.modules[mod_name] = mock

import pytest
from agentic_core.config.loader import settings
from agentic_core.builder.conversational_engine import ConversationalEngine
from agentic_core.builder.refinement_engine import RefinementEngine

def test_settings_loader():
    assert settings.get("VERSION") == "99.0.0"
    assert settings.get("FIDELITY_TARGET") == 0.992

@pytest.mark.asyncio
async def test_app_generation_and_refinement():
    builder = ConversationalEngine()
    app = await builder.build_from_prompt("Create a health portal")
    assert app.app_id.startswith("app-")
    assert "health" in app.frontend_code.lower()

    refiner = RefinementEngine(builder)
    refined_app = await refiner.refine_component(app, "Add dark mode toggle")
    assert "dark mode" in refined_app.frontend_code.lower()
