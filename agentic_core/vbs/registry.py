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
from agentic_core.vbs.dcms import DocumentControlManagementSystem
from agentic_core.vbs.backbone import MycelialBackbone

# Shared, stateful living systems (CO2 accrues, artifacts version, defects accumulate — by design).
bms = BusinessManagementSystem("vbs")
qms = QualityManagementSystem("vbs")
ems = EnvironmentalManagementSystem("vbs")
dcms = DocumentControlManagementSystem("vbs")
backbone = MycelialBackbone()

CATALOGUE: List[Dict[str, Any]] = [
    {"id": "bms", "name": "Business Management System", "owned": True,
     "real": ["unit economics (cost-per-insight, ROI)", "viral k-factor"],
     "simulated": ["energy $/Wh rate constant"]},
    {"id": "qms", "name": "Quality Management System", "owned": True,
     "real": ["ISO-9001-aligned quality gates (coverage + zero-stub)", "non-conformance rate"],
     "simulated": []},
    {"id": "ems", "name": "Environmental Management System", "owned": True,
     "real": ["CO2 accumulation (kgCO2 per Wh)"],
     "simulated": ["efficiency-gain constant", "resource-gain constant"]},
    {"id": "dcms", "name": "Document Control Management System", "owned": True,
     "real": ["SHA3-512 cryptographic versioning", "multi-version audit trail"],
     "simulated": []},
    {"id": "backbone", "name": "Mycelial Backbone", "owned": True,
     "real": ["zero-trust DID agent registry", "failover rerouting"],
     "simulated": ["transport latency"]},
]
