import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock
from src.organism.python.ai_gateway import AIGateway
from src.organism.python.ai_gateway.adapters.base import SovereignLLMClient
from src.organism.python.neural.event_bus import AsyncEventBus
from src.organism.python.neural.event_types import AIActionInitiated, AIInferenceComplete

class MockAdapter(SovereignLLMClient):
    async def chat_completion(self, messages, **kwargs):
        return {
            "provider": "mock",
            "content": "Hello from mock AI",
            "usage": {"total_tokens": 10},
            "latency_ms": 100.0
        }
    async def get_embeddings(self, text):
        return [[0.1, 0.2]]

@pytest.mark.asyncio
async def test_ai_gateway_flow():
    bus = AsyncEventBus()
    await bus.start()

    # Track events
    initiated_detected = asyncio.Event()
    complete_detected = asyncio.Event()

    async def initiated_handler(event: AIActionInitiated):
        initiated_detected.set()

    async def complete_handler(event: AIInferenceComplete):
        complete_detected.set()

    bus.subscribe(AIActionInitiated, initiated_handler)
    bus.subscribe(AIInferenceComplete, complete_handler)

    # Setup Gateway
    gateway = AIGateway(event_bus=bus)
    adapter = MockAdapter("mock-provider")
    gateway.register_provider("mock", adapter)

    # Execute
    result = await gateway.execute_completion("mock", [{"role": "user", "content": "hi"}])

    assert result["content"] == "Hello from mock AI"

    # Verify Events
    await asyncio.wait_for(initiated_detected.wait(), timeout=1.0)
    await asyncio.wait_for(complete_detected.wait(), timeout=1.0)

    await bus.stop()

@pytest.mark.asyncio
async def test_ai_gateway_fallback():
    gateway = AIGateway()
    adapter = MockAdapter("deepseek")
    gateway.register_provider("deepseek", adapter)

    # Attempting to use non-existent provider 'qwen', should fallback to 'deepseek'
    result = await gateway.execute_completion("qwen", [{"role": "user", "content": "hi"}])

    assert result["provider"] == "mock"
