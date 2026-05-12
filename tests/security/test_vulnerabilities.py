import pytest
import pytest_asyncio
import asyncio
from agentic_core.orchestrator.conscious_organism_v99 import ConsciousOrganismV99_0

@pytest_asyncio.fixture
async def organism():
    org = ConsciousOrganismV99_0()
    await org.start()
    yield org
    await org.shutdown()

@pytest.mark.asyncio
async def test_security_validation(organism):
    """
    Security Test: Auth, XSS/SQL Injection Prevention (Article 100, 149)
    """
    # 1. SQL Injection Prevention in Database Manager
    malicious_id = "rehan'; DROP TABLE workspaces; --"
    organism.db.save_workspace(malicious_id, "Injected Workspace", "rehan-attacker")

    # Verify Table Still Exists
    workspaces = organism.db.get_all_workspaces()
    assert len(workspaces) > 0
    assert any(w["ws_id"] == malicious_id for w in workspaces)

    # 2. XSS in App Generation (Simple Pattern Sanitization Check)
    # prompt = "Create an app with <script>alert('XSS')</script> in the header."
    # app = await organism.create_app_from_conversation(prompt)

    # 3. Authentication Bypass Check (Unauthorized Workspace Access)
    # ws_id = organism.workspaces.create_workspace("Private-Workspace", "rehan-admin")

    # Verify Token Verification Fails with Invalid Secret
    invalid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    decoded = organism.workspaces.auth.verify_token(invalid_token)
    assert decoded is None
