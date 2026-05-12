import pytest
import asyncio
from agentic_core.legal.v2.precision_engine_v2 import LegalPrecisionEngineV2

@pytest.mark.asyncio
async def test_legal_v2_multi_jurisdiction():
    engine = LegalPrecisionEngineV2()

    # Test HMRC
    hmrc_payload = "PAYE Compliance and VAT Act 1994 are met, along with Corporation Tax Act and Income Tax Act."
    res = await engine.validate_jurisdiction("hmrc", {"data": hmrc_payload})
    assert res["passed"] is True

    # Test GDPR failure
    gdpr_payload = "Purpose Limitation only."
    res = await engine.validate_jurisdiction("gdpr", {"data": gdpr_payload})
    assert res["passed"] is False
    assert "Right to Erasure" in res["missing"]
