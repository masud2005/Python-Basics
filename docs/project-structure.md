# FastAPI + PostgreSQL + SQLAlchemy

A professional, modular, and scalable project structure for
production-ready FastAPI applications.

## Tech Stack

- **FastAPI** --- Web framework
- **PostgreSQL** --- Relational database
- **SQLAlchemy 2.0** --- ORM
- **Alembic** --- Database migrations
- **Pydantic v2** --- Data validation
- **Uvicorn / Gunicorn** --- ASGI server (Gunicorn as process manager in prod)
- **Redis** --- Caching / rate limiting (optional but recommended)
- **Docker & Docker Compose** --- Containerization
- **Pytest** --- Testing
- **Ruff / Black / isort** --- Linting & formatting
- **Poetry or uv** --- Dependency management (alternative to plain pip)

## Project Structure

```text
fastapi-project/
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── app/
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── security.py
│   │   ├── exceptions.py      # global exception handlers
│   │   └── logging.py
│   │
│   ├── common/                 # shared across features
│   │   ├── base_repository.py  # generic CRUD repository
│   │   ├── base_schema.py      # pagination, response wrappers
│   │   └── exceptions.py       # shared/base exception classes
│   │
│   ├── middlewares/
│   │   ├── cors.py
│   │   ├── logging_middleware.py
│   │   └── rate_limiter.py
│   │
│   ├── auth/
│   │   ├── router.py
│   │   ├── service.py
│   │   ├── repository.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── dependencies.py
│   │   ├── constants.py
│   │   ├── exceptions.py       # feature-specific exceptions
│   │   └── utils.py
│   │
│   ├── users/
│   │   ├── router.py
│   │   ├── service.py
│   │   ├── repository.py
│   │   ├── models.py
│   │   └── schemas.py
│   │
│   ├── posts/
│   │   ├── router.py
│   │   ├── service.py
│   │   ├── repository.py
│   │   ├── models.py
│   │   └── schemas.py
│   │
│   └── main.py
│
├── tests/
│   ├── conftest.py             # shared fixtures (test db, client)
│   ├── test_auth/
│   │   ├── test_router.py
│   │   └── test_service.py
│   ├── test_users/
│   └── test_posts/
│
├── .github/
│   └── workflows/
│       └── ci.yml              # lint + test on push/PR
│
├── .env
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
├── pyproject.toml              # or requirements.txt
└── requirements.txt
```

## Architecture Overview

Each feature is self-contained and follows the same internal structure.

| File | Responsibility |
|---|---|
| `router.py` | API endpoints (HTTP layer) |
| `service.py` | Business logic |
| `repository.py` | Database queries (SQLAlchemy) |
| `models.py` | Database models |
| `schemas.py` | Pydantic request/response models |
| `dependencies.py` | Dependency injection & authentication |
| `constants.py` | Enums and fixed values |
| `exceptions.py` | Feature-specific custom exceptions |
| `utils.py` | Helper functions |

## Request Flow

```text
Client
   │
   ▼
Middleware (CORS, logging, rate limit)
   │
   ▼
Router
   │
   ▼
Service
   │
   ▼
Repository
   │
   ▼
PostgreSQL
```

## Core Directory

The `core` folder contains application-wide modules.

| File | Purpose |
|---|---|
| `config.py` | Environment & settings (Pydantic `BaseSettings`) |
| `database.py` | SQLAlchemy engine and session |
| `security.py` | JWT, hashing, authentication |
| `exceptions.py` | Global exception handlers |
| `logging.py` | Logging configuration |

## Common / Shared Directory

The `common` folder holds logic reused across multiple features, so you
don't repeat CRUD boilerplate or pagination logic in every feature module.

| File | Purpose |
|---|---|
| `base_repository.py` | Generic repository class with reusable `get`, `list`, `create`, `update`, `delete` methods |
| `base_schema.py` | Shared response wrappers, pagination schema |
| `exceptions.py` | Base exception classes that feature-level exceptions can inherit from |

## Why Feature-First Architecture?

Instead of separating the project into global `models/`, `schemas/`, and
`services/`, each feature owns its own files.

Example:

```text
auth/
├── router.py
├── service.py
├── repository.py
├── models.py
└── schemas.py
```

This makes the codebase easier to maintain as the project grows.

## Best Practices

- Keep routers thin.
- Put business logic inside services.
- Keep SQL queries inside repositories.
- Never expose SQLAlchemy models directly as API responses — always map to Pydantic schemas.
- Use Alembic for all database schema changes.
- Store secrets in `.env`; commit only `.env.example` with placeholder values.
- Add a `/health` endpoint for uptime checks (required by most deployment platforms like Kubernetes, Railway, Render).
- Use dependency-injected DB sessions, never a global session.
- Version your API from day one (`/api/v1/...`).

## Typical API Versioning

```text
/api/v1/auth
/api/v1/users
/api/v1/posts
/health
```

## Development Workflow

```bash
# Create virtual environment
python -m venv .venv

# Activate
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt
# or, with Poetry:
poetry install
# or, with uv:
uv sync

# Run server
uvicorn app.main:app --reload
```

## Docker Workflow

**Dockerfile** (example, multi-stage):

```dockerfile
FROM python:3.12-slim AS base

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app
COPY alembic.ini .
COPY alembic ./alembic

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**docker-compose.yml** (example):

```yaml
services:
  app:
    build: .
    ports:
      - "8000:8000"
    env_file: .env
    depends_on:
      - db
      - redis

  db:
    image: postgres:16
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: app_db
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:7

volumes:
  pgdata:
```

```bash
docker compose up --build
```

## Database Migration

```bash
# Generate migration
alembic revision --autogenerate -m "create users table"

# Apply migration
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

## Testing

```bash
pytest -v
pytest --cov=app tests/
```

`tests/conftest.py` typically provides:
- A test database fixture (separate DB or transaction rollback per test)
- A `TestClient` / `httpx.AsyncClient` fixture
- Reusable factory fixtures for auth tokens, users, etc.

## Linting & Formatting

```bash
ruff check .
black .
isort .
```

Set these up as a `pre-commit` hook so they run automatically before every commit.

## CI/CD

A minimal `.github/workflows/ci.yml` should:
1. Install dependencies
2. Run `ruff` / `black --check`
3. Run `pytest`
4. (Optional) Build the Docker image

## Design Principles

- Modular Monolith
- Feature-first architecture
- Separation of concerns
- Dependency Injection
- Clean and scalable structure
- Fail fast, log everything, never expose internal errors to clients

---

**Recommended for:** SaaS, FinTech, ERP, E-commerce, and
production-grade FastAPI applications.