# Forecastle

Forecastle is a demand forecasting console for product teams and supply-chain operators. It combines historical sales, external demand signals, and explainable ML output into a React dashboard backed by a FastAPI service.

The current prototype includes seeded products, synthetic sales history, signal collection hooks, forecast generation, confidence bands, manual forecast overrides, and alert tracking.

## Features

- Product catalogue with latest forecast summaries
- Demand dashboard with 2, 4, and 8 week forecast horizons
- Forecast charts with upper and lower confidence bounds
- Signal contribution breakdowns for social, weather, news, and supplier inputs
- Manual forecast override workflow
- Alert history and threshold configuration APIs
- Seeded local demo data for fast development
- Celery tasks for periodic signal ingestion and scheduled model refreshes

## Tech Stack

**Frontend**

- React 19
- Vite
- React Router
- Zustand
- Recharts
- Framer Motion
- Heroicons

**Backend**

- FastAPI
- SQLAlchemy async ORM
- Alembic
- PostgreSQL
- Redis
- Celery
- Prophet, XGBoost, scikit-learn, pandas, and NumPy

## Repository Structure

```text
Forecastle/
|-- backend/              # FastAPI API, ML services, models, migrations, tasks
|   |-- app/
|   |   |-- api/          # Products, forecasts, signals, alerts, health routes
|   |   |-- db/           # Async database session and seed script
|   |   |-- ingestion/    # External signal collectors
|   |   |-- ml/           # Feature engineering and model pipeline
|   |   |-- models/       # SQLAlchemy models
|   |   |-- schemas/      # Pydantic schemas
|   |   |-- services/     # Forecast, signal, explanation, alert services
|   |   `-- tasks/        # Celery workers and schedules
|   `-- alembic/          # Database migrations
|-- frontend/             # Vite React demand console
|   `-- src/
|       |-- api/          # API clients
|       |-- components/   # Charts, cards, controls, layout
|       |-- pages/        # Dashboard, Products, Signals, Settings
|       `-- stores/       # Zustand stores
|-- scripts/              # Data generation utilities
`-- docker-compose.yml    # Local Postgres, Redis, backend service definitions
```

## Getting Started

### Prerequisites

- Python 3.11
- Node.js 20 or newer
- Docker Desktop, for PostgreSQL and Redis

### 1. Start Infrastructure

From the repository root:

```bash
docker compose up -d db redis
```

This starts PostgreSQL on `localhost:5432` and Redis on `localhost:6379`.

### 2. Configure The Backend

Create `backend/.env`:

```env
DATABASE_URL=postgresql+asyncpg://pulseflow:pulseflow_dev@localhost:5432/pulseflow
REDIS_URL=redis://localhost:6379/0
```

Install dependencies and prepare the database:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
python -m app.db.seed
```

Run the API:

```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

### 3. Run The Frontend

In a second terminal:

```bash
cd frontend
npm install
$env:VITE_API_BASE_URL="http://localhost:8000/api/v1"
npm run dev
```

Open `http://localhost:5173`.

On macOS or Linux, set the frontend API URL with:

```bash
VITE_API_BASE_URL=http://localhost:8000/api/v1 npm run dev
```

## API Overview

All API routes are mounted under `/api/v1`.

| Method | Route | Description |
| --- | --- | --- |
| `GET` | `/health/` | Check database and Redis connectivity |
| `GET` | `/products/` | List products |
| `POST` | `/products/` | Create a product |
| `GET` | `/products/{product_id}` | Get product details and latest forecast summary |
| `POST` | `/forecasts/generate` | Generate a forecast for a product |
| `GET` | `/forecasts/{product_id}` | Fetch the latest forecast for a horizon |
| `GET` | `/forecasts/{product_id}/history` | Fetch forecast history |
| `POST` | `/forecasts/{forecast_id}/override` | Save a manual forecast override |
| `GET` | `/signals/{product_id}` | Fetch recent product signals |
| `POST` | `/signals/collect` | Trigger signal collection |
| `GET` | `/signals/health/status` | Check signal source health |
| `GET` | `/alerts/` | List alert history |
| `POST` | `/alerts/config` | Create an alert threshold |
| `PUT` | `/alerts/{alert_id}/read` | Mark an alert as read |

Interactive API docs are available at `http://localhost:8000/docs` while the backend is running.

## Background Workers

Celery is configured to use Redis as both broker and result backend. The task schedule currently includes:

- Weekly model refresh on Sundays at 02:00 UTC
- Signal ingestion every 6 hours

Run a worker from `backend/`:

```bash
celery -A app.tasks.celery_app.celery_app worker --loglevel=info
```

Run Celery Beat from `backend/`:

```bash
celery -A app.tasks.celery_app.celery_app beat --loglevel=info
```

## Development Commands

### Backend

```bash
cd backend
alembic upgrade head
python -m app.db.seed
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm run dev
npm run build
npm run lint
```

## Data And Models

The demo seed flow loads products, synthetic sales rows, external signal examples, forecasts, and an unread alert. Forecast generation uses the backend ML pipeline to blend historical demand with external signals and return:

- Daily predictions
- Confidence bounds
- Aggregate predicted quantity
- Model confidence
- Signal contribution metadata
- Human-readable explanation text

## Current Status

Forecastle is a working prototype intended for local development and demo workflows. Production hardening areas include authentication, durable model registry workflows, full test coverage, deployment manifests, and real external signal integrations.

## License

No license has been specified yet.
