from typing import Any, Dict, List, Optional
import asyncio
import yaml
import os
from .base_agent import BaseAgent
from .protocols.samp import SAMPMessage
from .quantum_ai.hierarchy_manager import CapabilityHierarchyManager
from .interface.hybrid_granularity_controller import HybridGranularityController
from .tools.context_aware_integrator import ContextAwareToolIntegrator
from .infrastructure.quantum_ir_compiler import QuantumIRCompiler
from .security.sigstore_handler import SigstoreHandler
from .collaboration.workspace_manager import WorkspaceManager
from .pedagogy.pedagogy_engine import PedagogyEngine
from .collaboration.version_control import VersionControlManager
from .observatory.observatory import Observatory
from .evidence.unified_evidence_graph import UnifiedEvidenceGraph
from .causal.causal_reasoning_engine import CausalReasoningEngine
from .confidence.conformal_predictor import ConformalPredictor
from .collaboration.xr_workspace import XRWorkspaceManager
from .communication.translation_engine import NeuralTranslationEngine
from .learning.continual_learner import ContinualMetaLearner
from .reasoning.deepseek_adapter import DeepSeekR1Adapter
from .reasoning.qwen_adapter import Qwen25Adapter
from agents.research.literature_synthesizer import LiteratureSynthesizer
from agents.writing.manuscript_architect import ManuscriptArchitect
from agents.visualization.figure_generator import FigureGenerator
from agents.presentation.slide_maestro import SlideMaestro
from agents.audio.tts_synthesizer import TTSSynthesizer
from agents.video.scene_assembler import SceneAssembler
from agents.quality.vlm_critic import VLMCritic
from agents.quality.plagiarism_detector import PlagiarismDetector

