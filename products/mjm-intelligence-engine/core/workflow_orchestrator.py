import logging
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional, List
from .models import MJMPhase, WorkflowState, EvidenceGraph, AnalysisDossier, ProposalPackage
from .mushahida.engine import MushahidaEngine
from .jaiza.engine import JaizaEngine
from .muaina.engine import MuainaEngine

logger = logging.getLogger(__name__)

class MJMWorkflowOrchestrator:
    """
    State machine governing MJM pipeline execution.
    Supports checkpointing and phase transitions.
    """

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.mushahida = MushahidaEngine(self.config.get("mushahida"))
        self.jaiza = JaizaEngine(self.config.get("jaiza"))
        self.muaina = MuainaEngine(self.config.get("muaina"))
        self.checkpoints_dir = self.config.get("checkpoints_dir", "checkpoints")

        if not os.path.exists(self.checkpoints_dir):
            os.makedirs(self.checkpoints_dir)

    def run_mushahida(self, queries: List[str], contributor: str) -> str:
        """Executes Mushahida phase and returns checkpoint ID."""
        graph = self.mushahida.acquire_evidence(queries)
        state = WorkflowState(
            checkpoint_id=f"CHK-MUS-{int(datetime.utcnow().timestamp())}",
            phase=MJMPhase.MUSHAHIDA,
            data={"evidence_graph": graph.model_dump()},
            contributor=contributor
        )
        return self._save_checkpoint(state)

    def run_jaiza(self, checkpoint_id: str, contributor: str) -> str:
        """Executes Jaiza phase and returns checkpoint ID."""
        prev_state = self._load_checkpoint(checkpoint_id)
        if prev_state.phase != MJMPhase.MUSHAHIDA:
            raise ValueError("Jaiza phase must follow Mushahida.")

        graph = EvidenceGraph(**prev_state.data["evidence_graph"])
        dossier = self.jaiza.analyze(graph)

        state = WorkflowState(
            checkpoint_id=f"CHK-JAI-{int(datetime.utcnow().timestamp())}",
            phase=MJMPhase.JAIZA,
            data={
                "evidence_graph": graph.model_dump(),
                "analysis_dossier": dossier.model_dump()
            },
            contributor=contributor
        )
        return self._save_checkpoint(state)

    def run_muaina(self, checkpoint_id: str, selected_option_id: str, contributor: str) -> str:
        """Executes Muaina phase and returns checkpoint ID."""
        prev_state = self._load_checkpoint(checkpoint_id)
        if prev_state.phase != MJMPhase.JAIZA:
            raise ValueError("Muaina phase must follow Jaiza.")

        dossier = AnalysisDossier(**prev_state.data["analysis_dossier"])
        package = self.muaina.develop_proposal(dossier, selected_option_id)

        state = WorkflowState(
            checkpoint_id=f"CHK-MUA-{int(datetime.utcnow().timestamp())}",
            phase=MJMPhase.MUAINA,
            data={
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

    def get_provenance_trail(self, checkpoint_id: str) -> List[Dict[str, Any]]:
        """
        Traces back through checkpoints to provide a full audit trail.
        """
        # Simple v1.0 implementation: assume sequential checkpoints for now
        # In future, use checkpoint_id lineage
        return []
