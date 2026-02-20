#!/bin/bash
set -e

echo "Initializing Jules AI Workstation..."

# Create necessary directories
mkdir -p content/projects content/new content/assets content/archive

# Install dependencies if not in docker
if command -v poetry &> /dev/null; then
    poetry install
fi

# Initialize secrets
./scripts/init-secrets.sh

echo "Setup complete!"
