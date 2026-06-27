import pytest
from products.capital_fund.reporting.regulatory_reporter import RegulatoryReporter
from scripts.deploy_gnosis_safe import deploy_safe

@pytest.mark.asyncio
async def test_regulatory_reporter_merkle():
    reporter = RegulatoryReporter(fund_id="fund_v1")
    bundle = await reporter.generate_fca_compliance_bundle("2026-01-01", "2026-03-31")

    assert bundle["manifest"]["status"] == "FINAL_CERTIFIED"
    assert "merkle_root" in bundle["manifest"]
    assert await reporter.verify_external_audit(bundle) is True

@pytest.mark.asyncio
async def test_gnosis_safe_deployment_mock():
    members = [
        {"did": "d1", "address": "0x1"},
        {"did": "d2", "address": "0x2"},
        {"did": "d3", "address": "0x3"}
    ]
    result = await deploy_safe(members, threshold=2)
    assert result["safe_address"].startswith("0x")
    assert result["network"] == "polygon_mainnet"
