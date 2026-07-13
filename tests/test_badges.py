def test_create_badge(client):
    resp = client.post(
        "/api/badges/",
        json={"name": "First Steps", "description": "Complete your first material"},
    )
    assert resp.status_code == 201
    assert resp.json()["name"] == "First Steps"


def test_get_badge_not_found(client):
    assert client.get("/api/badges/does-not-exist").status_code == 404


def test_list_badges(client):
    client.post("/api/badges/", json={"name": "Explorer"})
    resp = client.get("/api/badges/")
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


def test_update_and_delete_badge(client):
    created = client.post("/api/badges/", json={"name": "Temp Badge"}).json()

    resp = client.patch(f"/api/badges/{created['id']}", json={"name": "Renamed Badge"})
    assert resp.status_code == 200
    assert resp.json()["name"] == "Renamed Badge"

    resp = client.delete(f"/api/badges/{created['id']}")
    assert resp.status_code == 204