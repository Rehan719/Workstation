# WST Tokenisation & Migration Path

## Overview
The Workstation Token (WST) is the primary economic unit of the Jules AI ecosystem. In v120.0, it is implemented as a cryptographically signed database ledger to ensure zero-cost infrastructure compliance while providing absolute non-repudiation.

## Current Infrastructure (v120.0)
- **Engine**: Ed25519 Cryptographic Signatures.
- **Verification**: Merkle-Tree hashing of transaction chains.
- **Storage**: SQL-backed signed ledger.

## Migration Path to Public Blockchain
The system is designed for a seamless "Airdrop & Swap" migration to a public chain (e.g., Polygon, Ethereum L2):

1. **Snapshot Phase**: The `TokenLedger` Merkle root is anchored to a public chain via a state proof.
2. **Smart Contract Deployment**: An ERC-20 (or similar) contract is deployed with the same supply cap.
3. **Bridge/Claim**: Users use their v120.0 public keys to claim native tokens on the destination chain.
4. **Symbiosis**: The `token_ledger.py` is updated with a Web3 provider to verify balances on-chain.

## Non-Repudiation
Every transaction in the current ledger is signed by the System Mint. Any tampering with the transaction history will invalidate the Merkle-tree chain, ensuring 100% auditability before the migration.
