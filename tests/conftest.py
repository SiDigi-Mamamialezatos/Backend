"""
Shared pytest fixtures.

Requires a real PostgreSQL test database (Material.questions uses JSONB,
which SQLite can't compile against). Point TEST_DATABASE_URL at a
throwaway database — never your dev/prod one, since tables are dropped
and recreated every test session.

    export TEST_DATABASE_URL="postgresql+psycopg2://user:password@localhost:5432/test_db"

Each test runs inside a DB transaction that's rolled back afterwards, so
tests never leak state into each other and the DB stays clean between runs.
"""

import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from app.api.deps import get_db
from app.db.base import Base
from main import app

TEST_DATABASE_URL = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql+psycopg://postgres:NebulaScore90MilkyWayEmpathyScalar@localhost:5432/siagaku_dev_test",
)

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@pytest.fixture(scope="session", autouse=True)
def create_test_schema():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session():
    """
    Wraps each test in an outer transaction + a SAVEPOINT. Repos/services
    freely call session.commit() or session.rollback() (e.g. on
    IntegrityError) — those only end the SAVEPOINT, which we immediately
    restart, so the outer transaction (and therefore full test isolation)
    is untouched. Everything is rolled back at the end of the test.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    session.begin_nested()

    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(sess, trans):
        if trans.nested and not trans._parent.nested:
            sess.expire_all()
            sess.begin_nested()

    yield session

    session.close()
    if transaction.is_active:
        transaction.rollback()
    connection.close()


@pytest.fixture()
def client(db_session):
    def _override_get_db():
        try:
            yield db_session
        finally:
            pass  # db_session fixture owns closing/rollback

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture()
def make_user(client):
    """Registers a user and returns (user_json, auth_headers)."""

    def _make_user(email: str = "test@example.com", password: str = "supersecret1", name: str = "Test User"):
        resp = client.post(
            "/api/users/register",
            json={"name": name, "email": email, "password": password, "age": 20},
        )
        assert resp.status_code == 201, resp.text
        user = resp.json()

        login_resp = client.post(
            "/api/users/login",
            json={"email": email, "password": password},
        )
        assert login_resp.status_code == 200, login_resp.text
        token = login_resp.json()["access_token"]

        return user, {"Authorization": f"Bearer {token}"}

    return _make_user