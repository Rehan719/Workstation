from typing import Dict, Any, Optional
from agentic_core.ueg.logger import VSBUEGLogger
from agentic_core.biomimicry.geospheric.orchestrator_legacy import GeosphericHomeostaticOrchestrator

from .layer_registry import get_layer_metadata

class LayerAdapter:
    def __init__(self, layer_id: int, manager: Any):
        self.layer_id = layer_id
        self.manager = manager
        self.metadata = get_layer_metadata(layer_id)

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Base execution logic with UCI validation (mocked for now)."""
        await self.manager.ueg.log_minimisation_event("layer_execution_triggered", {
            "layer_id": self.layer_id,
            "layer_name": self.metadata["name"],
            "task_id": task.get("id")
        })
        # Default behavior: log and return success
        return {"status": "SUCCESS", "layer": self.layer_id}

class EnrichedArchitecturalLayerManager:
    """
    14-Layer IDBO Core with backward-compatible 6-layer API.
    Mandate: Evolutionary Continuity + Supreme Convergence.
    """
    def __init__(self, ueg_logger: Optional[Any] = None):
        self.ueg = ueg_logger or VSBUEGLogger()
        self.geospheric = GeosphericHomeostaticOrchestrator(ueg_logger=self.ueg)

        # Initialize 14 layers via adapters
        self.layers_14 = {i: LayerAdapter(i, self) for i in range(14)}

        # Explicit registration of required supreme components
        from agentic_core.consultation.mushawara.mushawara_bridge_2 import MushawaraBridge2
        self.mushawara = MushawaraBridge2(self.ueg)

    # --- LEGACY 6-LAYER API (Preserved for Backward Compatibility) ---

    async def mycelial_propagation(self, data: Any):
        """Layer 0: Decentralized mesh routing."""
        data_id = hash(str(data))
        await self.ueg.log_minimisation_event("layer0_mycelial_broadcast", {"data_id": data_id, "nodes_reached": 12})
        return True

    async def ant_colony_orchestration(self, tasks: list):
        """Layer 1: Stigmergic task allocation."""
        sorted_tasks = sorted(tasks, key=lambda x: x.get('relevance', 0), reverse=True)
        for task in sorted_tasks:
             await self.ueg.log_minimisation_event("layer1_ant_allocation", {"task": task.get('id'), "pheromone": 0.95})
        return sorted_tasks

    async def octopus_hardware_hal(self, process_load: float):
        """Layer 2: Local-first processing."""
        summary = {"load_intensity": process_load, "salient_features": ["cpu_bound", "io_wait"]}
        await self.ueg.log_minimisation_event("layer2_octopus_hal_summarised", summary)
        return summary

    async def immune_resilience(self, threat_data: Any):
        """Layer 3: MHC-inspired identity binding + adaptive immunity."""
        detector_id = f"VDJ_{hash(str(threat_data))}"
        await self.ueg.log_minimisation_event("layer3_immune_detector_generated", {"detector": detector_id})
        return detector_id

    async def symbiotic_civilisation(self, value_exchange: Dict[str, Any]):
        """Layer 4: Value Exchange Ledger."""
        cert_hash = "CERT_" + str(value_exchange.get("output_hash"))
        await self.ueg.log_minimisation_event("layer4_symbiotic_certified", {"cert": cert_hash})
        return cert_hash

    async def geospheric_homeostasis(self, inputs: Dict[str, Any], context: Dict[str, Any]):
        """Layer 5: Six-cycle PID-controlled homeostasis."""
        return await self.geospheric.step(inputs, context)

    # --- SOVEREIGN 14-LAYER API (Phase 4+ Mandate) ---

    async def execute_sovereign(self, layer_id: int, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Unified 14-layer execution API.
        Routes to specialized handlers or legacy shims.
        """
        if layer_id not in self.layers_14:
             raise ValueError(f"Constitutional Violation: Invalid layer ID {layer_id}")

        # Specialized Routing Logic
        if layer_id == 0:
            return {"status": "SUCCESS", "result": await self.mycelial_propagation(task.get("data"))}
        elif layer_id == 5:
            return await self.geospheric_homeostasis(task.get("inputs", {}), task.get("context", {}))
        elif layer_id == 9:
            # Orchestration Layer (Mushawara Integration)
            res = await self.mushawara.consult(task, mode="sync")
            return {"status": "SUCCESS", "consensus": res}
        elif layer_id == 13:
            # Reflection Layer (SIL integration placeholder for Phase 4)
            await self.ueg.log_minimisation_event("civilizational_reflection_triggered", task)
            return {"status": "SUCCESS", "drift": 0.003}

        # Fallback to generic adapter execution
        return await self.layers_14[layer_id].execute(task)

    def get_layer(self, layer_id: int) -> LayerAdapter:
        return self.layers_14.get(layer_id)
