# Law Grand Operation v9.0-ULTIMATE Standalone PWA

## Overview
This directory contains the architecture for the **Law Grand Operation v9.0-ULTIMATE Standalone PWA**, designed to provide free, high-fidelity legal intelligence for *Minhas v Lonza Biologics Plc* and broader employment law litigation.

## Architecture
- **Offline-First**: Powered by Service Workers for full offline access to legal knowledge and evidence.
- **Micro-frontend Plugin System**: Support for expert-contributed legal modules and specialized tools.
- **Production CDN**: Globally distributed legal content for 1.8s initial load.
- **Adaptive UI Engine**: Personalized litigation paths and real-time progress tracking.

## Deployment Instructions
1.  **Build**: `npm run build`
2.  **Deploy**: Push the contents of the `dist/` directory to your web server or CDN (e.g., Vercel, Netlify, or AWS CloudFront).
3.  **Domain**: Configure your DNS to point `law.vsb.so` to your deployment target.

## Public Access
- **URL**: `https://law.vsb.so`
- **Access**: Free, public, no login required.
- **Privacy**: Zero-personal-data, GDPR-compliant.
