# agentic_core/architecture/hox_patterns.py
import logging
from typing import Any

logger = logging.getLogger(__name__)

class ConstitutionalViolation(Exception):
    """Exception raised for violations of master architectural patterns."""
    pass

class HoxPatternRegistry:
    """
    Registry of master architectural patterns that maintain structural integrity
    across evolutionary versions. Each pattern has:
    - pattern_id: Unique identifier
    - expression_order: Determines when pattern applies in development sequence
    - structural_constraints: Rules that modules must satisfy
    - version_compatibility: Maps pattern versions to Workstation versions
    """

    patterns = {
        "core_entity_pattern": {
            "expression_order": 1,
            "structural_constraints": [
                "all_entities_must_have_uuid",
                "entities_must_support_versioning",
                "relationships_must_be_traceable",
                "entities_must_have_provenance"
            ],
            "version_compatibility": ["v1.0", "v71.0", "v92.0", "v93.0", "v99.0"]
        },
        "governance_pattern": {
            "expression_order": 2,
            "structural_constraints": [
                "survival_hierarchy_supreme",
                "constitutional_checks_before_actions",
                "audit_logging_required",
                "regulatory_rules_must_be_versioned"
            ],
            "version_compatibility": ["v71.0", "v92.0", "v93.0", "v99.0"]
        },
        "deployment_pattern": {
            "expression_order": 3,
            "structural_constraints": [
                "artifacts_must_be_stage_tagged",
                "zero_downtime_required",
                "rollback_capability_mandatory",
                "environment_isolation"
            ],
            "version_compatibility": ["v92.0", "v93.0", "v99.0"]
        },
        "domain_specific_pattern": {
            "expression_order": 4,
            "structural_constraints": [
                "scientific_reasoning_must_be_rigor_verified",
                "legal_compliance_must_be_citation_traced",
                "religious_ethics_must_be_source_attributed"
            ],
            "version_compatibility": ["v93.0", "v99.0"]
        },
        "collaboration_pattern": {
            "expression_order": 5,
            "structural_constraints": [
                "real_time_sync_must_be_eventual_consistent",
                "conflict_resolution_must_be_operational_transform",
                "permission_inheritance_must_be_hierarchical"
            ],
            "version_compatibility": ["v94.0", "v99.0"]
        }
    }

    @classmethod
    def validate_module(cls, module, version):
        """Ensure module conforms to patterns active for its version"""
        applicable_patterns = [
            p for p in cls.patterns.values()
            if version in p["version_compatibility"]
        ]
        for pattern in sorted(applicable_patterns, key=lambda p: p["expression_order"]):
            for constraint in pattern["structural_constraints"]:
                if hasattr(module, "satisfies") and not module.satisfies(constraint):
                    raise ConstitutionalViolation(
                        f"Module {module.name} violates {pattern['pattern_id']}: {constraint}"
                    )
        return True
