import os
import json
import hashlib

def compute_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def verify_operation():
    base_dir = "outputs/education/sats_2026"
    subdirs = ["predicted_questions", "model_answers", "revision_schedule", "deliverable"]

    pdf_files = []
    for subdir in subdirs:
        path = os.path.join(base_dir, subdir)
        for f in os.listdir(path):
            if f.endswith(".pdf"):
                full_path = os.path.join(path, f)
                size = os.path.getsize(full_path)
                if size > 0:
                    pdf_files.append({
                        "name": f,
                        "path": full_path,
                        "size": size,
                        "hash": compute_sha256(full_path)
                    })

    print(f"Total PDFs found: {len(pdf_files)}")
    if len(pdf_files) != 12:
        print(f"CRITICAL ERROR: Expected 12 PDFs, found {len(pdf_files)}")
        exit(1)

    # Update manifest
    manifest_path = os.path.join(base_dir, "grand_operation_summary.json")
    if os.path.exists(manifest_path):
        with open(manifest_path, "r") as f:
            data = json.load(f)

        data["verified_pdf_deliverables"] = pdf_files
        data["total_pdf_count"] = len(pdf_files)
        data["verification_status"] = "PASSED"

        with open(manifest_path, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Manifest updated: {manifest_path}")
    else:
        print("Manifest not found!")
        exit(1)

if __name__ == "__main__":
    verify_operation()
