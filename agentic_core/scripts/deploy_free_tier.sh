#!/bin/bash
set -e
PROJECT_ID=$1
gcloud config set project $PROJECT_ID
gcloud services enable run.googleapis.com firestore.googleapis.com cloudbuild.googleapis.com
gcloud builds submit --tag gcr.io/$PROJECT_ID/workstation-api
gcloud run deploy workstation-api --image gcr.io/$PROJECT_ID/workstation-api --platform managed --region us-central1 --min-instances 0 --max-instances 5 --allow-unauthenticated
gcloud firestore rules deploy deployment/firestore.rules
echo "✅ vΩ∞-GEOSPHERIC-FINAL Deployed."
