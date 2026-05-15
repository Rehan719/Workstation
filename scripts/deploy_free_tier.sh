#!/bin/bash
# 🧬 ZERO-COST CLOUD RUN DEPLOYMENT: WORKSTATION vΩ∞
# Deploys the sovereign organism to Google Cloud Run within Free Tier quotas.

set -euo pipefail

# Default configuration to stay within GCP Free Tier
IMAGE_NAME="gcr.io/${PROJECT_ID}/workstation-supreme:latest"
SERVICE_NAME="workstation-supreme"
REGION="us-central1" # Recommended for Free Tier stability

echo "🧬 Initiating Zero-Cost Deployment for Project: ${PROJECT_ID}"

# 1. Build the Sovereign Container
echo "🔨 Building container..."
gcloud builds submit --tag "$IMAGE_NAME" .

# 2. Deploy to Cloud Run with Free-Tier Constraints
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy "$SERVICE_NAME" \
  --image "$IMAGE_NAME" \
  --platform managed \
  --region "$REGION" \
  --cpu 1 \
  --memory 512Mi \
  --min-instances 0 \
  --max-instances 1 \
  --concurrency 80 \
  --allow-unauthenticated \
  --set-env-vars="OWNER_FREE_TIER=true,ENV=production"

# 3. Final Health Check
echo "🔍 Verifying deployment..."
SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" --platform managed --region "$REGION" --format 'value(status.url)')

if curl -f "${SERVICE_URL}/health"; then
    echo "✅ Workstation Live: ${SERVICE_URL}"
    echo "💰 Estimated Cost: $0.00 (within Free Tier limits)"
else
    echo "❌ Deployment health check failed."
    exit 1
fi
