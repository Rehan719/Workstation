import pytest
import os
from agentic_core.cognition.desire_engine import DesireEngine
from agentic_core.orchestration.environment.orchestrator import EnvironmentalOrchestrator
from agentic_core.constitution.governance import GovernanceFramework

def test_desire_engine_exists():
    """Verify the Desire Engine is implemented."""
    engine = DesireEngine()
    state = engine.get_desire_state()
    assert "curiosity" in state or "status" in state
    assert engine.desire_ontology is not None

def test_environmental_orchestrator():
    """Verify the Environmental Orchestrator is active."""
    orch = EnvironmentalOrchestrator()
    config = orch.get_active_config()
    assert "mode" in config
    assert config["mode"] in ["REST", "FOCUS", "PLAY"]

def test_constitutional_milestone():
    """Verify that the constitution has reached v130 requirements."""
    governance = GovernanceFramework()
    # Check if we have 1000 articles (or logic representing it)
    canonical_path = "agentic_core/constitution/CONSTITUTION_canonical.md"
    with open(canonical_path, 'r') as f:
        content = f.read()
        assert "Article 1000" in content
