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
     "real": ["unit economics (cost-per-insight, ROI)", "viral k-factor"],
     "simulated": ["energy $/Wh rate constant"]},
    {"id": "qms", "name": "Quality Management System", "owned": True, "owns": ["dcms"],
     "real": ["ISO-9001-aligned quality gates (coverage + zero-stub)", "non-conformance rate",
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
     "real": ["zero-trust DID agent registry", "failover rerouting"],
     "simulated": ["transport latency"]},
]
