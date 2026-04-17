import torch
import pytest
import numpy as np
from agentic_core.biomimicry.minimisation.core.schrodinger_bridge import SchrödingerBridgeEngine
from agentic_core.biomimicry.minimisation.core.optimal_transport import OptimalTransportRouter
from agentic_core.biomimicry.minimisation.core.omega_functional import MinimisationObjective

def test_schrodinger_bridge_convergence():
    engine = SchrödingerBridgeEngine()

    # 1D distributions
    source = torch.tensor([0.5, 0.5])
    target = torch.tensor([0.2, 0.8])
    cost = torch.tensor([[0.0, 1.0], [1.0, 0.0]])

    plan, kl, info = engine.compute_bridge(source, target, cost, epsilon=0.1)

    assert info["converged"]
    assert plan.shape == (2, 2)
    # Check marginals
    assert torch.allclose(plan.sum(dim=1), source, atol=1e-5)
    assert torch.allclose(plan.sum(dim=0), target, atol=1e-5)

def test_optimal_transport_router():
    router = OptimalTransportRouter(epsilon=0.1, max_iter=2000, tol=1e-4)

    source = torch.tensor([1.0, 1.0])
    target = torch.tensor([1.0, 1.0])
    cost = torch.tensor([[0.1, 0.9], [0.8, 0.2]])

    plan, dist, info = router.solve(source, target, cost)

    assert info["converged"]
    # Should favour [0,0] and [1,1]
    assert plan[0, 0] > plan[0, 1]
    assert plan[1, 1] > plan[1, 0]

def test_omega_functional_legal_constraint():
    obj = MinimisationObjective()

    # Legal domain, non-compliant
    context_legal = {"domain": "legal", "layer": "L12_Policy"}
    metrics = {"free_energy": 0.1, "optimal_transport": 0.1}

    score = obj.evaluate(metrics, context_legal, legal_compliance=0.9)
    assert score == float('inf')

    # Legal domain, compliant
    score = obj.evaluate(metrics, context_legal, legal_compliance=1.0)
    assert score < float('inf')
    assert score > 0

    # Non-legal domain, partial compliance penalty
    context_general = {"domain": "general"}
    score_penalty = obj.evaluate(metrics, context_general, legal_compliance=0.5)
    score_no_penalty = obj.evaluate(metrics, context_general, legal_compliance=1.0)
    assert score_penalty > score_no_penalty
