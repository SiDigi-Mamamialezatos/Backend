import pytest


@pytest.fixture()
def chat_session(client, make_user):
    user, headers = make_user(email="chatmsg_owner@example.com")
    session = client.post(
        "/api/chat-sessions/", json={"user_id": user["id"]}, headers=headers
    ).json()
    return session, headers


def test_create_chat_message(client, chat_session):
    session, headers = chat_session
    resp = client.post(
        "/api/chat-messages/",
        json={"chat_session_id": session["id"], "role": "user", "content": "Halo!"},
        headers=headers,
    )
    assert resp.status_code == 201
    assert resp.json()["content"] == "Halo!"


def test_create_chat_message_wrong_owner_forbidden(client, chat_session, make_user):
    session, _ = chat_session
    _, other_headers = make_user(email="chatmsg_intruder@example.com")
    resp = client.post(
        "/api/chat-messages/",
        json={"chat_session_id": session["id"], "role": "user", "content": "Hi"},
        headers=other_headers,
    )
    assert resp.status_code == 403


def test_create_chat_message_session_not_found(client, make_user):
    _, headers = make_user(email="chatmsg_nosession@example.com")
    resp = client.post(
        "/api/chat-messages/",
        json={"chat_session_id": "does-not-exist", "role": "user", "content": "Hi"},
        headers=headers,
    )
    assert resp.status_code == 404


def test_list_chat_messages_by_session(client, chat_session):
    session, headers = chat_session
    client.post(
        "/api/chat-messages/",
        json={"chat_session_id": session["id"], "role": "user", "content": "Q"},
        headers=headers,
    )
    client.post(
        "/api/chat-messages/",
        json={"chat_session_id": session["id"], "role": "assistant", "content": "A"},
        headers=headers,
    )
    resp = client.get(f"/api/chat-messages/session/{session['id']}", headers=headers)
    assert resp.status_code == 200
    assert len(resp.json()) == 2