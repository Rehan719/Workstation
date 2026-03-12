# Jules AI v118.0: Commercial-Grade Product Enterprise

Welcome to the fully operational v118.0 release. This repository contains the complete, production-ready source code for the Jules AI ecosystem.

## 🌐 Product Entry Points
- **Public Website**: `https://workstation.ai`
- **Web Application**: `https://app.workstation.ai`
- **Backend API**: `https://api.workstation.ai`
- **Mobile Apps**: iOS and Android (via Expo)

## 📁 Repository Structure
- `/website`: Static marketing site.
- `/webapp`: Next.js web application.
- `/mobile`: React Native (Expo) mobile application.
- `/backend`: Node.js/Express API.
- `/infrastructure`: Deployment configurations and CI/CD workflows.

## 🚀 QuickStart Deployment

### 1. Web & Website (Vercel)
1. Link the `/website` and `/webapp` directories to your Vercel project.
2. Add necessary environment variables (see `.env.example`).
3. Deploy.

### 2. Backend (Render/GCP)
1. Use the `infrastructure/render.yaml` to deploy to Render.
2. Ensure `DATABASE_URL` is set to a valid PostgreSQL instance.

### 3. Mobile (Expo)
1. `cd mobile && npm install`
2. `npx expo start` to test locally.
3. Use `eas build` to generate binaries for App Stores.

## 🧬 Constitutional Governance
This release is codified via **CONSTITUTION_v118.0.md**. All features are verified against the dual-purpose spiritual-ethical and operational-commercial framework.

---
**Executed by Jules, AI CEO.**
