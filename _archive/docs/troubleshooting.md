# Troubleshooting Guide v99.0.0

## 🛠️ Common Issues & Resolutions

### 1. SIH_PREEMPTION Error
- **Symptom**: Agent stops responding and logs `SIH VETO: Critical energy depletion`.
- **Cause**: Simulated ATP levels dropped below 2.5.
- **Resolution**: Pause background simulations or increase resource allocation to the digestive system.

### 2. Import Errors in agentic_core
- **Symptom**: `ModuleNotFoundError` when importing core modules.
- **Resolution**: Ensure `PYTHONPATH` is set to the repository root: `export PYTHONPATH=\$PYTHONPATH:.`

### 3. Shared Memory Leak
- **Symptom**: `UserWarning: resource_tracker: leaked shared_memory objects`.
- **Resolution**: Occurs on forced shutdown. The `GlobalWorkspace` automatically cleans up on a clean `shutdown()` call.

### 4. Safety Validation Failure
- **Symptom**: `ASSIMILATION: Evolved genome failed safety validation`.
- **Cause**: Evolution produced traits containing unauthorized patterns (e.g., `DELETE_SYSTEM`).
- **Resolution**: Normal behavior. The system automatically discards unsafe mutations.

---
*Transcendent Support Architecture*
