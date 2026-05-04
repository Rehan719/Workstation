#!/bin/bash
set -e
# Workstation vΩ∞-MASTER: Free-Tier Deployment Automation

PROJECT_ID=$1
REGION=${2:-us-central1}

if [ -z "$PROJECT_ID" ]; then
  echo "Usage: ./scripts/deploy_free_tier.sh <project-id> [region]"
  exit 1
fi

echo "🚀 Deploying Workstation vΩ∞-MASTER to $PROJECT_ID ($REGION)..."

# 1. Enable Required Services
gcloud services enable \
  run.googleapis.com \
  firestore.googleapis.com \
  cloudbuild.googleapis.com \
  secretmanager.googleapis.com \
  artifactregistry.googleapis.com \
  --project $PROJECT_ID

# 2. Build and Push Container
echo "📦 Building sovereign container..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/workstation-api --project $PROJECT_ID

# 3. Deploy to Cloud Run (Free-Tier Optimized)
echo "☁️ Deploying to Cloud Run (minScale:0)..."
gcloud run deploy workstation-api \
  --image gcr.io/$PROJECT_ID/workstation-api \
  --platform managed \
  --region $REGION \
  --memory 512Mi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 5 \
  --allow-unauthenticated \
  --project $PROJECT_ID

# 4. Deploy Firestore Rules
echo "🔐 Deploying Firestore security rules..."
gcloud firestore rules deploy deployment/firestore.rules --project $PROJECT_ID

echo "✅ vΩ∞-MASTER deployed at: $(gcloud run services describe workstation-api --platform managed --region $REGION --format='value(status.url)' --project $PROJECT_ID)"
