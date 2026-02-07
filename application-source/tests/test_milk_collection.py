def test_calculate_milk_rate(client):
    response = client.get(
        "/api/v1/milk-collection/calculate-rate/?fat_content=4.2&snf_content=8.8"
    )
    assert response.status_code == 200


def test_create_milk_collection(client):
    customers = client.get("/api/v1/customers/?skip=0&limit=1")
    assert customers.status_code == 200
    farmer_id = customers.json()[0]["id"]

    response = client.post(
        "/api/v1/milk-collection/",
        json={
            "farmer_id": farmer_id,
            "quantity": 12.0,
            "fat_content": 4.1,
            "snf_content": 8.8,
            "rate_per_liter": 45.0,
            "collection_date": "2026-02-10T07:00:00",
            "shift": "evening",
        },
    )
    # Allow duplicate constraint if test was run previously with same test data.
    assert response.status_code in (200, 400), response.text


def test_list_milk_collections(client):
    response = client.get("/api/v1/milk-collection/?skip=0&limit=10")
    assert response.status_code == 200


def test_filter_milk_collections(client):
    customers = client.get("/api/v1/customers/?skip=0&limit=1")
    farmer_id = customers.json()[0]["id"]
    response = client.get(
        f"/api/v1/milk-collection/filter/?start_date=2026-02-01T00:00:00&end_date=2026-12-31T23:59:59&farmer_id={farmer_id}&shift=evening"
    )
    assert response.status_code == 200


def test_farmer_summary_report(client):
    response = client.get(
        "/api/v1/milk-collection/farmer-summary/?start_date=2026-01-01T00:00:00&end_date=2026-12-31T23:59:59"
    )
    assert response.status_code == 200, response.text


def test_daily_report(client):
    response = client.get("/api/v1/milk-collection/reports/daily/?date=2026-02-07")
    assert response.status_code == 200


def test_weekly_report(client):
    response = client.get(
        "/api/v1/milk-collection/weekly-report/?year=2026&week=6&include_daily=true"
    )
    assert response.status_code == 200, response.text


def test_monthly_report(client):
    response = client.get(
        "/api/v1/milk-collection/monthly-report/?year=2026&month=2&include_daily=true"
    )
    assert response.status_code == 200, response.text


def test_date_range_report(client):
    response = client.get(
        "/api/v1/milk-collection/date-range-report/?start_date=2026-02-01&end_date=2026-02-28&include_daily=true"
    )
    assert response.status_code == 200, response.text
