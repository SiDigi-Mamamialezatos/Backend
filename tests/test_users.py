def test_register_user(client):
    resp = client.post(
        "/api/users/register",
        json={"name": "Alice", "email": "alice@example.com", "password": "password123", "age": 25},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == "alice@example.com"
    assert "hashed_password" not in data
    assert "password" not in data


def test_register_duplicate_email_fails(client, make_user):
    make_user(email="dupe@example.com")
    resp = client.post(
        "/api/users/register",
        json={"name": "Bob", "email": "dupe@example.com", "password": "password123"},
    )
    assert resp.status_code == 400


def test_login_success(client, make_user):
    make_user(email="login@example.com", password="correcthorse1")
    resp = client.post(
        "/api/users/login",
        data={"username": "login@example.com", "password": "correcthorse1"},
    )
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_login_wrong_password_fails(client, make_user):
    make_user(email="wrongpw@example.com", password="correcthorse1")
    resp = client.post(
        "/api/users/login",
        data={"username": "wrongpw@example.com", "password": "incorrect"},
    )
    assert resp.status_code == 401


def test_read_current_user(client, make_user):
    user, headers = make_user(email="me@example.com")
    resp = client.get("/api/users/me", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["id"] == user["id"]


def test_read_current_user_requires_auth(client):
    resp = client.get("/api/users/me")
    assert resp.status_code == 401


def test_get_user_by_id(client, make_user):
    user, _ = make_user(email="getbyid@example.com")
    resp = client.get(f"/api/users/{user['id']}")
    assert resp.status_code == 200
    assert resp.json()["email"] == "getbyid@example.com"


def test_get_user_not_found(client):
    resp = client.get("/api/users/does-not-exist")
    assert resp.status_code == 404


def test_update_user(client, make_user):
    user, headers = make_user(email="update@example.com")
    resp = client.patch(
        f"/api/users/{user['id']}", json={"name": "Updated Name"}, headers=headers
    )
    assert resp.status_code == 200
    assert resp.json()["name"] == "Updated Name"


def test_update_other_user_forbidden(client, make_user):
    user1, headers1 = make_user(email="owner1@example.com")
    user2, _ = make_user(email="owner2@example.com")
    resp = client.patch(
        f"/api/users/{user2['id']}", json={"name": "Hacked"}, headers=headers1
    )
    assert resp.status_code == 403


def test_delete_other_user_forbidden(client, make_user):
    user1, headers1 = make_user(email="owner3@example.com")
    user2, _ = make_user(email="owner4@example.com")
    resp = client.delete(f"/api/users/{user2['id']}", headers=headers1)
    assert resp.status_code == 403


def test_delete_user(client, make_user):
    user, headers = make_user(email="delete@example.com")
    resp = client.delete(f"/api/users/{user['id']}", headers=headers)
    assert resp.status_code == 204
    assert client.get(f"/api/users/{user['id']}").status_code == 404