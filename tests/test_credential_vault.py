import os
import pytest
from agentic_core.governance.credentials.vault import CredentialVault

def test_credential_vault_hybrid_storage():
    vault_path = "tests/temp_vault.json"
    key_path = "tests/temp_master.key"

    # Cleanup pre-existing
    if os.path.exists(vault_path): os.remove(vault_path)
    if os.path.exists(key_path): os.remove(key_path)

    # Pass key path to constructor if possible, or ensure it's set before init
    # Since CredentialVault.__init__ calls _initialize_vault, we should be careful.

    # Use explicit paths in test
    vault = CredentialVault(vault_path, key_path)

    # 1. Store secret with metadata and sync
    vault.store_secret(
        key="TEST_KEY",
        value="secret_123",
        owner="entity@workstation",
        environment="production",
        purpose="sovereign",
        sync_to=["github"]
    )

    # 2. Retrieve secret
    val = vault.get_secret("TEST_KEY", "jules")
    assert val == "secret_123"

    # 3. Check metadata (excluding value)
    meta = vault._load_vault()["TEST_KEY"]["metadata"]
    assert meta["owner"] == "entity@workstation"
    assert meta["environment"] == "production"
    assert "github" in meta["external_sync"]
    assert meta["constitutional_floor"] == "Article_1035"

    # 4. Rotation
    vault.rotate_secret("TEST_KEY")
    new_val = vault.get_secret("TEST_KEY", "jules")
    assert new_val != "secret_123"
    assert "rotated_value_" in new_val

    # Cleanup
    if os.path.exists(vault_path): os.remove(vault_path)
    if os.path.exists(key_path): os.remove(key_path)
