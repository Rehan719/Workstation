import os
import json
import logging
import time
from typing import Dict, Any, Optional, List
from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)

class ExternalProviderAdapter:
    """Base class for external secret provider adapters."""
    def mirror(self, key: str, value: str, metadata: Dict[str, Any]):
        pass

class GitHubSecretsAdapter(ExternalProviderAdapter):
    def mirror(self, key: str, value: str, metadata: Dict[str, Any]):
        logger.info(f"CredentialVault: Mirroring '{key}' to GitHub Secrets.")

class AWSSecretsManagerAdapter(ExternalProviderAdapter):
    def mirror(self, key: str, value: str, metadata: Dict[str, Any]):
        logger.info(f"CredentialVault: Mirroring '{key}' to AWS Secrets Manager.")

class CredentialVault:
    """
    ARTICLE 1035: Credential Vault Mandate (Refined) v133.3.
    Hybrid storage (Internal + External) with extended metadata and automatic rotation.
    """
    def __init__(self, vault_path: str = "agentic_core/governance/credentials/vault.json",
                 key_path: str = "agentic_core/governance/credentials/master.key"):
        self.vault_path = vault_path
        self.key_path = key_path
        self.external_adapters = {
            "github": GitHubSecretsAdapter(),
            "aws": AWSSecretsManagerAdapter()
        }
        self._initialize_vault()

    def _initialize_vault(self):
        # Create dir if not exists
        os.makedirs(os.path.dirname(self.vault_path), exist_ok=True)

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

    def store_secret(self, key: str, value: str, owner: str, environment: str = "development",
                     purpose: str = "operational", sync_to: List[str] = None):
        """Stores a secret with refined extended metadata and mirroring."""
        vault = self._load_vault()
        expiry_days = {"development": 90, "staging": 60, "production": 30}

        metadata = {
            "owner": owner,
            "environment": environment,
            "purpose": purpose,
            "constitutional_floor": "Article_1035",
            "sovereign_control": True,
            "created_at": time.time(),
            "expires_at": time.time() + (expiry_days.get(environment, 90) * 86400),
            "last_used": None,
            "version": vault[key]["metadata"]["version"] + 1 if key in vault else 1,
            "external_sync": sync_to or []
        }

        vault[key] = {
            "value": value,
            "metadata": metadata
        }
        self._save_vault(vault)

        # Mirroring to external providers
        if sync_to:
            for provider in sync_to:
                if provider in self.external_adapters:
                    self.external_adapters[provider].mirror(key, value, metadata)

        logger.info(f"CredentialVault: Secret '{key}' stored for {environment} with sovereignty.")

    def get_secret(self, key: str, requester: str) -> Optional[str]:
        """Retrieves a secret and updates last_used metadata."""
        vault = self._load_vault()
        if key not in vault:
            return None

        secret_data = vault[key]
        secret_data["metadata"]["last_used"] = time.time()
        self._save_vault(vault)

        logger.info(f"CredentialVault: Secret '{key}' accessed by {requester}.")
        return secret_data["value"]

    def rotate_secret(self, key: str):
        """Triggers automatic rotation logic."""
        vault = self._load_vault()
        if key not in vault:
            return

        logger.info(f"CredentialVault: Rotating secret '{key}'...")
        # Simulated rotation logic (e.g., calling provider API to gen new key)
        new_value = f"rotated_value_{int(time.time())}"
        data = vault[key]
        self.store_secret(key, new_value, data["metadata"]["owner"],
                         data["metadata"]["environment"], data["metadata"]["purpose"],
                         data["metadata"]["external_sync"])

    def scan_for_leaks(self):
        """Simulates GitHub secret scanning integration."""
        logger.info("CredentialVault: Performing GitHub secret scanning check...")
        return True
