"""Billing endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas import billing as schemas

router = APIRouter(prefix="/billing", tags=["Billing"])


def ensure_billing_table(db: Session) -> None:
    """Create billing table for SQLite deployments if it does not exist."""
    db.execute(
        text(
            """
            CREATE TABLE IF NOT EXISTS billing (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL REFERENCES customer (id),
                bill_date DATETIME NOT NULL,
                due_date DATETIME NOT NULL,
                total_amount NUMERIC NOT NULL,
                status VARCHAR(30) NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                paid_amount NUMERIC,
                payment_date DATETIME
            )
            """
        )
    )
    db.commit()


@router.post("/", response_model=schemas.Bill)
def create_bill(bill: schemas.BillCreate, db: Session = Depends(get_db)):
    """Create a new bill"""
    ensure_billing_table(db)

    query = text(
        """
        INSERT INTO billing (
            customer_id, bill_date, due_date, total_amount, status
        )
        VALUES (
            :customer_id, :bill_date, :due_date, :total_amount, :status
        )
        RETURNING id, customer_id, bill_date, due_date, total_amount, status,
                  created_at, paid_amount, payment_date
        """
    )

    result = db.execute(
        query,
        {
            "customer_id": bill.customer_id,
            "bill_date": bill.bill_date,
            "due_date": bill.due_date,
            "total_amount": bill.total_amount,
            "status": bill.status,
        },
    )
    # SQLite requires consuming RETURNING rows before commit.
    created = result.first()
    db.commit()
    return created


@router.get("/", response_model=list[schemas.Bill])
def get_bills(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all bills"""
    ensure_billing_table(db)

    query = text(
        """
        SELECT id, customer_id, bill_date, due_date, total_amount, status,
               created_at, paid_amount, payment_date
        FROM billing
        ORDER BY id DESC
        LIMIT :limit OFFSET :skip
        """
    )
    result = db.execute(query, {"skip": skip, "limit": limit})
    return result.fetchall()
