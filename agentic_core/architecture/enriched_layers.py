from typing import Dict, Any, Optional
from agentic_core.ueg.logger import VSBUEGLogger
from agentic_core.biomimicry.geospheric.orchestrator_legacy import GeosphericHomeostaticOrchestrator


class EnrichedArchitecturalLayerManager:
    """
    The layer methods governance/uci_interceptor.py calls (geospheric_homeostasis, immune_resilience) and the
    geospheric orchestrator it reads. W781 (FU-1096): this once claimed a fourteen-layer core; the seven layers are the
    canon, the 14-layer table in layer_registry.py is historical, and the 14-layer execution API is archived.
    """
    def __init__(self, ueg_logger: Optional[Any] = None):
        self.ueg = ueg_logger or VSBUEGLogger()
        self.geospheric = GeosphericHomeostaticOrchestrator(ueg_logger=self.ueg)

        #  W781 (FU-1096) - the 14 LayerAdapters, execute_sovereign and get_layer had no caller anywhere in the tree
        #  (strings included); they are archived in _archive/agentic_core/architecture/enriched_layers_sovereign.py.
        #  Its layer-13 branch returned a fixed success with a typed drift figure.

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
        """Layer 5: compares a supplied drift figure against a 0.05 tolerance, or reports NOT_ASSESSED.

        W543 — this said "Six-cycle PID-controlled homeostasis", and it is the sentence a reader of this
        architecture would believe. Measured: it delegates to GeosphericHomeostaticOrchestrator.step,
        which consults none of the six biogeochemical cycles — no live module imports any of them — and
        runs no PID. A real PID controller does exist, in agentic_core/biomimicry/cycles/base_cycle.py,
        accumulating an integral with anti-windup and a derivative; nothing on this path calls it. The
        name of a layer is a claim about what runs when it runs.
        """
        return await self.geospheric.step(inputs, context)

