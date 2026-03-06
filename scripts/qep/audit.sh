#!/bin/bash
# QEP Verification Script
set -e

echo "Running QEP Constitutional Audit..."
grep -E "Article 23[6-9]|Article 24[0-9]|Article 250" CONSTITUTION_v99.0.0.md

echo "Verifying Traceability..."
ls docs/planning/traceability_matrix_v99.md

echo "Running Backend Unit Tests..."
PYTHONPATH=. pytest tests/test_religious_domain.py
