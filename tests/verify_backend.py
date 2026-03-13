import httpx
import asyncio
import time
import subprocess
import os

async def verify_backend():
    print("Starting master backend...")
    # Start server in background
    proc = subprocess.Popen(
        ["uvicorn", "agentic_core.main:app", "--host", "127.0.0.1", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(5) # Wait for startup

    async with httpx.AsyncClient() as client:
        try:
            # 1. Health
            res = await client.get("http://127.0.0.1:8000/health")
            print(f"Health: {res.json()}")
            assert res.status_code == 200

            # 2. QEP Ayah
            print("Testing QEP Ayah...")
            res = await client.get("http://127.0.0.1:8000/api/v1/qep/ayah/1:1")
            data = res.json()
            print(f"Ayah 1:1: {data['translation']}")
            assert res.status_code == 200
            assert "Merciful" in data["translation"]

            # 3. Governance
            print("Testing Governance...")
            res = await client.get("http://127.0.0.1:8000/api/v1/governance/okrs")
            data = res.json()
            print(f"Governance Report: {data['global_pas']}")
            assert data["global_pas"] >= 0.95

            print("Backend Verification SUCCESSFUL.")
        finally:
            proc.terminate()

if __name__ == "__main__":
    asyncio.run(verify_backend())
