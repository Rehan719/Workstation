"""
UEG provenance ledger — Workstation's OWN tamper-evident audit chain, as a shared in-house capability.

The VSBUEGLogger is a real hash-chained, append-only SHA3-512 Merkle-DAG ledger: every event embeds the
previous event's hash as its parent, and verify_chain() walks the whole file to confirm integrity. This
module exposes ONE shared singleton (its own dedicated log file) so the in-house AI fabric and the API
write to a single, continuously-verifiable chain — giving the AI's actions verifiable provenance.
"""
from __future__ import annotations

from agentic_core.ueg.logger import VSBUEGLogger

# Dedicated chain for the in-house AI fabric (separate from any legacy audit file) so it starts clean
# and stays continuously verifiable through this single writer.
ueg_ledger = VSBUEGLogger(log_path="data/ueg_native_ai.log")
