from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas import billing as schemas

router = APIRouter(prefix="/billing", tags=["Billing"])


@router.post("/", response_model=schemas.Bill)
def create_bill(bill: schemas.BillCreate, db: Session = Depends(get_db)):
    """Create a new bill"""
    pass


@router.get("/", response_model=List[schemas.Bill])
def get_bills(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all bills"""
    pass
