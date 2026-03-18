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

# 3. Ollama Check
if command -v ollama &> /dev/null
then
    echo "✅ Ollama detected."
else
    echo "⚠️ Ollama not found. Would you like to install it? (y/n)"
    # Installation logic...
fi

echo "✅ Setup Complete. Run 'npm run web:dev' to start."
