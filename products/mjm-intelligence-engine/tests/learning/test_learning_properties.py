import sys
import os
import asyncio
from hypothesis import given, strategies as st
import pytest

# Add product root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from core.learning.learning_engine import MJMLearningEngine, LearningSignal

@pytest.mark.asyncio
@given(domain=st.text(min_size=1), checkpoint=st.text(min_size=1))
async def test_learning_signal_ingestion_properties(domain, checkpoint):
    """
    Property: Ingesting a signal always produces an accepted receipt.
    """
    engine = MJMLearningEngine()
    signal = LearningSignal(
        signal_type="EXECUTION_SUCCESS",
        domain_id=domain,
        workflow_checkpoint=checkpoint,
        outcome_data={"success": True},
        context={"user": "tester"}
    )

    result = await engine.ingest_feedback(signal)
    assert result["status"] == "ACCEPTED"
    assert "receipt_id" in result
    assert len(engine.history) > 0
