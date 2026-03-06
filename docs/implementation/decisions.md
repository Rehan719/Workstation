# Architectural Decisions - Jules AI v60.0

## AD-001: Clean Migration to `agentic_core/`
- **Status**: Accepted
- **Decision**: Migrate all v60.0 core logic to the `agentic_core/` directory.
- **Rationale**: Signals the fundamental architectural shift from a tool-based system to an autonomous organism.
- **Consequences**: `src/` will be treated as legacy. All new imports should point to `agentic_core/`.

## AD-002: Biological Orchestration over Static Logic
- **Status**: Accepted
- **Decision**: Use biologically-inspired subsystems (Immune, Nervous, etc.) for system governance and task execution.
- **Rationale**: Provides a more robust, adaptive, and self-healing architecture compared to traditional static orchestrators.

## AD-003: "No Stubs" Policy
- **Status**: Accepted
- **Decision**: Every implemented component must be functional from the start.
- **Rationale**: Ensures the system is immediately usable and facilitates iterative self-improvement. Use functional defaults where complex ML models are still "learning".

## AD-004: Grand Synthesis Engine as a Living Component
- **Status**: Accepted
- **Decision**: The Grand Synthesis Engine is a permanent part of the repository, not just a build-time tool.
- **Rationale**: Allows for continuous historical analysis and pattern extraction as the system evolves.

## AD-005: Simulated Quantum Backend by Default
- **Status**: Accepted
- **Decision**: Use a simulated quantum backend for initial deployment, with clear production-ready hooks for PennyLane and Qiskit.
- **Rationale**: Ensures immediate functionality regardless of hardware availability.
