from datetime import date, datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas import milk_collection as schemas

router = APIRouter(prefix="/milk-collection", tags=["Milk Collection"])


def calculate_rate_per_liter(fat_content: float, snf_content: float) -> float:
    """
    Calculate rate per liter based on fat and SNF content
    Base rate: 40 Rs/liter
    Fat bonus: 2 Rs for each 0.1% above 3.5%
    SNF bonus: 1 Rs for each 0.1% above 8.5%
    """
    base_rate = 40.0
    fat_bonus = max(0, (fat_content - 3.5) * 20)  # 2 Rs per 0.1%
    snf_bonus = max(0, (snf_content - 8.5) * 10)  # 1 Rs per 0.1%
    return base_rate + fat_bonus + snf_bonus


@router.post("/", response_model=schemas.MilkCollection)
def create_milk_collection(
    collection: schemas.MilkCollectionCreate, db: Session = Depends(get_db)
):
    """Create a new milk collection record"""

    # Calculate total amount
    total_amount = collection.quantity * collection.rate_per_liter

    # Verify that the farmer exists
    farmer_query = text("SELECT id FROM public.customer WHERE id = :farmer_id")
    farmer = db.execute(farmer_query, {"farmer_id": collection.farmer_id}).first()

    if not farmer:
        raise HTTPException(
            status_code=404, detail=f"Farmer with id {collection.farmer_id} not found"
        )

    # Check if collection already exists for this farmer, date and shift
    existing_collection_query = text("""
        SELECT id FROM public.milk_collection 
        WHERE farmer_id = :farmer_id 
        AND DATE(collection_date) = DATE(:collection_date)
        AND shift = :shift
    """)

    existing = db.execute(
        existing_collection_query,
        {
            "farmer_id": collection.farmer_id,
            "collection_date": collection.collection_date,
            "shift": collection.shift,
        },
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Collection already exists for farmer {collection.farmer_id} on {collection.collection_date.date()} for {collection.shift} shift",
        )

    # Insert the milk collection record
    query = text("""
        INSERT INTO public.milk_collection (
            farmer_id, quantity, fat_content, snf_content,
            rate_per_liter, total_amount, collection_date, shift
        )
        VALUES (
            :farmer_id, :quantity, :fat_content, :snf_content,
            :rate_per_liter, :total_amount, :collection_date, :shift
        )
        RETURNING id, farmer_id, quantity, fat_content, snf_content,
                  rate_per_liter, total_amount, collection_date, shift, created_at
    """)

    try:
        result = db.execute(
            query,
            {
                "farmer_id": collection.farmer_id,
                "quantity": collection.quantity,
                "fat_content": collection.fat_content,
                "snf_content": collection.snf_content,
                "rate_per_liter": collection.rate_per_liter,
                "total_amount": total_amount,
                "collection_date": collection.collection_date,
                "shift": collection.shift,
            },
        )
        db.commit()
        return result.first()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[schemas.MilkCollection])
