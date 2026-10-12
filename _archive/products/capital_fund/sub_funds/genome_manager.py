from typing import Dict, Any
import hashlib
import json
from datetime import datetime
from firebase_admin import firestore
from agentic_core.ueg.logger import VSBUEGLogger as UEGLogger

db = firestore.client()

class SubFundGenomeManager:
    def __init__(self):
        self.ueg = UEGLogger()

    async def create_genome(self, rules: Dict[str, Any]) -> str:
        doc = {"rules": rules, "created_at": datetime.utcnow().isoformat(), "version": 1}
        doc_json = json.dumps(doc, sort_keys=True)
        doc_hash = hashlib.sha3_512(doc_json.encode()).hexdigest()
        await db.collection("sub_fund_genomes").document(doc_hash).set(doc)
        await self.ueg.log_event("SUB_FUND_GENOME_ANCHORED", {"genome_hash": doc_hash})
        return doc_hash
