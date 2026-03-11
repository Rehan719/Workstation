import json
import os
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class VersionGraph:
    """ARTICLE 295/321: UEG Extension for Business Process Lineage."""
    def __init__(self, ueg_path: str = "meta/ueg_graph.json"):
        self.ueg_path = ueg_path

    def add_version_node(self, version_id: str, metadata: Dict[str, Any]):
        self._add_node(version_id, "version", metadata)

    def add_variation_node(self, variation_id: str, version_id: str, metadata: Dict[str, Any]):
        self._add_node(variation_id, "variation", metadata)
        self._add_edge(variation_id, version_id, "variation_of")

    def add_pipeline_run(self, run_id: str, stage: str, status: str):
        metadata = {"stage": stage, "status": status, "timestamp": "2024-10-01T00:00:00"}
        self._add_node(run_id, "pipeline_run", metadata)

    def add_audit_trail(self, audit_id: str, stage: str, results: Dict[str, Any]):
        """Logs a QMS audit event."""
        metadata = {"stage": stage, "results": results, "timestamp": "2024-10-01T00:00:00"}
        self._add_node(audit_id, "audit_event", metadata)

    def _add_node(self, node_id: str, node_type: str, content: Dict[str, Any]):
        ueg = self._load_ueg()
        ueg["nodes"] = [n for n in ueg.get("nodes", []) if n.get("id") != node_id]
        ueg["nodes"].append({
            "id": node_id,
            "type": node_type,
            "content": content
        })
        self._save_ueg(ueg)

    def _add_edge(self, source: str, target: str, edge_type: str):
        ueg = self._load_ueg()
        if "edges" not in ueg: ueg["edges"] = []
        ueg["edges"].append({
            "source": source,
            "target": target,
            "type": edge_type
        })
        self._save_ueg(ueg)

    def _load_ueg(self) -> Dict[str, Any]:
        if os.path.exists(self.ueg_path):
            with open(self.ueg_path, "r") as f:
                return json.load(f)
        return {"nodes": [], "edges": []}

    def _save_ueg(self, ueg: Dict[str, Any]):
        os.makedirs(os.path.dirname(self.ueg_path), exist_ok=True)
        with open(self.ueg_path, "w") as f:
            json.dump(ueg, f, indent=4)
