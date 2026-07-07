"""Milk rate management endpoints."""

from datetime import date
from typing import Optional

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
        SELECT id FROM milk_rate_configuration
        WHERE (effective_from <= :effective_to OR :effective_to IS NULL)
        AND (effective_to >= :effective_from OR effective_to IS NULL)
    """)

    params = {
        "effective_from": rate_config.effective_from,
        "effective_to": rate_config.effective_to,
    }

    overlap = db.execute(overlap_query, params).first()
    if overlap:
        raise HTTPException(
            status_code=400,
            detail=(
                "A rate configuration already exists for this date range. "
                "Each date can only have one rate configuration."
            ),
        )

    # Insert new rate configuration
    query = text("""
        INSERT INTO milk_rate_configuration (
            base_rate, fat_rate, snf_rate, base_fat, base_snf,
            effective_from, effective_to, description
        )
        VALUES (
            :base_rate, :fat_rate, :snf_rate, :base_fat, :base_snf,
            :effective_from, :effective_to, :description
        )
        RETURNING id, base_rate, fat_rate, snf_rate, base_fat, base_snf,
                  effective_from, effective_to, description, created_at
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
        db_item = result.first()
        db.commit()
        return schemas.MilkRate.from_db(db_item)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/", response_model=list[schemas.MilkRate])
def get_milk_rates(
    for_date: Optional[date] = Query(None, alias="date"),
    db: Session = Depends(get_db),
):
    """Get milk rate configurations"""
    query_parts = [
        """
        SELECT id, base_rate, fat_rate, snf_rate, base_fat, base_snf,
               effective_from, effective_to, description, created_at
        FROM milk_rate_configuration
        WHERE 1=1
        """
    ]
    params = {}

    if for_date:
        query_parts.append("""
            AND effective_from <= :date
            AND (effective_to >= :date OR effective_to IS NULL)
        """)
        params["date"] = for_date

    query_parts.append("ORDER BY effective_from DESC")
    query = text(" ".join(query_parts))

    result = db.execute(query, params)
    db_items = result.fetchall()
    return [schemas.MilkRate.from_db(item) for item in db_items]


@router.get("/current", response_model=schemas.MilkRate)
def get_current_rate(db: Session = Depends(get_db)):
    """Get current milk rate configuration for today's date"""
    query = text("""
        SELECT id, base_rate, fat_rate, snf_rate, base_fat, base_snf,
               effective_from, effective_to, description, created_at
        FROM milk_rate_configuration
        WHERE effective_from <= CURRENT_DATE
        AND (effective_to >= CURRENT_DATE OR effective_to IS NULL)
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


@router.delete("/{rate_id}", response_model=schemas.MilkRate)
def delete_rate(rate_id: int, db: Session = Depends(get_db)):
    """Delete a milk rate configuration"""
    query = text("""
        DELETE FROM milk_rate_configuration
        WHERE id = :rate_id
        RETURNING id, base_rate, fat_rate, snf_rate, base_fat, base_snf,
                  effective_from, effective_to, description, created_at
    """)

    result = db.execute(query, {"rate_id": rate_id})
    # SQLite requires consuming RETURNING rows before commit.
    rate = result.first()
    db.commit()
    if not rate:
        raise HTTPException(
            status_code=404, detail=f"Rate configuration with id {rate_id} not found"
        )
    return schemas.MilkRate.from_db(rate)


@router.put("/update-range")
def update_rate_range(
    start_date: date,
    end_date: date,
    rate_update: schemas.MilkRateUpdate,
    db: Session = Depends(get_db),
):
    """Update milk rate configurations within a date range"""

    # Build dynamic update SQL
    update_fields = []
    params = {
        "start_date": start_date,
        "end_date": end_date,
    }

    for field, value in rate_update.model_dump(exclude_unset=True).items():
        update_fields.append(f"{field} = :{field}")
        params[field] = value

    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields provided to update")

    query = text(f"""
        UPDATE milk_rate_configuration
        SET {", ".join(update_fields)}
        WHERE (effective_from BETWEEN :start_date AND :end_date)
           OR (effective_to BETWEEN :start_date AND :end_date)
        RETURNING id, base_rate, fat_rate, snf_rate, base_fat, base_snf,
                  effective_from, effective_to, description, created_at
    """)

    result = db.execute(query, params)
    # SQLite requires consuming RETURNING rows before commit.
    updated = result.fetchall()
    db.commit()

    if not updated:
        raise HTTPException(
            status_code=404, detail="No configurations found in given range"
        )

    return [schemas.MilkRate.from_db(item) for item in updated]
