from typing import Dict, Any

class ConstitutionalAudit:
    def __init__(self, ueg_logger: Any):
        self.ueg_logger = ueg_logger

    def log_injection_audit(self,
                             job_id: str,
                             article_ids: list,
                             status: str,
                             metadata: Dict[str, Any]):
        """
        Logs a detailed constitutional audit entry for an injection event.
        """
        self.ueg_logger.log_event({
            "operation": "CONSTITUTIONAL_AUDIT",
            "job_id": job_id,
            "article_ids": article_ids,
            "status": status,
            "metadata": metadata,
            "integrity_hash": metadata.get("hash")
        })
