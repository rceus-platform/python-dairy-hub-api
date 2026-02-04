from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


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

    class Config:
        from_attributes = True
