import os
from .regulator import Regulator
from .reconfigulator import Reconfigulator

# Feature Flag for Legacy v2 implementations
FEATURE_FLAG_MINIMISATION_V2 = os.getenv("FEATURE_FLAG_MINIMISATION_V2", "False").lower() == "true"

def get_regulator(ueg_logger=None):
    if FEATURE_FLAG_MINIMISATION_V2:
        try:
            from .v2.regulator_v2 import RegulatorV2
            return RegulatorV2(ueg_logger)
        except ImportError:
            return Regulator(ueg_logger)
    return Regulator(ueg_logger)

def get_reconfigulator(ueg_logger=None):
    if FEATURE_FLAG_MINIMISATION_V2:
        try:
            from .v2.reconfigulator_v2 import ReconfigulatorV2
            return ReconfigulatorV2(ueg_logger)
        except ImportError:
            return Reconfigulator(ueg_logger)
    return Reconfigulator(ueg_logger)
