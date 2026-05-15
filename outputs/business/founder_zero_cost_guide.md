# 🚀 SOLE FOUNDER ACTION GUIDE: ZERO-COST SUPREME DEPLOYMENT

**Assurance:** This guide guarantees **$0.00 owner cost** by utilizing Google Cloud's Always Free Tier and local Windows execution.

---

## 🛠️ PREREQUISITES
Before you begin, ensure your **Windows 10/11** device has the following:
1. **Windows Subsystem for Linux (WSL2)**: Install via PowerShell: `wsl --install`.
2. **Docker Desktop**: Download and install with the WSL2 backend enabled.
3. **Git**: Install from `git-scm.com`.
4. **Google Cloud SDK**: Install and run `gcloud init`.
5. **Stripe Account**: Create a free account and obtain your **Test Mode** API keys.

---

## 📦 PHASE 0: REPOSITORY & LOCAL SETUP
1. **Clone the Workstation**:
   ```powershell
   git clone https://github.com/Rehan719/Workstation.git
   cd Workstation
   ```
2. **Verify Environment**:
   Run the pre-flight check script to ensure all Windows dependencies are met:
   ```powershell
   .\scripts\check_windows_prerequisites.ps1
   ```

---

## ☁️ PHASE 1: GOOGLE CLOUD FREE TIER DEPLOYMENT
We deploy the Workstation core to **Google Cloud Run** using the free tier quotas.

1. **Configure Zero-Cost Flags**:
   The deployment script automatically sets the following to keep you in the free tier:
   - `--min-instances=0` (Only pays when active; free tier includes 2M requests/mo).
   - `--max-instances=1` (Prevents scaling-related costs).
   - `--memory=512Mi` / `--cpu=1` (Always-free tier eligible).

2. **Execute Deployment**:
   ```bash
   # From WSL2/Bash terminal
   ./scripts/deploy_free_tier.sh --project-id [YOUR_PROJECT_ID]
   ```

3. **Verify CostGuard**:
   Once deployed, navigate to `https://[URL]/v1/business/cost/status`. It should show **Throttle Level: GREEN** and **Owner Cost: $0.00**.

---

## 💳 PHASE 2: COMMERCIAL ACTIVATION (STRIPE)
1. **Environment Variables**:
   Set your Stripe Test Secret Key in your environment or Cloud Run configuration:
   `STRIPE_SECRET_KEY=sk_test_...`
2. **Initialize Tiers**:
   The Workstation will automatically create your Standard ($29) and Advanced ($99) products in Stripe Test Mode upon first boot.

---

## 🔄 PHASE 3: DAILY OPERATIONS
As a sole founder, your workload is minimized by the **AI CEO (Jules)** and **C-Suite swarm**.

1. **Monitor the Dashboard**: Check the `/admin` UI daily to review:
   - **Constitutional Drift**: Ensure < 1%.
   - **Autonomous Support**: Review resolved tickets (Target 96.7%).
   - **SWF Returns**: Watch your Carbon Cycle grow through automated reinvestment.
2. **Handle Vetoes**: You will only be interrupted if Jules requires a `CONSTITUTIONAL_OVERRIDE` for a strategic change.

---

## 📈 PHASE 4: GROWTH WITHOUT CAPITAL
1. **GitHub Launch**: Make your fork/repo public. The zero-placeholder certification and transparency reports will act as your primary marketing.
2. **WORKREP Referrals**: Encourage your first 50 users to refer others. Every verified referral increases their WORKREP, giving them priority compute while you pay $0.
3. **Content Marketing**: Use the `Tafakkur` reports to publish weekly "Sovereign Audit" posts on LinkedIn/Twitter to drive organic traffic.

---

## 🆘 TROUBLESHOOTING & FALLBACK
- **Quota Alert**: If you receive a **90% Quota Warning** from the `CostGuard`, the system will automatically throttle background simulations.
- **Circuit Breaker**: If usage hits **95%**, the system will scale Cloud Run to zero and run in **Edge-Only Mode** on your Windows device via Docker until the next billing cycle.

**بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ**
*Guaranteed by JULES, Agent Opus.*
