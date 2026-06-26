# GCP Free Tier Setup

## 🚀 Free Tier Services
- **Cloud Run**: 2 million requests per month.
- **Firebase**: Generous Spark Plan (NoSQL, Auth, Hosting).
- **BigQuery**: 10 GB storage, 1 TB query per month.
- **Cloud Storage**: 5 GB-months of regional storage.

## 📝 Setup Instructions
1. Create a [GCP Account](https://cloud.google.com/free).
2. Enable Billing (GCP requires it for free tier).
3. Create a Service Account with 'Cloud Run Admin' and 'Storage Admin' roles.
4. Download the JSON Key.
5. Set 'GCP_PROJECT_ID' and 'GCP_SERVICE_ACCOUNT_KEY' in your environment.
