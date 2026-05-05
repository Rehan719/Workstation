import hashlib
import json
import logging
import time
import os
from typing import Dict, Any, Optional
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import serialization

logger = logging.getLogger(__name__)

class SovereignIdentity:
    """
    ARTICLE 1051: Sovereign Identity Layer.
    Implements Self-Sovereign Digital Identity (SSDI) with PQC preparedness.
    """
    def __init__(self, key_path: str = "data/organism/sovereign_key.pem"):
        self.key_path = key_path
        self._private_key: Optional[rsa.RSAPrivateKey] = None
        self._public_key: Optional[rsa.RSAPublicKey] = None
        self.did = f"did:sovereign:{self._generate_did_suffix()}"
        self._load_or_generate_key()

    def _generate_did_suffix(self) -> str:
        return hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]

    def _load_or_generate_key(self):
        if os.path.exists(self.key_path):
            try:
                with open(self.key_path, "rb") as f:
                    self._private_key = serialization.load_pem_private_key(
                        f.read(),
                        password=None
                    )
                self._public_key = self._private_key.public_key()
                logger.info("SovereignIdentity: Loaded existing cryptographic identity.")
            except Exception as e:
                logger.error(f"SovereignIdentity: Key load failure: {e}")
                self._generate_new_key()
        else:
            self._generate_new_key()

    def _generate_new_key(self):
        logger.info("SovereignIdentity: Generating new cryptographic identity...")
        os.makedirs(os.path.dirname(self.key_path), exist_ok=True)
        self._private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self._public_key = self._private_key.public_key()
        try:
            pem = self._private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            with open(self.key_path, "wb") as f:
                f.write(pem)
            logger.info(f"SovereignIdentity: New key saved to {self.key_path}")
        except Exception as e:
            logger.error(f"SovereignIdentity: Key save failure: {e}")

    def sign_action(self, action_data: Dict[str, Any]) -> str:
        if not self._private_key:
            raise RuntimeError("SovereignIdentity: Private key not loaded.")
        payload = json.dumps(action_data, sort_keys=True).encode()
        signature = self._private_key.sign(
            payload,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature.hex()

    def verify_action(self, action_data: Dict[str, Any], signature_hex: str) -> bool:
        if not self._public_key:
            return False
        payload = json.dumps(action_data, sort_keys=True).encode()
        try:
            self._public_key.verify(
                bytes.fromhex(signature_hex),
                payload,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False

    def get_public_key_pem(self) -> str:
        if not self._public_key:
            raise RuntimeError("SovereignIdentity: Public key not loaded.")
        pem = self._public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return pem.decode()

    def get_did_document(self) -> Dict[str, Any]:
        """Returns the SSDI DID Document for the organism."""
        return {
            "@context": "https://www.w3.org/ns/did/v1",
            "id": self.did,
            "verificationMethod": [{
                "id": f"{self.did}#key-1",
                "type": "RsaVerificationKey2018",
                "controller": self.did,
                "publicKeyPem": self.get_public_key_pem()
            }],
            "authentication": [f"{self.did}#key-1"],
            "assertionMethod": [f"{self.did}#key-1"],
            "service": [{
                "id": f"{self.did}#neural-bus",
                "type": "NeuralBusService",
                "serviceEndpoint": "ws://localhost:8000/ws/organism/neural-bus"
            }]
        }

class SovereignAuditLog:
    def __init__(self, log_path: str = "data/organism/activity.jsonl"):
        self.log_path = log_path
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        self._last_hash = "0" * 64
        self._load_last_hash()

    def _load_last_hash(self):
        if os.path.exists(self.log_path) and os.path.getsize(self.log_path) > 0:
            try:
                with open(self.log_path, "rb") as f:
                    f.seek(-2, os.SEEK_END)
                    while f.tell() > 0 and f.read(1) != b"\n":
                        f.seek(-2, os.SEEK_CUR)
                    last_line = f.readline().decode()
                    last_entry = json.loads(last_line)
                    self._last_hash = last_entry.get("hash", "0" * 64)
            except (OSError, json.JSONDecodeError, ValueError):
                pass

    def log_entry(self, entry: Dict[str, Any]):
        entry["prev_hash"] = self._last_hash
        entry["timestamp"] = time.time()
        entry_str = json.dumps(entry, sort_keys=True).encode()
        current_hash = hashlib.sha256(entry_str).hexdigest()
        entry["hash"] = current_hash
        self._last_hash = current_hash
        with open(self.log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")
        logger.info(f"AuditLog: Action {entry.get('id', 'unknown')} logged to ledger.")
