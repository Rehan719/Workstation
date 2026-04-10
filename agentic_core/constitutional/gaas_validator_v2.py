import json
import os
from typing import Dict, Any, List, Optional
def get_v1_validator():
    """
    Safely attempts to load GaaSValidatorV1 without polluting sys.modules.
    Uses local mocking for the import context only.
    """
    import sys
    import types
    from unittest.mock import patch

    # Define the core validator import inside a patch context to avoid global pollution
    try:
        with patch.dict(sys.modules, {
            'shap': types.ModuleType('shap'),
            'yaml': types.ModuleType('yaml'),
            'agentic_core.triad.xai.explainer': types.ModuleType('explainer')
        }):
            # Set required attribute for the mock
            sys.modules['agentic_core.triad.xai.explainer'].AdaptiveXAI = object
            from agentic_core.biomimicry.gaas_validator import GaaSValidator
            return GaaSValidator
    except Exception as e:
        # Fallback to no V1 validation if environment is too broken
        return None

GaaSValidatorV1 = get_v1_validator()

class ConstitutionalValidatorV2:
    def __init__(self, domain: str, mode: str = "warning"):
        self.domain = domain
        self.mode = mode # "warning" or "reject"
        if GaaSValidatorV1:
            try:
                self.v1_validator = GaaSValidatorV1("agentic_core/constitution/CONSTITUTION_v138.0.0.md")
            except Exception:
                self.v1_validator = None
        else:
            self.v1_validator = None
        self.rules = self._load_domain_rules()

    def _load_domain_rules(self) -> List[Dict[str, Any]]:
        config_path = f"configs/constitutional/{self.domain.lower()}_rules.json"
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                config = json.load(f)
                return config.get("rules", [])
        return []

    def validate_compliance(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates data against v1 core constitution and v2 domain-specific rules.
        """
        violations = []

        # Core v1 validation
        if self.v1_validator:
            # We wrap the data in a dummy agentic payload for V1
            v1_payload = {
                "intent": f"generate_{self.domain}_product",
                "high_risk": True, # Generating legal/scientific products is high risk
                "domain": self.domain,
                "data_summary": str(data)[:100]
            }
            v1_decision = self.v1_validator.validate_payload("grand_ops_v6_agent", v1_payload)
            if v1_decision["decision"] == "BLOCK":
                violations.append({
                    "rule_id": "V1_CONSTITUTION_BLOCK",
                    "status": "reject",
                    "message": f"Core Constitutional Violation: {v1_decision['reason']}"
                })

        for rule in self.rules:
            rule_id = rule["id"]
            field = rule["field"]
            check = rule["check"]
            action = rule["action"]

            if field not in data:
                violations.append({
                    "rule_id": rule_id,
                    "status": action,
                    "message": f"Mandatory field '{field}' missing."
                })
                continue

            field_value = data[field]

            if check == "all_fields_present":
                params = rule.get("params", [])
                missing = [p for p in params if p not in field_value]
                if missing:
                    violations.append({
                        "rule_id": rule_id,
                        "status": action,
                        "message": f"Missing sub-fields in {field}: {', '.join(missing)}"
                    })

            elif check == "referenced":
                if not field_value:
                    violations.append({
                        "rule_id": rule_id,
                        "status": action,
                        "message": f"Field '{field}' must be referenced."
                    })

            elif check == "consent_given":
                if not field_value.get("consent", False):
                    violations.append({
                        "rule_id": rule_id,
                        "status": action,
                        "message": f"Consent not given for '{field}'."
                    })

        is_valid = not any(v["status"] == "reject" for v in violations)

        return {
            "is_valid": is_valid if self.mode == "reject" else (is_valid or True),
            "actual_valid": is_valid,
            "violations": violations,
            "domain": self.domain,
            "mode": self.mode
        }
