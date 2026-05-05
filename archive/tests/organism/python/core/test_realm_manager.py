import pytest
import yaml
import os
from src.organism.python.realms.realm_manager import RealmManager, RealmConfig, ResourceQuota, IsolationLevel

@pytest.fixture
def realm_manager():
    return RealmManager()

def test_create_realm(realm_manager):
    config = RealmConfig(
        name="test-realm",
        isolation_level=IsolationLevel.SANDBOX,
        resource_limits=ResourceQuota(cpu="1 core", memory="1GB", disk="5GB"),
        allowed_actions=["test_action"],
        requires_approval=[]
    )
    realm = realm_manager.create_realm(config)
    assert realm.config.name == "test-realm"
    assert realm_manager.get_realm("test-realm") == realm

def test_enforce_boundary(realm_manager):
    config = RealmConfig(
        name="prod",
        isolation_level=IsolationLevel.RESTRICTED,
        resource_limits=ResourceQuota(cpu="1 core", memory="1GB", disk="5GB"),
        allowed_actions=["read_only"],
        requires_approval=["delete"]
    )
    realm_manager.create_realm(config)
    assert realm_manager.enforce_boundary("dev", "prod", "read_only") == True
    assert realm_manager.enforce_boundary("dev", "prod", "write_access") == False
    assert realm_manager.enforce_boundary("dev", "unknown", "read_only") == False

def test_realm_isolation_on_failure(realm_manager):
    config = RealmConfig(
        name="flaky-realm",
        isolation_level=IsolationLevel.SANDBOX,
        resource_limits=ResourceQuota(cpu="1 core", memory="1GB", disk="5GB"),
        allowed_actions=["ping"],
        requires_approval=[]
    )
    realm_manager.create_realm(config)
    for _ in range(11):
        realm_manager.track_failure("flaky-realm")
    realm = realm_manager.get_realm("flaky-realm")
    assert realm.is_isolated == True
    assert realm_manager.enforce_boundary("dev", "flaky-realm", "ping") == False

def test_yaml_config_loading():
    yaml_path = "src/organism/config/realms.yaml"
    if not os.path.exists(yaml_path):
        pytest.skip("realms.yaml not found")
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)
    assert "realms" in data
    assert "development" in data["realms"]
    assert "production" in data["realms"]
    assert data["realms"]["production"]["isolation"] == "RESTRICTED"
