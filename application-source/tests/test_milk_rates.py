def test_list_milk_rates(client):
    response = client.get("/api/v1/milk-rates/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_current_milk_rate(client):
    response = client.get("/api/v1/milk-rates/current")
    assert response.status_code in (200, 404)


def test_create_overlap_milk_rate_returns_400(client):
    response = client.post(
        "/api/v1/milk-rates/",
        json={
            "base_rate": 40.0,
            "fat_rate": 2.0,
            "snf_rate": 1.0,
            "base_fat": 3.5,
            "base_snf": 8.5,
            "effective_from": "2026-02-01",
            "effective_to": "2026-02-28",
            "description": "Overlap check",
        },
    )
    # Seed data already has overlapping windows for these dates.
    assert response.status_code == 400, response.text


def test_update_milk_rates_in_range(client):
    response = client.put(
        "/api/v1/milk-rates/update-range?start_date=2026-02-01&end_date=2026-02-28",
        json={"description": "Smoke update"},
    )
    assert response.status_code in (200, 404), response.text
