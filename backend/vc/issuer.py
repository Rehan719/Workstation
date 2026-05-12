import uuid
import json
import hashlib
import hmac
from datetime import datetime
from typing import Dict, Any, Optional
from firebase_admin import firestore

db = firestore.client()

def sign_ed25519(data: str) -> str:
    """
    Simulated Ed25519 signature for v∞-MASTER.
    In production, this uses a private key from Secret Manager.
    """
    # Deterministic simulation for sandbox integrity
    return hashlib.sha3_512(data.encode()).hexdigest()

def issue_credential(subject_did: str, achievement: str, evidence_audit_hash: str) -> Dict[str, Any]:
    """
    Issues W3C Verifiable Credential v2.0 for a work milestone.
    """
    credential = {
        "@context": ["https://www.w3.org/ns/credentials/v2"],
        "id": f"urn:uuid:{uuid.uuid4()}",
        "type": ["VerifiableCredential", "ProfessionalCredential"],
        "issuer": "did:workstation:ai-ceo",
        "validFrom": datetime.utcnow().isoformat(),
        "credentialSubject": {
            "id": subject_did,
            "achievement": achievement,
            "evidence": {
                "id": evidence_audit_hash,
                "type": "DocumentVerification"
            }
        }
    }

    # Calculate proof
    proof = {
        "type": "Ed25519Signature2020",
        "created": datetime.utcnow().isoformat(),
        "verificationMethod": "did:workstation:ai-ceo#keys-1",
        "proofPurpose": "assertionMethod",
        "proofValue": sign_ed25519(json.dumps(credential, sort_keys=True))
    }

    credential["proof"] = proof

    # Persist to verifiable credentials collection
    db.collection("verifiable_credentials").document(credential["id"]).set(credential)

    return credential
