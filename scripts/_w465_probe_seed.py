"""W465 probe seed — run with the probe backend's isolated DATA_DIR/WORKSTATION_DATA_DIR/WORKSTATION_UEG_PATH env BEFORE
starting that backend: registers two living entities and funds the client with one cycle (the materiality threshold is
raised in THIS process only, so the seed files no hold). Prints the two entity ids for scripts/_w465_probe.mjs.
Virtual WST only; never point it at a real data directory."""
import sys

from fastapi.testclient import TestClient

from agentic_core.app_mvp import app
from agentic_core.economy import governance as gv
from agentic_core.economy.living_vsbs import register

tag = sys.argv[1]
client_vsb, provider_vsb = f"w465p-client-{tag}", f"w465p-provider-{tag}"
register(client_vsb, "Probe client", "waqf_ltd_hybrid", "enterprise", "Rehan")
register(provider_vsb, "Probe provider", "waqf_ltd_hybrid", "enterprise", "Rehan")
gv.MATERIALITY_WST = 1e15
r = TestClient(app).post("/api/v1/economy/cycle", json={"vsb_id": client_vsb, "revenue": 50000})
assert r.status_code == 200 and r.json().get("cycle"), r.text
print(client_vsb, provider_vsb)
