"""Billing schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class BillBase(BaseModel):
    customer_id: int
    bill_date: datetime
    due_date: datetime
    total_amount: float
    status: str


class BillCreate(BillBase):
    pass


class Bill(BillBase):
    id: int
    created_at: datetime
    paid_amount: Optional[float] = None
    payment_date: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
