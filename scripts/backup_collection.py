#!/usr/bin/env python3
"""Copy the Anki collection and media folder to a timestamped backup directory."""

from __future__ import annotations

import os
import shutil
from datetime import datetime, timezone
from pathlib import Path


def main() -> None:
    data = Path(os.environ.get("ANKI_DATA_DIR", "data"))
    dest_root = Path(os.environ.get("BACKUP_DIR", "backups"))
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    dest = dest_root / stamp
    dest.mkdir(parents=True, exist_ok=True)
    collection = Path(os.environ.get("ANKI_COLLECTION", str(data / "collection.anki2")))
    if collection.exists():
        shutil.copy2(collection, dest / collection.name)
    media = data / "collection.media"
    if media.exists():
        shutil.copytree(media, dest / "collection.media", dirs_exist_ok=True)
    print(f"Backup written to {dest}")


if __name__ == "__main__":
    main()
