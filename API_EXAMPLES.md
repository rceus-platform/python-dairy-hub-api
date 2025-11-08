# API Endpoints Examples

## POST Endpoints

### 1. Create Milk Collection (POST /)

```json
// Request Payload
{
    "farmer_id": 123,
    "quantity": 25.5,
    "fat_content": 4.2,
    "snf_content": 8.8,
    "rate_per_liter": 45.5,
    "collection_date": "2025-11-09T08:30:00",
    "shift": "morning"
}

// Response
{
    "id": 1,
    "farmer_id": 123,
    "quantity": 25.5,
    "fat_content": 4.2,
    "snf_content": 8.8,
    "rate_per_liter": 45.5,
    "total_amount": 1160.25,
    "collection_date": "2025-11-09T08:30:00",
    "shift": "morning",
    "created_at": "2025-11-09T08:30:00"
}
```

## GET Endpoints

### 1. List All Collections (GET /)

```http
# Basic pagination
GET /milk-collection/?skip=0&limit=100

# Custom pagination
GET /milk-collection/?skip=50&limit=20
```

### 2. Filter Collections (GET /filter/)

```http
# Filter by date range only
GET /milk-collection/filter/?start_date=2025-11-01T00:00:00&end_date=2025-11-09T23:59:59

# Filter by farmer only
GET /milk-collection/filter/?farmer_id=123

# Filter by shift only
GET /milk-collection/filter/?shift=morning

# Filter by date range and farmer
GET /milk-collection/filter/?start_date=2025-11-01T00:00:00&end_date=2025-11-09T23:59:59&farmer_id=123

# Filter by date range and shift
GET /milk-collection/filter/?start_date=2025-11-01T00:00:00&end_date=2025-11-09T23:59:59&shift=evening

# Filter by farmer and shift
GET /milk-collection/filter/?farmer_id=123&shift=morning

# All filters combined
GET /milk-collection/filter/?start_date=2025-11-01T00:00:00&end_date=2025-11-09T23:59:59&farmer_id=123&shift=evening
```

### 3. Farmer Collection Summary (GET /farmer-summary/)

```http
# All-time summary
GET /milk-collection/farmer-summary/

# Summary for specific date range
GET /milk-collection/farmer-summary/?start_date=2025-11-01T00:00:00&end_date=2025-11-09T23:59:59
```

### 4. Daily Collection Report (GET /reports/daily/)

```http
# Today's report
GET /milk-collection/reports/daily/

# Specific date report
GET /milk-collection/reports/daily/?date=2025-11-09
```

### 5. Calculate Milk Rate (GET /calculate-rate/)

```http
# Basic rate calculation
GET /milk-collection/calculate-rate/?fat_content=4.2&snf_content=8.8

# Minimum values
GET /milk-collection/calculate-rate/?fat_content=3.5&snf_content=8.5

# Higher values
GET /milk-collection/calculate-rate/?fat_content=5.0&snf_content=9.5
```

### 6. Weekly Report (GET /weekly-report/)

```http
# Basic weekly report
GET /milk-collection/weekly-report/?year=2025&week=45

# Filter by farmer
GET /milk-collection/weekly-report/?year=2025&week=45&farmer_id=123

# Filter by shift
GET /milk-collection/weekly-report/?year=2025&week=45&shift=morning

# Exclude daily breakdown
GET /milk-collection/weekly-report/?year=2025&week=45&include_daily=false

# Filter by farmer and shift
GET /milk-collection/weekly-report/?year=2025&week=45&farmer_id=123&shift=evening

# All filters combined
GET /milk-collection/weekly-report/?year=2025&week=45&farmer_id=123&shift=evening&include_daily=false
```

### 7. Monthly Report (GET /monthly-report/)

```http
# Basic monthly report
GET /milk-collection/monthly-report/?year=2025&month=11

# Filter by farmer
GET /milk-collection/monthly-report/?year=2025&month=11&farmer_id=123

# Filter by shift
GET /milk-collection/monthly-report/?year=2025&month=11&shift=morning

# Exclude daily breakdown
GET /milk-collection/monthly-report/?year=2025&month=11&include_daily=false

# Filter by farmer and shift
GET /milk-collection/monthly-report/?year=2025&month=11&farmer_id=123&shift=evening

# All filters combined
GET /milk-collection/monthly-report/?year=2025&month=11&farmer_id=123&shift=evening&include_daily=false
```

### 8. Date Range Report (GET /date-range-report/)

```http
# Basic date range report
GET /milk-collection/date-range-report/?start_date=2025-11-01&end_date=2025-11-15

# Filter by farmer
GET /milk-collection/date-range-report/?start_date=2025-11-01&end_date=2025-11-15&farmer_id=123

# Filter by shift
GET /milk-collection/date-range-report/?start_date=2025-11-01&end_date=2025-11-15&shift=morning

# Exclude daily breakdown
GET /milk-collection/date-range-report/?start_date=2025-11-01&end_date=2025-11-15&include_daily=false

# Filter by farmer and shift
GET /milk-collection/date-range-report/?start_date=2025-11-01&end_date=2025-11-15&farmer_id=123&shift=evening

# All filters combined
GET /milk-collection/date-range-report/?start_date=2025-11-01&end_date=2025-11-15&farmer_id=123&shift=evening&include_daily=false
```

## Filter Parameters Reference

1. **Date/Time Filters:**

   - `start_date`: ISO format datetime (YYYY-MM-DDThh:mm:ss)
   - `end_date`: ISO format datetime (YYYY-MM-DDThh:mm:ss)
   - `date`: YYYY-MM-DD format

2. **Pagination:**

   - `skip`: Number of records to skip (default: 0)
   - `limit`: Number of records per page (default: 100)

3. **Entity Filters:**

   - `farmer_id`: Integer ID of the farmer
   - `shift`: String, either "morning" or "evening"

4. **Report Options:**
   - `include_daily`: Boolean (true/false) to include day-by-day breakdown
   - `year`: Integer (e.g., 2025)
   - `month`: Integer (1-12)
   - `week`: Integer (1-53)
