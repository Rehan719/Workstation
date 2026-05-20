import pytest
import asyncio
from agentic_core.avatars.core.avatar_engine import AvatarIdentityManager, AvatarState
from agentic_core.ueg.logger import VSBUEGLogger
import os

class MockUEG:
    async def log_event(self, event_type, data, actor="SYSTEM"):
        return "mock_hash"

@pytest.mark.asyncio
async def test_avatar_creation():
    ueg = MockUEG()
    manager = AvatarIdentityManager(ueg)
    state = await manager.create_avatar("user_123")

    assert state.user_id == "user_123"
    assert state.avatar_id.startswith("did:workstation:")
    assert len(state.state_checksum) == 128 # SHA-3-512

@pytest.mark.asyncio
async def test_attestation():
    ueg = MockUEG()
    manager = AvatarIdentityManager(ueg)
    state = await manager.create_avatar("user_123")
    attestation = await manager.attest_state(state)

    assert "quote" in attestation
    assert "signature" in attestation

@pytest.mark.asyncio
async def test_halo2_proof():
    ueg = MockUEG()
    manager = AvatarIdentityManager(ueg)
    proof = await manager.generate_halo2_proof({"test": "data"})
    assert proof.startswith("halo2:v1:")
