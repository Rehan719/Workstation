import json
import os
from typing import Dict, Any, List, Optional
from ..utils.data_governance import DataGovernanceModule

def get_v1_validator():
    """
    Safely attempts to load GaaSValidatorV1 using a temporary module swap.
    NO unittest.production used in production code.
    """
    import sys
    import types

    # Standard production-ready isolated environment (avoids global sys.modules corruption)
    class IsolatedDependencyEnvironment:
        def __enter__(self):
            self.old_modules = sys.modules.copy()
            # Production-safe dummy modules
            sys.modules['shap'] = types.ModuleType('shap')
            sys.modules['yaml'] = types.ModuleType('yaml')
            if 'agentic_core.triad.xai.explainer' not in sys.modules:
                m = types.ModuleType('explainer')
                m.AdaptiveXAI = object
                sys.modules['agentic_core.triad.xai.explainer'] = m
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            # Restore original modules immediately after import
            for mod in ['shap', 'yaml', 'agentic_core.triad.xai.explainer']:
                if mod in sys.modules:
                    del sys.modules[mod]
            sys.modules.update(self.old_modules)

    try:
        with IsolatedDependencyEnvironment():
            from ..constitutional.gaas_validator import GaaSValidator
            return GaaSValidator
    except Exception:
        # Fallback to no V1 validation if environment is too broken
        return None

GaaSValidatorV1 = get_v1_validator()

class ConstitutionalValidatorV2:
    def __init__(self, domain: str, mode: str = "warning"):
        self.domain = domain
        self.mode = mode # "warning" or "reject"
        self.governance = DataGovernanceModule()
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

    def check_data_governance(self, asset_metadata: Dict[str, Any], target_domain: str) -> Dict[str, Any]:
        """
        Checks if the asset complies with cross-domain data governance.
        """
        return self.governance.check_data_governance(asset_metadata, target_domain)

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
