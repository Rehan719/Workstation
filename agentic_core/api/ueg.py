"""
UEG Provenance API — Workstation's OWN tamper-evident audit ledger, exposed.

The in-house AI fabric records its workflow-tree runs to a real hash-chained SHA3-512 Merkle-DAG ledger
(agentic_core/ueg). This surface lets you VERIFY the chain's integrity (every event's parent_hash must
equal the prior event's hash) and read recent events — verifiable provenance for the AI's actions.
"""
from __future__ import annotations

import json
import os
from typing import Any, Dict, List

from fastapi import APIRouter
from pydantic import BaseModel

from agentic_core.ueg.registry import ueg_ledger

router = APIRouter(prefix="/api/v1/ueg", tags=["ueg-provenance"])


@router.get("/verify")
async def verify_chain():
    """Verify the whole audit chain's cryptographic integrity (real SHA3-512 Merkle-DAG walk)."""
    valid = ueg_ledger.verify_chain()
    return {"chain_valid": bool(valid), "merkle_root": ueg_ledger.merkle_root,
            "algo": "sha3_512", "log_path": ueg_ledger.log_path, "real": True}


@router.get("/recent")
async def recent_events(limit: int = 10):
    """Most-recent ledger events (event type · actor · timestamp · hash). Real, from the chain file."""
    path = ueg_ledger.log_path
    events: List[Dict[str, Any]] = []
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            for line in lines[-max(1, min(limit, 200)):]:
                try:
                    entry = json.loads(line)
                    p = entry.get("payload", {})
                    events.append({"event_type": p.get("event_type"), "actor": p.get("actor"),
                                   "timestamp": p.get("timestamp"), "hash": entry.get("hash"),
                                   "data": p.get("data")})
                except json.JSONDecodeError:
                    continue
        except OSError:
            pass
    events.reverse()  # newest first
    return {"events": events, "count": len(events), "merkle_root": ueg_ledger.merkle_root}


class UEGLog(BaseModel):
    event_type: str
    data: Dict[str, Any] = {}
    actor: str = "user"


@router.post("/log")
async def log_event(req: UEGLog):
    """Append a custom event to the owned provenance chain (real SHA3-512 hash-chained write)."""
    h = await ueg_ledger.log_event(req.event_type, req.data, actor=req.actor)
    return {"hash": h, "algo": "sha3_512", "chain_valid": ueg_ledger.verify_chain()}
