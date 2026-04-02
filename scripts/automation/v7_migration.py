import os
import shutil
import json
from datetime import datetime

def migrate():
    print("🚀 Starting Workstation v7.0 Enhanced Migration...")

    # 1. Standardized Casing Mapping
    domains = ["Religion", "Science", "Law", "Employment", "Care", "Enterprise"]
    base_dirs = ["ingest", "knowledge", "outputs", "scripts", "archive", "docs", "logs", "configs"]

    # Create all base and domain folders
    for base in base_dirs:
        for domain in domains:
            path = os.path.join(base, domain)
            if not os.path.exists(path):
                os.makedirs(path, exist_ok=True)

    # Create sub-structures
    sub_structures = {
        "ingest": ["sources", "metadata"],
        "ingest/metadata": ["hashes", "audit", "vsb"],
        "knowledge": ["ontology", "vsb_history", "grn"],
        "outputs": ["Cross-Domain"],
        "outputs/Cross-Domain": ["achievements", "reports", "integrations"],
        "archive": ["superseded", "reruns"],
    }
    for parent, subs in sub_structures.items():
        for sub in subs:
            path = os.path.join(parent, sub)
            if not os.path.exists(path):
                os.makedirs(path, exist_ok=True)

    # Re-create domain folders under sub-structures
    for domain in domains:
        os.makedirs(os.path.join("ingest", domain, "sources"), exist_ok=True)
        os.makedirs(os.path.join("archive/superseded", domain), exist_ok=True)
        os.makedirs(os.path.join("archive/reruns", domain), exist_ok=True)

    # 2. Migrate Source Documents to Ingest Folders
    # Religion Sources
    rel_sources = [f for f in os.listdir('.') if "Path to Allah" in f]
    rel_sources += [f for f in os.listdir('.') if "Loving-Allahs-Beloved" in f]
    for f in rel_sources:
        if os.path.isfile(f):
            shutil.copy2(f, os.path.join("ingest", "Religion", "sources", f))
            print(f"📄 Copied {f} to ingest/Religion/sources/")

    # Employment Sources
    emp_sources = [f for f in os.listdir('.') if "RM CV" in f or "Rehan Minhas CV" in f or "Lonza" in f or "Healthcare Scientist" in f or "Civil Service" in f or "Interview prep" in f or "Application_Form" in f or "Information+Sheet" in f]
    for f in emp_sources:
        if os.path.isfile(f):
            shutil.copy2(f, os.path.join("ingest", "Employment", "sources", f))
            print(f"📄 Copied {f} to ingest/Employment/sources/")

    # 3. Migrate Knowledge and Scripts (Standardizing Casing)
    migration_map = {
        "knowledge/religion": "knowledge/Religion",
        "knowledge/employment": "knowledge/Employment",
        "scripts/religion": "scripts/Religion",
        "scripts/career": "scripts/Employment/career_scripts",
    }
    for old_path, new_path in migration_map.items():
        if os.path.exists(old_path) and old_path != new_path:
            print(f"🔄 Standardizing {old_path} to {new_path}...")
            if os.path.exists(new_path):
                for item in os.listdir(old_path):
                    s = os.path.join(old_path, item)
                    d = os.path.join(new_path, item)
                    if os.path.isdir(s):
                        shutil.copytree(s, d, dirs_exist_ok=True)
                        shutil.rmtree(s)
                    else:
                        shutil.move(s, d)
                os.rmdir(old_path)
            else:
                os.rename(old_path, new_path)

    # 4. Handle Career/Employment Migration
    old_career_output = "outputs/Career"
    new_employment_output = "outputs/Employment"
    if os.path.exists(old_career_output):
        print(f"🚚 Migrating {old_career_output} to {new_employment_output}...")
        for item in os.listdir(old_career_output):
            s = os.path.join(old_career_output, item)
            d = os.path.join(new_employment_output, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
                shutil.rmtree(s)
            else:
                shutil.move(s, d)
        os.rmdir(old_career_output)

    # 5. Litigation Files Migration
    law_output = "outputs/Law"
    print(f"⚖️ Ensuring litigation files in {law_output}...")
    for filename in os.listdir("outputs"):
        if filename[0:2].isdigit() and filename[2] == "_" and os.path.isfile(os.path.join("outputs", filename)):
            shutil.move(os.path.join("outputs", filename), os.path.join(law_output, filename))
            print(f"  -> Moved {filename}")

    # 6. Archive Initialization with Real Artifacts
    # Religion v1.0-v6.0
    rel_output = "outputs/Religion"
    if os.path.exists(rel_output):
        for item in os.listdir(rel_output):
            if "release" in item or "v5.0" in item or "v4.0" in item:
                # Assuming existing releases go to superseded for v7.0
                print(f"📦 Preparing to archive Religion/{item}...")
                # (Actual movement will be handled by v7_init_systems.py)

    print("✅ Enhanced Migration Complete.")

if __name__ == "__main__":
    migrate()
