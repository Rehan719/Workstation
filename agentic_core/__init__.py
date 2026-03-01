"""
Jules AI v71.0 Beta – Living Synthesis Edition
Unified exports for the conscious biomimetic digital organism.
"""
__version__ = "71.0.0-beta"

# Layer 1: Molecular Triad
from .molecular.p53_oscillator import p53Oscillator
from .molecular.ubiquitin_system import UbiquitinSystem
from .molecular.hsp_network import HSPNetwork
from .molecular.triad_integration import TriadIntegrator as TriadIntegration
from .molecular.redox_sensor import RedoxSensor
from .molecular.atp_simulator import ATPSimulator as ATPsimulator

# Layer 2: Global Workspace & MCE
from .consciousness.global_workspace import GlobalWorkspace
from .consciousness.meta_cognitive_executive import MetaCognitiveExecutive
from .consciousness.gamma_coherence import GammaCoherenceMonitor
from .consciousness.ignition_detector import IgnitionDetector

# Layer 3: Genomic Registry
from .evolution.genomic_registry import GenomicRegistry
from .evolution.zkp_verifier import ZKPVerifier
from .evolution.heritability_tracker import HeritabilityTracker

# Layer 4: Governance
from .governance.sais_identity import SAISIdentity
from .governance.quorum_sensing import QuorumSensing
from .governance.danger_signaling import DangerSignaling

# Layer 5: Interface
from .interface.behavioral_proxies import BehavioralProxyPipeline as BehavioralProxies
from .interface.eeg_integration import EEGIntegration
from .interface.neuromorphic_cortex import NeuromorphicCortex

# Validation
from .validation.biomimetic_fidelity import BiomimeticFidelityScorer as BiomimeticFidelity
from .validation.phase_tracker import PhaseTracker

# Orchestrator
from .orchestration.conscious_organism_v70_0 import ConsciousOrganismV70_0 as ConsciousOrganismOrchestrator

# v71.0 Alpha Unified Orchestrator Export (Legacy support)
EnterpriseOrganism = ConsciousOrganismOrchestrator
ScholarshipOrchestrator = ConsciousOrganismOrchestrator

__all__ = [
    "p53Oscillator", "UbiquitinSystem", "HSPNetwork", "TriadIntegration",
    "GlobalWorkspace", "MetaCognitiveExecutive", "GenomicRegistry",
    "ConsciousOrganismOrchestrator", "BiomimeticFidelity"
]
