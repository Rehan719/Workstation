#!/bin/bash
set -e

if [ ! -f ".env" ]; then
    echo ".env not found! Run scripts/setup.sh first."
    exit 1
fi

export $(grep -v '^#' .env | xargs)

docker-compose -f infra/docker/docker-compose.yml up -d

echo "Jules AI services started."
