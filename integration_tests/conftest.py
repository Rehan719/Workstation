"""
Clean conftest for integration tests.
Does NOT mock pydantic, psutil, or other real dependencies
that the MVP spine requires.
"""
import os
import pytest

# Use isolated test data directories so tests don't pollute real data
os.environ["PROJECTS_DIR"] = "data/test_projects"
os.environ["SYNTHESIS_OUTPUT_DIR"] = "data/test_synthesis"
os.environ["PROPOSALS_DIR"] = "data/test_proposals"
