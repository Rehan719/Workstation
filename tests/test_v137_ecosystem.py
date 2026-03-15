import pytest
from agentic_core.governance.production_liability_v137 import ProductionLiabilityFund, FederationScaler

def test_liability_mainnet_deployment():
    fund = ProductionLiabilityFund()
    result = fund.deploy_to_mainnet()
    assert result["status"] == "DEPLOYED"
    assert result["network"] == "polygon-mainnet"
    assert result["contract_address"].startswith("0x")

def test_wst_circulation():
    fund = ProductionLiabilityFund()
    initial = fund.treasury_balance
    result = fund.process_wst_circulation(5000.0, "0xRecipient")
    assert result["remaining_treasury"] == initial - 5000.0
    assert "tx_id" in result

def test_federation_scaling():
    scaler = FederationScaler(node_count=55)
    health = scaler.validate_federation_health()
    assert health["node_count"] >= 50
    assert health["avg_latency_ms"] < 50.0
    assert health["article_1095_compliant"] == True
