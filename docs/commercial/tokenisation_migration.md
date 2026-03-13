# Workstation Token (WST) Blockchain Migration Roadmap

## Overview
This document outlines the migration path from the v120.0 simulated token ledger to a live blockchain implementation (Polygon/ERC-20), satisfying Articles 591-595.

## Phase 1: Simulated Ledger (v120.0 - Current)
- Database-backed tracking in `agentic_core/commercial/token_ledger.py`.
- Monthly allowances and burn-rate simulation.
- REST API integration with Web/Mobile dashboards.

## Phase 2: Hybrid State (Planned)
- Implement Smart Contracts on Polygon Testnet (Amoy).
- Mirror ledger transactions to the blockchain for transparency.
- Establish wallet-linking for Pro/Enterprise users.

## Phase 3: Full Apotheosis (Live)
- Transition all usage metering to smart contract calls.
- Automated billing via stablecoin-to-WST conversion.
- Community rewards distributed directly to user wallets.

## Technical Requirements
- Web3.py integration in the backend.
- MetaMask/WalletConnect support in the Web App.
- Polygon RPC node access.

---
© 2024 Virtual Sovereign Business
