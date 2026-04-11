#!/bin/bash
set -euo pipefail

echo "🧠 Running v2.0 Quality Gates for MJM Meta-Cognitive Engine..."

export PYTHONPATH=$PYTHONPATH:$(pwd)/products/mjm-intelligence-engine

# 1. Property-Based Testing
echo "✅ Quality Gate: Property-Based Testing..."
python3 -m pytest products/mjm-intelligence-engine/tests/learning/test_learning_properties.py

# 2. Meta-Cognitive Benchmark (v2)
echo "✅ Quality Gate: Meta-Cognitive Benchmark v2.0..."
python3 products/mjm-intelligence-engine/tests/run_benchmark_v2.py

# 3. Zero-Placeholder Check
echo "✅ Quality Gate: Zero-Placeholder Check..."
if grep -rE "pass|TODO|NotImplementedError|mock" products/mjm-intelligence-engine/core products/mjm-intelligence-engine/adapters | grep -v "integrity_pass" | grep -v "traceability_pass" | grep -v "__pycache__" | grep -v "node_modules"; then
    echo "❌ Zero-Placeholder check failed!"
    exit 1
fi

echo "🎉 All MJM v2.0 quality gates passed!"
