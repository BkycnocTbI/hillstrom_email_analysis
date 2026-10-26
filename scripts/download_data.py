"""Download the source mirror locally and verify both published checksums."""
import gzip
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
metadata = json.loads((ROOT / "data" / "provenance.json").read_text(encoding="utf-8"))
destination = ROOT / "data" / "raw" / "hillstrom.csv"
if destination.exists():
    if hashlib.sha256(destination.read_bytes()).hexdigest() != metadata["csv_sha256"]:
        raise RuntimeError("Existing CSV does not match the recorded source checksum")
    print("Verified existing input:", destination.name)
else:
    with urlopen(metadata["download_url"], timeout=60) as response:
        compressed = response.read()
    if hashlib.md5(compressed).hexdigest() != metadata["compressed_md5"]:
        raise RuntimeError("Compressed source does not match the loader reference MD5")
    if hashlib.sha256(compressed).hexdigest() != metadata["compressed_sha256"]:
        raise RuntimeError("Compressed source SHA-256 mismatch")
    data = gzip.decompress(compressed)
    if hashlib.sha256(data).hexdigest() != metadata["csv_sha256"]:
        raise RuntimeError("Decompressed CSV SHA-256 mismatch")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(data)
    print("Downloaded and verified:", destination.name)
