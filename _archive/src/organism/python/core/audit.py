import sys
import json
import hashlib
import argparse

def verify_chain(log_path: str) -> bool:
    """Verifies the hash chain integrity of the Sovereign Audit Log."""
    print(f"Auditing chain: {log_path}")

    expected_prev_hash = "0" * 64
    line_num = 0

    try:
        with open(log_path, "r") as f:
            for line in f:
                line_num += 1
                entry = json.loads(line)

                # Check current hash vs stored hash
                stored_hash = entry.pop("hash", None)
                calculated_hash = hashlib.sha256(json.dumps(entry, sort_keys=True).encode()).hexdigest()

                if stored_hash != calculated_hash:
                    print(f"CRITICAL: Hash mismatch at line {line_num}")
                    print(f"  Stored: {stored_hash}")
                    print(f"  Calc'd: {calculated_hash}")
                    return False

                # Check prev_hash link
                if entry.get("prev_hash") != expected_prev_hash:
                    print(f"CRITICAL: Chain broken at line {line_num}")
                    print(f"  Expected prev: {expected_prev_hash}")
                    print(f"  Found prev:    {entry.get('prev_hash')}")
                    return False

                expected_prev_hash = calculated_hash

        print(f"SUCCESS: Hash chain verified for {line_num} entries.")
        return True
    except Exception as e:
        print(f"ERROR: Audit failed: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sovereign Audit Chain Verifier")
    parser.add_argument("--path", default="data/organism/activity.jsonl", help="Path to audit log")
    args = parser.parse_args()

    if verify_chain(args.path):
        sys.exit(0)
    else:
        sys.exit(1)
