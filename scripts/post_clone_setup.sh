#!/bin/bash
# Workstation vΩ∞-MASTER Post-Clone Setup (Unix)

set -e

echo "🧬 Starting Workstation Post-Clone Setup..."

# 1. Create Virtual Environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# 2. Activate venv and install dependencies
source venv/bin/activate

echo "Installing dependencies (CPU-optimized torch)..."
pip install --upgrade pip
# Install CPU version of torch to ensure reliability
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt

# 3. Fix Genome Symlink
echo "Fixing genome symlink..."
python scripts/fix_genome_symlink.py

# 4. Initialize .env if missing
if [ ! -f ".env" ]; then
    echo "Creating .env from template..."
    if [ -f ".env.template" ]; then
        cp .env.template .env
    else
        touch .env
    fi
fi

echo "✅ Setup complete. To start the platform, run:"
echo "source venv/bin/activate"
echo "python -m uvicorn agentic_core.main:app --host 0.0.0.0 --port 8080 --reload"
