from typing import Dict, Any

class MockStripeClient:
    """
    Realistic mock for sandbox testing—no external network calls.
    Matches the vΩ∞-OMNISYNTHESIS-SUPREME specification for commercial integrity.
    """
    def __init__(self, api_key: str):
        self.api_key = api_key

    def create_checkout_session(self, tier: str, customer_email: str) -> Dict[str, Any]:
        return {
            "id": f"cs_mock_{tier}_123",
            "url": f"https://checkout.stripe.com/pay/cs_mock_{tier}_123",
            "status": "open",
            "customer_email": customer_email
        }

    def retrieve_subscription(self, subscription_id: str) -> Dict[str, Any]:
        return {
            "id": subscription_id,
            "status": "active",
            "current_period_end": 1715436300, # Simulated timestamp
            "plan": {"id": "price_standard_mock"}
        }
