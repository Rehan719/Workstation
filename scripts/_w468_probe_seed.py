"""W468 probe seed — run with the probe backend's isolated DATA_DIR/WORKSTATION_DATA_DIR/WORKSTATION_UEG_PATH env BEFORE
starting that backend. Registers two living entities (also saved as VSB entities, so the cockpit lists them), gives each
real books with one cycle (materiality raised in THIS process only), then makes ONE ledger unreadable the way a stray
editor or a copy tool does: a UTF-8 byte-order mark in front of otherwise valid books. Prints
`unreadable readable sha256-of-the-unreadable-file` for scripts/_w468_probe.mjs. Virtual WST only; never point it at a
real data directory."""
import hashlib
import sys
import time

from fastapi.testclient import TestClient

from agentic_core.api.vsb import _save_vsb
from agentic_core.app_mvp import app
from agentic_core.economy import governance as gv
from agentic_core.economy.ledger import VirtualLedger
from agentic_core.economy.living_vsbs import register
from agentic_core.economy.metabolism import EconomicMetabolism

tag = sys.argv[1]
bad, good = f"w468p-unreadable-{tag}", f"w468p-readable-{tag}"
gv.MATERIALITY_WST = 1e15
client = TestClient(app)
for vid, name in ((bad, "W468 probe - unreadable ledger"), (good, "W468 probe - readable ledger")):
    register(vid, name, "waqf_ltd_hybrid", "enterprise", "Rehan")
    m = EconomicMetabolism(vid, "waqf_ltd_hybrid", "Rehan")
    _save_vsb({"vsb_id": vid, "name": name, "domain": "enterprise", "status": "established", "stage": "launch",
               "owner_id": "default", "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "board": {"chief": {"name": "Chief (probe)"}, "directors": []},
               "economy": {"entity_type": "waqf_ltd_hybrid", "entity_name": m.template["name"],
                           "waterfall": m.waterfall, "capital_preserved": m.template["capital_preserved"],
                           "currency": "WST (virtual)"}})
    r = client.post("/api/v1/economy/cycle", json={"vsb_id": vid, "revenue": 5000})
    assert r.status_code == 200 and r.json().get("cycle"), r.text

# the readable entity's next heartbeat visit raises (its roster row keeps the raise, as a busy ledger lock would leave it)
from agentic_core.economy import living_vsbs as lv

real_sync = gv.governed_cycle_sync


def _raises(vsb_id, *x, **k):
    raise TimeoutError("w468 probe: the ledger's lock stayed busy")


gv.governed_cycle_sync = _raises
assert "error" in lv.operate_vsb(good)
gv.governed_cycle_sync = real_sync

path = VirtualLedger(bad).path
raw = b"\xef\xbb\xbf" + path.read_bytes()
path.write_bytes(raw)
assert VirtualLedger(bad).load_error and VirtualLedger(good).load_error is None
print(bad, good, hashlib.sha256(raw).hexdigest())
