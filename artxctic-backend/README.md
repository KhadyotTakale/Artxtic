# Artxtic Backend

Production-ready FastAPI backend for the **Artxtic AI Media Generation Platform**.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | FastAPI (Python 3.11+) |
| Database | PostgreSQL 16 (async via asyncpg) |
| ORM | SQLAlchemy 2.0 (async) |
| Migrations | Alembic |
| Auth | JWT (HTTP-only cookies) + bcrypt |
| Cache/Queue | Redis + Celery |
| Storage | Cloudflare R2 (S3-compatible) |
| AI Generation | Fal.ai API |
| Payments | Dodopayments SDK |
| Email | AWS SES SMTP |
| OAuth | Google OAuth 2.0 |

## Quick Start

### 1. Using Docker (Recommended)

```bash
# Start all services
docker-compose up -d

# Run migrations
docker-compose exec api alembic upgrade head

# API is at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### 2. Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Set up .env
cp .env.example .env
# Edit .env with your credentials

# Start PostgreSQL and Redis (local or Docker)
docker-compose up -d db redis

# Run migrations
alembic upgrade head

# Start the server
python run.py
```

### 3. Generate Migrations

```bash
# Auto-generate a migration from model changes
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1
```

### 4. Start Celery Workers

```bash
# Worker
celery -A app.tasks.celery_app worker --loglevel=info

# Beat (scheduler for cron jobs)
celery -A app.tasks.celery_app beat --loglevel=info
```

## API Endpoints

| Group | Count | Prefix |
|-------|-------|--------|
| Authentication | 9 | `/api/v1/auth/` |
| Generation | 3 | `/api/v1/generate/` |
| Library | 7 | `/api/v1/library/` |
| User Profile | 3 | `/api/v1/user/` |
| Subscription | 4 | `/api/v1/subscription/` |
| **Total** | **26** | |

Full API docs at: `http://localhost:8000/docs`

## Project Structure

```
app/
├── core/           # Config, database, security, snowflake IDs
├── models/         # SQLAlchemy models (10 tables, BigInt PKs)
├── schemas/        # Pydantic request/response schemas
├── api/v1/         # API endpoints (26 total)
├── services/       # Business logic (auth, email, storage, fal.ai, payments, oauth, usage)
├── middleware/      # Error handling, logging, rate limiting
├── tasks/          # Celery background tasks (email, cleanup, generation)
└── utils/          # Exceptions, validators, helpers
```

## Database

All tables use **BigInt primary keys** generated via **Snowflake IDs** (64-bit unique identifiers).

10 tables: `users`, `email_verification_tokens`, `password_reset_tokens`, `refresh_tokens`, `subscription_plans`, `subscriptions`, `media`, `usage_limits`, `generation_queue`, `audit_logs`
