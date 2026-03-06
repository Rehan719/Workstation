#!/bin/bash
# QEP Setup Script
set -e

echo "Initializing QEP Environment..."

# 1. Backend Dependencies
pip install -r requirements.txt || pip install numpy scipy scikit-learn pandas sqlalchemy fastapi uvicorn pytest pytest-asyncio networkx deap httpx

# 2. Frontend Dependencies
cd src/qep_frontend
npm install

# 3. Database Initialization
cd ../..
python3 -c "from agentic_core.db.manager import DatabaseManager; DatabaseManager()"

echo "QEP Setup Complete."
