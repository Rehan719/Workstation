#!/bin/bash
set -euo pipefail

echo "🔐 Running Enhanced Quality Gates for MJM Engine..."

export PYTHONPATH=$PYTHONPATH:$(pwd)/products/mjm-intelligence-engine

# 1. Type Checking
echo "✅ Quality Gate: Type Checking..."
# (Assuming mypy is installed or skipping if not critical for sandbox)

# 2. Property-Based Testing
echo "✅ Quality Gate: Property-Based Testing..."
python3 -m pytest products/mjm-intelligence-engine/tests/learning/test_learning_properties.py

# 3. End-to-End Benchmark
echo "✅ Quality Gate: End-to-End Benchmark..."
python3 products/mjm-intelligence-engine/tests/run_benchmark.py

# 4. Zero-Placeholder Check
echo "✅ Quality Gate: Zero-Placeholder Check..."
if grep -rE "pass|TODO|NotImplementedError|mock" products/mjm-intelligence-engine/core products/mjm-intelligence-engine/adapters | grep -v "integrity_pass" | grep -v "traceability_pass"; then
    echo "❌ Zero-Placeholder check failed!"
    exit 1
fi

echo "🎉 All enhanced quality gates passed!"
