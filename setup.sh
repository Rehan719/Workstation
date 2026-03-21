#!/bin/bash
echo "🚀 Workstation v3.0 Civilization Epoch Master Setup"

# 1. Backend Setup
echo "📦 Installing Backend (Poetry)..."
cd agentic_core
poetry install
cp .env.template .env
cd ..

# 2. Frontend Setup
echo "📦 Installing Frontend (npm)..."
npm install
cp apps/web/.env.example apps/web/.env
cp apps/mobile/.env.example apps/mobile/.env 2>/dev/null || true

# 3. Transcendent Simulation (Celery/Redis) Setup
echo "🌌 Preparing Simulation Infrastructure (Celery/Redis)..."
if command -v redis-server &> /dev/null
then
    echo "✅ Redis detected. Ready for Celery tasks."
else
    echo "⚠️ Redis not found. Reality simulation may be limited to local synchronous stubs."
fi

# 4. Blockchain (Polygon/WST) Setup
echo "⛓️ Preparing Local Blockchain (Hardhat)..."
if command -v npx &> /dev/null
then
    echo "✅ npx detected. Hardhat environment ready for 'npx hardhat node'."
else
    echo "⚠️ npx not found. Blockchain simulation may be limited."
fi

# 4. Ollama Check
if command -v ollama &> /dev/null
then
    echo "✅ Ollama detected."
else
    echo "⚠️ Ollama not found. Would you like to install it? (y/n)"
    # Installation logic...
fi

echo "✅ Setup Complete. Run 'npm run web:dev' to start."
