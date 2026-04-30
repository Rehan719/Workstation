import os
from typing import Optional
from .adapters.entropy_regularised_gaas import EntropyRegularisedGaaS
from agentic_core.organism.gaas_validator_v4 import GaaSValidatorV4
from agentic_core.legal.precision_engine import UKLegalPrecisionEngineImpl

def get_gaas_validator(config: Optional[dict] = None):
    """
    Factory function for retrieving the active GaaS validator.
    Supports runtime selection of the entropy-regularised adapter via environment variable or config.
    """
    base_validator = GaaSValidatorV4(
        genome_path=os.getenv("GENOME_PATH", "configs/constitutional_genome_v138.yaml"),
        legal_path=os.getenv("LEGAL_PATH", "configs/legal_precision.yaml")
    )

    if os.getenv("MINIMISATION_GAAS_ENABLED", "true").lower() == "true":
        legal_engine = UKLegalPrecisionEngineImpl(
            rules_path=os.getenv("LEGAL_PATH", "configs/legal_precision.yaml")
        )
        return EntropyRegularisedGaaS(base_validator, legal_engine)

    return base_validator
