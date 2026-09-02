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


def test_create_task_without_title_fails(client):
    """Sem title (obrigatório), a API deve rejeitar o pedido antes de chegar à BD."""
    response = client.post("/tasks", json={"description": "Falta o título"})

    assert response.status_code == 422  # erro de validação do Pydantic


def test_list_tasks(client):
    client.post("/tasks", json={"title": "Tarefa 1"})
    client.post("/tasks", json={"title": "Tarefa 2"})

    response = client.get("/tasks")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_get_task_by_id(client):
    create_response = client.post("/tasks", json={"title": "Ler um livro"})
    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["title"] == "Ler um livro"


def test_get_task_not_found(client):
    response = client.get("/tasks/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_update_task(client):
    create_response = client.post("/tasks", json={"title": "Tarefa antiga"})
    task_id = create_response.json()["id"]

    response = client.put(f"/tasks/{task_id}", json={"completed": True})

    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is True
    assert data["title"] == "Tarefa antiga"  # não foi alterado


def test_update_task_not_found(client):
    response = client.put("/tasks/999", json={"completed": True})

    assert response.status_code == 404


def test_delete_task(client):
    create_response = client.post("/tasks", json={"title": "Tarefa a apagar"})
    task_id = create_response.json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


def test_delete_task_not_found(client):
    response = client.delete("/tasks/999")

    assert response.status_code == 404