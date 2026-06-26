import requests
import json
import os
import hashlib
from datetime import datetime, timezone

class QuranAPIFetcher:
    """
    Fetcher for Quranic text and metadata from Quran.com API
    Domain: RELIGION::QEP
    """
    BASE_URL = "https://api.quran.com/api/v4"

    def __init__(self, output_dir="ingest/sources/Religion/QuranEducation/quran_text"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.session = requests.Session()

    def fetch_surah(self, surah_number):
        """Fetches surah details and verses"""
        endpoint = f"{self.BASE_URL}/chapters/{surah_number}"
        response = self.session.get(endpoint)
        response.raise_for_status()
        data = response.json()

        # Save Surah metadata
        filename = f"surah_{surah_number}_metadata.json"
        self._save_json(filename, data)
        return data

    def fetch_verses(self, surah_number, page=1):
        """Fetches verses for a specific surah"""
        endpoint = f"{self.BASE_URL}/verses/by_chapter/{surah_number}"
        params = {
            "language": "en",
            "words": True,
            "page": page,
            "per_page": 50
        }
        response = self.session.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()

        # Save verses
        filename = f"surah_{surah_number}_verses_page_{page}.json"
        self._save_json(filename, data)
        return data

    def _save_json(self, filename, data):
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

        # Log hashing for VSB
        content = json.dumps(data, sort_keys=True)
        file_hash = hashlib.sha256(content.encode()).hexdigest()
        print(f"Saved {filename} (Hash: {file_hash})")

        # Register in audit log (simulated)
        self._log_audit(filename, file_hash)

    def _log_audit(self, filename, file_hash):
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": "INGEST_FETCH",
            "file": filename,
            "hash": file_hash,
            "domain": "RELIGION::QEP"
        }
        log_file = "outputs/Religion/QuranEducation/audit/ingest_audit.jsonl"
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        with open(log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

if __name__ == "__main__":
    fetcher = QuranAPIFetcher()
    print("Fetching Surah Al-Fatihah (1)...")
    fetcher.fetch_surah(1)
    fetcher.fetch_verses(1)
    print("Ingestion complete.")
