# Backend Application — Documentation

### NOTE : VIBECODED

## 1. Overview

FastAPI backend for a gamified learning app (modules → materials with
embedded quizzes → user attempts → badges) plus an AI-chat feature
(chat sessions/messages). Built in layers so each concern stays isolated
and testable:

```
Request
  │
  ▼
app/api/*_router.py    FastAPI routes — parse request, call a service, return a schema
  │
  ▼
app/services/*.py      Business logic — validation, ownership checks, HTTPException
  │
  ▼
app/repositories/*.py  Pure data access — SQLAlchemy queries only, no HTTP concerns
  │
  ▼
app/models/*.py         SQLAlchemy ORM tables
```

`app/schemas/*.py` (Pydantic) sit alongside all of this and define the
request/response shape for every endpoint.

## 2. Project structure

```
app/
├── core/
│   ├── config.py          # settings (DATABASE_URL, JWT_SECRET, ...)
│   └── security.py        # hash_password, verify_password,
│                           # create_access_token, decode_access_token
├── db/
│   ├── base.py             # declarative Base
│   ├── session.py          # engine + SessionLocal
│   └── init_db.py          # create_all() on startup
├── models/                 # one file per table
│   ├── user.py  module.py  material.py  attempt.py
│   ├── badge.py  user_badge.py  chat.py (ChatSession + ChatMessage)
│   └── __init__.py         # imports every model so Base.metadata sees all tables
├── schemas/                 # one file per table: *Create, *Update, *Response
├── repositories/            # one file per table: Session-based CRUD
├── services/                 # one file per table: business logic + HTTPException
├── api/                      # one router per table + api_router aggregator
└── deps.py                   # get_db, get_current_user

alembic/
└── env.py                    # wired to settings.DATABASE_URL + Base.metadata

tests/
├── conftest.py                # DB isolation + auth fixtures
└── test_*.py                  # one file per resource

main.py                         # FastAPI app, lifespan, mounts api_router at /api
```

## 3. Data model

| Table          | Notes                                                                 |
|----------------|------------------------------------------------------------------------|
| `users`        | `email` unique; `hashed_password` (Argon2id via `pwdlib`); never returned in responses |
| `modules`      | Top-level categories (e.g. "Bencana Alam", "Cyber Security", "Sosial") |
| `materials`    | Belongs to a module; `questions` is Postgres `JSONB` — array of `{question, choices: [{text, isCorrect, feedback}]}` |
| `attempts`     | A user's attempt at a material; `is_completed` / `completed_at`      |
| `badges`       | Achievement definitions                                               |
| `user_badges`  | Join table, unique on `(user_id, badge_id)` — a user can't earn the same badge twice |
| `chat_sessions`| Belongs to a user                                                      |
| `chat_messages`| Belongs to a chat session; `role` is `"user"` or `"assistant"`        |

> **Note:** `materials.questions` uses Postgres-native `JSONB`. This means
> both your dev/prod database and your test database must be PostgreSQL —
> SQLite cannot compile the `JSONB` type.

## 4. Setup

### 4.1 Install dependencies

```bash
pip install fastapi[standard] sqlalchemy psycopg2-binary alembic \
            pydantic[email] pwdlib[argon2] pyjwt pytest
```

### 4.2 Environment variables (`.env`)

Loaded via `app.core.config.settings` (adjust names to match your actual
`Settings` class):

```env
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/app_db
JWT_SECRET=change-me-to-a-long-random-string
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30
```

### 4.3 Database migrations (Alembic)

```bash
alembic revision --autogenerate -m "create initial tables"
alembic upgrade head
```

`alembic/env.py` imports the `app.models` package so every table is
registered on `Base.metadata` before autogenerate runs — you don't need to
import models manually.

### 4.4 Run the app

```bash
fastapi dev main.py
# or
uvicorn main:app --reload
```

- Swagger UI: `http://localhost:8000/docs`
- Health check: `GET /health`

All resource endpoints are mounted under `/api` (see §6).

## 5. Authentication

- **Register:** `POST /api/users/register` with `{name, email, password, age?}`.
  Password is hashed with Argon2id (`pwdlib`) before storage — never stored
  or returned in plaintext.
