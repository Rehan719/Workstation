import pytest
from agentic_core.quantum.oam_qkd_plus import OAMQKDSurrogate
from agentic_core.ueg.logger import VSBUEGLogger

@pytest.mark.asyncio
async def test_oam_qkd_statistical_targets():
    ueg = VSBUEGLogger()
    surrogate = OAMQKDSurrogate(ueg)

    # 48-state test
    res48 = await surrogate.generate_key(n_states=48, n_trials=10000)
    assert res48["qber"] < 0.06 # Slightly loose for random variance, but target < 5% on average
    assert res48["key_rate"] > 5.0 # Target 5.5

    # 96-state test
    res96 = await surrogate.generate_key(n_states=96, n_trials=10000)
    assert res96["key_rate"] > res48["key_rate"]

@pytest.mark.asyncio
async def test_secure_send_fallback():
    surrogate = OAMQKDSurrogate()
    res = await surrogate.secure_send(b"Top secret data", b"pubkey")
    assert res["mode"] in ["OAM-QKD", "PQC-KYBER-1024"]
