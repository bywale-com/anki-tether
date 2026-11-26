"""Application-owned SQLite records stored beside the Anki collection."""

from contextlib import contextmanager
import json
import sqlite3

from app import config


def _path():
    return config.COLLECTION_PATH.with_suffix(".timed.sqlite3")


@contextmanager
def _database():
    db = sqlite3.connect(_path())
    try:
        with db:
            db.execute("""create table if not exists attempts (
                id text primary key, status text not null, started_at text not null, data text not null
            )""")
            db.execute("""create unique index if not exists one_open_attempt
                on attempts ((1)) where status in ('active', 'paused')""")
            yield db
    finally:
        db.close()


def active_id():
    if not _path().exists():
        return None
    with _database() as db:
        row = db.execute("select id from attempts where status in ('active', 'paused')").fetchone()
    return row[0] if row else None


def read(session_id):
    if not _path().exists():
        return None
    with _database() as db:
        row = db.execute("select data from attempts where id = ?", (session_id,)).fetchone()
    return json.loads(row[0]) if row else None


def save(session):
    with _database() as db:
        db.execute(
            """insert into attempts values (?, ?, ?, ?)
               on conflict(id) do update set status = excluded.status, data = excluded.data""",
            (session["id"], session["status"], session["started_at"], json.dumps(session)),
        )


def history():
    if not _path().exists():
        return []
    with _database() as db:
        return [json.loads(row[0]) for row in db.execute("select data from attempts order by started_at, id")]
