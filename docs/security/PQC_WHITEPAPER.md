# Workstation Security Whitepaper: Post-Quantum Cryptography (v146.0)

## Executive Summary
The Workstation federation has transitioned to a mandatory Post-Quantum Cryptographic (PQC) security model as of version 146.0. All classical cryptographic fallbacks (RSA, ECC) are now disabled, making the ecosystem quantum-safe by default. This transition protects the global digital civilization against the threat of future quantum computers capable of breaking current encryption standards.

## 1. Cryptographic Standards
The federation utilizes the NIST-standardized CRYSTALS (Cryptographic Suite for Algebraic Lattices) algorithms:

- **Key Encapsulation Mechanism (KEM)**: CRYSTALS-Kyber (Kyber768). Used for establishing shared secrets between nodes and between clients and servers.
- **Digital Signatures**: CRYSTALS-Dilithium (Dilithium3). Used for signing all instructions, code deployments, and transactions within the Merkle-DAG audit trail.

## 2. PQC-Mandatory Enforcement
- **Node Discovery**: Handshakes between nodes in the libp2p DHT now require Kyber-based key exchange.
- **API Communication**: The `v260` API and beyond enforce Kyber-encrypted sessions.
- **BTO Deployment**: All BTO product reactors must be signed with Dilithium to be accepted by the federation.
- **Zero Fallback**: Attempting to initiate a session using classical RSA or ECC will result in an immediate connection termination by the Homeostatic OS.

## 3. Governance and Compliance
This security model aligns with **Article 1089** (OWASP ASI Compliance) and **Article 1095** (Civilizational Scale Validation). It ensures that the Workstation's sovereign data remains private and its operations remain untampered even in the post-quantum era.

## 4. Implementation Details
The `agentic_core/crypto/pqc.py` module serves as the central enforcement point. It monitors environment variables and system state to ensure that `PQC_MANDATORY` mode is active at all times.

---
*Authorized by the VSB AI CEO & Sovereign Security Council.*
