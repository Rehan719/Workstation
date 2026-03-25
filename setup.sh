#!/bin/bash
# Workstation vFinal.0.0: Unified Setup Script

echo "Checking prerequisites..."
command -v node >/dev/null 2>&1 || { echo >&2 "Node.js not found. Aborting."; }
command -v python3 >/dev/null 2>&1 || { echo >&2 "Python 3 not found. Aborting."; }

echo "Initializing Backend Data..."
mkdir -p agentic_core/data
echo "{}" > agentic_core/data/memory.json

echo "Installing Backend Dependencies (Poetry)..."
cd agentic_core && poetry install && cd ..

echo "Installing Web Dependencies..."
cd apps/web && npm install && cd ../..

echo "Installing Mobile Dependencies..."
cd apps/mobile && npm install && cd ../..

echo "🚀 Setup Complete. Run the following to start:"
echo "Backend: cd agentic_core && poetry run uvicorn main:app --reload"
echo "Web: cd apps/web && npm run dev"
echo "Mobile: cd apps/mobile && npx expo start"
