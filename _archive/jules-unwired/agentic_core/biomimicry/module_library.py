import hashlib
import json
import time
from typing import Dict, Any, List, Optional

class ModuleRegistry:
    """
    Content-addressed registry for AI components (Models, Adapters, Tools, Blueprints).
    Uses Merkle DAG-like addressing and simulated vector indexing.
    """
    def __init__(self):
        # Maps Hash -> Module Metadata
        self.storage: Dict[str, Dict[str, Any]] = {}
        # Simulated vector index (Name -> Vector -> Hash)
        self.vector_index: List[Dict[str, Any]] = []

        self._seed_initial_modules()

    def _compute_hash(self, data: Dict[str, Any]) -> str:
        """Computes SHA-256 hash for content addressing."""
        content = json.dumps(data, sort_keys=True).encode('utf-8')
        return hashlib.sha256(content).hexdigest()

    def register_module(self, module_type: str, name: str, version: str, content: Any, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Registers a new module and returns its content hash."""
        module_data = {
            "type": module_type,
            "name": name,
            "version": version,
            "content": content,
            "metadata": metadata or {},
            "timestamp": time.time()
        }

        content_hash = self._compute_hash(module_data)
        self.storage[content_hash] = module_data

        # Simulated vector embedding (random for Phase 1)
        simulated_vector = [hash(name) % 100 / 100.0] * 128
        self.vector_index.append({
            "name": name,
            "vector": simulated_vector,
            "hash": content_hash
        })

        return content_hash

    def get_module(self, content_hash: str) -> Optional[Dict[str, Any]]:
        """Retrieves a module by its content hash."""
        return self.storage.get(content_hash)

    def query_modules(self, query: str) -> List[Dict[str, Any]]:
        """
        Simulated vector search for modules.
        Target: Query < 50ms.
        """
        start_time = time.perf_counter()

        # Simulated search logic
        results = []
        for item in self.vector_index:
            if query.lower() in item["name"].lower():
                results.append(self.storage[item["hash"]])

        end_time = time.perf_counter()
        query_time_ms = (end_time - start_time) * 1000

        # Ensure we log the metric
        # print(f"Query latency: {query_time_ms:.2f}ms")

        return results

    def _seed_initial_modules(self):
        """Seed 15 canonical modules to validate the framework."""
        # 3 Edge LLMs
        self.register_module("edge_llm", "Nematron-1B", "v1.0", "bin://nematron_1b_q4.gguf")
        self.register_module("edge_llm", "Nemoclaw-3B", "v1.0", "bin://nemoclaw_3b_q4.gguf")
        self.register_module("edge_llm", "OpenClaw-7B", "v1.0", "bin://openclaw_7b_q4.gguf")

        # 4 LoRA Adapters
        self.register_module("lora_adapter", "Law-Expert-LoRA", "v2.1", "bin://law_adapter.bin")
        self.register_module("lora_adapter", "Science-Expert-LoRA", "v1.5", "bin://science_adapter.bin")
        self.register_module("lora_adapter", "Medical-Safety-LoRA", "v3.0", "bin://medical_adapter.bin")
        self.register_module("lora_adapter", "Code-Optimization-LoRA", "v1.0", "bin://code_adapter.bin")

        # 5 Tool Wrappers
        self.register_module("tool", "Search-Engine-Wrapper", "v1.0", "py://search_tool.py")
        self.register_module("tool", "FileSystem-Tool", "v1.2", "py://fs_tool.py")
        self.register_module("tool", "Calculator-Tool", "v1.0", "py://calc_tool.py")
        self.register_module("tool", "Weather-API-Wrapper", "v2.0", "py://weather_tool.py")
        self.register_module("tool", "Git-Orchestrator", "v1.0", "py://git_tool.py")

        # 3 Agent Blueprints
        self.register_module("agent_blueprint", "Research-Agent-Config", "v1.0", {"role": "researcher", "tools": ["search"]})
        self.register_module("agent_blueprint", "Developer-Agent-Config", "v1.0", {"role": "coder", "tools": ["fs", "git"]})
        self.register_module("agent_blueprint", "Legal-Analyst-Config", "v1.0", {"role": "legal", "tools": ["search"]})

if __name__ == "__main__":
    registry = ModuleRegistry()
    print(f"Total modules registered: {len(registry.storage)}")
    results = registry.query_modules("Law")
    print(f"Query results for 'Law': {len(results)}")
    if results:
        print(f"First result: {results[0]['name']} ({results[0]['version']})")
