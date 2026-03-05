# agentic_core/architecture/phylotypic_core.py
import logging

logger = logging.getLogger(__name__)

class CoreViolation(Exception):
    pass

class PhylotypicCore:
    """
    Immutable core platform logic that remains stable while peripheral features diversify.
    Changes to core require constitutional amendment process with supermajority approval.
    """

    CORE_INTERFACES = {
        "entity_system": ["create_entity", "get_entity", "update_entity", "delete_entity", "query_entities"],
        "governance": ["check_compliance", "enforce_hierarchy", "audit_action", "evaluate_rules"],
        "security": ["authenticate", "authorize", "encrypt", "attest", "audit_log"],
        "persistence": ["save", "load", "query", "migrate", "backup", "restore"],
        "domain_reasoning": ["verify_scientific_rigor", "check_legal_compliance", "validate_religious_ethics"],
        "collaboration": ["sync_state", "resolve_conflict", "broadcast_update"]
    }

    CORE_SCHEMAS = {
        "entity": ["id", "version", "created_at", "updated_at", "provenance", "stage_tag"],
        "user": ["id", "email", "roles", "permissions", "preferences", "mfa_enabled"],
        "permission": ["resource", "action", "conditions", "granted_by", "granted_at", "expires_at"],
        "module": ["name", "version", "stage", "dependencies", "patterns", "health_status"],
        "workspace": ["id", "owner", "members", "resources", "collaboration_state"],
        "generation": ["id", "prompt", "specification", "artifacts", "deployment_status"]
    }

    CORE_METRICS = {
        "max_annual_change": 0.05,  # 5% maximum change per year
        "min_stability_score": 0.95,  # 95% stability required
        "regression_test_coverage": 1.0,  # 100% coverage for core changes
        "biomimetic_fidelity_threshold": 0.992  # 99.2% minimum fidelity
    }

    @classmethod
    def validate_core_compliance(cls, module):
        """Verify module uses core interfaces and schemas correctly"""
        for interface_name, methods in cls.CORE_INTERFACES.items():
            if hasattr(module, interface_name):
                impl = getattr(module, interface_name)
                for method in methods:
                    if not hasattr(impl, method):
                        raise CoreViolation(
                            f"Module {module.name} missing core method {interface_name}.{method}"
                        )

        # Verify schema compliance for entity attributes
        if hasattr(module, "entity_schema"):
            for required_field in cls.CORE_SCHEMAS["entity"]:
                if required_field not in module.entity_schema:
                    raise CoreViolation(
                        f"Module {module.name} missing core entity field: {required_field}"
                    )
        return True

    @classmethod
    def validate_stability(cls, module_name: str, change_rate: float) -> bool:
        """Enforces strict change control on the phylotypic core."""
        if change_rate > cls.CORE_METRICS["max_annual_change"]:
            logger.warning(f"PHYLOTYPIC: Stability violation in {module_name}")
            return False
        logger.info(f"PHYLOTYPIC: Module {module_name} verified for stability (drift: {change_rate:.4f})")
        return True
