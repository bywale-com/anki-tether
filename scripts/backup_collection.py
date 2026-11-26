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
    collection = Path(os.environ.get("ANKI_COLLECTION", str(data / "collection.anki2")))
    if not collection.is_file():
        raise SystemExit(f"Collection does not exist: {collection}")
    dest.mkdir(parents=True, exist_ok=False)
    shutil.copy2(collection, dest / collection.name)
    timed = collection.with_suffix(".timed.sqlite3")
    if timed.is_file():
        shutil.copy2(timed, dest / timed.name)
    media = collection.with_suffix(".media")
    if media.is_dir():
        shutil.copytree(media, dest / media.name)
    media_db = collection.with_suffix(".media.db2")
    if media_db.is_file():
        shutil.copy2(media_db, dest / media_db.name)
    print(f"Backup written to {dest}")


if __name__ == "__main__":
    main()
