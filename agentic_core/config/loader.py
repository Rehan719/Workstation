import os
import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class ConfigLoader:
    """
    ARTICLE 150: Centralized configuration management for v99.0 Workstation.
    Supports environment variables, JSON files, and default values.
    """
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or os.getenv("JULES_CONFIG_PATH", "config/settings.json")
        self.config: Dict[str, Any] = self._load_defaults()
        self._load_from_file()
        self._load_from_env()

    def _load_defaults(self) -> Dict[str, Any]:
        """Loads baseline default values."""
        return {
            "AGENT_ID": f"transcendent-{os.urandom(4).hex()}",
            "VERSION": "99.0.0",
            "LOG_LEVEL": "INFO",
            "SIH_ATP_THRESHOLD": 2.5,
            "FIDELITY_TARGET": 0.992,
            "API_PORT": 8000,
            "DB_URL": "sqlite:///workstation.db",
            "JWT_SECRET": os.getenv("JULES_JWT_SECRET", None),
            "RATE_LIMIT_CONNECTOR": 100,
            "TRANSITION_PHASES": 5
        }

    def _load_from_file(self):
        """Loads configuration from a JSON file if it exists."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    file_config = json.load(f)
                    self.config.update(file_config)
                    logger.info(f"ConfigLoader: Loaded configuration from {self.config_path}")
            except Exception as e:
                logger.error(f"ConfigLoader: Failed to load config file: {str(e)}")

    def _load_from_env(self):
        """Overrides configuration values from environment variables."""
        for key in self.config.keys():
            env_val = os.getenv(f"JULES_{key}")
            if env_val:
                # Type casting based on default value type
                default_type = type(self.config[key])
                try:
                    self.config[key] = default_type(env_val)
                    logger.debug(f"ConfigLoader: Overriding {key} from environment.")
                except:
                    logger.error(f"ConfigLoader: Env override failed for {key}. Check type mismatch.")

    def get(self, key: str, default: Any = None) -> Any:
        """Returns the configuration value for the specified key."""
        return self.config.get(key, default)

    def set_override(self, key: str, value: Any):
        """Dynamically overrides a configuration value (in-memory only)."""
        self.config[key] = value
        logger.info(f"ConfigLoader: Dynamic override for {key} set.")

# Singleton instance for global access
settings = ConfigLoader()
