import json
from datetime import datetime
import random
import os

class BiasDetector:
    def __init__(self, ethics_path="outputs/Religion/QuranEducation/ethics/bias_audits.jsonl"):
        self.ethics_path = ethics_path
        os.makedirs(os.path.dirname(self.ethics_path), exist_ok=True)

    def detect_bias(self, content_id, content_data, bias_type="sectarian"):
        # Bias detection simulation
        if bias_type == "sectarian":
            # Check for mention of specific schools of thought
            keywords = ["hanafi", "maliki", "shafi'i", "hanbali", "ja'fari"]
            bias_score = self._calculate_bias_score(content_data, keywords)
            self._log_bias_assessment(content_id, "sectarian", bias_score)
            return {"success": True, "bias_score": bias_score, "mitigation_required": bias_score > 0.7}

        elif bias_type == "dialect":
            # Check for regional dialect bias in Tajweed audio (Simulation)
            dialects = ["egyptian", "gulf", "maghrebi", "south_asian"]
            bias_score = random.uniform(0.1, 0.4) # Mock dialect bias score
            self._log_bias_assessment(content_id, "dialect", bias_score)
            return {"success": True, "bias_score": bias_score, "mitigation_required": bias_score > 0.6}

        elif bias_type == "gender":
            # Check for gender representation in examples (Simulation)
            bias_score = random.uniform(0.3, 0.6) # Mock gender bias score
            self._log_bias_assessment(content_id, "gender", bias_score)
            return {"success": True, "bias_score": bias_score, "mitigation_required": bias_score > 0.8}

        return {"success": False, "reason": "Unsupported bias type"}

    def _calculate_bias_score(self, content, keywords):
        # Very simple keyword-based bias score calculation for simulation
        if not content:
            return 0.0
        content_lower = content.lower()
        counts = [content_lower.count(k) for k in keywords]
        if sum(counts) == 0:
            return 0.1 # Baseline bias

        # Calculate deviation from even distribution
        # High deviation = high bias toward one school
        max_count = max(counts)
        total_counts = sum(counts)
        bias_score = max_count / total_counts if total_counts > 0 else 0.1
        return min(0.9, bias_score)

    def _log_bias_assessment(self, content_id, bias_type, score):
        assessment = {
            "timestamp": str(datetime.now()),
            "content_id": content_id,
            "bias_type": bias_type,
            "bias_score": score,
            "mitigation_performed": score > 0.7 # In a real system, this would trigger a mitigation action
        }
        with open(self.ethics_path, 'a') as f:
            f.write(json.dumps(assessment) + "\n")
        return assessment

class EthicsAuditor:
    def __init__(self, audit_path="outputs/Religion/QuranEducation/ethics/ethics_audit_trail.jsonl"):
        self.audit_path = audit_path
        os.makedirs(os.path.dirname(self.audit_path), exist_ok=True)

    def audit_ai_ethics(self, model_id, action_id, ethics_metadata):
        audit_entry = {
            "timestamp": str(datetime.now()),
            "model_id": model_id,
            "action_id": action_id,
            "ethics_metadata": ethics_metadata,
            "compliance_status": "pass" if ethics_metadata.get("bias_score", 0) < 0.7 else "fail"
        }
        with open(self.audit_path, 'a') as f:
            f.write(json.dumps(audit_entry) + "\n")
        return audit_entry
