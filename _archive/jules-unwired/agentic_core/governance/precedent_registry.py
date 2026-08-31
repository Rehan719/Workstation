"""
PrecedentRegistry – manages UEG-anchored sovereign case law and precedents.
"""
import hashlib
import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime
from firebase_admin import firestore
from agentic_core.ueg.logger import VSBUEGLogger as UEGLogger

db = firestore.client()

class PrecedentRegistry:
    def __init__(self):
        self.ueg = UEGLogger()
        self.seed_dir = "data/sovereign_case_law/"

    async def bootstrap(self):
        """Seed the registry with initial precedents if empty."""
        if not os.path.exists(self.seed_dir):
             return

        for filename in os.listdir(self.seed_dir):
            if filename.endswith(".json"):
                with open(os.path.join(self.seed_dir, filename), "r") as f:
                    precedent = json.load(f)
                    await self.add_precedent(precedent)

    async def add_precedent(self, precedent_data: Dict[str, Any]) -> str:
        """
        Adds a new precedent to the registry and anchors it in UEG.
        """
        precedent_id = precedent_data.get("precedent_id")

        # Calculate SHA-3-512 hash for anchoring
        doc_json = json.dumps(precedent_data, sort_keys=True)
        doc_hash = hashlib.sha3_512(doc_json.encode()).hexdigest()

        # Store in Firestore
        await db.collection("precedents").document(precedent_id).set(precedent_data)

        # Anchor in UEG
        await self.ueg.log_event(
            "PRECEDENT_ANCHORED",
            {
                "precedent_id": precedent_id,
                "title": precedent_data.get("title"),
                "ueg_hash": doc_hash
            }
        )

        return doc_hash

    async def get_all_precedents(self) -> List[Dict[str, Any]]:
        """Retrieves all precedents from the registry."""
        docs = db.collection("precedents").stream()
        return [doc.to_dict() for doc in docs]
