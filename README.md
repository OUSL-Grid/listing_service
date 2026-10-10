# Listings Service

Campus Marketplace — Listings Service  
**Stack:** FastAPI · SQLAlchemy (async) · Postgres · NATS · Redis

---

## 📋 Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (package manager)
- Docker & Docker Compose

---

## 🚀 Local Setup

### 1. Clone the repo

```bash
git clone https://github.com/OSUL-Grid/listing_service.git
cd listing_service
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Start infrastructure

```bash
docker compose up -d
```

This starts: Postgres (5432), NATS (4222), Redis (6379)

### 4. Configure environment

```bash
cp .env.example .env
# Edit .env as needed
```

### 5. Run migrations

```bash
uv run alembic upgrade head
```

### 6. Start the service

```bash
uv run uvicorn listing_service.main:app --reload --port 8000
```

---

## 📚 API Documentation

Once running, visit:

| URL | Description |
|-----|-------------|
| http://localhost:8000/docs | Swagger UI (interactive) |
| http://localhost:8000/redoc | ReDoc |
| http://localhost:8000/openapi.json | Raw OpenAPI spec |

---

## 🔧 Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `ENV` | Environment (`dev`/`prod`) | `dev` | ❌ |
| `LOG_LEVEL` | Logging level | `INFO` | ❌ |
| `DATABASE_URL` | Postgres async connection string | — | ✅ |
| `DATABASE_URL_SYNC` | Postgres sync URL (for Alembic) | — | ✅ |
| `NATS_URL` | NATS server URL | `nats://localhost:4222` | ✅ |
| `REDIS_URL` | Redis URL | `redis://localhost:6379` | ❌ |
| `JWT_PUBLIC_KEY` | Public key from Auth Service | — | ✅ |
| `JWT_ALGORITHM` | JWT algorithm | `RS256` | ❌ |
| `JWT_ISSUER` | Expected JWT issuer | `campus-auth` | ❌ |

---

## 🗄️ Database Migrations

We use **Alembic** for schema migrations.

```bash
# Create a new migration (auto-detect model changes)
uv run alembic revision --autogenerate -m "add xyz"

# Apply all pending migrations
uv run alembic upgrade head

# Rollback one migration
uv run alembic downgrade -1

# View current revision
uv run alembic current
```

Migration files: `alembic/versions/`

---

## 🧪 Testing

```bash
uv run pytest -v --cov=listing_service
```

---

## 📡 Events

This service publishes and consumes NATS events.  
See [EVENTS.md](./EVENTS.md) for the full contract.

**Published:** `listing.created`, `listing.updated`, `listing.sold`, `listing.flagged`  
**Consumed:** `moderation.listing.hidden`, `moderation.listing.approved`, `user.deleted`

---

## 🏗️ Project Structure

```
listing_service/
├── src/listing_service/
│   ├── main.py            # FastAPI app
│   ├── config.py          # Settings (pydantic-settings)
│   ├── db.py              # DB engine/session
│   ├── models/            # SQLAlchemy models
│   ├── schemas/           # Pydantic schemas
│   ├── routers/           # API routes
│   ├── services/          # Business logic
│   ├── events/            # NATS publisher
│   └── auth/              # JWT middleware
├── alembic/               # Migrations
├── tests/                 # Pytest tests
├── docker-compose.yml     # Postgres + NATS + Redis
├── EVENTS.md              # Event contract
└── README.md
```

---

## 🤝 Contributing

1. Create a branch: `git checkout -b feat/your-feature`
2. Commit: `git commit -m "feat: add listing search"`
3. Push & open a PR

---

## 📄 License

MIT — see [LICENSE](./LICENSE)