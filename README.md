# python-dairy-hub-api

Central place for all dairy operations.

# Dairy Hub API Documentation

Comprehensive API reference for managing milk collection, rate configuration, customers, billing, and reporting.

---

## 🧭 Table of Contents

1. [Overview](#overview)
2. [Authentication Endpoints](#authentication-endpoints)
3. [Customer Endpoints](#customer-endpoints)
4. [Milk Rate Endpoints](#milk-rate-endpoints)
5. [Milk Collection Endpoints](#milk-collection-endpoints)
6. [Billing Endpoints](#billing-endpoints)
7. [Report and Filter Parameters](#report-and-filter-parameters)
8. [Common Response Structures](#common-response-structures)
9. [HTTP Status Codes](#http-status-codes)

---

## Overview

**Base URL:** `/api/v1`

All endpoints are grouped under the following prefixes:

| Module          | Prefix             |
| --------------- | ------------------ |
| Authentication  | `/auth`            |
| Customers       | `/customers`       |
| Milk Rates      | `/milk-rates`      |
| Milk Collection | `/milk-collection` |
| Billing         | `/billing`         |

---

## Authentication Endpoints

### 1. Login

**Endpoint:** `POST /auth/login`

**Request:**

```json
{
  "username": "admin",
  "password": "secure_password"
}
```

**Response:**

```json
{
  "status": "success",
  "message": "Login successful"
}
```

---

## Customer Endpoints

### 1. Create Customer

**Endpoint:** `POST /customers/`

**Request:**

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "address": "123 Farm Road",
  "customer_type": "farmer"
}
```

**Response:**

```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "address": "123 Farm Road",
  "customer_type": "farmer",
  "created_at": "2025-11-09T10:00:00",
  "is_active": true
}
```

### 2. List Customers

**Endpoint:** `GET /customers/`

Examples:

```http
GET /customers/?skip=0&limit=100
GET /customers/?skip=20&limit=10
```

---

## Milk Rate Endpoints

### 1. Create Milk Rate Configuration

**Endpoint:** `POST /milk-rates/`

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

### 2. List Milk Rates

**Endpoint:** `GET /milk-rates/`

```http
GET /milk-rates/
GET /milk-rates/?date=2025-11-09
GET /milk-rates/?is_active=true
```

### 3. Get Current Rate

**Endpoint:** `GET /milk-rates/current`

```http
GET /milk-rates/current
```

**Response:**

```json
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

### 4. Update Rate by Range

**Endpoint:** `PUT /milk-rates/update-range?start_date=2025-11-01&end_date=2025-12-31`

**Request:**

```json
{
  "base_rate": 42.0,
  "fat_rate": 2.5,
  "snf_rate": 1.2,
  "base_fat": 3.5,
  "base_snf": 8.5,
  "description": "Updated Winter 2025 rates"
}
```

**Response:**

```json
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
```

### 5. Deactivate Rate

**Endpoint:** `PATCH /milk-rates/{rate_id}/deactivate`

```http
PATCH /milk-rates/1/deactivate
```

**Response:**

```json
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
  "is_active": false
}
```

---

## Milk Collection Endpoints

### 1. Create Milk Collection

**Endpoint:** `POST /milk-collection/`

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

### 2. List All Collections

**Endpoint:** `GET /milk-collection/`

```http
GET /milk-collection/?skip=0&limit=100
```

### 3. Filter Collections

**Endpoint:** `GET /milk-collection/filter/`

**Parameters:** `start_date`, `end_date`, `farmer_id`, `shift`

```http
GET /milk-collection/filter/?start_date=2025-11-01&end_date=2025-11-09&shift=morning
```

### 4. Farmer Summary

**Endpoint:** `GET /milk-collection/farmer-summary/`

```http
GET /milk-collection/farmer-summary/?start_date=2025-11-01&end_date=2025-11-09
```

### 5. Reports

#### Daily Report

```http
GET /milk-collection/reports/daily/?date=2025-11-09
```

#### Weekly Report

```http
GET /milk-collection/weekly-report/?year=2025&week=45&include_daily=true
```

#### Monthly Report

```http
GET /milk-collection/monthly-report/?year=2025&month=11&include_daily=true
```

#### Date Range Report

```http
GET /milk-collection/date-range-report/?start_date=2025-11-01&end_date=2025-11-15
```

### 6. Rate Calculation

**Endpoint:** `GET /milk-collection/calculate-rate/`

```http
GET /milk-collection/calculate-rate/?fat_content=4.2&snf_content=8.8
```

**Response Example:**

```json
{
  "fat_content": 4.0,
  "snf_content": 9.0,
  "rate_per_liter": 50.0,
  "calculation_breakdown": {
    "base_rate": 40.0,
    "fat_bonus": 10.0,
    "snf_bonus": 5.0
  }
}
```

---

## Billing Endpoints

### 1. Create Bill

**Endpoint:** `POST /billing/`

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

### 2. List Bills

**Endpoint:** `GET /billing/`

```http
GET /billing/?skip=0&limit=100
```

---

## Report and Filter Parameters

| Parameter       | Type   | Description                |
| --------------- | ------ | -------------------------- |
| `start_date`    | date   | Start date (YYYY-MM-DD)    |
| `end_date`      | date   | End date (YYYY-MM-DD)      |
| `date`          | date   | Specific date              |
| `skip`          | int    | Number of records to skip  |
| `limit`         | int    | Max records per page       |
| `farmer_id`     | int    | Filter by farmer ID        |
| `shift`         | string | morning / evening          |
| `include_daily` | bool   | Include daily breakdown    |
| `year`          | int    | For weekly/monthly reports |
| `month`         | int    | Month number (1-12)        |
| `week`          | int    | Week number (1-53)         |

---

## Common Response Structures

### ✅ Success

```json
{
  "status": "success",
  "data": {}
}
```

### ⚠️ Error

```json
{
  "detail": "Error message"
}
```

### ⚙️ Validation Error

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

---

## HTTP Status Codes

| Code | Meaning               |
| ---- | --------------------- |
| 200  | OK / Success          |
| 201  | Created Successfully  |
| 400  | Bad Request           |
| 401  | Unauthorized          |
| 404  | Not Found             |
| 422  | Validation Error      |
| 500  | Internal Server Error |