class Orchestrator(BaseAgent):
    """
    v40.0 Orchestrator Agent: Universal collaborative intelligence.
    Integrates Evidence Graphs (Article AU), Causal Reasoning (Article AO),
    and Conformal Calibration (Article AV).
    """
    def __init__(self, agent_id: str = "orchestrator.v40", config: Optional[Dict[str, Any]] = None):
        super().__init__(agent_id, config)
        self.workers: Dict[str, BaseAgent] = {}

        # v40.0 Intelligence Amplifiers
        self.register_worker(DeepSeekR1Adapter())
        self.register_worker(Qwen25Adapter())

        # v40.0 Strategic Workers
        self.register_worker(LiteratureSynthesizer())
        self.register_worker(ManuscriptArchitect())
        self.register_worker(FigureGenerator())
        self.register_worker(SlideMaestro())
        self.register_worker(TTSSynthesizer())
        self.register_worker(SceneAssembler())
        self.register_worker(VLMCritic())
        self.register_worker(PlagiarismDetector())

        # v40.0 Advanced Engines
        self.ueg = UnifiedEvidenceGraph()
        self.causal_engine = CausalReasoningEngine()
        self.conformal_predictor = ConformalPredictor()
        self.xr_manager = XRWorkspaceManager()
        self.translation_engine = NeuralTranslationEngine()
        self.continual_learner = ContinualMetaLearner()

        # Legacy v34.0/v36.0 Engines
        self.hierarchy_manager = CapabilityHierarchyManager()
        self.granularity_controller = HybridGranularityController()
        self.tool_integrator = ContextAwareToolIntegrator()
        self.ir_compiler = QuantumIRCompiler()
        self.sigstore = SigstoreHandler()
        self.workspace_manager = WorkspaceManager()
        self.pedagogy_engine = PedagogyEngine()
        self.version_control = VersionControlManager()
        self.observatory = Observatory()

    def register_worker(self, worker: BaseAgent):
        self.workers[worker.agent_id] = worker
        self.log(f"Registered worker: {worker.agent_id}")

    async def execute(self, task: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Decomposes a high-level goal into subtasks and coordinates execution with v34.0 enhancements.
        """
        self.log(f"Starting C-IV orchestration for task: {task.get('goal', 'No goal specified')}")

        # v34.0 Article X: Pedagogy Support
        user_id = (context or {}).get('user_id', 'default')
        if task.get('learning_mode'):
            hint = await self.pedagogy_engine.get_contextual_hint(user_id, task)
            if hint: self.log(f"Pedagogy Hint: {hint}")

        # v34.0 Article S: Process Granularity Signals
        if context and 'interaction' in context:
            await self.granularity_controller.process_interaction(context.get('user_id', 'default'), context['interaction'])

        # v31.0 Article R: Check Hierarchy Prerequisites
        target_tier = task.get('tier', 'tier1')
        await self.hierarchy_manager.ensure_tier_prerequisites(target_tier)

        # 1. Plan (Goal Decomposition)
        plan = await self._plan(task)
        self.log(f"Generated execution plan with {len(plan)} subtasks")

        # v40.0 Causal Identification
        if task.get("causal_inference"):
            discovery = self.causal_engine.identify_causal_effect(task['goal'], "output", {})
            self.log(discovery)

        # 2. Execute subtasks with Context-Aware Tooling and Dynamic Hybrid Orchestration
        results = {}
        for subtask in plan:
            # Dynamic Hybrid Selection
            framework = self._select_framework(subtask)
            subtask['framework'] = framework
            self.log(f"Selected framework '{framework}' for subtask: {subtask['id']}")

            # v33.0 Article U: Hierarchical Compilation
            if subtask.get("type") == "quantum_circuit":
                self.log(f"Routing subtask {subtask['id']} through Hierarchical Compiler Pipeline")
                backend_ir = await self.ir_compiler.compile(
                    subtask.get("circuit"),
                    subtask.get("framework"),
                    subtask.get("target_backend", "ibm"),
                    context or {}
                )
                subtask['backend_ir'] = backend_ir

            # Activate toolchain if needed
            enhanced_task = await self.tool_integrator.process_task(subtask)
            subtask.update(enhanced_task)

            worker_id = subtask.get("assigned_agent") or subtask.get("agent")
            if worker_id in self.workers:
                self.log(f"Delegating subtask '{subtask['id']}' to {worker_id} via {framework} (Tools: {subtask.get('tools_used', [])})")

                # Execution
                result = await self.workers[worker_id].execute(subtask, context)

                # v40.0 Conformal Calibration
                if 'confidence_score' in result:
                    result['calibration'] = self.conformal_predictor.predict_with_interval(
                        result.get('output'), result['confidence_score']
                    )

                # v40.0 UEG Trace
                self.ueg.add_evidence(worker_id, subtask['id'], "EXECUTES")

                results[subtask["id"]] = result
            else:
                self.log(f"No worker registered for agent type: {worker_id}", level="ERROR")

        # 3. Aggregate results
        final_output = self._aggregate(results)

        # Sign final artifact if requested (Article T)
        if task.get('produces_artifact'):
            signing_result = await self.tool_integrator.process_task({**task, 'artifact_data': final_output})
            final_output['metadata'] = signing_result

        return final_output

    async def _plan(self, task: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Dynamic planning: selects a workflow based on task type or uses LLM reasoning.
        """
        task_type = task.get("type", "scientific_publication")

        if task_type == "agent_direct":
            return [task]
        workflow_path = f"config/workflows/{task_type}.yaml"

        if os.path.exists(workflow_path):
            self.log(f"Loading workflow from {workflow_path}")
            with open(workflow_path, 'r') as f:
                workflow = yaml.safe_load(f)
                return workflow.get("steps", [])

        # Fallback to simple static planning
        goal = task.get("goal", "").lower()
        if "paper" in goal or "manuscript" in goal:
            return [
                {"id": "lit_review", "assigned_agent": "research.literature.v3", "query": goal},
                {"id": "drafting", "assigned_agent": "writing.manuscript.architect.v4", "content": "${lit_review}"}
            ]
        return []

    def _select_framework(self, subtask: Dict[str, Any]) -> str:
        """
        Dynamic Framework Router: Selects the optimal agentic framework based on task complexity,
        interaction patterns, and statefulness requirements.
        """
        task_type = subtask.get("type", "").lower()
        description = subtask.get("description", "").lower()
        goal = subtask.get("goal", "").lower()

        # Rule-based routing logic (Article: Dynamic Hybrid Orchestration)
        if any(keyword in description or keyword in goal for keyword in ["conversation", "brainstorm", "multi-agent chat"]):
            return "AutoGen"
        elif any(keyword in task_type or keyword in goal for keyword in ["role-based", "crew", "organization"]):
            return "CrewAI"
        elif any(keyword in task_type or keyword in description for keyword in ["stateful", "cyclical", "graph", "non-linear"]):
            return "LangGraph"
        elif "gui" in description or "procedural" in description:
            return "PC-Agent"

        # Enterprise-grade routing for monitored apps
        if subtask.get("enterprise_mode"):
            return "Microsoft Agent Framework"

        # Default to the foundational hierarchical model
        return "PC-Agent"

    def _aggregate(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Aggregates results from workers.
        """
        return {
            "status": "completed",
            "components": results
        }

if __name__ == "__main__":
    # Entry point for the orchestrator service
    orchestrator = Orchestrator()
    print("🚀 Jules AI C-IV Orchestrator Service is running...")

    async def main_loop():
        while True:
            # In a real system, this would listen to a message queue (RabbitMQ/Redis)
            await asyncio.sleep(60)

    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        print("Stopping Orchestrator...")