- **Login:** `POST /api/users/login` — **form-encoded**, not JSON (it's an
  `OAuth2PasswordRequestForm`). Send `username` (= the user's email) and
  `password`. Returns `{"access_token": "...", "token_type": "bearer"}`.
- **Authenticated requests:** send `Authorization: Bearer <access_token>`.
  `app/deps.py::get_current_user` decodes the JWT (`sub` claim = user id)
  and loads the `User` row; invalid/expired tokens → `401`.

Ownership is enforced in the service layer, not just by requiring a
logged-in user:

- A user can only create/update/delete **their own** attempts, chat
  sessions, chat messages, and account (`403` otherwise).
- Awarding the same badge to the same user twice returns `400` (the DB's
  unique constraint on `user_badges (user_id, badge_id)` is what actually
  prevents it; the service just turns the `IntegrityError` into a clean
  HTTP response).

## 6. API Reference

All paths are prefixed with `/api`.

### Users (`/api/users`)
| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/register` | – | Create an account |
| POST | `/login` | – | Form login, returns JWT |
| GET | `/me` | ✅ | Current user |
| GET | `/{user_id}` | – | Get a user |
| GET | `/` | – | List users |
| PATCH | `/{user_id}` | ✅ (self only) | Update name/email/age/password |
| DELETE | `/{user_id}` | ✅ (self only) | Delete account |

### Modules (`/api/modules`)
| Method | Path | Description |
|---|---|---|
| POST | `/` | Create a module |
| GET | `/{module_id}` | Get a module |
| GET | `/` | List modules |
| PATCH | `/{module_id}` | Update a module |
| DELETE | `/{module_id}` | Delete a module |

### Materials (`/api/materials`)
| Method | Path | Description |
|---|---|---|
| POST | `/` | Create a material (404 if `module_id` doesn't exist) |
| GET | `/{material_id}` | Get a material |
| GET | `/module/{module_id}` | List materials in a module |
| PATCH | `/{material_id}` | Update a material |
| DELETE | `/{material_id}` | Delete a material |

### Attempts (`/api/attempts`) — auth required for writes
| Method | Path | Description |
|---|---|---|
| POST | `/` | Start an attempt (must be your own `user_id`) |
| GET | `/{attempt_id}` | Get an attempt |
| GET | `/user/{user_id}` | List a user's attempts |
| PATCH | `/{attempt_id}` | Update (owner only) |
| POST | `/{attempt_id}/complete` | Mark completed (owner only) |
| DELETE | `/{attempt_id}` | Delete (owner only) |

### Badges (`/api/badges`)
| Method | Path | Description |
|---|---|---|
| POST | `/` | Create a badge |
| GET | `/{badge_id}` | Get a badge |
| GET | `/` | List badges |
| PATCH | `/{badge_id}` | Update a badge |
| DELETE | `/{badge_id}` | Delete a badge |

### User Badges (`/api/user-badges`)
| Method | Path | Description |
|---|---|---|
| POST | `/` | Award a badge (400 if already awarded) |
| GET | `/{user_badge_id}` | Get an award record |
| GET | `/user/{user_id}` | List a user's badges |
| DELETE | `/{user_badge_id}` | Revoke a badge |

### Chat Sessions (`/api/chat-sessions`) — auth required for writes
| Method | Path | Description |
|---|---|---|
| POST | `/` | Create a session (must be your own `user_id`) |
| GET | `/{session_id}` | Get a session (owner only) |
| GET | `/user/{user_id}` | List a user's sessions |
| DELETE | `/{session_id}` | Delete (owner only) |

### Chat Messages (`/api/chat-messages`) — auth required for writes
| Method | Path | Description |
|---|---|---|
| POST | `/` | Post a message (must own the parent session) |
| GET | `/{message_id}` | Get a message |
| GET | `/session/{chat_session_id}` | List a session's messages (owner only) |
| DELETE | `/{message_id}` | Delete a message |

## 7. Testing

### 7.1 Requirements

Tests hit a **real Postgres database** (not SQLite) because
`materials.questions` is `JSONB`. Point a throwaway database at
`TEST_DATABASE_URL` — tables are created and dropped every test session,
so never use your dev/prod database.

```bash
createdb test_db
export TEST_DATABASE_URL="postgresql+psycopg2://user:password@localhost:5432/test_db"
```

### 7.2 How it works

- `tests/conftest.py` creates all tables once per test session, then wraps
  **each individual test** in an outer transaction plus a SAVEPOINT. Any
  `commit()`/`rollback()` your services/repos do (e.g. the `IntegrityError`
  handling in `user_badge_service`) only affects the SAVEPOINT — the outer
  transaction is rolled back after every test, so tests never leak state
  into each other and the database is clean on every run.
- `app.dependency_overrides[get_db]` swaps in the test session so
  `TestClient` requests use the same transaction the test is asserting
  against.
- The `make_user` fixture registers a user via the real `/api/users/register`
  + `/api/users/login` endpoints and returns `(user_json, auth_headers)` —
  so protected-endpoint tests get a real JWT, not a mocked one.

### 7.3 Running the tests

```bash
pip install pytest
export TEST_DATABASE_URL="postgresql+psycopg2://user:password@localhost:5432/test_db"
pytest tests/ -v
```

Run a single file or test:

```bash
pytest tests/test_attempts.py -v
pytest tests/test_users.py::test_login_wrong_password_fails -v
```

### 7.4 Coverage

48 tests across 8 files — happy paths, 404s for missing parents
(module/material/user/badge/chat session), 401 for missing auth, 403 for
cross-user access attempts, and the 400 on duplicate badge awards /
duplicate email registration.

## 8. Known assumptions to double-check against your real project

These were inferred from partial context and should be verified:

- `app.core.config.settings` exposes `DATABASE_URL`, `JWT_SECRET`,
  `JWT_ALGORITHM`, `JWT_EXPIRE_MINUTES`.
- `app.db.session` exposes a `SessionLocal` sessionmaker.
- `app.deps.get_current_user` calls `security.decode_access_token(token)`
  — confirm this matches your actual `security.py`.
- Alembic's `env.py` imports settings from `db.core.config` per an earlier
  message; if your real path is `app.core.config`, adjust the import there.