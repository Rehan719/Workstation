import pytest
from backend.stripe.tiered_subscriptions import TIER_CONFIG
from backend.stripe.mock_client import MockStripeClient

def test_stripe_mock_integration():
    client = MockStripeClient(api_key="sk_test_supreme")
    session = client.create_checkout_session(tier="standard", customer_email="test@example.com")
    assert "cs_mock_standard" in session["id"]
    sub = client.retrieve_subscription("sub_mock_123")
    assert sub["status"] == "active"
    assert TIER_CONFIG["standard"]["price_id"] == "price_standard_mock"
