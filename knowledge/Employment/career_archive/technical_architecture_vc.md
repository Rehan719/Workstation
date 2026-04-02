# 🛡️ Technical Architecture: Verifiable Credentials (VCs) & DIDs
## *Decentralized Identity Framework for Sovereign Career Management*

**Version**: 1.0
**Standard**: W3C Verifiable Credentials Data Model v2.0
**Integration**: Workstation Sovereign Audit Log

---

## 1. Overview
This architecture enables the Workstation to issue, hold, and verify professional credentials using W3C standards. It links career achievements (e.g., "Led GMP Audit") to cryptographic proofs stored in the `SovereignAuditLog`, creating a tamper-evident professional identity.

## 2. Core Components

### 2.1 Decentralized Identifiers (DIDs)
- **Standard**: W3C DID Core 1.0
- **Method**: `did:key` (for local self-sovereign identity) or `did:web` (for domain-linked identity).
- **Function**: Provides a persistent, cryptographic identifier for the User independent of any centralized platform (e.g., LinkedIn).
- **Implementation**:
  ```json
  {
    "@context": ["https://www.w3.org/ns/did/v1"],
    "id": "did:key:z6MkhaXgBZDvotDkWL5Tn...",
    "verificationMethod": [{
      "id": "did:key:z6MkhaXgBZDvotDkWL5Tn...#z6MkhaXgBZDvotDkWL5Tn...",
      "type": "Ed25519VerificationKey2018",
      "controller": "did:key:z6MkhaXgBZDvotDkWL5Tn...",
      "publicKeyMultibase": "z6MkhaXgBZDvotDkWL5Tn..."
    }]
  }
  ```

### 2.2 Verifiable Credentials (VCs)
- **Standard**: W3C VC Data Model v2.0
- **Structure**: JSON-LD formatted claims signed by an Issuer (e.g., University, Employer, or Self-Attested via Workstation).
- **Linkage**: Each VC includes a `credentialSubject.id` matching the User's DID and a `proof` section containing the cryptographic signature.
- **Audit Link**: A custom field `workstationAuditHash` links the VC to the specific entry in the `SovereignAuditLog`.

### 2.3 Cryptographic Signing (JOSE/COSE)
- **Standard**: RFC 7515 (JOSE) or RFC 9052 (COSE)
- **Algorithm**: EdDSA (Ed25519) for high security and small key sizes.
- **Purpose**: Ensures integrity and non-repudiation of the credential data.

## 3. Integration Workflow

1.  **Event Trigger**: User completes a project (logged in `Master Career Graph`).
2.  **VC Issuance**: Workstation generates a VC claiming the skill/achievement.
3.  **Signing**: VC is signed using the User's private key (stored in local secure enclave).
4.  **Audit Linking**: The VC's hash is appended to the `SovereignAuditLog`.
5.  **Presentation**: User presents the VC to LinkedIn (via "Featured" link) or a verifier.

## 4. Security Considerations
- **Private Key Storage**: Keys must never leave the local Workstation environment unencrypted.
- **Revocation**: Implement a Status List 2021 for revoking compromised credentials.
- **Privacy**: Use selective disclosure to reveal only necessary claims (e.g., prove "GMP Certified" without revealing specific project details).
