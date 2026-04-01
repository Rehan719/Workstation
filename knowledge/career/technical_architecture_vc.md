# Technical Architecture: Verifiable Credentials & Decentralized Identity (DID)

## 1. Decentralized Identifier (DID) Framework
- **Mechanism:** The Workstation acts as a non-custodial wallet for the applicant's self-sovereign identity.
- **DID Specification:** `did:key` or `did:web` (depending on deployment target).
- **Function:** Serves as the persistent, globally unique identifier for professional attestations.

## 2. Verifiable Credentials (VC) Integration
- **Data Model:** W3C Verifiable Credentials Data Model v2.0.
- **Issuer Protocol:** Integration with Credly/Open Badges for automated ingestion.
- **Verification Logic:**
    - Recruiter clicks "Verify" on LinkedIn.
    - API call to Workstation's verification endpoint.
    - Workstation verifies the cryptographic signature (JOSE/COSE) against the known public keys.
    - Result: "Verified Fact: 15+ years scientific experience, hash: [8a7b6c...]"

## 3. Cryptographic Provenance (Audit Trail)
- **Hash-Chaining:** Every VC is anchored to a timestamped entry in the `SovereignAuditLog`.
- **Blockchain Anchoring:** Hashes of critical transformation batches are anchored to public ledgers (e.g., Bitcoin/Ethereum via OpenTimestamps) to prevent retroactive tampering.

## 4. Workstation Workflow
1.  **Ingest:** Skills City certification received via Credly API.
2.  **Attest:** Career Agent signs the credential metadata with the user's DID private key.
3.  **Deploy:** Metadata updated on LinkedIn via Verified API or manual "Featured" link with embedded verification hash.
