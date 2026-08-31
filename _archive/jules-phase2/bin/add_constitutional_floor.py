#!/usr/bin/env python3
import argparse
import json
import hashlib
import os
from datetime import datetime

def add_floor(floor_id, source_path, constitution_path):
    """
    Add a new constitutional floor to the specified constitution file.
    Includes SHA-3-512 audit trail for each article.
    """
    if not os.path.exists(source_path):
        print(f"Error: Source file {source_path} not found.")
        return

    with open(source_path, 'r') as f:
        floor_data = json.load(f)

    if not os.path.exists(constitution_path):
        # Create a new version if it doesn't exist
        with open(constitution_path, 'w') as f:
            f.write(f"# Workstation Constitution v139.0.0\n\nGenerated on {datetime.utcnow()}\n\n")

    with open(constitution_path, 'a') as f:
        f.write(f"\n## Floor {floor_id}: {floor_data.get('name')}\n")
        f.write(f"**Status: Immutable** | **Timestamp: {datetime.utcnow().isoformat()}**\n\n")

        for article in floor_data.get("articles", []):
            art_num = article.get("number")
            title = article.get("title")
            mandate = article.get("mandate")

            # Compute audit hash
            payload = json.dumps(article, sort_keys=True)
            audit_hash = hashlib.sha3_512(payload.encode()).hexdigest()

            f.write(f"### Article {art_num}: {title}\n")
            f.write(f"{mandate}\n\n")
            f.write(f"*Audit Hash (SHA-3-512):* `{audit_hash}`\n\n")

    print(f"Successfully added Floor {floor_id} to {constitution_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add constitutional floor with SHA-3-512 audit trail.")
    parser.add_argument("--floor", required=True, type=int, help="Floor ID to add")
    parser.add_argument("--source", required=True, help="Path to JSON floor definition")
    parser.add_argument("--target", default="agentic_core/constitution/CONSTITUTION_v139.0.0.md", help="Target constitution file")

    args = parser.parse_args()
    add_floor(args.floor, args.source, args.target)
