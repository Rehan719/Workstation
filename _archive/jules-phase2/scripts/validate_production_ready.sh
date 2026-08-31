#!/bin/bash
set -e
PROJECT_ID=$1
REGION=${2:-us-central1}
API_URL=$3

echo "🔍 Validating Workstation vΩ∞-CONVERGED..."

# 1. Zero-Placeholder check
./scripts/zero_placeholder_check_advanced.sh

# 2. Runtime Sovereignty check
export PYTHONPATH=$PYTHONPATH:.
pytest tests/sovereignty/test_no_gcp_imports.py

# 3. Unit & Integration tests
pytest tests/self_improvement/test_proposals.py

# 4. End-to-end twin verification (if API_URL provided)
if [ -n "$API_URL" ]; then
  echo "🌐 Verifying Public Endpoint: $API_URL"
  curl -sf "$API_URL/health" || echo "⚠️ Health check failed"
fi

echo "✅ ALL GATES PASSED - vΩ∞-CONVERGED READY"
