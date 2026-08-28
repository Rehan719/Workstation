"""
W344 — the real-cadence organism soak: beats at the TRUE 60s heartbeat over wall-clock time,
measuring what back-to-back API beats never could (every prior observation fired beats sub-second).

Establishes three living VSBs with distinct activity profiles:
  - "active":  periodic virtual revenue events (labelled synthetic — virtual WST, honestly marked)
  - "idle":    zero activity (must cost ~nothing under W340's material-change staleness)
  - "mixed":   occasional revenue

Runs auto_compliance + auto_economy (+auto_ship) on a real cadence and samples every N beats:
DCMS registry bytes · UEG event counts by class · per-entity repo git object counts · beat
wall-time · W327 recompute-and-verify duration. Writes an honest JSON report; fabricates nothing.

Usage (isolated env, NEVER against real data):
    DATA_DIR=<fresh> WORKSTATION_DATA_DIR=<fresh> WORKSTATION_UEG_PATH=<fresh>/ueg.json \
    venv/Scripts/python.exe scripts/soak_organism.py --minutes 60 --cadence 60

Short validation runs (e.g. --minutes 9) are honest samples, not the full §8 soak — the report
records the actual duration; nothing extrapolates.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import time
from pathlib import Path


def _dir_size(p: Path) -> int:
    return sum(f.stat().st_size for f in p.rglob("*") if f.is_file()) if p.exists() else 0


def _git_objects(repo: Path) -> int:
    objs = repo / ".git" / "objects"
    return sum(1 for f in objs.rglob("*") if f.is_file()) if objs.exists() else 0


async def soak(minutes: float, cadence: float) -> dict:
    import warnings
    warnings.filterwarnings("ignore")
    from fastapi.testclient import TestClient
    from agentic_core.app_mvp import app
    from agentic_core.economy import living_vsbs as lv
    from agentic_core.economy.revenue import record_event
    from agentic_core.organism.heartbeat import heartbeat

    c = TestClient(app)
    dd = Path(os.environ["DATA_DIR"])
    profiles = {}
    for key, problem in (("active", "soak active halal grocer"),
                         ("idle", "soak idle library co-op"),
                         ("mixed", "soak mixed tailoring studio")):
        est = c.post("/api/v1/genesis/establish",
                     json={"problem": problem, "ship_output": True}).json()
        profiles[key] = est["vsb_id"]

    heartbeat.configure(auto_compliance=True, auto_economy=True, auto_ship=True)
    samples, beat_times = [], []
    t_end = time.time() + minutes * 60
    beat_n = 0
    try:
        while time.time() < t_end:
            beat_n += 1
            if beat_n % 3 == 1:      # the active profile earns each 3rd beat
                record_event(profiles["active"], "revenue", 120.0, "soak_synthetic",
                             ref=f"soak-{beat_n}", note="SYNTHETIC soak revenue — virtual WST, labelled")
            if beat_n % 7 == 1 and beat_n > 1:
                record_event(profiles["mixed"], "revenue", 60.0, "soak_synthetic",
                             ref=f"soakm-{beat_n}", note="SYNTHETIC soak revenue — virtual WST, labelled")
            t0 = time.time()
            beat = await heartbeat.beat()
            beat_ms = int((time.time() - t0) * 1000)
            beat_times.append(beat_ms)
            if beat_n % 5 == 0 or time.time() >= t_end:
                from agentic_core.gaas.v5 import UEGLogger
                v0 = time.time()
                verify = UEGLogger().verify_chain()
                verify_ms = int((time.time() - v0) * 1000)
                ueg_summary = UEGLogger().summary().get("by_type", {})
                samples.append({
                    "beat": beat_n, "at": time.strftime("%H:%M:%S", time.gmtime()),
                    "beat_ms": beat_ms, "actions": beat.get("actions"),
                    "dcms_bytes": (dd / "dcms_registry.json").stat().st_size
                                  if (dd / "dcms_registry.json").exists() else 0,
                    "ueg_events": sum(ueg_summary.values()), "ueg_by_type_top": dict(
                        sorted(ueg_summary.items(), key=lambda kv: -kv[1])[:6]),
                    "git_objects": {k: _git_objects(dd / "vsb_repos" / v)
                                    for k, v in profiles.items()},
                    "ueg_verify_ms": verify_ms, "ueg_verify_valid": bool(verify.get("valid")),
                })
            wait = cadence - (time.time() - t0)
            if wait > 0 and time.time() + wait < t_end + cadence:
                await asyncio.sleep(wait)
    finally:
        heartbeat.configure(auto_compliance=False, auto_economy=False, auto_ship=False)

    reg = lv._load()
    return {
        "requested_minutes": minutes, "cadence_s": cadence, "beats": beat_n,
        "beat_ms": {"min": min(beat_times), "max": max(beat_times),
                    "avg": round(sum(beat_times) / len(beat_times))},
        "profiles": {k: {"vsb_id": v, "operating_cycles": (reg.get(v) or {}).get("operating_cycles", 0)}
                     for k, v in profiles.items()},
        "samples": samples,
        "note": ("REAL-cadence sample — actual measurements only, nothing extrapolated. "
                 "Virtual WST throughout; soak revenue explicitly labelled synthetic."),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--minutes", type=float, default=60.0)
    ap.add_argument("--cadence", type=float, default=60.0)
    ap.add_argument("--out", default="")
    args = ap.parse_args()
    assert os.getenv("DATA_DIR"), "refusing to soak without an ISOLATED DATA_DIR"
    report = asyncio.new_event_loop().run_until_complete(soak(args.minutes, args.cadence))
    out = args.out or str(Path(os.environ["DATA_DIR"]) / "soak_report.json")
    Path(out).write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("beats", "beat_ms", "profiles", "note")}, indent=2))
    print(f"full report: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
