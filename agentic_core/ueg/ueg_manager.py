import json
import os
import logging
import time
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class UEGManager:
    """
    v60 Mastery: Unified Evidence Graph Manager.
    Manages the semantic relationships and provenance of all scientific claims.
    """
    def __init__(self, storage_path: str = "meta/ueg_graph.json"):
        self.storage_path = storage_path
        self.graph = self._load_graph()

    def _load_graph(self) -> Dict[str, Any]:
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        return {"nodes": [], "edges": []}

    def add_claim(self, claim: str, evidence: List[str], claim_type: str = "hypothesis"):
        node = {
            "id": f"claim_{len(self.graph['nodes'])}",
            "type": claim_type,
            "content": claim,
            "evidence": evidence
        }
        self.graph["nodes"].append(node)
        self._save()
        return node

    def add_product_specification(self, product_name: str, specs: Dict[str, Any], trace_id: str):
        """ARTICLE 401: Adds a Product Specification node to the UEG."""
        node = {
            "id": f"spec_{len(self.graph['nodes'])}",
            "type": "ProductSpecification",
            "product": product_name,
            "specifications": specs,
            "trace_id": trace_id,
            "timestamp": time.time()
        }
        self.graph["nodes"].append(node)
        self._save()
        return node

    def add_design_artifact(self, artifact_type: str, metadata: Dict[str, Any], trace_id: str):
        """ARTICLE 402: Adds a Design Artifact node to the UEG."""
        node = {
            "id": f"artifact_{len(self.graph['nodes'])}",
            "type": "DesignArtifact",
            "artifact_type": artifact_type,
            "metadata": metadata,
            "trace_id": trace_id,
            "timestamp": time.time()
        }
        self.graph["nodes"].append(node)
        self._save()
        return node

    def add_agent_task(self, goal: str, parent_id: str = None):
        """ARTICLE 386: Adds an Agent Task node to the UEG."""
        node = {
            "id": f"task_{len(self.graph['nodes'])}",
            "type": "AgentTask",
            "goal": goal,
            "parent": parent_id,
            "status": "pending",
            "created_at": time.time()
        }
        self.graph["nodes"].append(node)
        self._save()
        return node

    def add_execution_plan(self, task_id: str, steps: List[Dict[str, Any]]):
        """ARTICLE 386: Adds an Execution Plan node to the UEG."""
        node = {
            "id": f"plan_{len(self.graph['nodes'])}",
            "type": "ExecutionPlan",
            "task_id": task_id,
            "steps": steps,
            "status": "created"
        }
        self.graph["nodes"].append(node)
        self._save()
        return node

    def add_sandbox(self, task_id: str, environment_info: Dict[str, Any]):
        """ARTICLE 387: Adds a Sandbox Environment node to the UEG."""
        node = {
            "id": f"sandbox_{len(self.graph['nodes'])}",
            "type": "SandboxEnvironment",
            "task_id": task_id,
            "info": environment_info,
            "status": "active"
        }
        self.graph["nodes"].append(node)
        self._save()
        return node

    def add_audit_log(self, source_id: str, message: str, metadata: Dict[str, Any] = None):
        """ARTICLE 390: Adds an Audit Log node to the UEG."""
        node = {
            "id": f"audit_{len(self.graph['nodes'])}",
            "type": "AuditLog",
            "source": source_id,
            "message": message,
            "metadata": metadata or {},
            "timestamp": time.time()
        }

        # v129.0: Federated UEG Shared Memory Protocol
        if metadata and metadata.get("broadcast_to_federation"):
            logger.info(f"UEG: Broadcasting audit event to federated partners.")
            node["federated_status"] = "BROADCAST_PENDING"

        self.graph["nodes"].append(node)
        self._save()
        return node

    def add_conversation(self, url: str, transcript: List[Dict[str, Any]], metadata: Dict[str, Any] = None):
        """ARTICLE 356: Adds an LLM Conversation node to the UEG."""
        node = {
            "id": f"conv_{len(self.graph['nodes'])}",
            "type": "LLMConversation",
            "url": url,
            "transcript": transcript,
            "metadata": metadata or {},
            "timestamp": time.time() if 'time' in globals() else None
        }
        self.graph["nodes"].append(node)
        self._save()
        return node

    def add_insight(self, content: str, source_id: str, category: str = "key_insight", confidence: float = 0.9, metadata: Dict[str, Any] = None):
        """ARTICLE 357: Adds an Extracted Insight node to the UEG."""
        node = {
            "id": f"insight_{len(self.graph['nodes'])}",
            "type": "ExtractedInsight",
            "content": content,
            "source": source_id,
            "category": category,
            "confidence": confidence,
            "metadata": metadata or {}
        }
        self.graph["nodes"].append(node)
        self._save()
        return node

    def _save(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, 'w') as f:
            json.dump(self.graph, f, indent=4)
