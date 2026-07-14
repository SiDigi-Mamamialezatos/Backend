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
        json={"email": "login@example.com", "password": "correcthorse1"},
    )
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_login_wrong_password_fails(client, make_user):
    make_user(email="wrongpw@example.com", password="correcthorse1")
    resp = client.post(
        "/api/users/login",
        json={"email": "wrongpw@example.com", "password": "incorrect"},
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

# Append these tests to ./tests/test_users.py

# =====================================================================
# ADDITIONS TO: ./tests/test_users.py
# =====================================================================

import pytest
from unittest.mock import MagicMock, patch
from app.core.config import settings
import app.api.user_router as user_router

def test_login_returns_expected_payload(client, make_user):
    """Ensures standard password login returns both tokens and correct token type schema."""
    make_user(email="login_meta@example.com", password="securepassword123")
    resp = client.post(
        "/api/users/login",
        json={"email": "login_meta@example.com", "password": "securepassword123"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_google_callback_success_new_user(client):
    """Simulates a successful code exchange with Google for a brand new account registration."""
    
    # Mock responses for both AsyncClient calls
    mock_token_resp = MagicMock()
    mock_token_resp.status_code = 200
    mock_token_resp.json.return_value = {"access_token": "mock-google-access-token"}

    mock_user_resp = MagicMock()
    mock_user_resp.status_code = 200
    mock_user_resp.json.return_value = {
        "sub": "google-id-12345",
        "email": "oauth_new@example.com",
        "name": "OAuth New User"
    }

    # Use patch.object on httpx.AsyncClient itself to catch the instantiation inside the route
    with patch("httpx.AsyncClient.post", return_value=mock_token_resp), \
         patch("httpx.AsyncClient.get", return_value=mock_user_resp):

        resp = client.get(
            "/api/users/auth/google/callback", 
            params={"code": "valid-google-code"},
            follow_redirects=False
        )
    
    assert resp.status_code == 307
    target_url = resp.headers["location"]
    assert settings.FRONTEND_URL in target_url
    assert "access_token=" in target_url
    assert "refresh_token=" in target_url


def test_google_callback_failed_exchange(client):
    """Verifies that an invalid or rejected code from Google properly crashes out with a 400."""
    mock_token_resp = MagicMock()
    mock_token_resp.status_code = 400

    with patch("httpx.AsyncClient.post", return_value=mock_token_resp):
        resp = client.get(
            "/api/users/auth/google/callback", 
            params={"code": "bad-or-expired-code"}
        )
        
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Google token exchange failed"

def test_refresh_token_rotation(client, make_user):
    """Verifies that an active refresh token can safely request a brand new access/refresh pair."""
    make_user(email="refreshtest@example.com", password="password123")
    login_resp = client.post(
        "/api/users/login",
        json={"email": "refreshtest@example.com", "password": "password123"},
    )
    raw_refresh_token = login_resp.json()["refresh_token"]

    resp = client.post(
        "/api/users/refresh",
        json={"refresh_token": raw_refresh_token}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["refresh_token"] != raw_refresh_token


def test_logout_revokes_token(client, make_user):
    """Ensures hitting the logout pipeline invalidates the session refresh token row."""
    make_user(email="logouttest@example.com", password="password123")
    login_resp = client.post(
        "/api/users/login",
        json={"email": "logouttest@example.com", "password": "password123"},
    )
    raw_refresh_token = login_resp.json()["refresh_token"]

    logout_resp = client.post(
        "/api/users/logout",
        json={"refresh_token": raw_refresh_token}
    )
    assert logout_resp.status_code == 200

    retry_refresh = client.post(
        "/api/users/refresh",
        json={"refresh_token": raw_refresh_token}
    )
    assert retry_refresh.status_code == 401