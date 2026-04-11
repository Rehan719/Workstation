import os
from typing import List, Dict, Any, Optional

from .constitution.articles_parser import ConstitutionParser
from .constitution.compliance_checker import ComplianceChecker, EscalationManager, ConstitutionalViolation
from .constitution.constitutional_audit import ConstitutionalAudit
from .workstation.ai_ceo_client import AICEOClient
from .workstation.csuite_coordinator import CSuiteCoordinator, COEGatekeeper
from .workstation.quad_engine_bridge import QuadEngineBridge
from .workstation.bto_configurator import BTOConfigurator
from .intelligence.mycelial_router import MycelialRouter
from .intelligence.ant_colony_parallelizer import AntColonyParallelizer
from .intelligence.octopus_embodiment import OctopusArm
from .intelligence.immune_learner import ImmuneLearner
from .intelligence.injection_planner import InjectionPlanner
from .omnimedia.injector import OmnimediaInjector
from .omnimedia.decision_engine_v4 import OmnimediaDecisionEngineV4
from .constitutional.ueg_logger import UEGLogger

class OctoVeritasEngineV4:
    def __init__(self,
                 domain: str,
                 output_dir: str = "outputs/veritas-v4",
                 db_path: str = "outputs/v4_effectiveness.db"):
        self.domain = domain
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        # 1. Foundation & Logging
        self.ueg = UEGLogger(os.path.join(output_dir, "ueg_audit.jsonl"))
        self.decision_engine = OmnimediaDecisionEngineV4(db_path=db_path)

        # 2. Constitutional Layer
        self.parser = ConstitutionParser()
        self.articles = self.parser.load_articles()
        self.compliance = ComplianceChecker(self.articles)
        self.escalation = EscalationManager(self.ueg)
        self.audit = ConstitutionalAudit(self.ueg)

        # 3. Workstation Layer
        self.ceo = AICEOClient()
        self.csuite = CSuiteCoordinator()
        self.coe = COEGatekeeper()
        self.quad = QuadEngineBridge(self.ueg)
        self.bto = BTOConfigurator()

        # 4. Biomimetic Layer
        self.mycelial = MycelialRouter(self.ueg)
        self.ants = AntColonyParallelizer()
        self.arm = OctopusArm(domain, OmnimediaInjector(output_dir=output_dir))
        self.immune = ImmuneLearner(self.decision_engine, self.ueg)

        # 5. Injection Planner
        from .pipelines.registry import PipelineRegistry
        from .modes.mode_router import ModeRouter
        self.registry = PipelineRegistry()
        self.router = ModeRouter()
        self.planner = InjectionPlanner(self.registry, self.router, db_path)

    def produce_sovereign_package(self, assets: list, bto_config: dict = None):
        """
        Final v4.0 Orchestration: Constitutional, Biomimetic, and Strategic.
        """
        # A. BTO Configuration
        config = self.bto.validate_config(bto_config or {})
        mode = config.get("default_mode", "jaiza")
        self.router.set_mode(mode)

        # B. Quad Discovery
        discovered_assets = self.quad.discover(self.domain)
        all_assets = assets + discovered_assets

        # C. Strategic Priorities (AI CEO)
        priority = self.ceo.get_strategic_priority(self.domain)

        # D. Planning (Synthesize)
        plan = self.planner.plan_injection(all_assets, mode=mode, audience="all")

        # E. CoE Gatekeeping
        # We wrap the plan for CoE review
        review_plan = type('Plan', (), {
            'accessibility': all(a.get('accessibility', {}).get('alt_text') for a in assets),
            'hashed': all(a.get('hash') for a in assets)
        })
        coe_results = self.coe.approve_plan(review_plan)

        # F. Parallel Deployment
        def deploy_worker(job):
            # 1. Compliance Check (P0)
            action_context = {
                "jurisdiction": "Sovereign",
                "accessibility": job.asset.get('accessibility', {}),
                "logging_enabled": True,
                "ceo_approved": priority["strategic_alignment"] == "HIGH",
                "strategic_priority": "high" if priority["strategic_alignment"] == "HIGH" else "normal"
            }

            try:
                for art_id in ComplianceChecker.P0_ARTICLES:
                    self.compliance.check_compliance(art_id, action_context)
            except ConstitutionalViolation as e:
                self.escalation.escalate(e)
                return f"REJECTED: {str(e)}"

            # 2. Immune Memory Check
            if self.immune.is_pathogen_present({"format": job.format, "pipeline": job.pipeline, "mode": mode}):
                job.modifiers.append("PROACTIVE_FALLBACK")

            # 3. Resilient Injection (Mycelial)
            try:
                return self.mycelial.execute_with_resilience(job.format, self.arm.inject_asset, job)
            except Exception as e:
                self.immune.learn_from_failure("injection_failure", {"format": job.format, "pipeline": job.pipeline, "mode": mode})
                raise

        # Execute in parallel
        results = self.ants.execute_parallel(plan, deploy_worker)

        # G. Final Audit
        self.audit.log_injection_audit("v4_batch", ComplianceChecker.P0_ARTICLES, "SUCCESS", {"count": len(results)})

        return results
