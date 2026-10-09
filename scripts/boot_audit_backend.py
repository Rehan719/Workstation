"""Boot the backend a MILESTONE M1/M2 fidelity audit measures: a FRESH store and the CI AI posture.

Started through .claude/launch.json ("Backend M1 Audit"), never from a shell — a dev server goes through the
preview mechanism so the session can see it, stop it, and read its log. The environment is set HERE rather than
in .env because .env holds live secrets, and because load_dotenv() does not override already-set variables,
which would make the precedence between the two unreadable.

AI_DISABLE_LOCAL=1 is NOT the shipped default. It mirrors CI, and it is the posture that makes floor-disclosure
assessable: with the flag unset and Ollama reachable, the gateway serves from the local model and an assessor
cannot tell a disclosed floor from a served answer. fidelity_audit_v7.js says so in its own header.

THE STORE IS SCRATCH ON PURPOSE. An audit against an empty platform is exactly where fabrication shows — a
surface with no data either says so or invents something. A finding of the form "there are no entities" is
about the STORE, not the platform, and a refuter should correct it.

THE PORT MUST BE FREE BEFORE THIS STARTS. During W629 an audit agent started its own backend on :8031 and a
second boot exited silently, so the audit measured the wrong process. The launcher refuses rather than
silently losing: if the port answers already, it says so and exits non-zero. Confirm the booted commit through
/api/v1/health or any route only HEAD carries before spending twelve agents on it.
"""
import os
import pathlib
import socket
import sys

PORT = int(os.environ.get("M1_PORT", "8031"))
STORE = pathlib.Path(os.environ.get("M1_STORE", r"C:\tmp\m1_audit"))


def _port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex(("127.0.0.1", port)) == 0


if _port_in_use(PORT):
    print(f"REFUSED: something already answers on :{PORT}. A second boot would exit silently and the audit "
          f"would measure the wrong process (W629). Stop it first, or set M1_PORT.", file=sys.stderr)
    raise SystemExit(2)

for sub in ("data", "projects", "proposals", "synth", "listings"):
    (STORE / sub).mkdir(parents=True, exist_ok=True)

os.environ.update({
    "DATA_DIR": str(STORE / "data"),
    "WORKSTATION_DATA_DIR": str(STORE / "data"),
    "WORKSTATION_UEG_PATH": str(STORE / "data" / "ueg.json"),
    "PROJECTS_DIR": str(STORE / "projects"),
    "PROPOSALS_DIR": str(STORE / "proposals"),
    "SYNTHESIS_OUTPUT_DIR": str(STORE / "synth"),
    "LISTINGS_DIR": str(STORE / "listings"),
    "AI_DISABLE_LOCAL": "1",
    "PYTHONIOENCODING": "utf-8",
})

ROOT = str(pathlib.Path(__file__).resolve().parents[1])
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import uvicorn  # noqa: E402 — imported AFTER the env is set, so module-level config reads it

if __name__ == "__main__":
    print(f"audit backend: store {STORE} · port {PORT} · AI_DISABLE_LOCAL=1", flush=True)
    #  no --reload: a reloader forks a second process that re-reads the store, and the audit must see ONE
    uvicorn.run("agentic_core.app_mvp:app", host="127.0.0.1", port=PORT, reload=False, log_level="warning")
