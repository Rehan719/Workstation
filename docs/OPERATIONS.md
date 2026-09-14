# Operational Manual

> **Historical (Jules-era) fragment — not a description of the running system.** None of the three mechanisms it listed exists at HEAD: nothing monitors a mesh for treaty violations (the Council Judiciary's AI Judge rules on disputes filed through `POST /api/council/judge/disputes`, plus two it seeds at startup); `products/capital_fund/treasury/defi_yield_aggregator.py` (`TreasuryYieldManager`) is imported by nothing and `defi_yield_aggregator_enabled` is `false` — the economy is virtual WST only and nothing is placed in any external protocol; no `RECOVERY_REQUEST` message exists (the Gossipsub references are log-only stubs).

For current operations see [DEPLOYMENT.md](DEPLOYMENT.md). For economy governance see [VSB_ECONOMIC_LEGAL_MODEL.md](VSB_ECONOMIC_LEGAL_MODEL.md) §8 (Change Control for material financial actions); the materiality threshold is `ECONOMY_MATERIALITY_WST` (default 250,000 virtual WST) in `agentic_core/economy/governance.py`.
