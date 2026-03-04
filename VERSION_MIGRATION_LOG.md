# Jules AI: Version Migration Log

## [99.0.0] - 2026-02-25
### Unified Transcendent Release
- **Unified Orchestrator:** `ConsciousOrganismV99_0` is now the sole entry point.
- **Legacy Removal:** `v92` and `v93` orchestrators have been moved to `archive/`.
- **Imports:** All internal modules now import from `agentic_core.orchestrator.conscious_organism_v99`.

### Migration Steps
For users upgrading from v93:
1. Update imports from `agentic_core.orchestrator.conscious_organism_v93` to `agentic_core.orchestrator.conscious_organism_v99`.
2. Initialize `DatabaseManager` for persistent telemetry.
3. Configure `JULES_JWT_SECRET` in your environment.
