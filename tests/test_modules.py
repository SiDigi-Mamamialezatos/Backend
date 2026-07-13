def test_create_module(client):
    resp = client.post(
        "/api/modules/",
        json={"name": "Bencana Alam", "description": "Natural disasters", "order": 1},
    )
    assert resp.status_code == 201
    assert resp.json()["name"] == "Bencana Alam"


def test_get_module(client):
    created = client.post("/api/modules/", json={"name": "Cyber Security"}).json()
    resp = client.get(f"/api/modules/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Cyber Security"


def test_get_module_not_found(client):
    resp = client.get("/api/modules/does-not-exist")
    assert resp.status_code == 404


def test_list_modules(client):
    client.post("/api/modules/", json={"name": "Sosial"})
    resp = client.get("/api/modules/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    assert len(resp.json()) >= 1


def test_update_module(client):
    created = client.post("/api/modules/", json={"name": "Old Name"}).json()
    resp = client.patch(f"/api/modules/{created['id']}", json={"name": "New Name"})
    assert resp.status_code == 200
    assert resp.json()["name"] == "New Name"


def test_delete_module(client):
    created = client.post("/api/modules/", json={"name": "To Delete"}).json()
    resp = client.delete(f"/api/modules/{created['id']}")
    assert resp.status_code == 204
    assert client.get(f"/api/modules/{created['id']}").status_code == 404