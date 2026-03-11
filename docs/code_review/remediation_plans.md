# Remediation Plans - Cycle 1

## Sprint 1: Security & Core Engine (High Priority)
### 112-04: Resolve Hardcoded JWT Secret
- **Action**: Remove the hardcoded string in `agentic_core/collaboration/workspace_manager.py`. Replace with a mandatory environment variable check or a secure dynamic generation if missing in dev mode.
- **Effort**: Low (1 SP)
- **Impact**: High (Security hardening)
- **Owner**: SecuritySquad

### 112-05: Optimize Predictive Sync
- **Action**: Refactor `GrandSynthesisEngine.run_synthesis`. Replace `asyncio.sleep(0.02)` with a robust event-driven sync mechanism or a configurable interval tied to telemetry.
- **Effort**: Medium (3 SP)
- **Impact**: Medium (Engine reliability)
- **Owner**: GSE-Team

## Sprint 2: UI & Maintenance (Medium Priority)
### 112-03: Dashboard Versioning Synchronization
- **Action**: Update `src/dashboard/app.py` to use a central version constant or pull from the Genomic Registry to ensure UI matches the actual system state (v112.0).
- **Effort**: Low (1 SP)
- **Impact**: Medium (Professional standards)
- **Owner**: CoE-PP

### 112-01 & 112-06: Root Hygiene
- **Action**: Delete redundant log files and move `workstation.db` to `meta/data/`. Audit `vercel.json` and move to `infra/deployment/` if still needed.
- **Effort**: Medium (2 SP)
- **Impact**: High (Repository hygiene)
- **Owner**: CleanupSquad

## Sprint 3: Documentation & Type Safety (Low Priority)
### 112-02: Type Hint Coverage
- **Action**: Add explicit type hints to all methods in `GrandSynthesisEngine` and related synthesis modules.
- **Effort**: Medium (3 SP)
- **Impact**: Medium (Maintainability)
- **Owner**: GSE-Team
