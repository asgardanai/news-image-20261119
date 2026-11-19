"""news-image-20261119 entrypoint.

Copies the entry image (entry.png, next to this file) to the output
directory (/output, or $MAKEFUN_OUTPUT_DIR for local runs) and verifies
byte identity between source and copy via SHA-256.

Stdlib only, no network.
"""

import hashlib
import os
import shutil
import sys


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")

    shutil.copyfile(src, dst)

    src_hash = sha256_of(src)
    dst_hash = sha256_of(dst)
    if src_hash != dst_hash:
        print(f"self-check FAILED: {src_hash} != {dst_hash}", file=sys.stderr)
        return 1
    # Also confirm the copy has the same size as the source.
    if os.path.getsize(src) != os.path.getsize(dst):
        print("self-check FAILED: size mismatch", file=sys.stderr)
        return 1
    print(f"entry.png copied to {dst} (sha256 {dst_hash})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
