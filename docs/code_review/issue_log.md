# Code Review Issue Log

| ID | Component | Severity | Category | Description | Status | Owner |
|----|-----------|----------|----------|-------------|--------|-------|
| 112-01 | Root | Medium | Cleanup | Redundant log files in root (`streamlit.log`, `streamlit_v111.log`, `streamlit_verify.log`, `streamlit_output.log`). | Resolved | CleanupSquad |
| 112-02 | agentic_core/synthesis | Low | Documentation | Missing type hints in `GrandSynthesisEngine._get_url_list` return type and other helpers. | Resolved | GSE-Team |
| 112-03 | src/dashboard/app.py | Medium | Design | Dashboard title and sidebar text still reference v111.0 while codebase evolves to v112.0. | Resolved | CoE-PP |
| 112-04 | agentic_core/collaboration/workspace_manager.py | High | Security | Hardcoded fallback JWT secret found: `"fallback-secret-for-testing-only-v99"`. | Resolved | SecuritySquad |
| 112-05 | agentic_core/synthesis | Medium | Performance | `GrandSynthesisEngine.run_synthesis` uses a hardcoded `await asyncio.sleep(0.02)` for "predictive sync" which is a non-expert design pattern. | Resolved | GSE-Team |
| 112-06 | Root | Medium | Cleanup | `workstation.db` (SQLite) and `vercel.json` present in root without explicit purpose in the new hierarchy. | Resolved | CleanupSquad |
