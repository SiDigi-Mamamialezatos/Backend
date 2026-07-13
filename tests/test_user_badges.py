import pytest


@pytest.fixture()
def badge(client):
    return client.post("/api/badges/", json={"name": "Achiever"}).json()


def test_award_badge(client, make_user, badge):
    user, _ = make_user(email="award@example.com")
    resp = client.post(
        "/api/user-badges/", json={"user_id": user["id"], "badge_id": badge["id"]}
    )
    assert resp.status_code == 201
    assert resp.json()["badge_id"] == badge["id"]


def test_award_duplicate_badge_fails(client, make_user, badge):
    user, _ = make_user(email="dupeaward@example.com")
    client.post("/api/user-badges/", json={"user_id": user["id"], "badge_id": badge["id"]})
    resp = client.post(
        "/api/user-badges/", json={"user_id": user["id"], "badge_id": badge["id"]}
    )
    assert resp.status_code == 400


def test_award_badge_user_not_found(client, badge):
    resp = client.post(
        "/api/user-badges/", json={"user_id": "does-not-exist", "badge_id": badge["id"]}
    )
    assert resp.status_code == 404


def test_list_user_badges(client, make_user, badge):
    user, _ = make_user(email="listbadges@example.com")
    client.post("/api/user-badges/", json={"user_id": user["id"], "badge_id": badge["id"]})
    resp = client.get(f"/api/user-badges/user/{user['id']}")
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_revoke_badge(client, make_user, badge):
    user, _ = make_user(email="revoke@example.com")
    awarded = client.post(
        "/api/user-badges/", json={"user_id": user["id"], "badge_id": badge["id"]}
    ).json()
    resp = client.delete(f"/api/user-badges/{awarded['id']}")
    assert resp.status_code == 204