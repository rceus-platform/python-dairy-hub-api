# Dairy Hub API Documentation

## Base URL

All endpoints are prefixed with `/milk-collection`

## Endpoints

### 1. Create Milk Collection

**Endpoint:** `POST /`  
**Description:** Create a new milk collection record for a farmer  
**Payload:**

```json
{
  "farmer_id": "integer",
  "quantity": "float (> 0)",
  "fat_content": "float (> 0, < 100)",
  "snf_content": "float (> 0, < 100)",
  "rate_per_liter": "float (> 0)",
  "collection_date": "datetime",
  "shift": "string (morning/evening)"
}
```

**Response:** Returns the created milk collection record with additional fields like `id`, `total_amount`, and `created_at`

### 2. List All Collections

**Endpoint:** `GET /`  
**Description:** Get all milk collection records with pagination  
**Query Parameters:**

- `skip`: integer (default: 0) - Number of records to skip
- `limit`: integer (default: 100) - Maximum number of records to return

### 3. Filter Collections

**Endpoint:** `GET /filter/`  
**Description:** Get milk collections filtered by various parameters  
**Query Parameters:**

- `start_date`: datetime (optional) - Filter collections from this date
- `end_date`: datetime (optional) - Filter collections until this date
- `farmer_id`: integer (optional) - Filter by specific farmer
- `shift`: string (optional) - Filter by shift (morning/evening)

### 4. Farmer Collection Summary

**Endpoint:** `GET /farmer-summary/`  
**Description:** Get summary of milk collections grouped by farmer with shift-wise breakdown  
**Query Parameters:**

- `start_date`: datetime (optional) - Start date for the summary
- `end_date`: datetime (optional) - End date for the summary

### 5. Daily Collection Report

**Endpoint:** `GET /reports/daily/`  
**Description:** Get collection report for a specific date  
**Query Parameters:**

- `date`: date (optional) - Date for the report (defaults to current date)

### 6. Calculate Milk Rate

**Endpoint:** `GET /calculate-rate/`  
**Description:** Calculate rate per liter based on fat and SNF content  
**Query Parameters:**

- `fat_content`: float (> 0, < 100) - Fat percentage in milk
- `snf_content`: float (> 0, < 100) - SNF percentage in milk

### 7. Weekly Report

**Endpoint:** `GET /weekly-report/`  
**Description:** Get detailed milk collection report for a specific week  
**Query Parameters:**

- `year`: integer (required) - Year for the report
- `week`: integer (required, 1-53) - Week number
- `farmer_id`: integer (optional) - Filter by specific farmer
- `shift`: string (optional) - Filter by shift (morning/evening)
- `include_daily`: boolean (default: true) - Include day-by-day breakdown

### 8. Monthly Report

**Endpoint:** `GET /monthly-report/`  
**Description:** Get detailed milk collection report for a specific month  
**Query Parameters:**

- `year`: integer (required) - Year for the report
- `month`: integer (required, 1-12) - Month number
- `farmer_id`: integer (optional) - Filter by specific farmer
- `shift`: string (optional) - Filter by shift (morning/evening)
- `include_daily`: boolean (default: true) - Include day-by-day breakdown

### 9. Date Range Report

**Endpoint:** `GET /date-range-report/`  
**Description:** Get detailed milk collection report for a custom date range  
**Query Parameters:**

- `start_date`: date (required) - Start date for the report
- `end_date`: date (required) - End date for the report
- `farmer_id`: integer (optional) - Filter by specific farmer
- `shift`: string (optional) - Filter by shift (morning/evening)
- `include_daily`: boolean (default: true) - Include day-by-day breakdown

## Report Response Structure

All report endpoints (weekly, monthly, date-range) return data in the following structure:

```json
{
  "start_date": "date",
  "end_date": "date",
  "total_farmers": "integer",
  "total_collections": "integer",
  "total_quantity": "float",
  "avg_fat": "float",
  "avg_snf": "float",
  "total_amount": "float",
  "shift_wise_summary": {
    "morning": {
      "shift": "morning",
      "total_farmers": "integer",
      "total_quantity": "float",
      "avg_fat": "float",
      "avg_snf": "float",
      "total_amount": "float"
    },
    "evening": {
      "shift": "evening",
      "total_farmers": "integer",
      "total_quantity": "float",
      "avg_fat": "float",
      "avg_snf": "float",
      "total_amount": "float"
    }
  },
  "daily_summaries": [
    {
      "collection_date": "date",
      "total_farmers": "integer",
      "total_quantity": "float",
      "avg_fat": "float",
      "avg_snf": "float",
      "total_amount": "float",
      "morning_collection": {
        "shift": "morning",
        "total_farmers": "integer",
        "total_quantity": "float",
        "avg_fat": "float",
        "avg_snf": "float",
        "total_amount": "float"
      },
      "evening_collection": {
        "shift": "evening",
        "total_farmers": "integer",
        "total_quantity": "float",
        "avg_fat": "float",
        "avg_snf": "float",
        "total_amount": "float"
      }
    }
  ]
}
```

## Rate Calculation Logic

The rate per liter is calculated based on:

- Base rate: 40 Rs/liter
- Fat bonus: 2 Rs for each 0.1% above 3.5%
- SNF bonus: 1 Rs for each 0.1% above 8.5%

Example calculation response:

```json
{
  "fat_content": 4.0,
  "snf_content": 9.0,
  "rate_per_liter": 50.0,
  "calculation_breakdown": {
    "base_rate": 40.0,
    "fat_bonus": 10.0, // (4.0 - 3.5) * 20
    "snf_bonus": 5.0 // (9.0 - 8.5) * 10
  }
}
```
