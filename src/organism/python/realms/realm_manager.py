from typing import Dict, List, Optional
from enum import Enum

class IsolationLevel(Enum):
    SANDBOX = "SANDBOX"
    RESTRICTED = "RESTRICTED"
    FULL = "FULL"

class ResourceQuota:
    def __init__(self, cpu: str, memory: str, disk: str):
        self.cpu = cpu
        self.memory = memory
        self.disk = disk

class RealmConfig:
    def __init__(self, name: str, isolation_level: IsolationLevel, resource_limits: ResourceQuota, allowed_actions: List[str], requires_approval: List[str]):
        self.name = name
        self.isolation_level = isolation_level
        self.resource_limits = resource_limits
        self.allowed_actions = allowed_actions
        self.requires_approval = requires_approval

class Realm:
    def __init__(self, config: RealmConfig):
        self.config = config
        self.failure_count = 0
        self.is_isolated = False

    def check_access(self, action_type: str) -> bool:
        if action_type in self.config.allowed_actions:
            return True
        return False

class RealmManager:
    def __init__(self, configs: Optional[Dict[str, RealmConfig]] = None):
        self.realms: Dict[str, Realm] = {}
        if configs:
            for name, config in configs.items():
                self.realms[name] = Realm(config)

    def create_realm(self, config: RealmConfig) -> Realm:
        realm = Realm(config)
        self.realms[config.name] = realm
        return realm

    def get_realm(self, name: str) -> Optional[Realm]:
        return self.realms.get(name)

    def enforce_boundary(self, source_realm: str, target_realm: str, action_type: str) -> bool:
        target = self.get_realm(target_realm)
        if not target:
            return False
        if target.is_isolated:
            return False
        return target.check_access(action_type)

    def track_failure(self, realm_name: str):
        realm = self.get_realm(realm_name)
        if realm:
            realm.failure_count += 1
            if realm.failure_count > 10:
                realm.is_isolated = True
