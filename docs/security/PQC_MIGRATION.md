# v143.0 Post-Quantum Cryptography Migration Plan

## 1. Objective
Ensure the Workstation federation is resilient against quantum-scale computing threats by migrating from classical (ECC/RSA) to NIST-standardized PQC algorithms.

## 2. Technical Stack
- **Key Exchange**: CRYSTALS-Kyber (Kyber-768)
- **Digital Signatures**: CRYSTALS-Dilithium (Dilithium-3)
- **Wrapper**: `liboqs` via `liboqs-python`

## 3. Migration Roadmap
- **Phase 1 (v143.0)**: Dual-stack mode. All DIDs are generated with both classical and PQC keys.
- **Phase 2 (v144.0)**: PQC-MANDATORY for all production connections. No classical fallback.
- **Phase 3 (v145.0)**: Full hardware-level PQC enforcement in the UEG.

## 4. Implementation Status
- [x] v240 PQC Mandatory API
- [x] Classical Fallback Disabled
- [ ] Mobile PQC bridge (CryptoKit/Conscrypt)
