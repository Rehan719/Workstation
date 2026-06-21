"""
Payments — honest, launch-ready rails.

Safety model (NEVER moves real money autonomously):
- mode "simulation": no STRIPE_SECRET_KEY → clearly-labelled simulated sessions.
- mode "test":       a test key (sk_test_…) → real Stripe TEST sessions, no real charge.
- mode "live_gated": a live key (sk_live_…) WITHOUT STRIPE_LIVE_ENABLED=true → charges refused.
- mode "live":       live key AND STRIPE_LIVE_ENABLED=true → real charges (Owner must set BOTH).

WST balances are read from the real Capital Fund — never fabricated. The previous
version returned a hardcoded wallet and `stripe_connected: True`; that has been removed.
"""
import os
import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/payments", tags=["Economic Sovereignty"])


def _mode() -> str:
    key = os.getenv("STRIPE_SECRET_KEY", "")
    if not key:
        return "simulation"
    if key.startswith("sk_live_"):
        return "live" if os.getenv("STRIPE_LIVE_ENABLED", "false").lower() == "true" else "live_gated"
    return "test"   # sk_test_… (or any non-live key) → Stripe test mode


def _stripe():
    try:
        import stripe
        stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")
        return stripe
    except Exception:
        return None


def _wst_available():
    try:
        from agentic_core.api.capital_fund import _load_fund
        return _load_fund().get("available")
    except Exception:
        return None


_NOTES = {
    "simulation": "No STRIPE_SECRET_KEY set — sessions are clearly-labelled simulations; no real money.",
    "test": "Stripe TEST mode — real Stripe sessions, but no real charges.",
    "live_gated": "Live key present but STRIPE_LIVE_ENABLED is not 'true' — real charges are refused.",
    "live": "LIVE — real charges enabled by the Owner (live key + STRIPE_LIVE_ENABLED=true).",
}


class CheckoutSession(BaseModel):
    item_id: str
    price_wst: float = 0.0
    amount_gbp: float = 0.0
    user_id: str = "default"
    payment_method: str = "card"   # card | wst_balance


@router.get("/status")
async def payments_status():
    """Truthful payment-rail status — never claims a connection that isn't real."""
    mode = _mode()
    return {
        "mode": mode,
        "stripe_configured": mode in ("test", "live", "live_gated"),
        "stripe_library_installed": _stripe() is not None,
        "live_charges_enabled": mode == "live",
        "wst_available": _wst_available(),
        "note": _NOTES[mode],
    }


@router.post("/create-session")
async def create_checkout_session(session: CheckoutSession):
    mode = _mode()

    # Pay from the virtual WST balance (Capital Fund) — always available, no real money.
    if session.payment_method == "wst_balance":
        bal = _wst_available()
        ok = bal is not None and bal >= session.price_wst
        return {"mode": "wst_ledger", "status": "settled" if ok else "insufficient",
                "wst_available": bal, "price_wst": session.price_wst, "currency": "WST (virtual)"}

    if mode == "live_gated":
        raise HTTPException(status_code=403,
            detail="A live Stripe key is present but live charges are disabled. "
                   "Set STRIPE_LIVE_ENABLED=true to enable real charges.")

    if mode in ("test", "live"):
        s = _stripe()
        if s is None:
            return {"mode": f"stripe_{mode}", "status": "unavailable",
                    "error": "stripe library not installed — run: pip install stripe"}
        try:
            cs = s.checkout.Session.create(
                mode="payment",
                line_items=[{"price_data": {"currency": "gbp",
                    "product_data": {"name": session.item_id},
                    "unit_amount": int(max(session.amount_gbp, 0) * 100)}, "quantity": 1}],
                success_url="https://workstation.ai/checkout/success",
                cancel_url="https://workstation.ai/checkout/cancel",
            )
            return {"mode": f"stripe_{mode}", "status": "session_created",
                    "session_id": cs.get("id"), "payment_url": cs.get("url")}
        except Exception as e:
            return {"mode": f"stripe_{mode}", "status": "error", "error": str(e)[:160]}

    # simulation
    return {"mode": "simulation", "status": "simulated_session",
            "tx_ref": f"SIM-{uuid.uuid4().hex[:8].upper()}", "payment_url": None,
            "note": "Simulated — set a Stripe test key (sk_test_…) for real test sessions. No real money."}


@router.get("/wallet/{user_id}")
async def get_wallet(user_id: str):
    """Honest wallet — WST from the real Capital Fund; payment mode reported truthfully."""
    mode = _mode()
    return {
        "user_id": user_id,
        "wst_available": _wst_available(),   # real (None if unavailable) — never fabricated
        "currency": "WST (virtual)",
        "payment_mode": mode,
        "stripe_configured": mode in ("test", "live", "live_gated"),
    }


@router.get("/wallet/{user_id}/v2")
async def get_wallet_v2(user_id: str):
    """Back-compat alias for the prior wallet path."""
    return await get_wallet(user_id)


@router.post("/payout")
async def request_payout(user_id: str, amount: float):
    mode = _mode()
    if mode != "live":
        return {"status": "simulated", "mode": mode, "user_id": user_id, "amount": amount,
                "note": "Payout simulated — real payouts require a live Stripe key + STRIPE_LIVE_ENABLED=true."}
    # Even in live mode we do NOT auto-execute a real payout: that needs Stripe
    # Connect setup and an explicit Owner action. We return a prepared intent only.
    return {"status": "prepared", "mode": "live", "user_id": user_id, "amount": amount,
            "note": "Live payout prepared — execution requires Stripe Connect configuration by the Owner."}
