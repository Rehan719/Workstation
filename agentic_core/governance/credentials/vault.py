import os
import json
import logging
import time
from typing import Dict, Any, Optional
from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)

class CredentialVault:
    """
    ARTICLE 1003: Secure Credential Management v131.0.
    Handles encrypted storage of secrets with extended metadata and rotation tracking.
    """
    def __init__(self, vault_path: str = "agentic_core/governance/credentials/vault.json"):
        self.vault_path = vault_path
        self.key_path = "agentic_core/governance/credentials/master.key"
        self._initialize_vault()

    def _initialize_vault(self):
        if not os.path.exists(self.key_path):
            key = Fernet.generate_key()
            with open(self.key_path, "wb") as f:
                f.write(key)

        with open(self.key_path, "rb") as f:
            self.fernet = Fernet(f.read())

        if not os.path.exists(self.vault_path):
            self._save_vault({})

    def _save_vault(self, data: Dict[str, Any]):
        encrypted_data = self.fernet.encrypt(json.dumps(data).encode())
        with open(self.vault_path, "wb") as f:
            f.write(encrypted_data)

    def _load_vault(self) -> Dict[str, Any]:
        if not os.path.exists(self.vault_path):
            return {}
        with open(self.vault_path, "rb") as f:
            encrypted_data = f.read()
        if not encrypted_data:
            return {}
        decrypted_data = self.fernet.decrypt(encrypted_data)
        return json.loads(decrypted_data.decode())

    def store_secret(self, key: str, value: str, owner: str, environment: str = "development"):
        """Stores a secret with extended metadata."""
        vault = self._load_vault()
        expiry_days = {"development": 90, "staging": 60, "production": 30}

        vault[key] = {
            "value": value,
            "metadata": {
                "owner": owner,
                "environment": environment,
                "created_at": time.time(),
                "expires_at": time.time() + (expiry_days.get(environment, 90) * 86400),
                "last_used": None,
                "version": 1
            }
        }
        self._save_vault(vault)
        logger.info(f"CredentialVault: Secret '{key}' stored for {environment} by {owner}.")

    def get_secret(self, key: str, requester: str) -> Optional[str]:
        """Retrieves a secret and updates last_used metadata."""
        vault = self._load_vault()
        if key not in vault:
            logger.warning(f"CredentialVault: Secret '{key}' not found.")
            return None

        secret_data = vault[key]
        # Role-based access logic could be expanded here

        secret_data["metadata"]["last_used"] = time.time()
        self._save_vault(vault)

        logger.info(f"CredentialVault: Secret '{key}' accessed by {requester}.")
        return secret_data["value"]

    def list_metadata(self) -> Dict[str, Any]:
        """Returns metadata for all secrets (excluding values)."""
        vault = self._load_vault()
        metadata_only = {}
        for k, v in vault.items():
            metadata_only[k] = v["metadata"]
        return metadata_only
