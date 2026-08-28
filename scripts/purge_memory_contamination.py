"""
W334 — one-time Owner-run remediation for the pre-W332/W333 cross-tenant memory bleed.

Before W332/W333, agentic_core/ai/memory.py was ONE global pool with an empty metadata field, so
every user's prompts/responses were retrievable into every other user's AI calls — and the native
engine baked recalled lines into GENERATED PUBLIC COPY (reproduced live: one tenant's confidential
prompt shipped verbatim into another tenant's git-committed website). W332/W333 close the leak for
all NEW writes; this script cleans up what already accumulated.

HONEST + NON-DESTRUCTIVE by construction:
  - Nothing is silently deleted. Contaminated stores are QUARANTINED (moved under
    DATA_DIR/quarantine/<timestamp>/) so the Owner can inspect them.
  - Every action is UEG-logged (type='memory.contamination_purge') with real counts.
  - Owner-run ONLY: this is a script, never wired to a route or the heartbeat.

Usage (from the repo root, with the same DATA_DIR the app uses):
    venv/Scripts/python.exe scripts/purge_memory_contamination.py            # dry run (report only)
    venv/Scripts/python.exe scripts/purge_memory_contamination.py --apply    # quarantine + reset

Shipped entity repos are also scanned: any web/webapp page whose working tree still carries a recall
signature ('Subject: ', 'User: … | AI:', 'Native Structured Engine') is REPORTED for re-shipping via
POST /api/v1/vsb/{id}/repo/ship (which now regenerates clean copy) — the script does not rewrite git
history (that is the Owner's call; the report names each file and repo).
"""
from __future__ import annotations

import json
import os
import shutil
import sys
import time
from pathlib import Path

_RECALL_SIGNS = ("Subject: ", " | AI:", "Native Structured Engine", "_[")


def _data_dir() -> Path:
    return Path(os.getenv("DATA_DIR") or os.getenv("WORKSTATION_DATA_DIR") or "agentic_core/data")


def _ueg(event: dict) -> None:
    try:
        from agentic_core.gaas.v5 import UEGLogger
        UEGLogger().log(event)
    except Exception:
        pass


def scan(dd: Path) -> dict:
    """Report contamination WITHOUT changing anything."""
    report: dict = {"memory_json": None, "chroma": None, "repos": []}
    mem = dd / "memory.json"
    if mem.exists():
        try:
            rows = json.loads(mem.read_text(encoding="utf-8"))
        except Exception:
            rows = []
        untagged = [r for r in rows if not (r.get("metadata") or {}).get("owner_id")]
        report["memory_json"] = {"total": len(rows), "untagged_legacy": len(untagged)}
    chroma = dd / "chroma"
    if chroma.exists():
        report["chroma"] = {"present": True, "note": "unscoped memory_v01 collection — quarantine to reset"}
    repos = dd / "vsb_repos"
    if repos.exists():
        for root in repos.iterdir():
            if not root.is_dir():
                continue
            hits = []
            for page in list(root.glob("web/*.html")) + list(root.glob("webapp/**/*.html")):
                try:
                    txt = page.read_text(encoding="utf-8", errors="replace")
                except Exception:
                    continue
                if any(s in txt for s in _RECALL_SIGNS):
                    hits.append(str(page.relative_to(repos)))
            if hits:
                report["repos"].append({"vsb_id": root.name, "contaminated_pages": hits})
    return report


def apply(dd: Path, report: dict) -> dict:
    """Quarantine the contaminated stores (never delete) and reset them clean."""
    ts = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    qdir = dd / "quarantine" / ts
    qdir.mkdir(parents=True, exist_ok=True)
    moved = []
    mem = dd / "memory.json"
    if mem.exists():
        shutil.move(str(mem), str(qdir / "memory.json"))
        mem.write_text("[]", encoding="utf-8")
        moved.append("memory.json")
    chroma = dd / "chroma"
    if chroma.exists():
        shutil.move(str(chroma), str(qdir / "chroma"))
        moved.append("chroma/")
    _ueg({"type": "memory.contamination_purge", "quarantine": str(qdir), "moved": moved,
          "memory_report": report.get("memory_json"),
          "contaminated_repos": [r["vsb_id"] for r in report.get("repos", [])],
          "note": "W334 Owner-run remediation — stores quarantined (not deleted), reset clean"})
    return {"quarantine_dir": str(qdir), "moved": moved,
            "repos_to_reship": [r["vsb_id"] for r in report.get("repos", [])]}


def main() -> int:
    dd = _data_dir()
    if not dd.exists():
        print(f"DATA_DIR {dd} does not exist — nothing to scan.")
        return 0
    report = scan(dd)
    print("── contamination scan ──")
    print(json.dumps(report, indent=2))
    if "--apply" not in sys.argv:
        print("\nDRY RUN. Re-run with --apply to quarantine + reset (nothing was changed).")
        return 0
    result = apply(dd, report)
    print("\n── applied ──")
    print(json.dumps(result, indent=2))
    if result["repos_to_reship"]:
        print("\nRe-ship these entities to regenerate clean public copy (W332 makes the re-ship clean):")
        for vid in result["repos_to_reship"]:
            print(f"  POST /api/v1/vsb/{vid}/repo/ship")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
