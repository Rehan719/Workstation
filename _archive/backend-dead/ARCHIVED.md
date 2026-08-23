# Dead backend modules — ARCHIVED (W331 cleanup, 2026-08-23)

- `tier_manager.py` (was `agentic_core/commercial/tier_manager.py`): imports
  `from backend.stripe.tiered_subscriptions import TIER_CONFIG`, but no `backend/` package has
  ever existed in this repo — the module was unimportable, with zero importers anywhere.
  Archived per the W314 precedent for the fabricated/broken payment-code class.

The platform's ONE real payment path is `agentic_core/api/v310/payments.py` (simulation by
default; live charging triple-gated behind REAL_MONEY_ENABLED=True in code — currently False).
