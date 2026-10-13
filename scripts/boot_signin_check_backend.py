"""Boot a backend WITH SIGN-IN ON, on a FRESH scratch store - to drive the pages once with a signed-in session.

Started through .claude/launch.json ("Backend sign-in check"), never from a shell. Nothing here touches the
Owner's store, the Owner's settings file or the Owner's switch: sign-in is on for THIS PROCESS ONLY, and the
store is a scratch folder outside the repository.

THE ADMIN PASSWORD IS MADE HERE, FOR THIS RUN, AND IS NEVER PRINTED. It is written to one file inside the
scratch store so that the session driving the check can sign in. It is a test value for a scratch store: it is
not the Owner's password for anything, and it is replaced on the next boot.

The local model is disabled, as on the build server: this check is about whether each page's data call carries
the token, and a model's answer has no part in that.
"""
import os
import pathlib
import secrets
import socket
import sys

PORT = int(os.environ.get("SIGNIN_CHECK_PORT", "8032"))
STORE = pathlib.Path(os.environ.get("SIGNIN_CHECK_STORE", r"C:\tmp\signin_check"))


def _port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex(("127.0.0.1", port)) == 0


if _port_in_use(PORT):
    print(f"REFUSED: something already answers on :{PORT}; a second boot would exit silently and the check "
          f"would drive the wrong process. Stop it first, or set SIGNIN_CHECK_PORT.", file=sys.stderr)
    raise SystemExit(2)

for sub in ("data", "projects", "proposals", "synth", "listings"):
    (STORE / sub).mkdir(parents=True, exist_ok=True)

_password = secrets.token_urlsafe(24)
(STORE / "admin_password.txt").write_text(_password, encoding="utf-8")

os.environ["WORKSTATION_AUDIT_BACKEND"] = "1"
os.environ["LEGAL_BUNDLE_DIR"] = str(STORE / "legal_bundle_of_no_one")
os.environ.update({
    "AUTH_ENABLED": "true",
    "ADMIN_PASSWORD": _password,
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
#  the scratch store must not inherit a signing key or an admin from anywhere else
os.environ.pop("JWT_SECRET", None)

ROOT = str(pathlib.Path(__file__).resolve().parents[1])
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import uvicorn  # noqa: E402 - imported AFTER the environment is set, so module-level settings read it

if __name__ == "__main__":
    print(f"sign-in check backend: store {STORE} · port {PORT} · sign-in ON for this process · local model off",
          flush=True)
    uvicorn.run("agentic_core.app_mvp:app", host="127.0.0.1", port=PORT, reload=False, log_level="warning")
