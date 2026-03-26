import pytest
from agentic_core.security.pqc_hardening import pqc_hardener
from agentic_core.homeostasis.resilience import resilience_manager

def test_pqc_jwt_enforcement():
    payload = {"user": "jules", "role": "CEO"}
    token = pqc_hardener.generate_token(payload)
    assert token is not None

    decoded = pqc_hardener.verify_token(token)
    assert decoded["user"] == "jules"
    assert decoded["pqc_verified"] is True

def test_resilience_prediction():
    metrics = {
        "latency": 500,
        "error_rate": 0.1,
        "memory": 8000,
        "gaas_failures": 2,
        "ws_stability": 0.7,
        "cpu": 85
    }
    result = resilience_manager.update_metrics(metrics)
    assert "failure_probability" in result
    assert result["status"] in ["STABLE", "HEALING"]

def test_resilience_training():
    # Seed data
    for _ in range(20):
        resilience_manager.update_metrics({"latency": random.uniform(10, 100)})

    result = resilience_manager.train_model()
    assert result["status"] == "TRAINING_COMPLETE"
    assert result["samples"] >= 20

import random
