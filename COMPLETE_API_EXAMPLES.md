# Complete API Endpoints Examples

## Authentication Endpoints (Prefix: /auth)

### 1. Login (POST /auth/login)

```json
// Request Payload
{
    "username": "admin",
    "password": "secure_password"
}

// Response
{
    "status": "success",
    "message": "Login successful"
}
```

## Customer Endpoints (Prefix: /customers)

### 1. Create Customer (POST /customers/)

```json
// Request Payload
{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "+1234567890",
    "address": "123 Dairy Farm Road",
    "customer_type": "farmer"
}

// Response
{
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "+1234567890",
    "address": "123 Dairy Farm Road",
    "customer_type": "farmer",
    "created_at": "2025-11-09T10:00:00",
    "is_active": true
}
```

### 2. List Customers (GET /customers/)

```http
# Basic pagination
GET /customers/?skip=0&limit=100

# Custom pagination
GET /customers/?skip=50&limit=20
```

## Milk Rate Endpoints (Prefix: /milk-rates)

### 1. Create Milk Rate Configuration (POST /milk-rates/)

```json
// Request Payload
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

// Response
{
    "id": 1,
    "base_rate": 40.0,
    "fat_rate": 2.0,
    "snf_rate": 1.0,
    "base_fat": 3.5,
    "base_snf": 8.5,
    "effective_from": "2025-11-01",
    "effective_to": "2025-12-31",
    "description": "Winter 2025 rates",
    "created_at": "2025-11-09T10:00:00",
    "is_active": true
}
```

### 2. List Milk Rates (GET /milk-rates/)

```http
# List all rates
GET /milk-rates/

# Filter by date
GET /milk-rates/?date=2025-11-09

# Filter by status
GET /milk-rates/?is_active=true
```

### 3. Get Current Rate (GET /milk-rates/current)

```http
GET /milk-rates/current

// Response
{
    "id": 1,
    "base_rate": 40.0,
    "fat_rate": 2.0,
    "snf_rate": 1.0,
    "base_fat": 3.5,
    "base_snf": 8.5,
    "effective_from": "2025-11-01",
    "effective_to": "2025-12-31",
    "description": "Current active rate",
    "created_at": "2025-11-09T10:00:00",
    "is_active": true
}
```

### 4. Deactivate Rate (PATCH /milk-rates/{rate_id}/deactivate)

```http
PATCH /milk-rates/1/deactivate

// Response
{
    "id": 1,
    "base_rate": 40.0,
    "fat_rate": 2.0,
    "snf_rate": 1.0,
    "base_fat": 3.5,
    "base_snf": 8.5,
    "effective_from": "2025-11-01",
    "effective_to": "2025-12-31",
    "description": "Winter 2025 rates",
    "created_at": "2025-11-09T10:00:00",
    "is_active": false
}
```

### 5. Update Rate Range (PUT /milk-rates/update-range)

````http
PUT /milk-rates/update-range?start_date=2025-11-01&end_date=2025-12-31

// Request Payload
{
    "base_rate": 42.0,
    "fat_rate": 2.5,
    "snf_rate": 1.2,
    "base_fat": 3.5,
    "base_snf": 8.5,
    "description": "Updated Winter 2025 rates"
}

// Response
{
    "id": 2,
    "base_rate": 42.0,
    "fat_rate": 2.5,
    "snf_rate": 1.2,
    "base_fat": 3.5,
    "base_snf": 8.5,
    "effective_from": "2025-11-01",
    "effective_to": "2025-12-31",
    "description": "Updated Winter 2025 rates",
    "created_at": "2025-11-09T10:00:00",
    "is_active": true
}

```http
# All history
GET /milk-rates/history

# Filter by date range
GET /milk-rates/history/?start_date=2025-01-01&end_date=2025-12-31
````

## Billing Endpoints (Prefix: /billing)

### 1. Create Bill (POST /billing/)

```json
// Request Payload
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

// Response
{
    "id": 1,
    "farmer_id": 123,
    "billing_period_start": "2025-11-01",
    "billing_period_end": "2025-11-15",
    "total_amount": 1160.25,
    "items": [
        {
            "id": 1,
            "collection_id": 1,
            "quantity": 25.5,
            "rate": 45.5,
            "amount": 1160.25
        }
    ],
    "created_at": "2025-11-09T10:00:00",
    "status": "pending"
}
```

### 2. List Bills (GET /billing/)

```http
# Basic pagination
GET /billing/?skip=0&limit=100

# Custom pagination
GET /billing/?skip=50&limit=20
```

## Milk Collection Endpoints

See API_EXAMPLES.md for complete examples of milk collection endpoints.

## Filter Parameters Reference

1. **Authentication:**

   - No filters available, just login credentials

2. **Customers:**

   - `skip`: Number of records to skip (default: 0)
   - `limit`: Number of records per page (default: 100)

3. **Milk Rates:**

   - `date`: Date to check rates for (YYYY-MM-DD)
   - `is_active`: Boolean to filter active/inactive rates
   - `start_date`: Start date for history (YYYY-MM-DD)
   - `end_date`: End date for history (YYYY-MM-DD)

4. **Billing:**
   - `skip`: Number of records to skip (default: 0)
   - `limit`: Number of records per page (default: 100)

## Common Response Structures

1. **Success Response:**

```json
{
  "status": "success",
  "data": {
    // Response data here
  }
}
```

2. **Error Response:**

```json
{
  "detail": "Error message describing what went wrong"
}
```

3. **Validation Error:**

```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## HTTP Status Codes

- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 422: Validation Error
- 500: Internal Server Error
