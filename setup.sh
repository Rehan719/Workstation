#!/bin/bash
echo "🚀 Workstation v148.0 Master Setup"

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

# 3. Blockchain (Polygon/WST) Setup
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
