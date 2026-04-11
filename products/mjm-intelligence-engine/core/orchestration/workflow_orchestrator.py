import logging
import os
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Union
from core.models import (
    MJMPhase, WorkflowState, EvidenceGraph, AnalysisDossier,
    ProposalPackage, MJMOutputBundle
)
from core.mushahida.engine import MushahidaEngine
from core.jaiza.engine import JaizaEngine
from core.muaina.engine import MuainaEngine
from core.genome_manager import GenomeManager
from core.provenance_graph import ProvenanceGraph
from core.learning.learning_engine import MJMLearningEngine, LearningSignal
from core.biomimetics.homeostasis_controller import HomeostasisController
from core.biomimetics.metabolism_manager import MetabolismManager
from core.security.zero_trust_manager import ZeroTrustSecurityManager
from core.security.runtime_attestation import RuntimeAttestationManager

logger = logging.getLogger(__name__)

class MJMWorkflowOrchestrator:
    """
    State machine governing MJM pipeline execution.
    - Supports synchronous single-user and asynchronous collaborative modes.
    - Checkpointing at each phase for auditability.
    """
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.checkpoints_dir = self.config.get("checkpoints_dir", "checkpoints")
        self.genomes = GenomeManager(self.config.get("genomes_dir", "config/domains"))
        self.provenance = ProvenanceGraph()
        self.learning = MJMLearningEngine(self.config.get("learning"))
        self.homeostasis = HomeostasisController(self.config.get("homeostasis"))
        self.metabolism = MetabolismManager()
        self.security = ZeroTrustSecurityManager()
        self.attestation = RuntimeAttestationManager()

        if not os.path.exists(self.checkpoints_dir):
            os.makedirs(self.checkpoints_dir)

        # Capture baseline for attestation
        self.attestation.capture_baseline([
            "core/orchestration/workflow_orchestrator.py",
            "core/models.py",
            "core/mushahida/engine.py"
        ])

    async def execute_pipeline(self, input_spec: Dict[str, Any], mode: str = "sync") -> MJMOutputBundle:
        """
        Executes the end-to-end MJM pipeline.
        - input_spec: {domain_id: str, queries: List[str], selected_option_id: Optional[str]}
        """
        domain_id = input_spec.get("domain_id", "default")
        queries = input_spec.get("queries", [])
        contributor = input_spec.get("contributor", "system")

        logger.info(f"Executing pipeline in {mode} mode for domain {domain_id}")

        # 1. Mushahida
        mush_id = await self.run_mushahida(domain_id, queries, contributor)
        mush_state = self._load_checkpoint(mush_id)
        evidence_graph = EvidenceGraph(**mush_state.data["evidence_graph"])

        # 2. Jaiza
        jaiza_id = await self.run_jaiza(mush_id, contributor)
        jaiza_state = self._load_checkpoint(jaiza_id)
        analysis_dossier = AnalysisDossier(**jaiza_state.data["analysis_dossier"])

        # 3. Muaina
        option_id = input_spec.get("selected_option_id") or analysis_dossier.strategic_options[0]["id"]
        muaina_id = await self.run_muaina(jaiza_id, option_id, contributor)
        muaina_state = self._load_checkpoint(muaina_id)
        proposal_package = ProposalPackage(**muaina_state.data["proposal_package"])

        bundle = MJMOutputBundle(
            evidence_graph=evidence_graph,
            analysis_dossier=analysis_dossier,
            proposal_package=proposal_package,
            provenance_json_ld=self.provenance.export_json_ld()
        )

        return bundle

    async def run_mushahida(self, domain_id: str, queries: List[str], contributor: str) -> str:
        domain_config = self.genomes.get_domain_config(domain_id)
        await self.metabolism.allocate_resources(domain_id, "mushahida")

        engine = MushahidaEngine(domain_config, self.provenance)
        graph = await engine.acquire_evidence_async(queries)

        self.homeostasis.update_metrics(domain_id, "mushahida", 1.0)

        state_data = {"domain_id": domain_id, "evidence_graph": graph.model_dump()}
        return self.checkpoint(MJMPhase.MUSHAHIDA, state_data, contributor)

    async def run_jaiza(self, checkpoint_id: str, contributor: str) -> str:
        prev_state = self._load_checkpoint(checkpoint_id)
        domain_id = prev_state.data["domain_id"]
        domain_config = self.genomes.get_domain_config(domain_id)
        await self.metabolism.allocate_resources(domain_id, "jaiza")

        engine = JaizaEngine(domain_config, self.provenance)
        graph = EvidenceGraph(**prev_state.data["evidence_graph"])
        dossier = await engine.analyze_async(graph)

        self.homeostasis.update_metrics(domain_id, "jaiza", 0.95)

        state_data = {
            "domain_id": domain_id,
            "evidence_graph": graph.model_dump(),
            "analysis_dossier": dossier.model_dump()
        }
        return self.checkpoint(MJMPhase.JAIZA, state_data, contributor)

    async def run_muaina(self, checkpoint_id: str, option_id: str, contributor: str) -> str:
        prev_state = self._load_checkpoint(checkpoint_id)
        domain_id = prev_state.data["domain_id"]
        domain_config = self.genomes.get_domain_config(domain_id)
        await self.metabolism.allocate_resources(domain_id, "muaina")

        engine = MuainaEngine(domain_config, self.provenance)
        dossier = AnalysisDossier(**prev_state.data["analysis_dossier"])
        package = engine.develop_proposal(dossier, option_id)

        # Trigger learning
        signal = LearningSignal(
            signal_type="EXECUTION_SUCCESS",
            domain_id=domain_id,
            workflow_checkpoint=checkpoint_id,
            outcome_data={"proposal_id": package.sha256},
            context={"contributor": contributor}
        )
        await self.learning.ingest_feedback(signal)

        self.homeostasis.update_metrics(domain_id, "muaina", 0.98)

        state_data = {
            "domain_id": domain_id,
            "evidence_graph": prev_state.data["evidence_graph"],
            "analysis_dossier": dossier.model_dump(),
            "proposal_package": package.model_dump()
        }
        return self.checkpoint(MJMPhase.MUAINA, state_data, contributor)

    def checkpoint(self, phase: MJMPhase, data: Dict[str, Any], contributor: str) -> str:
        """Persists workflow state to disk with integrity hash."""
        timestamp = int(datetime.now(timezone.utc).timestamp())
        checkpoint_id = f"CHK-{phase[:3].upper()}-{timestamp}"

        state = WorkflowState(
            checkpoint_id=checkpoint_id,
            phase=phase,
            data=data,
            contributor=contributor
        )
        state.calculate_hash()

        filepath = os.path.join(self.checkpoints_dir, f"{checkpoint_id}.json")
        with open(filepath, "w") as f:
            f.write(state.model_dump_json())

        logger.info(f"Checkpoint created: {checkpoint_id}")
        return checkpoint_id

    def collaborate_async(self, checkpoint_id: str, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generates GitHub-native instructions for asynchronous review/contribution."""
        state = self._load_checkpoint(checkpoint_id)

        instruction = f"""
## MJM Intelligence Engine: Async Contribution Request
**Phase:** {state.phase}
**Checkpoint ID:** `{checkpoint_id}`
**Contributor:** {user_context.get('name', 'Peer Reviewer')}

### Action Required:
Please review the generated {state.phase} output and provide feedback via comments or a PR.
- **Evidence Review:** Verify provenance of latest acquisitions.
- **Analysis Review:** Validate pattern detection and risk scoring.
- **Proposal Review:** Ensure roadmap feasibility.

**Branch Policy:** `feature/mjm-review-{checkpoint_id}`
"""
        return {
            "receipt_id": f"REC-{hashlib.sha256(checkpoint_id.encode()).hexdigest()[:8]}",
            "github_instruction": instruction,
            "pr_template": "mjm_contribution_v1.md"
        }

    def verify_output(self, output_bundle: MJMOutputBundle) -> Dict[str, Any]:
        """Performs cross-layer traceability and integrity verification."""
        results = {
            "integrity_pass": True,
            "traceability_pass": True,
            "checks": []
        }

        # 1. Integrity check
        if output_bundle.evidence_graph.sha256 != output_bundle.evidence_graph.calculate_hash():
            results["integrity_pass"] = False
            results["checks"].append("EvidenceGraph hash mismatch")

        # 2. Traceability check
        p_ref = output_bundle.proposal_package.analysis_ref
        a_hash = output_bundle.analysis_dossier.sha256
        if p_ref != a_hash:
            results["traceability_pass"] = False
            results["checks"].append(f"Proposal reference {p_ref} does not match Analysis hash {a_hash}")

        return results

    def _load_checkpoint(self, checkpoint_id: str) -> WorkflowState:
        filepath = os.path.join(self.checkpoints_dir, f"{checkpoint_id}.json")
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Checkpoint {checkpoint_id} not found.")
        with open(filepath, "r") as f:
            return WorkflowState.model_validate_json(f.read())
