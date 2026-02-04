#!/usr/bin/env python3
"""
Seed the SQLite database with sample data from the project README.

This script will attempt to insert sample rows into these tables:
- admin (username, password)
- customer (name, email, phone, address, customer_type, created_at, is_active)
- milk_rate_configuration (base_rate, fat_rate, snf_rate, base_fat, base_snf, effective_from, effective_to, description, created_at)
- milk_collection (farmer_id, quantity, fat_content, snf_content, rate_per_liter, collection_date, shift, total_amount, created_at)

The script is idempotent: it will skip inserting rows that appear to already exist.

Run from repository root:
    python scripts/seed_sqlite.py
"""
from pathlib import Path
import sqlite3
import sys
import subprocess
from datetime import datetime


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "app" / "database" / "dairy_hub.db"
INIT_SCRIPT = ROOT / "scripts" / "init_sqlite.py"


def ensure_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def run_init_if_needed(conn: sqlite3.Connection):
    cur = conn.cursor()
    try:
        # quick check for an expected table
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='customer'")
        if not cur.fetchone():
            raise sqlite3.OperationalError("no customer table")
    except sqlite3.OperationalError:
        print("Tables not found: running init_sqlite.py to create schema...")
        subprocess.check_call([sys.executable, str(INIT_SCRIPT)])


def insert_admins(conn: sqlite3.Connection):
    """Insert multiple admin users from README examples."""
    cur = conn.cursor()
    admins = [
        ("admin", "admin"),
        ("manager", "secure_password"),
    ]
    inserted = 0
    for username, password in admins:
        cur.execute("SELECT 1 FROM admin WHERE username=?", (username,))
        if cur.fetchone():
            continue
        cur.execute("INSERT INTO admin (username, password) VALUES (?, ?)", (username, password))
        inserted += 1
    if inserted > 0:
        conn.commit()
        print(f"Inserted {inserted} admin users")
    else:
        print("All admin users already exist, skipping")


def insert_customers(conn: sqlite3.Connection):
    """Insert multiple customers from README examples."""
    cur = conn.cursor()
    customers = [
        ("John Doe", "john@example.com", "+1234567890", "123 Farm Road", "regular"),
        ("Jane Smith", "jane@example.com", "+9876543210", "456 Dairy Lane", "regular"),
        ("Farm Cooperative", "coop@example.com", "+5555555555", "789 Rural Route", "wholesale"),
        ("Local Dairy", "dairy@example.com", "+4444444444", "321 Milk Street", "wholesale"),
        ("Individual Farmer", "farmer@example.com", "+3333333333", "654 Pastoral Avenue", "regular"),
    ]
    now = datetime.utcnow().isoformat()
    inserted_ids = []
    for name, email, phone, address, ctype in customers:
        cur.execute("SELECT id FROM customer WHERE email=?", (email,))
        if cur.fetchone():
            cur.execute("SELECT id FROM customer WHERE email=?", (email,))
            inserted_ids.append(cur.fetchone()[0])
            continue
        cur.execute(
            "INSERT INTO customer (name, email, phone, address, customer_type, created_at, is_active) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (name, email, phone, address, ctype, now, 1),
        )
        inserted_ids.append(cur.lastrowid)
    if len(inserted_ids) > 0:
        conn.commit()
        print(f"Inserted {len([x for x in inserted_ids if x])} customers")
    return inserted_ids


def insert_milk_rates(conn: sqlite3.Connection):
    """Insert multiple milk rate configurations from README examples."""
    cur = conn.cursor()
    rates = [
        (40.0, 2.0, 1.0, 3.5, 8.5, "2025-11-01", "2025-12-31", "Winter 2025 rates"),
        (42.0, 2.5, 1.2, 3.5, 8.5, "2026-01-01", "2026-02-28", "Updated Winter 2025 rates"),
        (38.0, 1.8, 0.9, 3.5, 8.5, "2025-10-01", "2025-10-31", "October 2025 rates"),
        (45.0, 2.8, 1.3, 3.5, 8.5, "2026-03-01", "2026-04-30", "Spring 2026 rates"),
    ]
    now = datetime.utcnow().isoformat()
    inserted = 0
    for base_rate, fat_rate, snf_rate, base_fat, base_snf, eff_from, eff_to, desc in rates:
        cur.execute(
            "SELECT id FROM milk_rate_configuration WHERE effective_from=? AND base_rate=?",
            (eff_from, base_rate),
        )
        if cur.fetchone():
            continue
        cur.execute(
            "INSERT INTO milk_rate_configuration (base_rate, fat_rate, snf_rate, base_fat, base_snf, effective_from, effective_to, description, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (base_rate, fat_rate, snf_rate, base_fat, base_snf, eff_from, eff_to, desc, now),
        )
        inserted += 1
    if inserted > 0:
        conn.commit()
        print(f"Inserted {inserted} milk rate configurations")
    else:
        print("All milk rates already exist, skipping")


def insert_milk_collections(conn: sqlite3.Connection, customer_ids: list):
    """Insert multiple milk collection records from README examples."""
    cur = conn.cursor()
    if not customer_ids:
        print("No customers available, skipping milk collections")
        return
    
    now = datetime.utcnow().isoformat()
    collections = [
        (customer_ids[0], 25.5, 4.2, 8.8, 45.5, "2025-11-09T08:30:00"),
        (customer_ids[0], 30.0, 4.0, 8.9, 45.5, "2025-11-09T17:00:00"),
        (customer_ids[1], 22.3, 3.9, 8.6, 45.5, "2025-11-09T08:15:00"),
        (customer_ids[1], 28.5, 4.1, 8.7, 45.5, "2025-11-09T17:30:00"),
        (customer_ids[2], 50.0, 4.0, 8.8, 45.5, "2025-11-08T08:00:00"),
        (customer_ids[3], 45.5, 4.3, 9.0, 45.5, "2025-11-08T17:45:00"),
        (customer_ids[4], 20.0, 3.8, 8.5, 45.5, "2025-11-07T08:30:00"),
    ]
    inserted = 0
    for farmer_id, qty, fat, snf, rate, collection_dt in collections:
        cur.execute(
            "SELECT id FROM milk_collection WHERE farmer_id=? AND collection_date=?",
            (farmer_id, collection_dt),
        )
        if cur.fetchone():
            continue
        total = qty * rate
        cur.execute(
            "INSERT INTO milk_collection (farmer_id, quantity, fat_content, snf_content, rate_per_liter, collection_date, total_amount, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (farmer_id, qty, fat, snf, rate, collection_dt, total, now),
        )
        inserted += 1
    if inserted > 0:
        conn.commit()
        print(f"Inserted {inserted} milk collection records")
    else:
        print("All milk collections already exist, skipping")


def main():
    ensure_db()
    conn = sqlite3.connect(DB_PATH)
    try:
        run_init_if_needed(conn)
        insert_admins(conn)
        customer_ids = insert_customers(conn)
        insert_milk_rates(conn)
        insert_milk_collections(conn, customer_ids)
    finally:
        conn.close()

    print("Seeding complete. DB at:", DB_PATH)


if __name__ == "__main__":
    main()
