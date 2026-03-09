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
    # ARTICLE 246: Human-in-the-loop veto enforcement.
    commander = AICommander()

    # Intent that triggers the FinancialResolver (which requires 'riba-free')
    intent = {
        "action": "distribute_profits",
        "scope": "financial:investment",
        "compliance": ["standard"] # Missing 'riba-free'
    }

    # This should be rejected by the resolver
    allowed = await commander.execute_intent(intent)
    assert allowed is False

    # Corrected intent
    valid_intent = {
        "action": "distribute_profits",
        "scope": "financial:investment",
        "compliance": ["riba-free"]
    }
    allowed_valid = await commander.execute_intent(valid_intent)
    assert allowed_valid is True

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
async def test_evolved_prompt_compiler_dna():
    # ARTICLE 167: Genotype-to-Phenotype mapping.
    compiler = BiologicalCompiler()

    res = compiler.compile("Quranic Study App")

    assert "dna_hash" in res
    assert len(res["parts"]) > 0
    # Phenotype verification: Ensure essential parts are selected
    part_names = [p["name"] for p in res["parts"]]
    assert "auth_module" in part_names

def test_pwa_icon_integrity():
    # Scenario 10.6: Accessibility check
    public_dir = "src/qep_frontend/public"
    icons = ["pwa-192x192.png", "pwa-512x512.png", "pwa-64x64.png"]

    for icon in icons:
        path = os.path.join(public_dir, icon)
        assert os.path.exists(path), f"Icon {icon} missing"
        assert os.path.getsize(path) > 0, f"Icon {icon} is empty"
