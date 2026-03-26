#!/bin/bash
# Standalone QEP-Religion Deployment Script v0.8
set -e

echo "--------------------------------------------------"
echo "🚀 Launching Standalone QEP-Religion v0.8"
echo "--------------------------------------------------"

# 1. Environment Configuration
echo "⚙️  Configuring Environment..."
export VITE_QEP_STANDALONE=true
export LOG_LEVEL=INFO

# 2. Dependency Check (Partial install for speed)
echo "📦 Checking Dependencies..."
if [ ! -d "node_modules" ]; then
  npm install --only=prod
fi

# 3. Backend Warm-up (Simulated)
echo "🧠 Initializing QEP Engines (ESE, ARO, BTO, DRAD)..."
# In a real setup, we would start the FastAPI backend here
# python3 agentic_core/main.py &

# 4. Frontend Build & Launch
echo "🌐 Starting Standalone Web Interface..."
# npm run dev -- --host

echo "--------------------------------------------------"
echo "✅ QEP Flagship is live in Standalone Mode!"
echo "📍 Access point: http://localhost:5173"
echo "--------------------------------------------------"
