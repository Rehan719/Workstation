#!/bin/bash
echo "--- QEP Formatting Suite (Article 150 Hardening) ---"
if command -v black &> /dev/null
then
    black agentic_core/religious_domain
else
    echo "Black not found. Skipping format."
fi
