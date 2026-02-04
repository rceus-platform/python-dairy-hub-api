from datetime import date, datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class CollectionShift(str, Enum):
    MORNING = "morning"
    EVENING = "evening"


class MilkCollectionBase(BaseModel):
    farmer_id: int
    quantity: float = Field(..., gt=0)
    fat_content: float = Field(..., gt=0, lt=100)
    snf_content: float = Field(..., gt=0, lt=100)
    rate_per_liter: float = Field(..., gt=0)
    collection_date: datetime
    shift: CollectionShift = Field(..., description="Morning or evening collection")


class MilkCollectionCreate(MilkCollectionBase):
    pass


class MilkCollection(MilkCollectionBase):
    id: int
    total_amount: float
    created_at: datetime
    farmer_name: Optional[str] = None

    class Config:
        from_attributes = True


class ShiftWiseFarmerSummary(BaseModel):
    shift: CollectionShift
    total_collections: int
    total_quantity: float
    avg_fat: float
    avg_snf: float
    total_amount: float

    class Config:
        from_attributes = True


class FarmerCollectionSummary(BaseModel):
    farmer_id: int
    farmer_name: str
    total_collections: int
    total_quantity: float
    avg_fat: float
    avg_snf: float
    total_amount: float
    morning_collections: Optional[ShiftWiseFarmerSummary]
    evening_collections: Optional[ShiftWiseFarmerSummary]

    class Config:
        from_attributes = True


class ShiftCollectionSummary(BaseModel):
    shift: CollectionShift
    total_farmers: int
    total_quantity: float
    avg_fat: float
    avg_snf: float
    total_amount: float

    class Config:
        from_attributes = True


class DailyCollectionReport(BaseModel):
    collection_date: date
    morning_collection: Optional[ShiftCollectionSummary]
    evening_collection: Optional[ShiftCollectionSummary]
    total_farmers: int
    total_quantity: float
    avg_fat: float
    avg_snf: float
    total_amount: float

    class Config:
        from_attributes = True


class DateRangeReport(BaseModel):
    start_date: date
    end_date: date
    total_farmers: int
    total_collections: int
    total_quantity: float
    avg_fat: float
    avg_snf: float
    total_amount: float
    daily_summaries: List[DailyCollectionReport]
    shift_wise_summary: dict[str, ShiftCollectionSummary]

    class Config:
        from_attributes = True


class WeeklyReport(DateRangeReport):
    week_number: int
    year: int


class MonthlyReport(DateRangeReport):
    month: int
    year: int


class RateCalculation(BaseModel):
    fat_content: float = Field(..., gt=0, lt=100)
    snf_content: float = Field(..., gt=0, lt=100)
    rate_per_liter: float
    calculation_breakdown: dict
