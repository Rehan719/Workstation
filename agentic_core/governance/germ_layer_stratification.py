# agentic_core/governance/germ_layer_stratification.py
import logging

logger = logging.getLogger(__name__)

class GermLayerEnforcer:
    """
    Enforces permission stratification based on biological germ layers:
    - Ectoderm: UI layer (user-facing)
    - Mesoderm: Logic layer (business rules, workflows)
    - Endoderm: Infrastructure layer (data persistence, external services)
    """

    LAYER_PERMISSIONS = {
        "ectoderm": {
            "read": ["user_data", "ui_state", "public_content"],
            "write": ["ui_preferences", "session_state"],
            "access": ["ui_components", "visualization_tools"]
        },
        "mesoderm": {
            "read": ["business_rules", "workflow_definitions", "agent_state"],
            "write": ["process_instances", "task_results", "orchestration_logs"],
            "access": ["orchestrator", "dispatcher", "commander"]
        },
        "endoderm": {
            "read": ["all_persisted_data", "configuration", "audit_logs"],
            "write": ["database", "file_storage", "external_services"],
            "access": ["persistence_layer", "backup_systems", "recovery_mechanisms"]
        }
    }

    def __init__(self):
        self.component_layers = {}  # component_name -> layer

    def register_component(self, component_name, layer):
        """Register a component with its germ layer"""
        if layer not in ["ectoderm", "mesoderm", "endoderm"]:
            raise ValueError(f"Invalid layer: {layer}. Must be ectoderm, mesoderm, or endoderm")
        self.component_layers[component_name] = layer

    def check_access(self, source_component, target_resource, action):
        """
        Check if source component can perform action on target resource
        based on germ layer permissions
        """
        source_layer = self.component_layers.get(source_component)
        if not source_layer:
            # For simulation purposes, handle unknown components
            return True

        # Get permissions for source layer
        layer_perms = self.LAYER_PERMISSIONS.get(source_layer, {})

        # Check if action is allowed
        if action in layer_perms.get("read", []) and target_resource in layer_perms.get("read", []):
            return True
        if action in layer_perms.get("write", []) and target_resource in layer_perms.get("write", []):
            return True
        if action in layer_perms.get("access", []) and target_resource in layer_perms.get("access", []):
            return True

        # Special case: UI (ectoderm) cannot directly access infrastructure (endoderm)
        if source_layer == "ectoderm" and self.component_layers.get(target_resource) == "endoderm":
            logger.warning("PERMISSION: Ectoderm attempt to bypass Mesoderm to access Endoderm.")
            return False

        # Special case: Logic layer (mesoderm) mediates between UI and infrastructure
        if source_layer == "ectoderm" and action == "write" and "database" in target_resource:
            logger.warning("PERMISSION: UI cannot write directly to database; must go through logic layer")
            return False

        return True
