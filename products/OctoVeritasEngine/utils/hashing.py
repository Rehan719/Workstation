import hashlib
import os
from typing import Any

def calculate_sha3_512(content: Any) -> str:
    sha3 = hashlib.sha3_512()
    if isinstance(content, bytes):
        sha3.update(content)
    else:
        sha3.update(str(content).encode())
    return sha3.hexdigest()

def attach_hash_to_file(file_path: str, content: Any):
    """
    Appends the SHA3-512 hash to a hidden manifest file or metadata.
    For Phase Q2, we create a .hash file alongside the asset.
    """
    asset_hash = calculate_sha3_512(content)
    hash_file = f"{file_path}.hash"
    with open(hash_file, "w") as f:
        f.write(asset_hash)
    return asset_hash

def verify_asset_integrity(file_path: str) -> bool:
    hash_file = f"{file_path}.hash"
    if not os.path.exists(hash_file):
        return False

    with open(hash_file, "r") as f:
        stored_hash = f.read().strip()

    with open(file_path, "rb") as f:
        current_content = f.read()

    current_hash = calculate_sha3_512(current_content)
    return stored_hash == current_hash
