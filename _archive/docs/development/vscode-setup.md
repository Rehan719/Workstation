# Jules v99.0 VS Code Setup Guide

## One-Click Operations

This workstation includes a suite of automated tasks for development and governance. Access them via `Ctrl+Shift+B` (Build) or `Tasks: Run Task`.

### Core Tasks
- **QEP: Setup Environment**: Installs all backend and frontend dependencies.
- **QEP: Build Frontend**: Compiles the React PWA for production.
- **QEP: Start Dev Mode**: Launches the Vite development server.
- **QEP: Run Tests**: Executes the comprehensive `pytest` suite.
- **QEP: Constitutional Audit**: Verifies that all Articles 1-250 are present and traceable.
- **QEP: Sync Database**: Initializes SQLite with required spiritual and telemetry tables.

### Debugging
The `launch.json` file provides configurations for:
- **QEP: Run All Domains**: Launches a simulation of the orchestrator with spiritual KPIs active.

### GitHub Integration
- **CI Workflow**: Automatically runs on every push to verify code quality, tests, and build stability.
- **Release Workflow**: Triggers on version tags (e.g., `v*`) to bundle production assets and create a release.
