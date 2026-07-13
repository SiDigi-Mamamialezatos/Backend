import pytest


@pytest.fixture()
def material(client):
    module = client.post("/api/modules/", json={"name": "Sosial"}).json()
    return client.post(
        "/api/materials/", json={"module_id": module["id"], "title": "Bullying"}
    ).json()


def test_create_attempt(client, make_user, material):
    user, headers = make_user(email="attempt1@example.com")
    resp = client.post(
        "/api/attempts/",
        json={"user_id": user["id"], "material_id": material["id"]},
        headers=headers,
    )
    assert resp.status_code == 201
    assert resp.json()["is_completed"] is False


def test_create_attempt_requires_auth(client, make_user, material):
    user, _ = make_user(email="attempt2@example.com")
    resp = client.post(
        "/api/attempts/", json={"user_id": user["id"], "material_id": material["id"]}
    )
    assert resp.status_code == 401


def test_create_attempt_for_another_user_forbidden(client, make_user, material):
    user1, headers1 = make_user(email="attempt3a@example.com")
    user2, _ = make_user(email="attempt3b@example.com")
    resp = client.post(
        "/api/attempts/",
        json={"user_id": user2["id"], "material_id": material["id"]},
        headers=headers1,
    )
    assert resp.status_code == 403


def test_create_attempt_material_not_found(client, make_user):
    user, headers = make_user(email="attempt4@example.com")
    resp = client.post(
        "/api/attempts/",
        json={"user_id": user["id"], "material_id": "does-not-exist"},
        headers=headers,
    )
    assert resp.status_code == 404


def test_mark_attempt_completed(client, make_user, material):
    user, headers = make_user(email="attempt5@example.com")
    attempt = client.post(
        "/api/attempts/",
        json={"user_id": user["id"], "material_id": material["id"]},
        headers=headers,
    ).json()
    resp = client.post(f"/api/attempts/{attempt['id']}/complete", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["is_completed"] is True


def test_list_attempts_by_user(client, make_user, material):
    user, headers = make_user(email="attempt6@example.com")
    client.post(
        "/api/attempts/",
        json={"user_id": user["id"], "material_id": material["id"]},
        headers=headers,
    )
    resp = client.get(f"/api/attempts/user/{user['id']}")
    assert resp.status_code == 200
    assert len(resp.json()) == 1