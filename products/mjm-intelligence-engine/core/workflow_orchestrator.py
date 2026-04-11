import logging
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from core.models import MJMPhase, WorkflowState, EvidenceGraph, AnalysisDossier, ProposalPackage
from core.mushahida.engine import MushahidaEngine
from core.jaiza.engine import JaizaEngine
from core.muaina.engine import MuainaEngine
from core.genome_manager import GenomeManager
from core.provenance_graph import ProvenanceGraph
from core.learning_engine import MJMLearningEngine

logger = logging.getLogger(__name__)

class MJMWorkflowOrchestrator:
    """
    Biomimetic state machine governing MJM pipeline execution.
    Handles domain routing and learning integration.
    """
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.genomes = GenomeManager(self.config.get("genomes_dir", "config/domains"))
        self.provenance = ProvenanceGraph()
        self.learning = MJMLearningEngine(self.config.get("learning"))
        self.checkpoints_dir = self.config.get("checkpoints_dir", "checkpoints")

        if not os.path.exists(self.checkpoints_dir):
            os.makedirs(self.checkpoints_dir)

    def _get_engines(self, domain_id: str):
        domain_config = self.genomes.get_domain_config(domain_id)
        return (
            MushahidaEngine(domain_config, self.provenance),
            JaizaEngine(domain_config, self.provenance),
            MuainaEngine(domain_config, self.provenance)
        )

    def run_mushahida(self, domain_id: str, queries: List[str], contributor: str) -> str:
        mush, _, _ = self._get_engines(domain_id)
        graph = mush.acquire_evidence(queries)

        state = WorkflowState(
            checkpoint_id=f"CHK-MUS-{int(datetime.utcnow().timestamp())}",
            phase=MJMPhase.MUSHAHIDA,
            data={"domain_id": domain_id, "evidence_graph": graph.model_dump()},
            contributor=contributor
        )
        return self._save_checkpoint(state)

    def run_jaiza(self, checkpoint_id: str, contributor: str) -> str:
        prev_state = self._load_checkpoint(checkpoint_id)
        domain_id = prev_state.data["domain_id"]
        _, jaiza, _ = self._get_engines(domain_id)

        graph = EvidenceGraph(**prev_state.data["evidence_graph"])
        dossier = jaiza.analyze(graph)

        state = WorkflowState(
            checkpoint_id=f"CHK-JAI-{int(datetime.utcnow().timestamp())}",
            phase=MJMPhase.JAIZA,
            data={
                "domain_id": domain_id,
                "evidence_graph": graph.model_dump(),
                "analysis_dossier": dossier.model_dump()
            },
            contributor=contributor
        )
        return self._save_checkpoint(state)

    def run_muaina(self, checkpoint_id: str, option_id: str, contributor: str) -> str:
        prev_state = self._load_checkpoint(checkpoint_id)
        domain_id = prev_state.data["domain_id"]
        _, _, muaina = self._get_engines(domain_id)

        dossier = AnalysisDossier(**prev_state.data["analysis_dossier"])
        package = muaina.develop_proposal(dossier, option_id)

        state = WorkflowState(
            checkpoint_id=f"CHK-MUA-{int(datetime.utcnow().timestamp())}",
            phase=MJMPhase.MUAINA,
            data={
                "domain_id": domain_id,
                "evidence_graph": prev_state.data["evidence_graph"],
                "analysis_dossier": dossier.model_dump(),
                "proposal_package": package.model_dump()
            },
            contributor=contributor
        )
        return self._save_checkpoint(state)

    def _save_checkpoint(self, state: WorkflowState) -> str:
        filepath = os.path.join(self.checkpoints_dir, f"{state.checkpoint_id}.json")
        with open(filepath, "w") as f:
            f.write(state.model_dump_json())
        return state.checkpoint_id

    def _load_checkpoint(self, checkpoint_id: str) -> WorkflowState:
        filepath = os.path.join(self.checkpoints_dir, f"{checkpoint_id}.json")
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Checkpoint {checkpoint_id} not found.")
        with open(filepath, "r") as f:
            return WorkflowState.model_validate_json(f.read())
