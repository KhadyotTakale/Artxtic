# Artxtic

A modern AI-powered image and video generation platform with a **Next.js** frontend and **FastAPI** backend.

## Features

- **OTP & Google OAuth Authentication** — Secure email OTP + Google sign-in with JWT (HTTP-only cookies)
- **AI Playground** — Generate images and videos using Fal.ai models (Flux, Stable Diffusion, etc.)
- **Flexible Aspect Ratios** — Choose from multiple output dimensions
- **Subscription Plans** — Free & Pro tiers with usage limits via Dodopayments
- **Media Library** — Browse, search, and manage your generated media
- **Background Processing** — Celery workers for async generation, email delivery, and cleanup

## Tech Stack

| Layer | Frontend | Backend |
|-------|----------|---------|
| Framework | Next.js 16 (App Router) | FastAPI (Python 3.11+) |
| Language | TypeScript | Python |
| Styling | Tailwind CSS 4 | — |
| Database | — | PostgreSQL 16 (async via asyncpg) |
| ORM / Migrations | — | SQLAlchemy 2.0 + Alembic |
| Cache / Queue | — | Redis 7 + Celery |
| Storage | — | Cloudflare R2 (S3-compatible) |
| AI Generation | — | Fal.ai API |
| Payments | — | Dodopayments SDK |
| Email | — | AWS SES SMTP |
| Auth | JWT cookies | JWT + bcrypt + Google OAuth 2.0 |

## Repository Layout

```
Artxtic/
├── artxctic-frontend/    # Next.js client application
├── artxctic-backend/     # FastAPI server + Celery workers
├── README.md             # ← you are here
└── ref/                  # Design references
```

---

## Prerequisites

| Tool | Version | Notes |
|------|---------|-------|
| **Node.js** | 18+ | For the frontend |
| **npm** | 9+ | Comes with Node.js |
| **Python** | 3.11+ | For the backend |
| **Docker & Docker Compose** | Latest | Required for PostgreSQL & Redis (or install them natively) |
| **Git** | Any | To clone the repo |

---

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/sarthak-g-n/Artxtic.git
cd Artxtic
```

---

### 2. Backend Setup (`artxctic-backend`)

#### Option A — Docker (Recommended)

Spins up **PostgreSQL**, **Redis**, the **API server**, and **Celery** workers in one command:

```bash
cd artxctic-backend

# Copy the example env and fill in your credentials
cp .env.example .env
# ✏️  Edit .env — at minimum set SECRET_KEY, FAL_API_KEY, and SMTP credentials

# Start everything
docker-compose up -d

# Run database migrations
docker-compose exec api alembic upgrade head
```

The API will be available at **http://localhost:8000** and interactive docs at **http://localhost:8000/docs**.

#### Option B — Local Development

```bash
cd artxctic-backend

# 1. Create & activate a virtual environment
python -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# ✏️  Edit .env with your credentials

# 4. Start PostgreSQL & Redis via Docker (if not installed natively)
docker-compose up -d db redis

# 5. Run database migrations
alembic upgrade head

# 6. Start the API server
python run.py                   # → http://localhost:8000
```

#### Start Celery Workers (required for background tasks)

```bash
# In a new terminal (with venv activated)
celery -A app.tasks.celery_app worker --loglevel=info

# In another terminal — scheduler for cron jobs
celery -A app.tasks.celery_app beat --loglevel=info
```

#### Environment Variables Reference

<details>
<summary>Click to expand full <code>.env</code> reference</summary>

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | JWT signing key (≥ 32 chars) | *required* |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://postgres:postgres@localhost:5432/artxtic` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379/0` |
| `FAL_API_KEY` | Fal.ai API key for AI generation | *required* |
| `GOOGLE_CLIENT_ID` | Google OAuth client ID | *optional* |
| `GOOGLE_CLIENT_SECRET` | Google OAuth client secret | *optional* |
| `SMTP_HOST` / `SMTP_USERNAME` / `SMTP_PASSWORD` | AWS SES SMTP for emails | *required for OTP* |
| `R2_ACCESS_KEY_ID` / `R2_SECRET_ACCESS_KEY` | Cloudflare R2 storage keys | *required for media storage* |
| `DODOPAYMENTS_API_KEY` | Dodopayments payment key | *optional* |
| `CORS_ORIGINS` | Allowed origins JSON array | `["http://localhost:3000"]` |

See [`artxctic-backend/.env.example`](artxctic-backend/.env.example) for the complete list.

</details>

---

### 3. Frontend Setup (`artxctic-frontend`)

```bash
cd artxctic-frontend

# 1. Install dependencies
npm install

# 2. Start the development server
npm run dev                     # → http://localhost:3000
```

> **Note:** The frontend expects the backend API at `http://localhost:8000` by default. Update the API base URL in the frontend code if your backend runs on a different host/port.

#### Frontend Build Commands

```bash
npm run build    # Production build
npm start        # Serve the production build
npm run lint     # Run ESLint
```

---

## Running the Full Stack

For the complete development experience, run these in separate terminals:

```bash
# Terminal 1 — Backend infrastructure (PostgreSQL + Redis)
cd artxctic-backend && docker-compose up -d db redis

# Terminal 2 — Backend API
cd artxctic-backend && source venv/bin/activate && python run.py

# Terminal 3 — Celery worker
cd artxctic-backend && source venv/bin/activate && celery -A app.tasks.celery_app worker --loglevel=info

# Terminal 4 — Frontend
cd artxctic-frontend && npm run dev
```

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |
| PostgreSQL | localhost:5433 |
| Redis | localhost:6379 |

---

## Database Migrations

```bash
cd artxctic-backend

# Auto-generate a migration from model changes
alembic revision --autogenerate -m "description of change"

# Apply all pending migrations
alembic upgrade head

# Rollback the last migration
alembic downgrade -1
```

---

## Project Structure

<details>
<summary><strong>Backend</strong> — <code>artxctic-backend/</code></summary>

```
app/
├── core/           # Config, database, security, snowflake IDs
├── models/         # SQLAlchemy models (10 tables, BigInt PKs)
├── schemas/        # Pydantic request/response schemas
├── api/v1/         # API endpoints (26 routes)
├── services/       # Business logic (auth, email, storage, fal.ai, payments, oauth, usage)
├── middleware/      # Error handling, logging, rate limiting
├── tasks/          # Celery background tasks (email, cleanup, generation)
└── utils/          # Exceptions, validators, helpers
```

</details>

<details>
<summary><strong>Frontend</strong> — <code>artxctic-frontend/</code></summary>

```
app/
├── (auth)/         # Sign-in, Sign-up, OAuth callback
├── (dashboard)/    # Playground, Library, Profile, Pricing
└── (landing)/      # Landing page
components/
├── dashboard/      # Dashboard-specific components
├── landing/        # Landing page components
└── ui/             # Reusable UI components (shadcn/ui)
contexts/           # Auth & Playground React contexts
lib/                # API client, utilities
```

</details>

---

## API Endpoints

| Group | Routes | Prefix |
|-------|--------|--------|
| Authentication | 9 | `/api/v1/auth/` |
| Generation | 3 | `/api/v1/generate/` |
| Library | 7 | `/api/v1/library/` |
| User Profile | 3 | `/api/v1/user/` |
| Subscription | 4 | `/api/v1/subscription/` |

Full interactive docs → **http://localhost:8000/docs**

---

## License

MIT

## Author

Sarthak G N
