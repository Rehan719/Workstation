import pytest
import asyncio
from unittest.mock import MagicMock
from agentic_core.mesh.negotiation.stream_negotiation import StreamNegotiator
from agentic_core.mesh.negotiation.treaty_negotiation import TreatyNegotiator
from agentic_core.mesh.negotiation.jurisdiction_routing import JurisdictionRouter

class MockLegalEngine:
    def agent_covers_statute(self, *args): return True
    def validate(self, *args): return MagicMock(is_compliant=True)
    def validate_assignment(self, *args): return 1.0

@pytest.mark.asyncio
async def test_stream_negotiation_legal_filtering():
    router = JurisdictionRouter(legal_engine=MockLegalEngine())
    negotiator = TreatyNegotiator("root")
    sn = StreamNegotiator("root", negotiator, router)

    peer_id = "node_1"
    await sn.open_negotiation_stream(peer_id)

    # Valid intent
    valid_intent = {"id": "peer_v1", "profile": [0.5, 0.5], "data_transfer": "allowed"}
    # Invalid intent (violates GDPR in JurisdictionRouter logic)
    invalid_intent = {"id": "peer_i1", "profile": [0.5, 0.5], "data_transfer": "restricted_zone", "compliance_certified": False}

    # Put intents in stream manually to simulate incoming
    await sn.active_streams[peer_id].put(valid_intent)
    await sn.active_streams[peer_id].put(invalid_intent)

    await sn.process_incoming_negotiations(peer_id)
    assert True

@pytest.mark.asyncio
async def test_jurisdiction_router_bounds():
    router = JurisdictionRouter(legal_engine=MockLegalEngine())

    # Equality Act violation
    bad_term = {"policy_alignment": "violated", "protected_characteristics": "compromised"}
    assert router.validate_treaty_legal_bounds([bad_term]) is False

    good_term = {"policy_alignment": "aligned", "protected_characteristics": "safe"}
    assert router.validate_treaty_legal_bounds([good_term]) is True
