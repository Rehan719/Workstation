import pytest
import os
import json
from tests.formal.generate_certificate import FormalVerificationCertificate

@pytest.mark.asyncio
async def test_generate_certificate_success():
    gen = FormalVerificationCertificate(tla_spec_path="tests/formal/verify_capital_constitution.tla")
    invariants = ["LiquidityInvariant", "AllocationInvariant"]

    cert = await gen.generate_signed_certificate(invariants)

    assert cert["status"] == "VERIFIED_FORMALLY"
    assert "pqc_signature_stub" in cert
    assert len(cert["specification_hash"]) == 128 # SHA-3-512

    # Check file was written
    cert_path = f"tests/formal/certificates/{cert['certificate_id']}.json"
    assert os.path.exists(cert_path)
    with open(cert_path, 'r') as f:
        stored_cert = json.load(f)
    assert stored_cert["certificate_id"] == cert["certificate_id"]

@pytest.mark.asyncio
async def test_generate_certificate_fail_missing_spec():
    gen = FormalVerificationCertificate(tla_spec_path="missing.tla")
    with pytest.raises(RuntimeError, match="Formal Verification Failed"):
        await gen.generate_signed_certificate([])
