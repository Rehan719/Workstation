# Jules AI: Troubleshooting Guide (v99.0)

Common issues and resolution steps for the Jules AI Workstation.

## 🛠 Common Issues

### 1. SIH Preemption (Error: `SIH_PREEMPTION`)
- **Cause:** System energy levels (ATP/ADP ratio) are below the threshold (2.5).
- **Resolution:** Reduce system load or wait for the Triad cycle to recover energy levels. Check `molecular/triad_integration.py` for metabolic state.

### 2. Rate Limit Exceeded (`RATE_LIMIT_EXCEEDED`)
- **Cause:** Too many requests to an external connector (e.g., Slack, GSheets) within a one-minute window.
- **Resolution:** Implement client-side exponential backoff or increase the `rate_limit` for the connector in `agentic_core/integrations/connector_registry.py`.

### 3. JWT Authentication Failure
- **Cause:** Token expired or invalid `JULES_JWT_SECRET`.
- **Resolution:** Re-authenticate to obtain a new token. Ensure the secret key matches across all services.

### 4. Quantum Routing Failure
- **Cause:** No available backend meets the circuit requirements.
- **Resolution:** Simplify the quantum circuit or add more backends to the `UnifiedQuantumGateway`.

## 📜 Error Codes
| Code | Description | Action |
|---|---|---|
| `E100` | Constitutional Violation | Check `traceability_matrix_v99.md` |
| `E150` | Database Connection Failed | Verify `JULES_DB_URL` |
| `E147` | Sandbox Escape Detected | System Locked; Manual Reset Required |
| `E99`  | Transcendent Desync | Restart the Pulse Clock |
