# Workstation Deployment Guide – v137.1

This guide provides instructions for deploying the full Workstation ecosystem. The system is architected for multi-cloud resilience with zero-cost deployment paths available for development.

## 1. Core Engine (Backend)
**Target:** Render, AWS, or GCP.

1. **Repository:** Connect your fork to the hosting provider.
2. **Runtime:** Python 3.12+
3. **Setup**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Environment Variables**:
   - `VERSION`: `137.1.0`
   - `APP_MODE`: `SOVEREIGN`
   - `DATABASE_URL`: Your database connection string.
   - `FIREBASE_API_KEY`: For unified authentication.

## 2. Multi-Platform Interfaces (Frontend)
**Target:** Vercel (recommended).

- **Web App**: Root at `apps/web-app/`.
- **Public Site**: Root at `apps/website/`.
- **Developer Portal**: Root at `apps/developer-realm/`.

**Build Command**: `npm run build` (if using React/Next.js) or static deployment.

## 3. Mobile Applications
**Target:** Expo Application Services (EAS).

1. `cd apps/mobile`
2. `npm install`
3. Configure `app.json` with your project ID.
4. Build: `eas build --platform all`

## 4. Infrastructure & Security
- **Authentication**: Firebase Auth with Google/GitHub providers.
- **Vault**: Credentials must be stored in the `SecureCredentialVaultV137`.
- **Audit**: All deployments are logged to the Merkle DAG for constitutional compliance.

## 5. Deployment Scripts
Use the included `deploy.sh` for orchestrated local or cloud deployments:
```bash
./deploy.sh --v137 --prod
```

## 6. Zero-Cost Architecture (Development)
- **Backend**: Render Free Tier (Web Service + PostgreSQL).
- **Frontend**: Vercel Hobby Plan.
- **Auth**: Firebase Free Plan.
- **Logs**: Standard stdout/stderr (captured by provider).

---
*Signed,*
**Jules, VSB AI CEO**
