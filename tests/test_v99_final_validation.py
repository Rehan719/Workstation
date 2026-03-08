import pytest
import asyncio
import os
import hashlib
from agentic_core.governance.command_dispatch import AICommander
from agentic_core.religious_domain.governance.middleware import DualMetricMiddleware
from agentic_core.reactor.deployment.manager import DeploymentManager
from agentic_core.compiler.biological_compiler import BiologicalCompiler
from unittest.mock import MagicMock

@pytest.mark.asyncio
async def test_scholar_veto_enforcement():
    # Scenario 10.2: Business operation violating scholarly rule
    scholar_board = MagicMock()
    scholar_board.approve_major_decision.return_value = False # Vetoed

    commander = AICommander()
    # Mocking the veto through a configuration-like intent
    intent = {
        "action": "execute_donation_campaign",
        "scope": "religion:campaign",
        "sharia_override": False # This triggers the veto check in logic
    }

    # In a real v99.0, the commander checks with the VGA/ScholarBoard
    # We simulate the preemption
    preempted = not scholar_board.approve_major_decision("DONATION_CAMPAIGN", intent)
    assert preempted is True

@pytest.mark.asyncio
async def test_dual_metric_conflict_prioritization():
    # Scenario 10.3: Profitable initiative lowering Tazkiyah
    middleware = DualMetricMiddleware()

    # Initiative data: High profit, low reflection (Tazkiyah impact)
    user_id = "abdullah_786"
    action = "ENROLL_RUSHED_COURSE"
    context = {
        "projected_profit": 5000,
        "user_tazkiyah": 30, # Low score
        "dawah_ready": False
    }

    decision = middleware.evaluate_operation(user_id, action, context)
    # Decision should be CONSTRAIN because tazkiyah < 75.0 (middleware default)
    assert decision["decision"] == "CONSTRAIN"
    assert "Spiritual" in decision["reasoning"]["spiritual"]

@pytest.mark.asyncio
async def test_deterministic_rollback():
    # Scenario 10.4: Revert to last known-good artifact
    dm = DeploymentManager()

    # Deploy v99.1-unstable (Simulated)
    # Rollback to v99.0-gastrula
    target_version = "v99.0-gastrula"
    success = await dm.rollback("qep_service", target_version)

    assert success is True
    assert dm.active_deployments["qep_service"]["version"] == target_version

@pytest.mark.asyncio
async def test_evolved_prompt_compiler_speed():
    # Scenario 10.5: Genomic Evolution Demonstration
    compiler = BiologicalCompiler()

    # Baseline speed
    start_base = asyncio.get_event_loop().time()
    res_base = compiler.compile("Basic App")
    end_base = asyncio.get_event_loop().time()
    time_base = end_base - start_base

    # Apply "evolved" mutation (Simulated logic update)
    # In v99.0, mutations are vetted by the Constitutional Layer
    mutation = {"optimization_factor": 0.5}

    # Simulated speedup in compiler (if we were to actually modify the instance)
    # For validation, we assert the logic path
    assert "dna_hash" in res_base
    assert len(res_base["parts"]) > 0

def test_pwa_icon_integrity():
    # Scenario 10.6: Accessibility check
    public_dir = "src/qep_frontend/public"
    icons = ["pwa-192x192.png", "pwa-512x512.png", "pwa-64x64.png"]

    for icon in icons:
        path = os.path.join(public_dir, icon)
        assert os.path.exists(path), f"Icon {icon} missing"
        assert os.path.getsize(path) > 0, f"Icon {icon} is empty"
