import pytest
import asyncio
import numpy as np
from agentic_core.validation.statistical_rigor import StatisticalValidator
from agentic_core.constitutional.pqc_abstraction import PQCAbstraction
from agentic_core.divine.alignment import DivineAlignmentEngine

def test_statistical_rigor():
    validator = StatisticalValidator()
    data = [15.2, 15.5, 14.8, 15.1, 15.3]
    report = validator.validate_metric(data, baseline=10.0)
    assert report.mean > 0
    assert len(report.confidence_interval) == 2
    assert bool(report.passed) is True

def test_pqc_signatures():
    pqc = PQCAbstraction()
    msg = b"Sovereign Mandate"
    sig = pqc.sign(msg, "agent_opus_priv")
    assert pqc.verify(msg, sig, "agent_opus_priv") is True
    assert pqc.verify(msg, sig, "wrong_key") is False

@pytest.mark.asyncio
async def test_divine_alignment():
    engine = DivineAlignmentEngine()
    # Mocking check: "serve" or "help"
    sincerity = await engine.calibrate_niyyah("Selfless help to others", {})
    assert sincerity > 0.8
