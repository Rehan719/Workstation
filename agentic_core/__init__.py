# agentic_core package
#
# NOTE (2026-06-18): Heavy ML organism imports (JulesOmegaOrganismV138,
# ConsciousOrganismV99_0) were removed from this __init__.py because they
# pull in a transitive dependency on `torch` (via governance/gaas/adapters/
# entropy_regularised_gaas.py), which is not installed in the API deployment
# environment and is not needed by any of the 32 mounted FastAPI routers.
#
# These classes are not wired into app_mvp.py. They live in:
#   agentic_core/organism/organism.py
#   agentic_core/orchestration/conscious_organism_v99.py
#
# Any module that needs them should import directly from those paths.
# This __init__.py is intentionally minimal to keep the package importable
# in environments without ML dependencies.
