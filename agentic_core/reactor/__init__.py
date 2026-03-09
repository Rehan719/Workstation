import logging
from .science.physics import PhysicsReactor
from .science.chemistry import ChemistryReactor
from .science.biology import BiologyReactor
from .science.compsci import CompSciReactor
from .science.materials import MaterialsReactor
from .science.astronomy import AstronomyReactor
from .science.math import MathReactor
from .science.interdisciplinary import InterdisciplinaryReactor
from .science.engineering import EngineeringReactor
from .science.environmental import EnvironmentalReactor
from .science.neuroscience import NeuroscienceReactor

from .religion.tafsir import TafsirReactor
from .religion.hadith import HadithReactor
from .religion.fiqh import FiqhReactor
from .religion.aqidah import AqidahReactor
from .religion.sirah import SirahReactor
from .religion.qiraat import QiraatReactor
from .religion.dawah import DawahReactor
from .religion.islamic_finance import IslamicFinanceReactor
from .religion.history import IslamicHistoryReactor
from .religion.tazkiyah import TazkiyahReactor

from .law.contract import ContractReactor
from .law.corporate import CorporateLawReactor
from .law.ip import IPLawReactor
from .law.litigation import LitigationReactor
from .law.regulatory import RegulatoryReactor
from .law.tax import TaxLawReactor
from .law.employment import EmploymentLawReactor
from .law.international import InternationalLawReactor
from .law.family import FamilyLawReactor
from .law.criminal import CriminalLawReactor

from .employment.resume import ResumeReactor
from .employment.cover_letter import CoverLetterReactor
from .employment.linkedin import LinkedInReactor
from .employment.interview import InterviewReactor
from .employment.career_path import CareerPathReactor
from .employment.job_search import JobSearchReactor
from .employment.skill_dev import SkillDevReactor
from .employment.branding import BrandingReactor
from .employment.freelance import FreelanceReactor
from .employment.entrepreneurship import EntrepreneurshipReactor

from .education.k12 import K12Reactor
from .education.higher_ed import HigherEdReactor
from .education.vocational import VocationalReactor
from .education.language import LanguageReactor
from .education.stem import STEMReactor
from .education.humanities import HumanitiesReactor
from .education.special_ed import SpecialEdReactor
from .education.teacher import TeacherReactor
from .education.parent import ParentReactor
from .education.policy import PolicyReactor
from .education.assessment import AssessmentReactor
from .education.curriculum import CurriculumReactor
from .education.edtech import EdTechReactor
from .education.early_childhood import EarlyChildhoodReactor
from .education.lifelong import LifelongLearningReactor
from .education.analytics import LearningAnalyticsReactor

from .ecosystem.registry import ReactorRegistry

logger = logging.getLogger(__name__)

def initialize_reactor_ecosystem():
    """Initializes and registers all 40+ specialized sub-reactors."""
    registry = ReactorRegistry()

    # Science (10)
    registry.register(PhysicsReactor())
    registry.register(ChemistryReactor())
    registry.register(BiologyReactor())
    registry.register(CompSciReactor())
    registry.register(MaterialsReactor())
    registry.register(AstronomyReactor())
    registry.register(MathReactor())
    registry.register(InterdisciplinaryReactor())
    registry.register(EngineeringReactor())
    registry.register(EnvironmentalReactor())
    registry.register(NeuroscienceReactor())

    # Religion (10)
    registry.register(TafsirReactor())
    registry.register(HadithReactor())
    registry.register(FiqhReactor())
    registry.register(AqidahReactor())
    registry.register(SirahReactor())
    registry.register(QiraatReactor())
    registry.register(DawahReactor())
    registry.register(IslamicFinanceReactor())
    registry.register(IslamicHistoryReactor())
    registry.register(TazkiyahReactor())

    # Law (10)
    registry.register(ContractReactor())
    registry.register(CorporateLawReactor())
    registry.register(IPLawReactor())
    registry.register(LitigationReactor())
    registry.register(RegulatoryReactor())
    registry.register(TaxLawReactor())
    registry.register(EmploymentLawReactor())
    registry.register(InternationalLawReactor())
    registry.register(FamilyLawReactor())
    registry.register(CriminalLawReactor())

    # Employment (10)
    registry.register(ResumeReactor())
    registry.register(CoverLetterReactor())
    registry.register(LinkedInReactor())
    registry.register(InterviewReactor())
    registry.register(CareerPathReactor())
    registry.register(JobSearchReactor())
    registry.register(SkillDevReactor())
    registry.register(BrandingReactor())
    registry.register(FreelanceReactor())
    registry.register(EntrepreneurshipReactor())

    # Education (16)
    registry.register(K12Reactor())
    registry.register(HigherEdReactor())
    registry.register(VocationalReactor())
    registry.register(LanguageReactor())
    registry.register(STEMReactor())
    registry.register(HumanitiesReactor())
    registry.register(SpecialEdReactor())
    registry.register(TeacherReactor())
    registry.register(ParentReactor())
    registry.register(PolicyReactor())
    registry.register(AssessmentReactor())
    registry.register(CurriculumReactor())
    registry.register(EdTechReactor())
    registry.register(EarlyChildhoodReactor())
    registry.register(LifelongLearningReactor())
    registry.register(LearningAnalyticsReactor())

    logger.info("Ecosystem: All 57 specialized sub-reactors registered successfully.")
    return registry
