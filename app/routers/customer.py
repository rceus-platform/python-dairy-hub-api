from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas import customer as schemas

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.post("/", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    """Create a new customer"""

    # Insert the customer and return the created record
    query = text("""
        INSERT INTO public.customer (name, email, phone, address, customer_type)
        VALUES (:name, :email, :phone, :address, :customer_type)
        RETURNING id, name, email, phone, address, customer_type, created_at, is_active
    """)

    result = db.execute(
        query,
        {
            "name": customer.name,
            "email": customer.email,
            "phone": customer.phone,
            "address": customer.address,
            "customer_type": customer.customer_type,
        },
    )

    db.commit()
    customer_data = result.first()

    if not customer_data:
        raise HTTPException(status_code=400, detail="Failed to create customer")

    return customer_data


@router.get("/", response_model=List[schemas.Customer])
def get_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all customers"""

    query = text("""
        SELECT id, name, email, phone, address, customer_type, created_at, is_active
        FROM public.customer
        ORDER BY id
        LIMIT :limit OFFSET :skip
    """)

    result = db.execute(query, {"skip": skip, "limit": limit})
    customers = result.fetchall()

    return customers
