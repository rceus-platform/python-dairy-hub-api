def test_list_bills(client):
    response = client.get("/api/v1/billing/?skip=0&limit=10")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_bill(client):
    response = client.post(
        "/api/v1/billing/",
        json={
            "customer_id": 1,
            "bill_date": "2026-02-07T10:00:00",
            "due_date": "2026-02-15T10:00:00",
            "total_amount": 1000.0,
            "status": "pending",
        },
    )
    assert response.status_code == 200, response.text
