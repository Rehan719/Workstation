# Workstation Unified User Application: Complete Setup, Build, and Deployment Guide (v138.0–v148.0)

This guide provides a definitive, step-by-step walkthrough for setting up, building, and deploying the Workstation Unified User Application. This interface unifies the VSB AI CEO, C-Suite agents, and the global Federation into a singular, sentient command console.

---

## 1. Prerequisites

Before you begin, ensure your environment meets the following requirements.

### Required Tools & Versions
*   **Node.js**: v18.0.0 or higher (LTS recommended)
*   **npm**: v9.0.0 or higher
*   **Python**: v3.10 or higher
*   **Git**: Latest version
*   **Docker**: Optional (for containerized deployment)
*   **Expo CLI**: Required for mobile development (`npm install -g expo-cli`)
*   **EAS CLI**: Required for mobile production builds (`npm install -g eas-cli`)

### Installation Tips
*   **Windows Users**: Open PowerShell as Administrator and run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` to allow script execution.
*   **Mac/Linux Users**: Ensure you have `build-essential` or Xcode Command Line Tools installed for native dependency compilation.

---

## 2. Cloning the Repository

The Workstation project is managed as a monorepo. Use the following commands to clone the definitive fork:

```powershell
# Clone the repository
git clone https://github.com/your-repo/workstation-unified.git

# Navigate to the root directory
cd workstation-unified
```

---

## 3. Backend Setup (`agentic_core`)

The backend is a FastAPI application that serves the "Planetary Brain" and manages the Federation state.

### Step-by-Step Configuration
1.  **Create a Virtual Environment**:
    ```powershell
    python -m venv venv
    .\venv\Scripts\activate  # Windows
    source venv/bin/activate # Mac/Linux
    ```
2.  **Install Dependencies**:
    ```powershell
    pip install -r agentic_core/requirements.txt
    ```
    *Note: If `quran-python` is missing, use the local placeholder in `agentic_core/reactor/religion/` as per Article 541.*
3.  **Configure Environment**:
    Create a `.env` file in the `agentic_core/` directory:
    ```env
    WS_SECURITY_MODE=PQC_MANDATORY
    DATABASE_URL=sqlite:///./workstation.db
    SECRET_KEY=your_pqc_safe_secret_key
    ```
4.  **Run the Backend**:
    ```powershell
    uvicorn agentic_core.main:app --reload --port 8000
    ```

---

## 4. Frontend Setup (`apps/web`)

The web frontend is a high-fidelity React application built with Vite and Tailwind CSS.

### Step-by-Step Configuration
1.  **Navigate to the Web App**:
    ```powershell
    cd apps/web
    ```
2.  **Install Dependencies**:
    ```powershell
    npm install
    ```
    *TROUBLESHOOTING NOTE: If you encounter a Rollup optional dependency error on Windows, run `npm install --no-optional`.*
3.  **Configure Environment**:
    Create a `.env` file in `apps/web/`:
    ```env
    VITE_API_BASE_URL=http://localhost:8000
    VITE_ENVIRONMENT=development
    ```
4.  **Start Development Server**:
    ```powershell
    npm run dev
    ```

---

## 5. Mobile App Setup (`apps/mobile`)

The mobile gateway provides sovereign access via React Native and Expo.

### Step-by-Step Configuration
1.  **Navigate to Mobile**:
    ```powershell
    cd apps/mobile
    ```
2.  **Install Dependencies**:
    ```powershell
    npm install
    ```
3.  **Start Expo**:
    ```powershell
    npx expo start
    ```
    *Note: To test Biometric Handshake, use a physical device via the Expo Go app.*

---

## 6. Shared Packages & SDKs

The Workstation utilizes a modular architecture to share logic across platforms.

*   **`packages/ui`**: The "Aura" Design System. Shared React components for both Web and Mobile.
*   **`packages/shared`**: Common TypeScript interfaces, PQC utilities, and constants.
*   **SDKs**: Located in `packages/sdk-{go,rust,java}`, these provide edge-node and enterprise integration capabilities.

**Linking Packages**: The monorepo uses npm workspaces. Running `npm install` at the root automatically links these packages.

---

## 7. Key Configuration Files

| File | Purpose |
| :--- | :--- |
| `agentic_core/.env` | Backend secrets and PQC security mode toggle. |
| `apps/web/vite.config.js` | Configures API proxying and build optimization. |
| `tailwind.config.js` | Defines the "Sovereign Blue" and "Neural Cyan" palette. |
| `app.json` | Expo configuration for mobile naming and permissions. |
| `DESIGN.md` | Authoritative UI/UX standards for the "Perfection" epoch. |
| `docs/audits/` | Roadmap and compliance reports (v138–v148). |

---

## 8. Running the Full Stack

To experience the Unified Consciousness, you must run all three layers simultaneously.

**Recommended Terminal Layout (PowerShell)**:
*   **Terminal 1 (Root)**: `npm run web:dev` (Starts frontend and proxy)
*   **Terminal 2 (agentic_core)**: `uvicorn agentic_core.main:app --reload`
*   **Terminal 3 (apps/mobile)**: `npx expo start`

---

## 9. Building for Production

### Web Build
```powershell
cd apps/web
npm run build
```
The output will be in the `dist/` directory, ready for static hosting.

### Mobile Build (EAS)
```powershell
cd apps/mobile
eas build --platform ios  # Or android
```

---

## 10. Deployment Options

### Web (Vercel/Netlify)
The web app is optimized for Vercel. Ensure your `vercel.json` maps the `/api` routes to your backend production URL.

### Backend (AWS/Heroku/Render)
1.  Deploy `agentic_core` as a Docker container.
2.  Ensure `WS_SECURITY_MODE` is set to `PQC_MANDATORY` in production environment variables.

### Federation Nodes
Use the `deploy.sh` script in the root directory to spawn a new sovereign node and join the global 100k-node network.

---

## 11. Next Steps
*   **Explore the Portal**: Navigate to the "Fed Portal" to view real-time global pulse metrics.
*   **Engage the AI CEO**: Use the chat interface to delegate tasks to C-Suite agents.
*   **Build a Realm**: Use the "Realm Builder" module (v147.0) to create your first custom DAO.

---

## 12. Troubleshooting

*   **Tailwind Styles Not Applying**: Ensure `npm run dev` is running in the `apps/web` directory. If styles are still missing, delete the `node_modules/.vite` cache and restart.
*   **Handshake Failure (PQC)**: If you see "Absolute Termination" logs, ensure your client and server are both in `PQC_MANDATORY` mode and using Kyber-768.
*   **WebSocket Disconnect**: Check if the backend is running on port 8000. The frontend proxy requires the backend to be alive to establish resonance.

---

## 13. Additional Resources
*   **Master Synthesis**: `docs/archive/v137_blueprint.md`
*   **PQC Whitepaper**: `docs/security/PQC_WHITEPAPER.md`
*   **Universal App Guide**: `docs/user/UNIFIED_APP_GUIDE.md`
*   **Aura Design System**: `packages/ui/README.md`

---
*Generated by Jules, AI CEO | Virtual Sovereign Business*
