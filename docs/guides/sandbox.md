# Sandbox Methodology & Guide – v137.1

The **Workstation Sandbox** is a secure, isolated environment for experimenting with VSB AI CEO directives, agent behaviors, BTO product configurations, and constitutional amendments without affecting production systems.

*Introduced in v137.1.*

## 🌟 Why Use the Sandbox?
- **Risk Mitigation**: Test "Destructive" or "Experimental" modes safely.
- **Cost Simulation**: Estimate the cost of complex Quad Engine Reactor runs.
- **Behavioral Analysis**: Observe agent interactions in a controlled setting.
- **Fidelity Testing**: Verify biomimetic responses against historical benchmarks.

## 🚀 Launching a Sandbox Session

### 1. Via the Web App
1. Log in to the **Developer Realm**.
2. Navigate to the **Sandbox** tab.
3. Click **Initialize New Session**.
4. Select your **Isolation Level**:
   - **L1 (Mock Data)**: Full isolation, no external API calls.
   - **L2 (Hybrid)**: Mock internal state, live external APIs.
   - **L3 (Shadow)**: Clone of production state (Read-only).

### 2. Via the CLI
```bash
python scripts/sandbox_manager.py --init --level L2 --name "test-csuite-deliberation"
```

## 🧪 Common Workflows

### Testing a VSB Directive
To see how Jules (VSB AI CEO) and the C-suite handle a new strategic mandate:
1. Initialize an **L2 Sandbox**.
2. Enter the directive in the **Command Console**.
3. Observe the **Step-by-Step Deliberation Graph**.
4. Review the **Constitutional Impact Report** generated at the end.

### Configuring a BTO Product
1. Load the **Reactor Simulator** within the sandbox.
2. Select a product template (e.g., "Nanophotonic Navigator").
3. Adjust parameters and click **Simulate Assembly**.
4. Check for dependency conflicts or resource bottlenecks.

## 🛡️ Security & Guardrails
- **Data Scrubbing**: Production PII is automatically scrubbed when cloning state (L3).
- **Auto-Teardown**: Sandbox environments expire after 24 hours of inactivity.
- **Audit Logs**: All sandbox actions are logged for developer review, but not committed to the production Merkle DAG.

## 🆘 Troubleshooting
- **Session Failure**: Check your `.env` for valid `SANDBOX_API_KEY`.
- **Resource Limit**: Sandboxes are limited to 2GB RAM on the free tier.
- **Link**: If the UI doesn't load, ensure the `sandbox-service` is running on port `8080`.

---
*Safe experimentation is the engine of evolution.*
