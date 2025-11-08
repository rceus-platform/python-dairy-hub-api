from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas import milk_rate as schemas

router = APIRouter(prefix="/milk-rates", tags=["Milk Rates"])


@router.post("/", response_model=schemas.MilkRate)
def create_milk_rate(
    rate_config: schemas.MilkRateCreate, db: Session = Depends(get_db)
):
    """Create a new milk rate configuration"""

    # Check for overlapping date ranges
    overlap_query = text("""
        SELECT id FROM public.milk_rate_configuration
        WHERE (effective_from <= :effective_to OR :effective_to IS NULL)
        AND (effective_to >= :effective_from OR effective_to IS NULL)
        AND is_active = TRUE
    """)

    params = {
        "effective_from": rate_config.effective_from,
        "effective_to": rate_config.effective_to,
    }

    overlap = db.execute(overlap_query, params).first()
    if overlap:
        raise HTTPException(
            status_code=400, detail="Date range overlaps with existing configuration"
        )

    # Insert new rate configuration
    query = text("""
        INSERT INTO public.milk_rate_configuration (
            base_rate, fat_rate, snf_rate, base_fat, base_snf,
            effective_from, effective_to, description
        )
        VALUES (
            :base_rate, :fat_rate, :snf_rate, :base_fat, :base_snf,
            :effective_from, :effective_to, :description
        )
        RETURNING id, base_rate, fat_rate, snf_rate, base_fat, base_snf,
                  effective_from, effective_to, description, created_at, is_active
    """)

    try:
        result = db.execute(
            query,
            {
                "base_rate": rate_config.base_rate,
                "fat_rate": rate_config.fat_rate,
                "snf_rate": rate_config.snf_rate,
                "base_fat": rate_config.base_fat,
                "base_snf": rate_config.base_snf,
                "effective_from": rate_config.effective_from,
                "effective_to": rate_config.effective_to,
                "description": rate_config.description,
            },
        )
        db.commit()
        db_item = result.first()
        return schemas.MilkRate.from_db(db_item)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[schemas.MilkRate])
def get_milk_rates(
    date: Optional[date] = Query(None),
    active_only: bool = Query(True),
    db: Session = Depends(get_db),
):
    """Get milk rate configurations"""
    query_parts = [
        """
        SELECT id, base_rate, fat_rate, snf_rate, base_fat, base_snf,
               effective_from, effective_to, description, created_at, is_active
        FROM public.milk_rate_configuration
        WHERE 1=1
        """
    ]
    params = {}

    if active_only:
        query_parts.append("AND is_active = TRUE")

    if date:
        query_parts.append("""
            AND effective_from <= :date
            AND (effective_to >= :date OR effective_to IS NULL)
        """)
        params["date"] = date

    query_parts.append("ORDER BY effective_from DESC")
    query = text(" ".join(query_parts))

    result = db.execute(query, params)
    db_items = result.fetchall()
    return [schemas.MilkRate.from_db(item) for item in db_items]


@router.get("/current", response_model=schemas.MilkRate)
def get_current_rate(db: Session = Depends(get_db)):
    """Get currently active milk rate configuration"""
    query = text("""
        SELECT id, base_rate, fat_rate, snf_rate, base_fat, base_snf,
               effective_from, effective_to, description, created_at, is_active
        FROM public.milk_rate_configuration
        WHERE effective_from <= CURRENT_DATE
        AND (effective_to >= CURRENT_DATE OR effective_to IS NULL)
        AND is_active = TRUE
        ORDER BY effective_from DESC
        LIMIT 1
    """)

    result = db.execute(query).first()
    if not result:
        raise HTTPException(
            status_code=404,
            detail="No active rate configuration found for current date",
        )
    return schemas.MilkRate.from_db(result)


@router.patch("/{rate_id}/deactivate", response_model=schemas.MilkRate)
def deactivate_rate(rate_id: int, db: Session = Depends(get_db)):
    """Deactivate a milk rate configuration"""
    query = text("""
        UPDATE public.milk_rate_configuration
        SET is_active = FALSE
        WHERE id = :rate_id
        RETURNING id, base_rate, fat_rate, snf_rate, base_fat, base_snf,
                  effective_from, effective_to, description, created_at, is_active
    """)

    result = db.execute(query, {"rate_id": rate_id})
    db.commit()

    rate = result.first()
    if not rate:
        raise HTTPException(
            status_code=404, detail=f"Rate configuration with id {rate_id} not found"
        )
    return schemas.MilkRate.from_db(rate)


@router.put("/update-range", response_model=schemas.MilkRate)
def update_rate_range(
    start_date: date,
    end_date: date,
    rate_update: schemas.MilkRateUpdate,
    db: Session = Depends(get_db),
):
    """Update or create milk rate for a specific date range"""

    # First, check if there are any existing rates in this date range
    overlap_query = text("""
        SELECT id FROM public.milk_rate_configuration
        WHERE effective_from <= :end_date
        AND (effective_to >= :start_date OR effective_to IS NULL)
        AND is_active = TRUE
    """)

    existing = db.execute(
        overlap_query, {"start_date": start_date, "end_date": end_date}
    ).fetchall()

    if existing:
        # Deactivate overlapping rates
        deactivate_query = text("""
            UPDATE public.milk_rate_configuration
            SET is_active = FALSE
            WHERE id = ANY(:rate_ids)
        """)
        db.execute(deactivate_query, {"rate_ids": [r[0] for r in existing]})

    # Create new rate configuration
    # Build the update fields dynamically based on what was provided
    fields = []
    params = {"effective_from": start_date, "effective_to": end_date}

    for field, value in rate_update.dict(exclude_unset=True).items():
        if value is not None:
            fields.append(field)
            params[field] = value

    # Get the latest rate configuration for any missing fields
    latest_query = text("""
        SELECT base_rate, fat_rate, snf_rate, base_fat, base_snf
        FROM public.milk_rate_configuration
        WHERE is_active = TRUE
        ORDER BY effective_from DESC
        LIMIT 1
    """)
    latest_rate = db.execute(latest_query).first()

    if latest_rate:
        for field in ["base_rate", "fat_rate", "snf_rate", "base_fat", "base_snf"]:
            if field not in params:
                params[field] = getattr(latest_rate, field)
    else:
        # If no previous rate exists, use default values for missing fields
        defaults = {
            "base_rate": 40.0,
            "fat_rate": 2.0,
            "snf_rate": 1.0,
            "base_fat": 3.5,
            "base_snf": 8.5,
        }
        for field, default_value in defaults.items():
            if field not in params:
                params[field] = default_value

    # Insert new rate configuration
    insert_query = text("""
        INSERT INTO public.milk_rate_configuration (
            base_rate, fat_rate, snf_rate, base_fat, base_snf,
            effective_from, effective_to, description
        )
        VALUES (
            :base_rate, :fat_rate, :snf_rate, :base_fat, :base_snf,
            :effective_from, :effective_to, :description
        )
        RETURNING id, base_rate, fat_rate, snf_rate, base_fat, base_snf,
                  effective_from, effective_to, description, created_at, is_active
    """)

    try:
        result = db.execute(insert_query, params)
        db.commit()
        return schemas.MilkRate.from_db(result.first())
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
