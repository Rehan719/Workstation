#!/bin/bash
set -e
echo "Starting Enhanced Deployment Readiness Check..."
python3 agentic_core/scripts/zero_placeholder_check_advanced.py agentic_core
echo "Import test..."
python3 -c "import agentic_core; print('Agentic Core import successful')"
echo "ALL GATES PASSED."
