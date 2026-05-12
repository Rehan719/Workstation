import pytest
import asyncio
from agentic_core.llm.gemma4_engine import Gemma4SovereignEngine

@pytest.mark.asyncio
async def test_gemma4_emulation():
    config = {"emulation_mode": True}
    engine = Gemma4SovereignEngine(config)
    response = await engine.generate("Translate 'Sovereign' to Arabic")
    # Response is a dict since we call response.dict() in Gemma4SovereignEngine
    assert "Supreme Sovereign response" in response["content"]
    assert response["model_id"] == "Gemma-4-Sovereign-4bit"
