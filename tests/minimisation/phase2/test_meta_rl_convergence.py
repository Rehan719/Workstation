import pytest
import torch
from agentic_core.minimisation.recirculation.meta_rl_tuner import MetaRLTuner

def test_meta_rl_tuner_convergence():
    tuner = MetaRLTuner(learning_rate=0.1)

    initial_weights = tuner.get_weights()

    # Run 5 cycles with positive reward
    for _ in range(5):
        tuner.update(reward=1.0, entropy_reduction=0.20)

    final_weights = tuner.get_weights()

    # Weights should have shifted significantly
    # Sum of absolute differences
    diff = sum(abs(initial_weights[k] - final_weights[k]) for k in initial_weights)
    assert diff > 0.05
    assert sum(final_weights.values()) == pytest.approx(1.0)
