"""Entry for make.fun news-image-20261119.

Copies the pre-built image for Thursday 19 November 2026 to the
output directory. Standard library only, no network, deterministic:
the same bytes are written on every run.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png"


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    shutil.copyfile(SRC, dest)
    # Fail loudly instead of silently shipping a partial copy.
    if not dest.is_file() or dest.stat().st_size != SRC.stat().st_size:
        raise RuntimeError("entry.png was not copied completely")
    print(f"wrote {dest} ({dest.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
