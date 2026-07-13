import pytest


@pytest.fixture()
def module(client):
    return client.post("/api/modules/", json={"name": "Bencana Alam"}).json()


def test_create_material(client, module):
    resp = client.post(
        "/api/materials/",
        json={
            "module_id": module["id"],
            "title": "Gempa Bumi",
            "narrative": "Ceritanya di sini...",
            "questions": [
                {
                    "question": "Apa yang harus dilakukan saat gempa?",
                    "choices": [
                        {"text": "Diam saja", "isCorrect": False, "feedback": "Kurang tepat"},
                        {"text": "Berlindung di bawah meja", "isCorrect": True, "feedback": "Benar!"},
                    ],
                }
            ],
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Gempa Bumi"
    assert data["questions"][0]["choices"][1]["isCorrect"] is True


def test_create_material_module_not_found(client):
    resp = client.post(
        "/api/materials/", json={"module_id": "does-not-exist", "title": "Orphan"}
    )
    assert resp.status_code == 404


def test_list_materials_by_module(client, module):
    client.post("/api/materials/", json={"module_id": module["id"], "title": "M1"})
    client.post("/api/materials/", json={"module_id": module["id"], "title": "M2"})
    resp = client.get(f"/api/materials/module/{module['id']}")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_update_material(client, module):
    created = client.post(
        "/api/materials/", json={"module_id": module["id"], "title": "Old Title"}
    ).json()
    resp = client.patch(f"/api/materials/{created['id']}", json={"title": "New Title"})
    assert resp.status_code == 200
    assert resp.json()["title"] == "New Title"


def test_delete_material(client, module):
    created = client.post(
        "/api/materials/", json={"module_id": module["id"], "title": "To Delete"}
    ).json()
    resp = client.delete(f"/api/materials/{created['id']}")
    assert resp.status_code == 204