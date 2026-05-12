import subprocess
import pytest

def test_no_gcp_imports():
    """ARTICLE 1125: Runtime Sovereignty Gate."""
    # Core logic should not depend on google-cloud-sdk direct imports
    result = subprocess.run(
        ["grep", "-r", "google.cloud", "agentic_core/", "--include=*.py", "--exclude=deploy_free_tier.sh"],
        capture_output=True,
        text=True
    )
    # If findings exist, it violates sovereignty
    if result.stdout:
        print(f"Sovereignty violation detected:\n{result.stdout}")

    assert result.returncode != 0 or not result.stdout, "GCP SDK detected in core agentic logic"
