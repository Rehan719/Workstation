#!/bin/bash
set -euo pipefail
echo "🧬 Running Workstation Supreme Regression Suite (Phase 0, 1, 2)..."
export PYTHONPATH=.
python3 -m pytest tests/unit/validation/ tests/unit/commercial/ tests/unit/llm/ tests/integration/ tests/phase2/integration/
