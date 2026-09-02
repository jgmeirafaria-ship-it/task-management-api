def test_create_task(client):
    response = client.post(
        "/tasks",
        json={"title": "Comprar leite", "description": "Ir ao supermercado"},
    )

    assert response.status_code == 201

    data = response.json()
    assert data["title"] == "Comprar leite"
    assert data["description"] == "Ir ao supermercado"
    assert data["completed"] is False
    assert "id" in data