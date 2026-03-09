import logging
from .science.physics import PhysicsReactor
from .science.chemistry import ChemistryReactor
from .science.biology import BiologyReactor
from .science.compsci import CompSciReactor
from .science.materials import MaterialsReactor
from .science.astronomy import AstronomyReactor
from .science.math import MathReactor
from .science.interdisciplinary import InterdisciplinaryReactor

from .religion.tafsir import TafsirReactor
from .religion.hadith import HadithReactor
from .religion.fiqh import FiqhReactor
from .religion.aqidah import AqidahReactor
from .religion.sirah import SirahReactor
from .religion.qiraat import QiraatReactor
from .religion.dawah import DawahReactor
from .religion.islamic_finance import IslamicFinanceReactor

from .law.contract import ContractReactor
from .law.corporate import CorporateLawReactor
from .law.ip import IPLawReactor
from .law.litigation import LitigationReactor
from .law.regulatory import RegulatoryReactor
from .law.tax import TaxLawReactor
from .law.employment import EmploymentLawReactor
from .law.international import InternationalLawReactor

from .employment.resume import ResumeReactor
from .employment.cover_letter import CoverLetterReactor
from .employment.linkedin import LinkedInReactor
from .employment.interview import InterviewReactor
from .employment.career_path import CareerPathReactor
from .employment.job_search import JobSearchReactor
from .employment.skill_dev import SkillDevReactor
from .employment.branding import BrandingReactor

from .education.k12 import K12Reactor
from .education.higher_ed import HigherEdReactor
from .education.vocational import VocationalReactor
from .education.language import LanguageReactor
from .education.stem import STEMReactor
from .education.humanities import HumanitiesReactor
from .education.special_ed import SpecialEdReactor
from .education.teacher import TeacherReactor

from .ecosystem.registry import ReactorRegistry

logger = logging.getLogger(__name__)

def initialize_reactor_ecosystem():
    """Initializes and registers all 40+ specialized sub-reactors."""
    registry = ReactorRegistry()

    # Science (8)
    registry.register(PhysicsReactor())
    registry.register(ChemistryReactor())
    registry.register(BiologyReactor())
    registry.register(CompSciReactor())
    registry.register(MaterialsReactor())
    registry.register(AstronomyReactor())
    registry.register(MathReactor())
    registry.register(InterdisciplinaryReactor())

    # Religion (8)
    registry.register(TafsirReactor())
    registry.register(HadithReactor())
    registry.register(FiqhReactor())
    registry.register(AqidahReactor())
    registry.register(SirahReactor())
    registry.register(QiraatReactor())
    registry.register(DawahReactor())
    registry.register(IslamicFinanceReactor())

    # Law (8)
    registry.register(ContractReactor())
    registry.register(CorporateLawReactor())
    registry.register(IPLawReactor())
    registry.register(LitigationReactor())
    registry.register(RegulatoryReactor())
    registry.register(TaxLawReactor())
    registry.register(EmploymentLawReactor())
    registry.register(InternationalLawReactor())

    # Employment (8)
    registry.register(ResumeReactor())
    registry.register(CoverLetterReactor())
    registry.register(LinkedInReactor())
    registry.register(InterviewReactor())
    registry.register(CareerPathReactor())
    registry.register(JobSearchReactor())
    registry.register(SkillDevReactor())
    registry.register(BrandingReactor())

    # Education (8)
    registry.register(K12Reactor())
    registry.register(HigherEdReactor())
    registry.register(VocationalReactor())
    registry.register(LanguageReactor())
    registry.register(STEMReactor())
    registry.register(HumanitiesReactor())
    registry.register(SpecialEdReactor())
    registry.register(TeacherReactor())

    logger.info("Ecosystem: All 40+ specialized sub-reactors registered successfully.")
    return registry
