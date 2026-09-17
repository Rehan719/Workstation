"""W466 probe seed — run with the probe backend's isolated DATA_DIR/WORKSTATION_DATA_DIR/WORKSTATION_UEG_PATH env BEFORE
starting that backend. Registers two living entities, funds the sender with one cycle (materiality raised in THIS
process only), and leaves one REAL stranded transfer: the sender debited, the receiver's queue lock made to time out
for that one call (what store_lock raises when another writer holds it too long). Prints `sender receiver transfer_id`
for scripts/_w466_probe.mjs. Virtual WST only; never point it at a real data directory."""
import sys

from fastapi.testclient import TestClient

from agentic_core.app_mvp import app
from agentic_core.config import store_lock as _real_store_lock
from agentic_core.economy import governance as gv
from agentic_core.economy import transfers as tr
from agentic_core.economy.living_vsbs import register

tag = sys.argv[1]
sender, receiver = f"w466p-sender-{tag}", f"w466p-receiver-{tag}"
register(sender, "Probe sender", "waqf_ltd_hybrid", "enterprise", "Rehan")
register(receiver, "Probe receiver", "waqf_ltd_hybrid", "enterprise", "Rehan")
gv.MATERIALITY_WST = 1e15
r = TestClient(app).post("/api/v1/economy/cycle", json={"vsb_id": sender, "revenue": 50000})
assert r.status_code == 200 and r.json().get("cycle"), r.text


class _QueueBusy(_real_store_lock):
    def __enter__(self):
        if self._lockpath.name.startswith("economy_pending_transfers"):
            raise TimeoutError(f"store_lock timeout on {self._lockpath.name}")
        return super().__enter__()


xid = f"xfer-{tag}probe"
tr.store_lock = _QueueBusy
try:
    tr.record_transfer(sender, receiver, 42.0, "w466 probe stranded", transfer_id=xid)
except TimeoutError:
    pass
finally:
    tr.store_lock = _real_store_lock
assert tr.debit_posted(sender, xid) and tr.peek_pending_transfers(receiver) == 0.0
print(sender, receiver, xid)
