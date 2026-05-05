
import pytest
import asyncio
import time
from agentic_core.integrations.connector_registry import RateLimiter, ConnectorRegistry

@pytest.mark.asyncio
async def test_offline_first_sim():
    print("\n1. Verifying Offline-First Rate Limiting (Backpressure)...")
    registry = ConnectorRegistry()
    registry.register_custom_connector("satellite_link", {"rate_limit": 2}) # 2 calls per min

    # First two calls should succeed
    res1 = registry.execute_integration("satellite_link", "ping")
    res2 = registry.execute_integration("satellite_link", "ping")
    assert res1["status"] == "success"
    assert res2["status"] == "success"

    # Third call should fail (backpressure/offline-first queueing)
    res3 = registry.execute_integration("satellite_link", "ping")
    print(f"   Third call status: {res3['status']} - {res3.get('msg')}")
    assert res3["status"] == "error"
    assert res3["msg"] == "RATE_LIMIT_EXCEEDED"

    print("2. Verifying Low-Bandwidth Install Size...")
    # This is a conceptual check of the built artifact
    import os
    dist_size = 0
    dist_path = "src/qep_frontend/dist/"
    assert os.path.exists(dist_path), "Build directory missing. Run 'npm run build' in qep_frontend."

    for f in os.listdir(dist_path):
        fp = os.path.join(dist_path, f)
        if os.path.isfile(fp):
            dist_size += os.path.getsize(fp)

    size_mb = dist_size / (1024 * 1024)
    print(f"   Frontend Dist Size: {size_mb:.2f} MB")
    assert size_mb > 0, "Build directory is empty."
    assert size_mb < 15.0

if __name__ == "__main__":
    asyncio.run(test_offline_first_sim())
