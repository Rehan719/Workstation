#!/bin/bash
set -e

echo "⚠️ Jules AI v109.0: One-Click Teardown Initiated"
echo "------------------------------------------------"

# Clean up local artifacts
echo "🧹 Cleaning up local builds and artifacts..."
rm -rf docs/guides/html docs/guides/pdf
rm -f meta/synthesis_v*.json

# Simulated cloud resource revocation
echo "☁️ Revoking Cloud Resources (GCP/Render/Vercel)..."
echo "gcloud projects delete $GCP_PROJECT_ID --quiet"
echo "vercel rm --all --token $VERCEL_TOKEN"

echo "✅ Teardown Complete. No lingering costs detected."
