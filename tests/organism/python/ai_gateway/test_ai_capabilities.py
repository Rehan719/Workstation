import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock
from src.organism.python.ai_gateway.middleware.enhancers import ai_ingestion_enhancer
from src.organism.python.ai_gateway.agents.legal_research import QwenLegalAgent
from src.organism.python.ai_gateway.agents.codebase_assistant import MinimaxCoder
from src.organism.python.ai_gateway import gateway

@pytest.mark.asyncio
async def test_ai_ingestion_enhancer():
    # Mock gateway
    gateway.execute_completion = AsyncMock(return_value={"content": "AI analysis summary"})

    @ai_ingestion_enhancer(provider="mock")
    async def legacy_ingestor():
        return [{"url": "http://test.com", "data": "legacy text"}]

    results = await legacy_ingestor()
    assert len(results) == 1
    assert results[0]["ai_forensic_analysis"] == "AI analysis summary"

@pytest.mark.asyncio
async def test_qwen_legal_agent():
    gateway.execute_completion = AsyncMock(return_value={"content": "Detailed legal analysis"})

    agent = QwenLegalAgent(provider="mock")
    result = await agent.analyze_precedent("Summary of a dismissal case.")

    assert "analysis" in result
    assert result["analysis"] == "Detailed legal analysis"
    assert "EqA 2010" in result["statutory_references"]

@pytest.mark.asyncio
async def test_minimax_coder():
    gateway.execute_completion = AsyncMock(return_value={"content": "Refactored code snippet"})

    coder = MinimaxCoder(provider="mock")
    result = await coder.suggest_refactor("def old(): pass", "context")

    assert "suggestion" in result
    assert result["suggestion"] == "Refactored code snippet"
