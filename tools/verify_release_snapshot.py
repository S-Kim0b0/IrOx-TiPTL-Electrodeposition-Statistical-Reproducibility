#!/usr/bin/env python3
"""Verify the release snapshot against frozen SHA-256 checksums.

This test uses only the Python standard library. Checksums attest byte identity,
not the validity or experimental independence of the original measurements.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
from pathlib import Path
import subprocess
import sys

REPO = Path(__file__).resolve().parents[1]
MANIFEST = REPO / "RELEASE_SHA256_MANIFEST.csv"

def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as fp:
        for chunk in iter(lambda: fp.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def git_commit(tag):
    # Git repository metadata is not included in GitHub-generated source ZIPs.
    if not (REPO / ".git").exists():
        print("GIT_TAG_CHECK: NOT_APPLICABLE (downloaded source archive has no .git)")
        return True
    p = subprocess.run(["git", "rev-parse", "--verify", f"{tag}^{{commit}}"], cwd=REPO, capture_output=True, text=True)
    if p.returncode:
        print(f"GIT_TAG_CHECK: FAIL (tag {tag} is not present)")
        return False
    tag_sha = p.stdout.strip()
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, check=True, text=True, capture_output=True).stdout.strip()
    print("RELEASE_TAG:",tag,"COMMIT:",tag_sha,"HEAD:",head)
    return tag_sha == head

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scope", choices=("source", "all"), default="source",
                    help="source: code/config/input/guide; all: also archived output CSV bytes")
    ap.add_argument("--tag", help="Optional Git tag to compare with checkout HEAD (e.g., v1.0.0)")
    opts = ap.parse_args()
    with MANIFEST.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    tested=0; failed=[]
    for r in rows:
        if opts.scope == "source" and r["category"] == "archived_output":
            continue
        path = REPO / r["path"]
        actual = digest(path) if path.is_file() else None
        if actual != r["sha256"]:
            failed.append(r["path"])
        tested+=1
    print(f"MANIFEST: checked={tested}, mismatches={len(failed)}, scope={opts.scope}")
    for name in failed[:20]: print("MISMATCH:",name)
    valid = not failed
    if opts.tag: valid = git_commit(opts.tag) and valid
    print("RELEASE_SNAPSHOT_VERDICT:","PASS" if valid else "FAIL")
    return 0 if valid else 1

if __name__ == "__main__":
    sys.exit(main())
