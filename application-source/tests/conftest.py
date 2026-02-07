import sqlite3
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "app" / "database" / "dairy_hub.db"


def _prepare_database():
    subprocess.run([sys.executable, "scripts/init_sqlite.py"], cwd=ROOT, check=True)
    subprocess.run([sys.executable, "scripts/seed_sqlite.py"], cwd=ROOT, check=True)

    # The schema initializer skips migration files; ensure `shift` exists for API queries.
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute("PRAGMA table_info(milk_collection)")
        columns = {row[1] for row in cur.fetchall()}
        if "shift" not in columns:
            cur.execute(
                "ALTER TABLE milk_collection ADD COLUMN shift VARCHAR(10) NOT NULL DEFAULT 'morning'"
            )
            conn.commit()
    finally:
        conn.close()


@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    _prepare_database()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def unique_email():
    return f"smoke_{int(datetime.now().timestamp())}@example.com"
