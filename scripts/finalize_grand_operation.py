import asyncio
import json
import os
import sys
from pathlib import Path

sys.path.append(os.getcwd())

from src.organism.python.utils.bundler import TribunalBundleGenerator
from src.organism.python.core.audit import verify_chain

async def finalize_operation():
    print("--- 🔐 Final Sovereign Verification & Packaging ---")

    # 1. Verify Audit Chain
    log_path = "data/organism/activity.jsonl"
    if not verify_chain(log_path):
        print("CRITICAL: Audit chain verification failed. Aborting packaging.")
        return

    # 2. Prepare Documents for Bundle
    outputs_dir = Path("outputs")
    documents = []
    for file in outputs_dir.glob("*.md"):
        documents.append({
            "name": file.name,
            "content": file.read_text().encode()
        })

    # 3. Load Audit Trail for inclusion
    audit_trail = []
    with open(log_path, "r") as f:
        for line in f:
            audit_trail.append(json.loads(line))

    # 4. Generate Immutable Package
    bundler = TribunalBundleGenerator()
    bundle_path = bundler.generate(
        case_id="MINHAS-LONZA-v5",
        documents=documents,
        audit_trail=audit_trail,
        output_dir="data/organism/bundles"
    )

    print(f"\nSUCCESS: Immutable Litigation Package created at: {bundle_path}")

if __name__ == "__main__":
    asyncio.run(finalize_operation())
