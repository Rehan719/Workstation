import logging
from .ecosystem.registry import ReactorRegistry
from .ecosystem.factory import get_factory_reactor

logger = logging.getLogger(__name__)

def initialize_reactor_ecosystem():
    """
    ARTICLE 298-302: Initializes and registers all 50+ specialized sub-reactors for v120.0.
    Uses Anchor Reactors for high-fidelity domains and Factory for the remaining ecosystem.
    """
    registry = ReactorRegistry()

    # Anchor Reactors (High-Fidelity Implementation)
    from .religion.quranic_studies import QuranicStudiesReactor
    from .law.contract_law import ContractLawReactor
    from .career.career_path import CareerPathReactor
    from .education.k12 import K12Reactor

    registry.register(QuranicStudiesReactor())
    registry.register(ContractLawReactor())
    registry.register(CareerPathReactor())
    registry.register(K12Reactor())

    # Factory-Specialized Reactors (Remaining 46+)
    # Science (10)
    registry.register(get_factory_reactor("science", "physics", "Twin of physical systems; PDE simulations."))
    registry.register(get_factory_reactor("science", "chemistry", "Molecular dynamics; reaction twinning."))
    registry.register(get_factory_reactor("science", "biology", "Genomic twinning; metabolic modeling."))
    registry.register(get_factory_reactor("science", "computer_science", "Algorithm twinning; complexity analysis."))
    registry.register(get_factory_reactor("science", "materials_science", "Lattice simulation; stress testing."))
    registry.register(get_factory_reactor("science", "astronomy", "Orbital mechanics; stellar evolution."))
    registry.register(get_factory_reactor("science", "mathematics", "Theorem proving; topology visualization."))
    registry.register(get_factory_reactor("science", "engineering", "Structural twinning; CAD integration."))
    registry.register(get_factory_reactor("science", "environmental_science", "Climate modeling; ecosystem twinning."))
    registry.register(get_factory_reactor("science", "neuroscience", "Neural mapping; synaptic simulation."))

    # Religion (9 Remaining)
    registry.register(get_factory_reactor("religion", "hadith_sciences", "Chain validation; semantic authenticity."))
    registry.register(get_factory_reactor("religion", "fiqh", "Legal precedent twinning; deductive reasoning."))
    registry.register(get_factory_reactor("religion", "aqidah", "Theological consistency; logical mapping."))
    registry.register(get_factory_reactor("religion", "sirah", "Historical timeline; context twinning."))
    registry.register(get_factory_reactor("religion", "qiraat", "Phonetic analysis; variation mapping."))
    registry.register(get_factory_reactor("religion", "dawah", "Discourse modeling; message optimization."))
    registry.register(get_factory_reactor("religion", "islamic_finance", "Sharia compliance; economic twinning."))
    registry.register(get_factory_reactor("religion", "islamic_history", "Civilization modeling; cause-effect analysis."))
    registry.register(get_factory_reactor("religion", "tazkiyah", "Ethical modeling; behavioral feedback."))

    # Law (9 Remaining)
    registry.register(get_factory_reactor("law", "corporate_law", "Entity twinning; compliance modeling."))
    registry.register(get_factory_reactor("law", "intellectual_property", "Patent mapping; infringement analysis."))
    registry.register(get_factory_reactor("law", "litigation", "Case strategy twinning; outcome prediction."))
    registry.register(get_factory_reactor("law", "regulatory_compliance", "Rule-based audit; risk twinning."))
    registry.register(get_factory_reactor("law", "tax_law", "Liability twinning; optimization simulation."))
    registry.register(get_factory_reactor("law", "employment_law", "Policy twinning; labor dispute modeling."))
    registry.register(get_factory_reactor("law", "international_law", "Treaty mapping; jurisdictional twinning."))
    registry.register(get_factory_reactor("law", "family_law", "Asset division; mediation simulation."))
    registry.register(get_factory_reactor("law", "criminal_law", "Evidence mapping; procedural twinning."))

    # Career (9 Remaining)
    registry.register(get_factory_reactor("career", "resume", "ATS optimization; impact twinning."))
    registry.register(get_factory_reactor("career", "cover_letter", "Persuasion modeling; tone optimization."))
    registry.register(get_factory_reactor("career", "linkedin", "Network twinning; visibility simulation."))
    registry.register(get_factory_reactor("career", "interview", "Scenario simulation; feedback modeling."))
    registry.register(get_factory_reactor("career", "job_search", "Market twinning; automated discovery."))
    registry.register(get_factory_reactor("career", "skill_development", "Learning path; competency twinning."))
    registry.register(get_factory_reactor("career", "personal_branding", "Identity twinning; reputation simulation."))
    registry.register(get_factory_reactor("career", "entrepreneurship", "Business model; venture twinning."))
    registry.register(get_factory_reactor("career", "remote_work", "Digital nomad; productivity twinning."))

    # Education (9 Remaining)
    registry.register(get_factory_reactor("education", "higher_education", "Academic path; research twinning."))
    registry.register(get_factory_reactor("education", "vocational", "Skill mastery; apprentice modeling."))
    registry.register(get_factory_reactor("education", "language_learning", "Fluency twinning; immersion simulation."))
    registry.register(get_factory_reactor("education", "stem", "Curriculum twinning; lab simulation."))
    registry.register(get_factory_reactor("education", "humanities", "Cultural mapping; critical twinning."))
    registry.register(get_factory_reactor("education", "special_education", "Individualized path; adaptive twinning."))
    registry.register(get_factory_reactor("education", "teacher_support", "Instructional design; classroom twinning."))
    registry.register(get_factory_reactor("education", "educational_policy", "Systemic modeling; outcome prediction."))
    registry.register(get_factory_reactor("education", "lifelong_learning", "Knowledge graph; wisdom twinning."))

    logger.info("Ecosystem: v120.0 Apotheosis Reactor Constellation (50+) initialized via Hybrid Anchor-Factory model.")
    return registry
