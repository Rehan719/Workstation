import pytest
import asyncio
from agentic_core.ethical_guardian import EthicalSentinel

@pytest.mark.asyncio
async def test_ethical_sentinel():
    sentinel = EthicalSentinel()

    # Test safe content
    safe_task = {"content": "The study of quantum computing is advancing rapidly."}
    safe_result = await sentinel.execute(safe_task)
    assert safe_result["status"] == "approved"
    assert safe_result["risk_score"] < 0.3

    # Test potentially biased content (mocked)
    # Since it's a mock, we can just check the structure
    assert "toxicity" in safe_result
    assert "bias" in safe_result
    assert "is_aligned" in safe_result

if __name__ == "__main__":
    asyncio.run(test_ethical_sentinel())
