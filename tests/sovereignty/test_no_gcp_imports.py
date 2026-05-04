import subprocess
import os

def test_no_gcp_imports():
    """Runtime Sovereignty: Prohibit google.cloud imports in backend/agentic_core."""
    # Scan agentic_core and backend for prohibited imports
    targets = ["agentic_core", "backend"]
    prohibited = "google.cloud"

    found_violations = []
    for target in targets:
        if not os.path.exists(target):
            continue
        result = subprocess.run(
            ["grep", "-r", prohibited, "--include=*.py", target],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            found_violations.append(result.stdout)

    assert not found_violations, f"Sovereignty Violated: Found {prohibited} imports:\n{''.join(found_violations)}"
