import pytest
import pytest_asyncio
import asyncio
from agentic_core.orchestrator.conscious_organism_v99 import ConsciousOrganismV99_0

@pytest_asyncio.fixture
async def organism():
    org = ConsciousOrganismV99_0(agent_id="test-agent")
    await org.start()
    yield org
    await org.shutdown()

@pytest.mark.asyncio
async def test_full_platform_workflow(organism):
    """
    Integration Test: Conversational Builder -> App Generation -> Deployment
    (Article 145/148)
    """
    # 1. Simulate Conversation for App Creation
    prompt = "Create a scientific research dashboard for tracking p53 protein kinetics."
    app = await organism.create_app_from_conversation(prompt)

    assert app.status == "compiled"
    assert "p53" in app.frontend_code
    assert app.app_id is not None

    # 2. Deploy the App to Environment
    target_env = "aws-production-99"
    deploy_res = await organism.deploy_app(app.app_id, target_env)

    # SIH check: if ATP is low, this will fail (handled in ConsciousOrganism)
    if deploy_res["status"] == "success":
        assert deploy_res["url"] is not None
        assert deploy_res["environment"] == target_env
    else:
        assert deploy_res["reason"] == "SIH_PREEMPTION"

@pytest.mark.asyncio
async def test_auth_and_workspace_rbac(organism):
    """
    Integration Test: Workspace creation -> RBAC Enforcement (Article 149)
    """
    ws_id = organism.workspaces.create_workspace("Test-Workspace", "rehan-admin")
    assert ws_id is not None

    # Create Admin Token
    token = organism.workspaces.auth.create_token("rehan-admin", ws_id, "admin")
    decoded = organism.workspaces.auth.verify_token(token)
    assert decoded["user_id"] == "rehan-admin"
    assert decoded["role"] == "admin"

    # Add Member
    organism.workspaces.add_member(ws_id, "dev-user", "developer")
    role = organism.workspaces.get_role(ws_id, "dev-user")
    assert role == "developer"