def get_milk_collections(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Get all milk collection records"""

    query = text("""
        SELECT 
            mc.id, mc.farmer_id, mc.quantity, mc.fat_content,
            mc.snf_content, mc.rate_per_liter, mc.total_amount,
            mc.collection_date, mc.created_at,
            c.name as farmer_name
        FROM public.milk_collection mc
        JOIN public.customer c ON mc.farmer_id = c.id
        ORDER BY mc.collection_date DESC
        LIMIT :limit OFFSET :skip
    """)

    result = db.execute(query, {"skip": skip, "limit": limit})
    return result.fetchall()


@router.get("/filter/", response_model=List[schemas.MilkCollection])
def filter_milk_collections(
    start_date: datetime = Query(None),
    end_date: datetime = Query(None),
    farmer_id: int = Query(None),
    shift: schemas.CollectionShift = Query(None),
    db: Session = Depends(get_db),
):
    """Get milk collections filtered by date range and/or farmer"""
    query_parts = [
        """
        SELECT 
            mc.id, mc.farmer_id, mc.quantity, mc.fat_content,
            mc.snf_content, mc.rate_per_liter, mc.total_amount,
            mc.collection_date, mc.shift, mc.created_at,
            c.name as farmer_name
        FROM public.milk_collection mc
        JOIN public.customer c ON mc.farmer_id = c.id
        WHERE 1=1
        """
    ]
    params = {}

    if start_date:
        query_parts.append("AND mc.collection_date >= :start_date")
        params["start_date"] = start_date

    if end_date:
        query_parts.append("AND mc.collection_date <= :end_date")
        params["end_date"] = end_date

    if farmer_id:
        query_parts.append("AND mc.farmer_id = :farmer_id")
        params["farmer_id"] = farmer_id

    if shift:
        query_parts.append("AND mc.shift = :shift")
        params["shift"] = shift

    query_parts.append("ORDER BY mc.collection_date DESC, mc.shift")
    query = text(" ".join(query_parts))

    result = db.execute(query, params)
    return result.fetchall()


@router.get("/farmer-summary/", response_model=List[schemas.FarmerCollectionSummary])
def get_farmer_collection_summary(
    start_date: datetime = Query(None),
    end_date: datetime = Query(None),
    db: Session = Depends(get_db),
):
    """Get summary of milk collection grouped by farmer with shift-wise breakdown"""
    query = text("""
        WITH shift_summaries AS (
            SELECT 
                mc.farmer_id,
                mc.shift,
                COUNT(*) as total_collections,
                SUM(mc.quantity) as total_quantity,
                AVG(mc.fat_content) as avg_fat,
                AVG(mc.snf_content) as avg_snf,
                SUM(mc.total_amount) as total_amount
            FROM public.milk_collection mc
            WHERE 1=1
            GROUP BY mc.farmer_id, mc.shift
        )
        SELECT 
            c.id as farmer_id,
            c.name as farmer_name,
            COUNT(*) as total_collections,
            SUM(mc.quantity) as total_quantity,
            AVG(mc.fat_content) as avg_fat,
            AVG(mc.snf_content) as avg_snf,
            SUM(mc.total_amount) as total_amount,
            jsonb_build_object(
                'shift', 'morning',
                'total_collections', morning.total_collections,
                'total_quantity', morning.total_quantity,
                'avg_fat', morning.avg_fat,
                'avg_snf', morning.avg_snf,
                'total_amount', morning.total_amount
            ) as morning_collections,
            jsonb_build_object(
                'shift', 'evening',
                'total_collections', evening.total_collections,
                'total_quantity', evening.total_quantity,
                'avg_fat', evening.avg_fat,
                'avg_snf', evening.avg_snf,
                'total_amount', evening.total_amount
            ) as evening_collections
        FROM public.milk_collection mc
        LEFT JOIN shift_summaries morning ON mc.farmer_id = morning.farmer_id AND morning.shift = 'morning'
        LEFT JOIN shift_summaries evening ON mc.farmer_id = evening.farmer_id AND evening.shift = 'evening'
        JOIN public.customer c ON mc.farmer_id = c.id
        WHERE 
            (:start_date IS NULL OR mc.collection_date >= :start_date)
            AND (:end_date IS NULL OR mc.collection_date <= :end_date)
        GROUP BY c.id, c.name
        ORDER BY total_amount DESC
    """)

    result = db.execute(query, {"start_date": start_date, "end_date": end_date})
    return result.fetchall()


@router.get("/reports/daily/", response_model=List[schemas.DailyCollectionReport])
def get_daily_collection_report(
    date: date = Query(None), db: Session = Depends(get_db)
):
    """Get daily collection report"""
    query = text("""
        SELECT 
            DATE(mc.collection_date) as collection_date,
            COUNT(DISTINCT mc.farmer_id) as total_farmers,
            SUM(mc.quantity) as total_quantity,
            AVG(mc.fat_content) as avg_fat,
            AVG(mc.snf_content) as avg_snf,
            SUM(mc.total_amount) as total_amount
        FROM public.milk_collection mc
        WHERE DATE(mc.collection_date) = COALESCE(:date, CURRENT_DATE)
        GROUP BY DATE(mc.collection_date)
    """)

    result = db.execute(query, {"date": date})
    return result.fetchall()


@router.get("/calculate-rate/")
def calculate_milk_rate(
    fat_content: float = Query(..., gt=0, lt=100),
    snf_content: float = Query(..., gt=0, lt=100),
):
    """Calculate rate per liter based on fat and SNF content"""
    rate = calculate_rate_per_liter(fat_content, snf_content)
    return {
        "fat_content": fat_content,
        "snf_content": snf_content,
        "rate_per_liter": rate,
        "calculation_breakdown": {
            "base_rate": 40.0,
            "fat_bonus": max(0, (fat_content - 3.5) * 20),
            "snf_bonus": max(0, (snf_content - 8.5) * 10),
        },
    }


def generate_collection_report(
    db: Session,
    start_date: date,
    end_date: date,
    farmer_id: Optional[int] = None,
    shift: Optional[schemas.CollectionShift] = None,
    include_daily_summaries: bool = True,
) -> dict:
    """Generate a collection report for a date range"""
    # Base conditions for all queries
    where_conditions = ["DATE(collection_date) BETWEEN :start_date AND :end_date"]
    params = {"start_date": start_date, "end_date": end_date}

    if farmer_id:
        where_conditions.append("farmer_id = :farmer_id")
        params["farmer_id"] = farmer_id

    if shift:
        where_conditions.append("shift = :shift")
        params["shift"] = shift

    where_clause = " AND ".join(where_conditions)

    # Get overall summary
    summary_query = text(f"""
        SELECT 
            COUNT(DISTINCT farmer_id) as total_farmers,
            COUNT(*) as total_collections,
            SUM(quantity) as total_quantity,
            AVG(fat_content) as avg_fat,
            AVG(snf_content) as avg_snf,
            SUM(total_amount) as total_amount
        FROM public.milk_collection
        WHERE {where_clause}
    """)

    summary = dict(
        db.execute(
            summary_query, {"start_date": start_date, "end_date": end_date}
        ).first()
    )

    # Get shift-wise summary
    shift_query = text(f"""
        SELECT 
            shift,
            COUNT(DISTINCT farmer_id) as total_farmers,
            SUM(quantity) as total_quantity,
            AVG(fat_content) as avg_fat,
            AVG(snf_content) as avg_snf,
            SUM(total_amount) as total_amount
        FROM public.milk_collection
        WHERE {where_clause}
        GROUP BY shift
    """)

    shift_results = db.execute(
        shift_query, {"start_date": start_date, "end_date": end_date}
    ).fetchall()

    shift_summary = {row.shift: dict(row._mapping) for row in shift_results}

    # Get daily summaries if requested
    daily_summaries = []
    if include_daily_summaries:
        daily_query = text(f"""
            WITH daily_totals AS (
                SELECT 
                    DATE(collection_date) as collection_date,
                    COUNT(DISTINCT farmer_id) as total_farmers,
                    SUM(quantity) as total_quantity,
                    AVG(fat_content) as avg_fat,
                    AVG(snf_content) as avg_snf,
                    SUM(total_amount) as total_amount
                FROM public.milk_collection
                WHERE {where_clause}
            GROUP BY DATE(collection_date)
        ),
        shift_totals AS (
            SELECT 
                DATE(collection_date) as collection_date,
                shift,
                COUNT(DISTINCT farmer_id) as total_farmers,
                SUM(quantity) as total_quantity,
                AVG(fat_content) as avg_fat,
                AVG(snf_content) as avg_snf,
                SUM(total_amount) as total_amount
            FROM public.milk_collection
            WHERE DATE(collection_date) BETWEEN :start_date AND :end_date
            GROUP BY DATE(collection_date), shift
        )
        SELECT 
            dt.collection_date,
            dt.total_farmers,
            dt.total_quantity,
            dt.avg_fat,
            dt.avg_snf,
            dt.total_amount,
            jsonb_build_object(
                'morning', (
                    SELECT jsonb_build_object(
                        'shift', 'morning',
                        'total_farmers', st.total_farmers,
                        'total_quantity', st.total_quantity,
                        'avg_fat', st.avg_fat,
                        'avg_snf', st.avg_snf,
                        'total_amount', st.total_amount
                    )
                    FROM shift_totals st 
                    WHERE st.collection_date = dt.collection_date AND st.shift = 'morning'
                ),
                'evening', (
                    SELECT jsonb_build_object(
                        'shift', 'evening',
                        'total_farmers', st.total_farmers,
                        'total_quantity', st.total_quantity,
                        'avg_fat', st.avg_fat,
                        'avg_snf', st.avg_snf,
                        'total_amount', st.total_amount
                    )
                    FROM shift_totals st 
                    WHERE st.collection_date = dt.collection_date AND st.shift = 'evening'
                )
            ) as shift_summary
        FROM daily_totals dt
        ORDER BY dt.collection_date
    """)

    daily_results = db.execute(
        daily_query, {"start_date": start_date, "end_date": end_date}
    ).fetchall()

    daily_summaries = [dict(row._mapping) for row in daily_results]

    return {
        **summary,
        "start_date": start_date,
        "end_date": end_date,
        "shift_wise_summary": shift_summary,
        "daily_summaries": daily_summaries,
    }


@router.get("/weekly-report/", response_model=schemas.WeeklyReport)
def get_weekly_report(
    year: int = Query(..., description="Year for the report"),
    week: int = Query(..., ge=1, le=53, description="Week number (1-53)"),
    farmer_id: Optional[int] = Query(None, description="Filter by specific farmer"),
    shift: Optional[schemas.CollectionShift] = Query(
        None, description="Filter by shift (morning/evening)"
    ),
    include_daily: bool = Query(True, description="Include day-by-day breakdown"),
    db: Session = Depends(get_db),
):
    """Get milk collection report for a specific week"""
    from app.utils.date_utils import get_week_dates

    start_date, end_date = get_week_dates(year, week)
    report_data = generate_collection_report(
        db,
        start_date,
        end_date,
        farmer_id=farmer_id,
        shift=shift,
        include_daily_summaries=include_daily,
    )

    return {
        **report_data,
        "week_number": week,
        "year": year,
    }


@router.get("/monthly-report/", response_model=schemas.MonthlyReport)
def get_monthly_report(
    year: int = Query(..., description="Year for the report"),
    month: int = Query(..., ge=1, le=12, description="Month number (1-12)"),
    farmer_id: Optional[int] = Query(None, description="Filter by specific farmer"),
    shift: Optional[schemas.CollectionShift] = Query(
        None, description="Filter by shift (morning/evening)"
    ),
    include_daily: bool = Query(True, description="Include day-by-day breakdown"),
    db: Session = Depends(get_db),
):
    """Get milk collection report for a specific month"""
    from app.utils.date_utils import get_month_dates

    start_date, end_date = get_month_dates(year, month)
    report_data = generate_collection_report(
        db,
        start_date,
        end_date,
        farmer_id=farmer_id,
        shift=shift,
        include_daily_summaries=include_daily,
    )

    return {
        **report_data,
        "month": month,
        "year": year,
    }


@router.get("/date-range-report/", response_model=schemas.DateRangeReport)
def get_date_range_report(
    start_date: date = Query(..., description="Start date for the report"),
    end_date: date = Query(..., description="End date for the report"),
    farmer_id: Optional[int] = Query(None, description="Filter by specific farmer"),
    shift: Optional[schemas.CollectionShift] = Query(
        None, description="Filter by shift (morning/evening)"
    ),
    include_daily: bool = Query(True, description="Include day-by-day breakdown"),
    db: Session = Depends(get_db),
):
    """Get milk collection report for a custom date range"""
    return generate_collection_report(
        db,
        start_date,
        end_date,
        farmer_id=farmer_id,
        shift=shift,
        include_daily_summaries=include_daily,
    )
