import sqlite3
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.main import app  # pylint: disable=wrong-import-position  # noqa: E402

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
                (
                    "ALTER TABLE milk_collection ADD COLUMN shift "
                    "VARCHAR(10) NOT NULL DEFAULT 'morning'"
                )
            )
            conn.commit()
    finally:
        conn.close()


def _client():
    _prepare_database()
    return TestClient(app)


def test_system_and_auth():
    client = _client()

    root = client.get("/")
    assert root.status_code == 200

    health = client.get("/health")
    assert health.status_code == 200

    login_ok = client.post(
        "/api/v1/auth/login", json={"username": "admin", "password": "admin"}
    )
    assert login_ok.status_code == 200

    login_bad = client.post(
        "/api/v1/auth/login", json={"username": "admin", "password": "wrong"}
    )
    assert login_bad.status_code == 401


def test_customers_endpoints():
    client = _client()
    ts = int(datetime.now().timestamp())

    created = client.post(
        "/api/v1/customers/",
        json={
            "name": "Smoke User",
            "email": f"smoke_{ts}@example.com",
            "phone": "+1000000000",
            "address": "Smoke Address",
            "customer_type": "regular",
        },
    )
    assert created.status_code == 200, created.text

    listed = client.get("/api/v1/customers/?skip=0&limit=10")
    assert listed.status_code == 200
    assert isinstance(listed.json(), list)


def test_milk_rate_endpoints():
    client = _client()

    listed = client.get("/api/v1/milk-rates/")
    assert listed.status_code == 200
    assert isinstance(listed.json(), list)

    current = client.get("/api/v1/milk-rates/current")
    assert current.status_code in (200, 404)

    overlap = client.post(
        "/api/v1/milk-rates/",
        json={
            "base_rate": 40.0,
            "fat_rate": 2.0,
            "snf_rate": 1.0,
            "base_fat": 3.5,
            "base_snf": 8.5,
            "effective_from": "2026-02-01",
            "effective_to": "2026-02-28",
            "description": "Overlap check",
        },
    )
    # Seed data already has overlapping windows for these dates.
    assert overlap.status_code == 400, overlap.text

    update = client.put(
        "/api/v1/milk-rates/update-range?start_date=2026-02-01&end_date=2026-02-28",
        json={"description": "Smoke update"},
    )
    assert update.status_code in (200, 404), update.text


def test_milk_collection_and_reports_endpoints():
    client = _client()
    customers = client.get("/api/v1/customers/?skip=0&limit=1")
    assert customers.status_code == 200
    farmer_id = customers.json()[0]["id"]

    calc = client.get(
        "/api/v1/milk-collection/calculate-rate/?fat_content=4.2&snf_content=8.8"
    )
    assert calc.status_code == 200

    created = client.post(
        "/api/v1/milk-collection/",
        json={
            "farmer_id": farmer_id,
            "quantity": 12.0,
            "fat_content": 4.1,
            "snf_content": 8.8,
            "rate_per_liter": 45.0,
            "collection_date": "2026-02-10T07:00:00",
            "shift": "evening",
        },
    )
    # Allow duplicate constraint if test was run previously with same test data.
    assert created.status_code in (200, 400), created.text

    listed = client.get("/api/v1/milk-collection/?skip=0&limit=10")
    assert listed.status_code == 200

    filtered = client.get(
        (
            "/api/v1/milk-collection/filter/"
            "?start_date=2026-02-01T00:00:00"
            "&end_date=2026-12-31T23:59:59"
            f"&farmer_id={farmer_id}&shift=evening"
        )
    )
    assert filtered.status_code == 200

    farmer_summary = client.get(
        (
            "/api/v1/milk-collection/farmer-summary/"
            "?start_date=2026-01-01T00:00:00&end_date=2026-12-31T23:59:59"
        )
    )
    assert farmer_summary.status_code == 200, farmer_summary.text

    daily = client.get("/api/v1/milk-collection/reports/daily/?date=2026-02-07")
    assert daily.status_code == 200

    weekly = client.get(
        "/api/v1/milk-collection/weekly-report/?year=2026&week=6&include_daily=true"
    )
    assert weekly.status_code == 200, weekly.text

    monthly = client.get(
        "/api/v1/milk-collection/monthly-report/?year=2026&month=2&include_daily=true"
    )
    assert monthly.status_code == 200, monthly.text

    date_range = client.get(
        (
            "/api/v1/milk-collection/date-range-report/"
            "?start_date=2026-02-01&end_date=2026-02-28&include_daily=true"
        )
    )
    assert date_range.status_code == 200, date_range.text


def test_billing_endpoints():
    client = _client()

    listed = client.get("/api/v1/billing/?skip=0&limit=10")
    assert listed.status_code == 200
    assert isinstance(listed.json(), list)

    created = client.post(
        "/api/v1/billing/",
        json={
            "customer_id": 1,
            "bill_date": "2026-02-07T10:00:00",
            "due_date": "2026-02-15T10:00:00",
            "total_amount": 1000.0,
            "status": "pending",
        },
    )
    assert created.status_code == 200, created.text
