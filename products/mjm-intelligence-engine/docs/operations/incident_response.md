# MJM Incident Response Playbook

## SEV-1: Provenance Chain Break
**Symptoms:**
- Integrity verification failures in `MJMWorkflowOrchestrator`.
- Hash mismatches in `ProvenanceGraph`.

**Immediate Actions:**
1. Halt all active workflows using the feature flag `workflows.enabled: false`.
2. Inspect `audit_logger.log` for the first sign of corruption.
3. Revert to the last known-good checkpoint.

## SEV-2: Zero-Trust Authentication Failure
**Symptoms:**
- High rejection rate in `ZeroTrustSecurityManager`.
- Signature mismatches.

**Actions:**
1. Verify if system secret keys have rotated without notification.
2. Check client signature implementation for compatibility.
