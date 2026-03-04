# Jules AI: Developer Persona Guide (v99.0)

Greetings, Architect. You are responsible for the structural integrity and technical evolution of the Workstation.

## 🧬 Core Architecture

### 1. The 150-Article Constitution
All system behavior is governed by `CONSTITUTION_v99.0.md`. Developers must ensure all new modules are traceable to specific articles.

### 2. PC-Agent Hierarchy
Tasks are executed via a four-tier agency model:
- **Manager Agent (MA):** High-level orchestration.
- **Progress Agent (PA):** State management and logging.
- **Decision Agent (DA):** Strategy selection and execution.
- **Reflection Agent (RA):** Error correction and transition rollback triggers.

### 3. Production Hardening
- **ReliabilityEngine:** Use `execute_with_retry` for all external calls.
- **OptimizationEngine:** Resource allocation is managed via Article 91 priority weights.
- **AccuracyValidator:** Automated validation of cognitive outputs against ground truth.

## 💻 Working with the Codebase
- **No-Stubs Mandate:** Placeholder logic (`pass`, `NotImplementedError`) is strictly forbidden.
- **Test-First Development:** Maintain ≥95% coverage across unit, integration, and performance tests.
- **Unified Quantum Gateway:** Leverage the gateway for score-based job routing to Qiskit or Pennylane backends.
