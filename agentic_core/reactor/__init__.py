import logging
from .ecosystem.registry import ReactorRegistry

logger = logging.getLogger(__name__)

def initialize_reactor_ecosystem():
    """Initializes and registers all 50+ specialized sub-reactors for v120.0."""
    registry = ReactorRegistry()

    # Science (10)
    from .science.physics import PhysicsReactor
    from .science.chemistry import ChemistryReactor
    from .science.biology import BiologyReactor
    from .science.computer_science import ComputerScienceReactor
    from .science.materials_science import MaterialsScienceReactor
    from .science.astronomy import AstronomyReactor
    from .science.mathematics import MathematicsReactor
    from .science.engineering import EngineeringReactor
    from .science.environmental_science import EnvironmentalScienceReactor
    from .science.neuroscience import NeuroscienceReactor

    registry.register(PhysicsReactor())
    registry.register(ChemistryReactor())
    registry.register(BiologyReactor())
    registry.register(ComputerScienceReactor())
    registry.register(MaterialsScienceReactor())
    registry.register(AstronomyReactor())
    registry.register(MathematicsReactor())
    registry.register(EngineeringReactor())
    registry.register(EnvironmentalScienceReactor())
    registry.register(NeuroscienceReactor())

    # Religion (10)
    from .religion.quranic_studies import QuranicStudiesReactor
    from .religion.hadith_sciences import HadithSciencesReactor
    from .religion.fiqh import FiqhReactor
    from .religion.aqidah import AqidahReactor
    from .religion.sirah import SirahReactor
    from .religion.qiraat import QiraatReactor
    from .religion.dawah import DawahReactor
    from .religion.islamic_finance import IslamicFinanceReactor
    from .religion.islamic_history import IslamicHistoryReactor
    from .religion.tazkiyah import TazkiyahReactor

    registry.register(QuranicStudiesReactor())
    registry.register(HadithSciencesReactor())
    registry.register(FiqhReactor())
    registry.register(AqidahReactor())
    registry.register(SirahReactor())
    registry.register(QiraatReactor())
    registry.register(DawahReactor())
    registry.register(IslamicFinanceReactor())
    registry.register(IslamicHistoryReactor())
    registry.register(TazkiyahReactor())

    # Law (10)
    from .law.contract_law import ContractLawReactor
    from .law.corporate_law import CorporateLawReactor
    from .law.intellectual_property import IntellectualPropertyReactor
    from .law.litigation import LitigationReactor
    from .law.regulatory_compliance import RegulatoryComplianceReactor
    from .law.tax_law import TaxLawReactor
    from .law.employment_law import EmploymentLawReactor
    from .law.international_law import InternationalLawReactor
    from .law.family_law import FamilyLawReactor
    from .law.criminal_law import CriminalLawReactor

    registry.register(ContractLawReactor())
    registry.register(CorporateLawReactor())
    registry.register(IntellectualPropertyReactor())
    registry.register(LitigationReactor())
    registry.register(RegulatoryComplianceReactor())
    registry.register(TaxLawReactor())
    registry.register(EmploymentLawReactor())
    registry.register(InternationalLawReactor())
    registry.register(FamilyLawReactor())
    registry.register(CriminalLawReactor())

    # Career (10)
    from .career.resume import ResumeReactor
    from .career.cover_letter import CoverLetterReactor
    from .career.linkedin import LinkedinReactor
    from .career.interview import InterviewReactor
    from .career.career_path import CareerPathReactor
    from .career.job_search import JobSearchReactor
    from .career.skill_development import SkillDevelopmentReactor
    from .career.personal_branding import PersonalBrandingReactor
    from .career.entrepreneurship import EntrepreneurshipReactor
    from .career.remote_work import RemoteWorkReactor

    registry.register(ResumeReactor())
    registry.register(CoverLetterReactor())
    registry.register(LinkedinReactor())
    registry.register(InterviewReactor())
    registry.register(CareerPathReactor())
    registry.register(JobSearchReactor())
    registry.register(SkillDevelopmentReactor())
    registry.register(PersonalBrandingReactor())
    registry.register(EntrepreneurshipReactor())
    registry.register(RemoteWorkReactor())

    # Education (10)
    from .education.k12 import K12Reactor
    from .education.higher_education import HigherEducationReactor
    from .education.vocational import VocationalReactor
    from .education.language_learning import LanguageLearningReactor
    from .education.stem import StemReactor
    from .education.humanities import HumanitiesReactor
    from .education.special_education import SpecialEducationReactor
    from .education.teacher_support import TeacherSupportReactor
    from .education.educational_policy import EducationalPolicyReactor
    from .education.lifelong_learning import LifelongLearningReactor

    registry.register(K12Reactor())
    registry.register(HigherEducationReactor())
    registry.register(VocationalReactor())
    registry.register(LanguageLearningReactor())
    registry.register(StemReactor())
    registry.register(HumanitiesReactor())
    registry.register(SpecialEducationReactor())
    registry.register(TeacherSupportReactor())
    registry.register(EducationalPolicyReactor())
    registry.register(LifelongLearningReactor())

    logger.info("Ecosystem: All 50 specialized sub-reactors registered successfully for v120.0.")
    return registry
