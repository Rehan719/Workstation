"""
VBS Living Management Systems — registered as Workstation's OWN in-house capabilities.

The VBS systems (Business / Quality / Environmental / Document-Control management + the Mycelial
agent backbone) are real, deterministic management-system code. This module instantiates them ONCE as
shared singletons so both the API surface and the in-house AI fabric (the native swarm / workflow-tree
orchestrator) can USE them as owned, deterministic capabilities — not model calls, real computation.

Honesty note: the per-system `real` / `simulated` lists below declare exactly which parts are genuine
computation versus placeholder constants (energy $/Wh rates, a fixed efficiency gain, transport
latency). Nothing here is presented as more than it is.
"""
from __future__ import annotations

from typing import Any, Dict, List

from agentic_core.vbs.bms import BusinessManagementSystem
from agentic_core.vbs.qms import QualityManagementSystem
from agentic_core.vbs.ems import EnvironmentalManagementSystem
from agentic_core.vbs.backbone import MycelialBackbone

# Shared, stateful living systems (CO2 accrues, artifacts version, defects accumulate — by design).
bms = BusinessManagementSystem("vbs")
qms = QualityManagementSystem("vbs")
ems = EnvironmentalManagementSystem("vbs")
# The DCMS is OWNED BY the QMS (ISO 9001 §7.5 — document control is a function of quality management).
# Exposed here as the same single instance for backward-compatible `from ...registry import dcms` use.
dcms = qms.dcms
backbone = MycelialBackbone()

CATALOGUE: List[Dict[str, Any]] = [
    {"id": "bms", "name": "Business Management System", "owned": True,
     "real": ["unit economics arithmetic (cost-per-insight)"],
     "simulated": ["energy $/Wh rate constant", "insight $0.50 value constant (inside ROI)",
                   "viral k-factor formula"]},
    {"id": "qms", "name": "Quality Management System", "owned": True, "owns": ["dcms"],
     "real": ["ISO-9001-aligned quality gates (coverage + zero-stub)",
              "persistent traceable defects + the §8.7/§10.2 correct→re-verify loop (W307)",
              "non-conformance rate (gate failures / gates run)",
              "owns document control (ISO 9001 §7.5) — quality records placed under DCMS control"],
     "simulated": []},
    {"id": "ems", "name": "Environmental Management System", "owned": True,
     "real": ["CO2 accumulation (kgCO2 per Wh)"],
     "simulated": ["efficiency-gain constant", "resource-gain constant"]},
    {"id": "dcms", "name": "Document Control Management System", "owned": True, "owned_by": "qms",
     "real": ["SHA3-512 cryptographic versioning", "multi-version audit trail",
              "operated as the QMS's document-control subsystem (ISO 9001 §7.5)"],
     "simulated": []},
    {"id": "backbone", "name": "Mycelial Backbone", "owned": True,
     # W440 refuter catch: "failover rerouting" sat in the REAL list while route_message/
     # _find_failover have zero callers and carry the §4.5 archetype (first-by-dict-order
     # selection, a DELIVERED constant for unregistered targets) — unreached machinery is not a
     # real capability
     "real": ["DID agent registry (in-memory, per-process)"],
     "simulated": ["transport latency (fixed 40ms sleep; the health figure is an EWMA of it, "
                   "not a measured p95)"]},
]
