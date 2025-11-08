from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class MilkRateBase(BaseModel):
    base_rate: float = Field(..., gt=0, description="Base rate per liter")
    fat_rate: float = Field(..., ge=0, description="Rate per 0.1% fat above base fat")
    snf_rate: float = Field(..., ge=0, description="Rate per 0.1% SNF above base SNF")
    base_fat: float = Field(..., gt=0, lt=100, description="Base fat percentage")
    base_snf: float = Field(..., gt=0, lt=100, description="Base SNF percentage")
    effective_from: date
    effective_to: Optional[date] = None
    description: Optional[str] = None


class MilkRateCreate(MilkRateBase):
    pass


class MilkRateUpdate(BaseModel):
    base_rate: Optional[float] = Field(None, gt=0, description="Base rate per liter")
    fat_rate: Optional[float] = Field(
        None, ge=0, description="Rate per 0.1% fat above base fat"
    )
    snf_rate: Optional[float] = Field(
        None, ge=0, description="Rate per 0.1% SNF above base SNF"
    )
    base_fat: Optional[float] = Field(
        None, gt=0, lt=100, description="Base fat percentage"
    )
    base_snf: Optional[float] = Field(
        None, gt=0, lt=100, description="Base SNF percentage"
    )
    effective_to: Optional[date] = None
    description: Optional[str] = None


class MilkRate(MilkRateBase):
    id: int
    created_at: Optional[date] = None
    is_active: bool

    @staticmethod
    def from_db(db_item):
        # Convert datetime to date for created_at
        if hasattr(db_item, "created_at") and db_item.created_at:
            created_at = db_item.created_at.date()
        else:
            created_at = None

        # Create a dict with known fields
        data = {
            "id": db_item.id,
            "base_rate": db_item.base_rate,
            "fat_rate": db_item.fat_rate,
            "snf_rate": db_item.snf_rate,
            "base_fat": db_item.base_fat,
            "base_snf": db_item.base_snf,
            "effective_from": db_item.effective_from,
            "effective_to": db_item.effective_to,
            "description": getattr(db_item, "description", None),
            "created_at": created_at,
            "is_active": getattr(db_item, "is_active", True),
        }

        return MilkRate(**data)

    class Config:
        orm_mode = True
