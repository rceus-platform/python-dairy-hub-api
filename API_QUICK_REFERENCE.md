# API Endpoints Quick Reference

## Milk Rate Endpoints

### 1. Create Rate (POST /milk-rates/)

Creates a new milk rate configuration.

```json
{
  "base_rate": 40.0,
  "fat_rate": 2.0,
  "snf_rate": 1.0,
  "base_fat": 3.5,
  "base_snf": 8.5,
  "effective_from": "2025-11-01",
  "effective_to": "2025-12-31",
  "description": "Winter 2025 rates"
}
```

### 2. List Rates (GET /milk-rates/)

- All rates: `GET /milk-rates/`
- Active only: `GET /milk-rates/?active_only=true`
- For specific date: `GET /milk-rates/?date=2025-11-09`

### 3. Get Current Rate (GET /milk-rates/current)

Returns the currently active rate configuration.

### 4. Deactivate Rate (PATCH /milk-rates/{rate_id}/deactivate)

Deactivates a specific rate configuration.

### 5. Update Rate Range (PUT /milk-rates/update-range)

Updates or creates rate for a specific date range.

```http
PUT /milk-rates/update-range?start_date=2025-11-01&end_date=2025-12-31
```

```json
{
  "base_rate": 42.0,
  "fat_rate": 2.5,
  "snf_rate": 1.2,
  "base_fat": 3.5,
  "base_snf": 8.5,
  "description": "Updated rates"
}
```

## Customer Endpoints

### 1. Create Customer (POST /customers/)

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "address": "123 Farm Road",
  "customer_type": "farmer"
}
```

### 2. List Customers (GET /customers/)

- Basic: `GET /customers/`
- Paginated: `GET /customers/?skip=20&limit=10`

## Authentication Endpoint

### 1. Login (POST /auth/login)

```json
{
  "username": "admin",
  "password": "secure_password"
}
```

## Milk Collection Endpoints

### 1. Create Collection (POST /milk-collection/)

```json
{
  "farmer_id": 123,
  "quantity": 25.5,
  "fat_content": 4.2,
  "snf_content": 8.8,
  "rate_per_liter": 45.5,
  "collection_date": "2025-11-09T08:30:00",
  "shift": "morning"
}
```

### 2. List Collections (GET /milk-collection/)

- Basic: `GET /milk-collection/?skip=0&limit=100`
- Filtered: `GET /milk-collection/filter/?start_date=2025-11-01&end_date=2025-11-09&farmer_id=123&shift=morning`

### 3. Farmer Summary (GET /milk-collection/farmer-summary/)

- Basic: `GET /milk-collection/farmer-summary/`
- Date range: `GET /milk-collection/farmer-summary/?start_date=2025-11-01&end_date=2025-11-09`

### 4. Daily Report (GET /milk-collection/reports/daily/)

- Today: `GET /milk-collection/reports/daily/`
- Specific date: `GET /milk-collection/reports/daily/?date=2025-11-09`

### 5. Weekly Report (GET /milk-collection/weekly-report/)

```http
GET /milk-collection/weekly-report/?year=2025&week=45&farmer_id=123&shift=morning&include_daily=true
```

### 6. Monthly Report (GET /milk-collection/monthly-report/)

```http
GET /milk-collection/monthly-report/?year=2025&month=11&farmer_id=123&shift=evening&include_daily=true
```

### 7. Date Range Report (GET /milk-collection/date-range-report/)

```http
GET /milk-collection/date-range-report/?start_date=2025-11-01&end_date=2025-11-15&farmer_id=123&shift=morning
```

### 8. Calculate Rate (GET /milk-collection/calculate-rate/)

```http
GET /milk-collection/calculate-rate/?fat_content=4.2&snf_content=8.8
```

## Billing Endpoints

### 1. Create Bill (POST /billing/)

```json
{
  "farmer_id": 123,
  "billing_period_start": "2025-11-01",
  "billing_period_end": "2025-11-15",
  "items": [
    {
      "collection_id": 1,
      "quantity": 25.5,
      "rate": 45.5,
      "amount": 1160.25
    }
  ]
}
```

### 2. List Bills (GET /billing/)

- Basic: `GET /billing/`
- Paginated: `GET /billing/?skip=20&limit=10`
