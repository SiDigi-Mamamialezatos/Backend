def test_create_chat_session(client, make_user):
    user, headers = make_user(email="chat1@example.com")
    resp = client.post("/api/chat-sessions/", json={"user_id": user["id"]}, headers=headers)
    assert resp.status_code == 201
    assert resp.json()["user_id"] == user["id"]


def test_create_chat_session_requires_auth(client, make_user):
    user, _ = make_user(email="chat2@example.com")
    resp = client.post("/api/chat-sessions/", json={"user_id": user["id"]})
    assert resp.status_code == 401


def test_create_chat_session_for_another_user_forbidden(client, make_user):
    user1, headers1 = make_user(email="chat3a@example.com")
    user2, _ = make_user(email="chat3b@example.com")
    resp = client.post(
        "/api/chat-sessions/", json={"user_id": user2["id"]}, headers=headers1
    )
    assert resp.status_code == 403


def test_get_own_chat_session(client, make_user):
    user, headers = make_user(email="chat4@example.com")
    session = client.post(
        "/api/chat-sessions/", json={"user_id": user["id"]}, headers=headers
    ).json()
    resp = client.get(f"/api/chat-sessions/{session['id']}", headers=headers)
    assert resp.status_code == 200


def test_get_other_users_chat_session_forbidden(client, make_user):
    user1, headers1 = make_user(email="chat5a@example.com")
    user2, headers2 = make_user(email="chat5b@example.com")
    session = client.post(
        "/api/chat-sessions/", json={"user_id": user1["id"]}, headers=headers1
    ).json()
    resp = client.get(f"/api/chat-sessions/{session['id']}", headers=headers2)
    assert resp.status_code == 403


def test_delete_chat_session(client, make_user):
    user, headers = make_user(email="chat6@example.com")
    session = client.post(
        "/api/chat-sessions/", json={"user_id": user["id"]}, headers=headers
    ).json()
    resp = client.delete(f"/api/chat-sessions/{session['id']}", headers=headers)
    assert resp.status_code == 204