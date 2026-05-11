import pytest
from agentic_core.orchestration.clownfish import ClownfishProtocol

def test_clownfish_role_rotation():
    clownfish = ClownfishProtocol("agent-001")
    assert clownfish.roles[clownfish.current_role_index] == "MODEL"

    role2 = clownfish.rotate_role()
    assert role2 == "EDITOR"

    role3 = clownfish.rotate_role()
    assert role3 == "WATCHER"

    role4 = clownfish.rotate_role()
    assert role4 == "MODEL"

def test_clownfish_full_triad():
    clownfish = ClownfishProtocol("agent-002")
    task = {"name": "Refine Constitutional Pacing"}
    result = clownfish.run_full_triad(task)

    assert result["triad_complete"] == True
    assert result["final_output"]["optimized"] == True
    assert result["audit"]["compliance"] == "PASSED"
