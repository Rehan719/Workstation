"""
WORKSTATION IDBO — Phase 0 Verification Script
Run this from the repo root on Windows with the venv active:

    .\\venv\\Scripts\\activate
    python scripts\\verify_phase0.py

This script:
1. Checks all new routers import cleanly
2. Starts the FastAPI app and hits key endpoints
3. Reports PASS / FAIL for each Phase 0 task
"""
import sys
import os
import json
import time
import subprocess
import threading
import urllib.request
import urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

BASE_URL = "http://localhost:8765"  # Use non-standard port to avoid conflicts

results = []

def check(label, passed, detail=""):
    status = "PASS" if passed else "FAIL"
    results.append((status, label, detail))
    print(f"  [{status}] {label}" + (f" — {detail}" if detail else ""))

def get(path, timeout=5):
    try:
        with urllib.request.urlopen(f"{BASE_URL}{path}", timeout=timeout) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, {}
    except Exception as e:
        return None, str(e)

print("\n" + "="*60)
print("WORKSTATION IDBO — Phase 0 Verification")
print("="*60 + "\n")

# ── Section 1: Import checks ──────────────────────────────────────
print("1. Router import checks")

new_routers = [
    ("agentic_core.api.agent_hub", "router"),
    ("agentic_core.api.ai_orchestration", "router"),
    ("agentic_core.api.partnerships", "router"),
    ("agentic_core.api.qep_analytics", "router"),
    ("agentic_core.api.tools", "router"),
    ("agentic_core.api.cross_platform", "api"),
]

import_ok = 0
for mod, attr in new_routers:
    try:
        m = __import__(mod, fromlist=[attr])
        obj = getattr(m, attr)
        check(f"Import {mod}", True, type(obj).__name__)
        import_ok += 1
    except Exception as e:
        check(f"Import {mod}", False, str(e)[:80])

# ── Section 2: agentic_core package imports without torch ─────────
print("\n2. Package-level import health")
try:
    import agentic_core  # noqa
    check("agentic_core imports cleanly (no torch required)", True)
except ImportError as e:
    check("agentic_core imports cleanly", False, str(e))

# ── Section 3: Cross-platform file syntax ─────────────────────────
print("\n3. Syntax checks")
import py_compile
for fname in [
    "agentic_core/api/cross_platform.py",
    "agentic_core/api/agent_hub.py",
    "agentic_core/app_mvp.py",
]:
    try:
        py_compile.compile(os.path.join(ROOT, fname), doraise=True)
        check(f"Syntax OK: {fname}", True)
    except py_compile.PyCompileError as e:
        check(f"Syntax OK: {fname}", False, str(e)[:80])

# ── Section 4: Data directories ───────────────────────────────────
print("\n4. Data directories")
for d in ["data/agent_messages", "data/handoffs", "data/agent_registry"]:
    path = os.path.join(ROOT, d)
    check(f"Directory exists: {d}", os.path.isdir(path))

check("data/shared_context.json exists",
      os.path.isfile(os.path.join(ROOT, "data/shared_context.json")))

# ── Section 5: Constitutional documents ───────────────────────────
print("\n5. Constitutional documents")
required_docs = [
    "PURPOSE.md", "DUA.md", "WORKSTATION_CONSTITUTION.md",
    "KNOWLEDGE_COMMONS.md", "CLAUDE_MEMORY.md", "WORKSTATION_MASTER.md",
    "AGENT_HUB_README.md", "WORKSTATION_TRANSFORMATION_PLAN.md",
    "CLAUDE_CODE_PROMPT.md",
]
for doc in required_docs:
    check(f"Present: {doc}", os.path.isfile(os.path.join(ROOT, doc)))

# ── Section 6: No fake certification files ────────────────────────
print("\n6. Repository cleanliness")
import glob
bad_patterns = ["*CERTIF*", "*SUPREME*", "*SOVEREIGN*", "*OMNI*"]
bad_found = []
for pat in bad_patterns:
    for f in glob.glob(os.path.join(ROOT, pat)):
        basename = os.path.basename(f)
        if "archive" not in f and basename.endswith(".md"):
            bad_found.append(basename)

check("No fake certification files at root", len(bad_found) == 0,
      f"Found: {bad_found}" if bad_found else "")

# ── Section 7: Live server test ───────────────────────────────────
print("\n7. Live server tests (starting server on port 8765...)")

server_proc = None
try:
    env = os.environ.copy()
    env["PORT"] = "8765"
    server_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn",
         "agentic_core.app_mvp:app", "--port", "8765", "--host", "127.0.0.1"],
        cwd=ROOT, env=env,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    time.sleep(4)  # Give server time to start

    # Health check
    status, data = get("/health")
    check("GET /health → 200", status == 200, str(data))

    # Agent Hub
    status, data = get("/api/v1/hub/agents")
    check("GET /api/v1/hub/agents → 200", status == 200,
          f"agents count: {len(data.get('agents', []))}")

    # Projects
    status, data = get("/api/v1/projects")
    check("GET /api/v1/projects → 200", status == 200)

    # Biometrics (no random numbers check)
    status, data = get("/api/v1/biometrics/status")
    check("GET /api/v1/biometrics/status → 200", status == 200)
    if status == 200:
        cpu = data.get("cardiovascular", {}).get("resource_flow")
        check("Biometrics: resource_flow is real psutil value (0-100)",
              cpu is not None and 0 <= cpu <= 100, f"value={cpu}")

    # Cross-platform (refactored)
    status, data = get("/api/cross-platform/ar/scene")
    check("GET /api/cross-platform/ar/scene → 200 (refactored APIRouter)",
          status == 200, f"status field: {data.get('status')}")

except Exception as e:
    check("Server started", False, str(e))
finally:
    if server_proc:
        server_proc.terminate()

# ── Summary ───────────────────────────────────────────────────────
print("\n" + "="*60)
passed = sum(1 for r in results if r[0] == "PASS")
failed = sum(1 for r in results if r[0] == "FAIL")
print(f"Phase 0 Verification: {passed} PASSED, {failed} FAILED")

if failed == 0:
    print("\n✓ Phase 0 COMPLETE — ready to begin Phase 1")
    print("  Next: run data/handoffs/2026-06-18_phase1_qep_cowork-to-code.json tasks")
else:
    print("\n✗ Phase 0 has failures — fix before starting Phase 1")
    print("  See WORKSTATION_TRANSFORMATION_PLAN.md Section 5 for fix instructions")
print("="*60 + "\n")

sys.exit(0 if failed == 0 else 1)
