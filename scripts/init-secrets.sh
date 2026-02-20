#!/bin/bash

if [ -f ".env" ]; then
    echo ".env already exists, skipping."
else
    echo "Creating .env from .env.template..."
    cp .env.template .env
    # Generate some random passwords
    sed -i "s/placeholder/$(openssl rand -base64 12)/g" .env
    echo "Generated random secrets in .env"
fi
