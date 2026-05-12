import pytest
import os
from agentic_core.governance.credentials.vault_v137 import SecureCredentialVaultV137

def test_v137_vault_operations():
    test_path = "tests/test_vault_v137.json"
    if os.path.exists(test_path): os.remove(test_path)

    vault = SecureCredentialVaultV137(storage_path=test_path)
    meta = {
        "purpose": "operational",
        "constitutional_floor": "Article_1094",
        "rotation_schedule": "30d",
        "owner": "did:key:jules"
    }

    # Store
    vault.store_credential("OPENAI_API_KEY", "sk-12345", meta)
    assert vault.get_credential("OPENAI_API_KEY") == "sk-12345"

    # Metadata check
    stored_meta = vault.get_metadata("OPENAI_API_KEY")
    assert stored_meta["owner"] == "did:key:jules"
    assert "last_rotated" in stored_meta

    # Rotate
    vault.rotate_credential("OPENAI_API_KEY")
    new_val = vault.get_credential("OPENAI_API_KEY")
    assert new_val.startswith("rotated_key_")
    assert vault.get_metadata("OPENAI_API_KEY")["rotation_count"] == 1

    if os.path.exists(test_path): os.remove(test_path)
