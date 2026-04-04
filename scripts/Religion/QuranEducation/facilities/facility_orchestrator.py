import os
import json
import time
import datetime
import yaml
import logging

class FacilityOrchestrator:
    """
    Facility-based management layer for QEP v8.8.
    Wraps pipeline execution and enforces safety protocols.
    """
    def __init__(self, protocols_path="configs/facilities/operational_protocols_v8.8.yaml"):
        with open(protocols_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.facilities = self.config['facility_protocols']
        self.log_dir = "archive/qep-v8.8-industrial-ecosystem/facility_logs/"
        os.makedirs(self.log_dir, exist_ok=True)

        self.audit_log_path = "outputs/Religion/QuranEducation/audit/sovereign_audit_log_v8.8.jsonl"
        os.makedirs(os.path.dirname(self.audit_log_path), exist_ok=True)

    def _log_to_audit(self, entry):
        entry['timestamp'] = datetime.datetime.now().isoformat()
        with open(self.audit_log_path, 'a') as f:
            f.write(json.dumps(entry) + "\n")

    def _log_facility_metric(self, facility_id, metric_type, value):
        log_file = os.path.join(self.log_dir, f"{facility_id}.jsonl")
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "metric": metric_type,
            "value": value
        }
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + "\n")

    def run_in_facility(self, facility_id, pipeline_step, task_fn, *args, **kwargs):
        """
        Runs a task within a specific facility context.
        """
        if facility_id not in self.facilities:
            raise ValueError(f"Unknown facility: {facility_id}")

        facility = self.facilities[facility_id]
        print(f"🏭 [Facility: {facility_id}] Starting task: {pipeline_step}")

        start_time = time.time()

        self._log_to_audit({
            "event": "facility_task_start",
            "facility": facility_id,
            "pipeline_step": pipeline_step,
            "status": "processing"
        })

        try:
            # Execute the task (pop item_count as it's a facility metric, not task arg)
            task_kwargs = kwargs.copy()
            item_count = task_kwargs.pop('item_count', 1)

            result = task_fn(*args, **task_kwargs)

            execution_time = time.time() - start_time

            # Log metrics
            self._log_facility_metric(facility_id, "execution_time", execution_time)
            self._log_facility_metric(facility_id, "throughput", item_count)

            self._log_to_audit({
                "event": "facility_task_complete",
                "facility": facility_id,
                "pipeline_step": pipeline_step,
                "status": "success",
                "duration": execution_time
            })

            print(f"✅ [Facility: {facility_id}] Task complete: {pipeline_step} ({execution_time:.2f}s)")
            return result

        except Exception as e:
            self._log_to_audit({
                "event": "facility_task_failure",
                "facility": facility_id,
                "pipeline_step": pipeline_step,
                "status": "failed",
                "error": str(e)
            })
            print(f"❌ [Facility: {facility_id}] Task failed: {pipeline_step} - {str(e)}")

            # Simulated Safety Protocol: Containment
            if facility_id == "reactors":
                self.handle_safety_containment(facility_id, pipeline_step, str(e))

            raise e

    def handle_safety_containment(self, facility_id, pipeline_step, error_msg):
        """
        Simulated Safety Protocol: Containment on theological anomaly.
        """
        print(f"⚠️  [SAFETY] REACTOR CONTAINMENT ACTIVATED: {pipeline_step}")
        self._log_to_audit({
            "event": "safety_containment",
            "facility": facility_id,
            "pipeline_step": pipeline_step,
            "type": "theological_anomaly",
            "message": error_msg,
            "action": "pause_for_scholar_review"
        })

        # Simulated HITL: Pause and wait for mock approval
        print("⏳ Waiting for Scholar Governance Board override...")
        time.sleep(2) # Simulate wait
        print("🔓 [HITL] Scholar override granted. Resuming with containment logs.")

        self._log_to_audit({
            "event": "safety_override",
            "facility": facility_id,
            "pipeline_step": pipeline_step,
            "approver": "Scholar Board (Simulator)",
            "justification": "Anomaly resolved via context injection."
        })

if __name__ == "__main__":
    orchestrator = FacilityOrchestrator()
    # Test Run
    def mock_task(items):
        time.sleep(0.5)
        return f"Processed {len(items)} items"

    orchestrator.run_in_facility("digital_engines", "test_scraping", mock_task, ["item1", "item2"], item_count=2)
