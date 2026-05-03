import os
import json
import logging
import time
from typing import Dict, Any, Optional, List
from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)

class CredentialVault:
    """
    ARTICLE 1035: Credential Vault Mandate.
    Hardened storage with Fernet encryption.
    """
    def __init__(self, vault_path: str = "agentic_core/governance/credentials/vault.json",
                 key_path: str = "agentic_core/governance/credentials/master.key"):
        self.vault_path = vault_path
        self.key_path = key_path
        self._initialize_vault()

    def _initialize_vault(self):
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
        if not os.path.exists(self.vault_path): return {}
        with open(self.vault_path, "rb") as f:
            encrypted_data = f.read()
        if not encrypted_data: return {}
        try:
            decrypted_data = self.fernet.decrypt(encrypted_data)
            return json.loads(decrypted_data.decode())
        except Exception:
            return {}

    def store_secret(self, key: str, value: str, owner: str):
        vault = self._load_vault()
        vault[key] = {"value": value, "owner": owner, "created_at": time.time()}
        self._save_vault(vault)

    def get_secret(self, key: str) -> Optional[str]:
        vault = self._load_vault()
        return vault.get(key, {}).get("value")
