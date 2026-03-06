#!/bin/bash
echo "Initializing production secrets for v52.0..."
if [ ! -f .env ]; then
    cp .env.template .env
    echo ".env created from template."
fi
