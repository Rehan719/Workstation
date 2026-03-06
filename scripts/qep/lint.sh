#!/bin/bash
echo "--- QEP Linting Suite (Article 150 Hardening) ---"
if command -v ruff &> /dev/null
then
    ruff check agentic_core/religious_domain
else
    echo "Ruff not found. Skipping lint."
fi
