def test_create_customer(client, unique_email):
    response = client.post(
        "/api/v1/customers/",
        json={
            "name": "Smoke User",
            "email": unique_email,
            "phone": "+1000000000",
            "address": "Smoke Address",
            "customer_type": "regular",
        },
    )
    assert response.status_code == 200, response.text


def test_list_customers(client):
    response = client.get("/api/v1/customers/?skip=0&limit=10")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
