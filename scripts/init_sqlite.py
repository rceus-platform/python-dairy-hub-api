#!/usr/bin/env python3
"""
Initialize a SQLite database from the SQL files in `app/database`.

This script performs simple, best-effort transformations from PostgreSQL SQL to
SQLite-compatible SQL so you can quickly use the project with a local SQLite
file. It intentionally keeps the transformations conservative; complex
Postgres-only constructs (EXCLUDE, gist, daterange, etc.) are removed.

Run this from the repository root:
    python scripts/init_sqlite.py
"""
from pathlib import Path
import re
import sqlite3


ROOT = Path(__file__).resolve().parents[1]
SQL_DIR = ROOT / "app" / "database"
DB_PATH = SQL_DIR / "dairy_hub.db"


def transform(sql: str) -> str:
    # Remove schema qualifiers like public. (do this early and multiple times to catch all)
    sql = re.sub(r"public\s*\.", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"public\s*\.", "", sql, flags=re.IGNORECASE)  # second pass for nested refs

    # Replace SERIAL PRIMARY KEY with SQLite autoincrement PK
    sql = re.sub(r"\bSERIAL\s+PRIMARY\s+KEY\b", "INTEGER PRIMARY KEY AUTOINCREMENT", sql, flags=re.IGNORECASE)
    sql = re.sub(r"\bSERIAL\b", "INTEGER", sql, flags=re.IGNORECASE)

    # TIMESTAMP WITH TIME ZONE -> DATETIME
    sql = re.sub(r"TIMESTAMP\s+WITH\s+TIME\s+ZONE", "DATETIME", sql, flags=re.IGNORECASE)

    # DECIMAL(x,y) -> NUMERIC
    sql = re.sub(r"DECIMAL\s*\(\s*\d+\s*,\s*\d+\s*\)", "NUMERIC", sql, flags=re.IGNORECASE)

    # Remove COMMENT ON ...; statements
    sql = re.sub(r"COMMENT\s+ON\s+[^;]+;", "", sql, flags=re.IGNORECASE)

    # Remove ALTER TABLE ... statements (migrations) - migrations may not be portable
    sql = re.sub(r"ALTER\s+TABLE[^;]+;", "", sql, flags=re.IGNORECASE)

    # Remove EXCLUDE/GIST/daterange constructs
    sql = re.sub(r"EXCLUDE\s+USING\s+gist[^;]+;", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"daterange\([^\)]*\)", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"::\s*date", "", sql, flags=re.IGNORECASE)
    sql = sql.replace("'infinity'", "'9999-12-31'")

    # Remove leftover CONSTRAINT lines containing unsupported tokens
    sql = re.sub(r"CONSTRAINT[^,\n\)]*(EXCLUDE|USING|gist|\binfinity\b)[^,\n\)]*(,)?", "", sql, flags=re.IGNORECASE)

    # Remove multiple blank lines
    sql = re.sub(r"\n\s*\n", "\n", sql)

    return sql


def apply_sql_file(conn: sqlite3.Connection, path: Path):
    raw = path.read_text()
    t = transform(raw)
    # Split statements on semicolon and execute
    stmts = [s.strip() for s in t.split(";") if s.strip()]
    cur = conn.cursor()
    for s in stmts:
        try:
            cur.execute(s)
        except Exception as e:
            print(f"[WARN] Failed to execute statement from {path.name}: {e}\n  Statement: {s[:200]}")
    conn.commit()


def main():
    SQL_DIR.mkdir(parents=True, exist_ok=True)
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)

    # Apply only top-level SQL files (skip migrations folder)
    for path in sorted(SQL_DIR.glob("*.sql")):
        print("Applying:", path.name)
        apply_sql_file(conn, path)

    conn.close()
    print("SQLite DB created/updated at:", DB_PATH)


if __name__ == "__main__":
    main()
