# Jules AI v52.0: Production Scientific Workstation

Jules AI v52.0 is a production-grade, self-evolving, multi-agent platform for scientific discovery. It integrates Neuro-Symbolic reasoning, Quantum Machine Learning, and a Five-Layer Verification Framework to deliver unassailable scientific truth.

## Key Features
- **Triad of Hybrid Intelligence**: Synergistic integration of Neural Networks (Transformer-based), Symbolic Logic (SymPy), and Quantum Optimization (PennyLane).
- **Five-Layer Verification**: Rigorous validation suite (Source Integrity, Logical Consistency, Numerical Correctness, Empirical Replication, Adversarial Robustness).
- **Unified Evidence Graph (UEG)**: Immutable knowledge graph with SHA-256 blockchain provenance and Sigstore signing.
- **Autonomous Self-Improvement**: Real-time recalibration and evolutionary mutation loops.
- **Production Dashboard**: Streamlit interface for monitoring discovery and integrity.

## Quick Start
1. **Prerequisites**:
   Ensure you have [Poetry](https://python-poetry.org/) installed.
2. **Setup**:
   ```bash
   poetry install
   ./scripts/init-secrets.sh
   ```
3. **Run Workstation**:
   ```bash
   poetry run streamlit run src/dashboard/app.py
   ```
4. **Run Tests**:
   ```bash
   poetry run pytest
   ```

## Repository Structure
- `src/`: Functional source code (Orchestrator, Triad, Verification, UEG, Security, Self-Improvement, Dashboard).
- `meta/`: Constitution and governance rules.
- `docs/`: User guides and API references.
- `tests/`: Comprehensive test suite.
- `scripts/`: Production infrastructure scripts.

## License
MIT License.
