from .scientific_research_pipeline import ScientificResearchPipeline
from .legal_services_pipeline import LegalServicesPipeline
from .religious_research_pipeline import ReligiousResearchPipeline

class BusinessPipeline:
    def __init__(self):
        self.science = ScientificResearchPipeline()
        self.legal = LegalServicesPipeline()
        self.religion = ReligiousResearchPipeline()
