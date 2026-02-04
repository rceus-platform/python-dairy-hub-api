from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class CustomerBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: str
    address: str
    customer_type: str  # regular, wholesale, etc.


class CustomerCreate(CustomerBase):
    pass


class Customer(CustomerBase):
    id: int
    created_at: datetime
    is_active: bool = True

    class Config:
        from_attributes = True
