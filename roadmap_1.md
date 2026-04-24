# PulseFlow — Step-by-Step Completion Roadmap

> Starting from your current ~18% completion → 100%
> Estimated total: ~30 hours of focused coding

---

## Step 1 — Fix Foundations & Install Missing Deps (~1 hr)

> [!IMPORTANT]
> Do this first. Everything else depends on having the right packages and config.

### 1.1 Backend dependencies
```bash
cd backend
uv add pydantic-settings python-dotenv celery redis
```

### 1.2 Frontend dependencies
```bash
cd frontend
npm install recharts zustand axios react-router-dom @tailwindcss/vite
npm install -D tailwindcss
npm install @heroicons/react clsx framer-motion
```

### 1.3 Create `backend/app/config.py`
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://pulseflow:pulseflow_dev@localhost:5432/pulseflow"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### 1.4 Update [db/session.py](file:///c:/Users/admin/Documents/Forecastle/backend/app/db/session.py) to use `settings.DATABASE_URL` instead of hardcoded URL

### 1.5 Create `.env.example` at project root

### 1.6 Setup Tailwind in [frontend/vite.config.js](file:///c:/Users/admin/Documents/Forecastle/frontend/vite.config.js) and [index.css](file:///c:/Users/admin/Documents/Forecastle/frontend/src/index.css)

**✅ Checkpoint:** `uvicorn app.main:app --reload` starts, `npm run dev` starts, Tailwind classes work.

---

## Step 2 — Complete All Database Models (~2 hrs)

### 2.1 Enhance [models/product.py](file:///c:/Users/admin/Documents/Forecastle/backend/app/models/product.py)
Add missing fields: `category`, `unit`, `created_at`

### 2.2 Enhance [models/sales.py](file:///c:/Users/admin/Documents/Forecastle/backend/app/models/sales.py)
Add missing fields: `revenue`, `channel`, `created_at`, unique constraint

### 2.3 Create `models/forecast.py`
```
Fields: id, product_id, forecast_date, generated_at, horizon_weeks,
        predicted_qty, lower_bound, upper_bound, confidence,
        model_version, explanation, signal_contributions (JSONB),
        is_override, override_qty
```

### 2.4 Create `models/signal.py`
```
Fields: id, product_id, date, source, signal_name, signal_value,
        raw_payload (JSONB), collected_at
```

### 2.5 Create `models/alert.py`
```
Two classes: AlertConfig and AlertHistory
AlertConfig: id, product_id, metric, threshold, direction, is_active
AlertHistory: id, config_id, product_id, triggered_at, metric_value, message, is_read
```

### 2.6 Create `models/model_registry.py` (optional, can defer)

### 2.7 Update [models/__init__.py](file:///c:/Users/admin/Documents/Forecastle/backend/app/models/__init__.py) to import all new models

### 2.8 Generate & run migration
```bash
cd backend
alembic revision --autogenerate -m "add_forecast_signal_alert_tables"
alembic upgrade head
```

**✅ Checkpoint:** All 6+ tables exist in PostgreSQL. `\dt` shows them all.

---

## Step 3 — Complete All Schemas (~1 hr)

### 3.1 Add `schemas/__init__.py`

### 3.2 Enhance [schemas/product.py](file:///c:/Users/admin/Documents/Forecastle/backend/app/schemas/product.py)
Add `ProductCreate` schema (for POST) with `category`, `unit`

### 3.3 Enhance [schemas/forecast.py](file:///c:/Users/admin/Documents/Forecastle/backend/app/schemas/forecast.py)
Add `ForecastResponse` with full fields (predictions array, explanation, signal_contributions, accuracy)

### 3.4 Create `schemas/signal.py`
`SignalResponse` — source, signal_name, signal_value, collected_at

### 3.5 Create `schemas/alert.py`
`AlertConfigCreate`, `AlertResponse`, `AlertHistoryResponse`

**✅ Checkpoint:** All Pydantic schemas import cleanly with no errors.

---

## Step 4 — Complete All API Routes (~2 hrs)

### 4.1 Fix [api/products.py](file:///c:/Users/admin/Documents/Forecastle/backend/app/api/products.py)
- Rename duplicate [get_products](file:///c:/Users/admin/Documents/Forecastle/backend/app/api/products.py#16-20) function
- Add `POST /products` endpoint for creating products

### 4.2 Enhance [api/forecasts.py](file:///c:/Users/admin/Documents/Forecastle/backend/app/api/forecasts.py)
- `GET /{product_id}/history` — forecast version history
- `POST /{id}/override` — manual override endpoint

### 4.3 Create `api/signals.py`
- `GET /signals/{product_id}` — latest signals for product
- `POST /signals/collect` — trigger signal collection
- `GET /signals/health` — signal source health status

### 4.4 Create `api/alerts.py`
- `GET /alerts` — list active/unread alerts
- `POST /alerts/config` — create alert threshold
- `PUT /alerts/{id}/read` — mark alert as read

### 4.5 Create `api/health.py`
- `GET /health` — health check with DB + Redis connectivity

### 4.6 Update [api/router.py](file:///c:/Users/admin/Documents/Forecastle/backend/app/api/router.py) — register all new routers

**✅ Checkpoint:** `http://localhost:8000/docs` shows ALL endpoints with Swagger UI.

---

## Step 5 — Synthetic Data Generator (~1.5 hrs)

### 5.1 Create `scripts/generate_synthetic_data.py`
Generate 2 years of daily sales data with:
- Base trend (slight upward)
- Weekly seasonality
- Monthly seasonality
- Annual seasonality (Q4 peak)
- Random noise + demand shocks

### 5.2 Enhance [db/seed.py](file:///c:/Users/admin/Documents/Forecastle/backend/app/db/seed.py)
- Seed 5–8 products across different categories
- Load generated synthetic sales data into DB
- Seed some mock signal data

```bash
python scripts/generate_synthetic_data.py
python -m app.db.seed
```

**✅ Checkpoint:** [products](file:///c:/Users/admin/Documents/Forecastle/backend/app/api/products.py#16-20) table has 5+ products, `sales_history` has 730+ rows per product.

---

## Step 6 — ML Pipeline (~5 hrs) ⭐ Core Feature

> [!IMPORTANT]
> This is the heart of PulseFlow. Take your time here.

### 6.1 Install ML deps
```bash
cd backend
uv add prophet xgboost scikit-learn pandas numpy joblib
```

### 6.2 Create `app/ml/prophet_model.py`
- Train Prophet on sales history
- Returns `yhat`, `yhat_lower`, `yhat_upper`
- Save/load model with JSON serialization

### 6.3 Create `app/ml/feature_engine.py`
- Engineer features from signals table
- Outputs: sentiment_score, weather_index, lead_time_ratio, news_event_flag

### 6.4 Create `app/ml/xgboost_model.py`
- Train XGBoost on residuals (actual − Prophet prediction)
- Uses signal features as inputs
- Save/load with `joblib`

### 6.5 Create `app/ml/pipeline.py`
- Orchestrator: Prophet → XGBoost → Final Forecast
- [generate_forecast(product_id, horizon_weeks)](file:///c:/Users/admin/Documents/Forecastle/backend/app/api/forecasts.py#17-26) → returns predictions + confidence

### 6.6 Create `app/ml/data_generator.py`
- Synthetic signal data generation for when real APIs aren't available

### 6.7 Create `app/ml/model_registry.py`
- Save trained models to `ml/models/` directory
- Track version, metrics (MAPE, RMSE) in `model_registry` table

### 6.8 Create `scripts/train_models.py`
```bash
python scripts/train_models.py
# → ml/models/prophet_v1.json, xgb_v1.joblib
# → prints MAPE to console
```

### 6.9 Update [services/forecast_service.py](file:///c:/Users/admin/Documents/Forecastle/backend/app/services/forecast_service.py)
- Replace mock random data with actual ML pipeline call
- Keep mock as fallback when models aren't trained yet

**✅ Checkpoint:** `POST /api/v1/forecasts/generate` returns ML-powered forecasts with confidence intervals.

---

## Step 7 — Signal Ingestion Layer (~3 hrs)

### 7.1 Create `app/ingestion/base.py`
Abstract `BaseCollector` with `collect()` and `source_name()` methods

### 7.2 Create 4 collectors (all with `use_mock=True` default):
- `ingestion/news_collector.py` — mock NewsAPI sentiment
- `ingestion/social_collector.py` — mock Twitter/X trends
- `ingestion/weather_collector.py` — mock weather impact
- `ingestion/supplier_collector.py` — mock supplier lead times

### 7.3 Create `services/signal_service.py`
- Orchestrates all collectors
- Stores results in `signals` table

### 7.4 Create `services/explanation_service.py`
- Maps XGBoost feature importances → human-readable text
- Template: *"Forecast revised upward 12% — driven by: (1) +18% social media spike..."*

### 7.5 Create `services/alert_service.py`
- Compares forecast vs thresholds in `alert_configs`
- Creates `alert_history` entries when breached

**✅ Checkpoint:** `GET /api/v1/signals/{product_id}` returns signals from all 4 sources.

---

## Step 8 — Celery Background Tasks (~1.5 hrs)

### 8.1 Create `tasks/celery_app.py`
Configure Celery with Redis broker

### 8.2 Create `tasks/forecast_tasks.py`
- Scheduled reforecasting (weekly via Celery beat)
- Manual retrain on API call

### 8.3 Create `tasks/ingestion_tasks.py`
- Periodic signal collection

**✅ Checkpoint:** `celery -A app.tasks.celery_app worker` runs, tasks execute.

---

## Step 9 — Frontend Dashboard (~8 hrs) ⭐ What People See

### 9.1 Layout Components
- `components/layout/Sidebar.jsx` — navigation (Dashboard, Products, Signals, Settings)
- `components/layout/Header.jsx` — top bar with product picker
- `components/layout/PageShell.jsx` — shared page wrapper

### 9.2 Setup Routing in [App.jsx](file:///c:/Users/admin/Documents/Forecastle/frontend/src/App.jsx)
```jsx
// Routes: /, /products/:id, /signals, /settings
```

### 9.3 API Client Layer
- `api/client.js` — Axios instance with base URL + interceptors
- `api/forecasts.js` — forecast API calls
- `api/products.js` — product API calls
- `api/signals.js` — signal API calls

### 9.4 Zustand Stores
- `stores/useForecastStore.js`
- `stores/useProductStore.js`
- `stores/useAlertStore.js`

### 9.5 Chart Components (Recharts)
- `components/charts/ForecastChart.jsx` — time-series line + confidence band (Area + Line)
- `components/charts/SignalContribution.jsx` — stacked bar of signal impact
- `components/charts/AccuracyGauge.jsx` — radial accuracy meter

### 9.6 Card Components
- `components/cards/ForecastSummaryCard.jsx` — KPI tiles
- `components/cards/ExplanationCard.jsx` — "Why did forecast change?"
- `components/cards/AlertCard.jsx` — breach notifications

### 9.7 Control Components
- `components/controls/HorizonSelector.jsx` — 2W / 4W / 8W toggle
- `components/controls/ProductPicker.jsx` — dropdown
- `components/controls/OverrideSlider.jsx` — manual override + simulation

### 9.8 Shared Components
- `components/shared/LoadingSpinner.jsx`
- `components/shared/EmptyState.jsx`
- `components/shared/Tooltip.jsx`

### 9.9 Custom Hooks
- `hooks/useForecast.js`
- `hooks/useSignalHealth.js`

### 9.10 Utils
- `utils/formatters.js` — number/date formatting
- `utils/constants.js` — API base URL, theme tokens

### 9.11 Build [Dashboard.jsx](file:///c:/Users/admin/Documents/Forecastle/frontend/src/pages/Dashboard.jsx) page
Wire everything together: ForecastChart + ExplanationCard + SummaryCards + HorizonSelector + AlertCards

### 9.12 Build remaining pages
- `pages/ProductDetail.jsx`
- `pages/Signals.jsx`
- `pages/Settings.jsx`

**✅ Checkpoint:** Full dashboard at `http://localhost:5173` with live data from backend.

---

## Step 10 — Polish & Wow Factors (~2 hrs)

- [ ] Dark + Light mode toggle
- [ ] Animated confidence bands (Framer Motion)
- [ ] Typing animation on explanation cards
- [ ] Real-time signal pulse indicator in sidebar
- [ ] Keyboard shortcuts (1/2/3 for horizon, N for next product)
- [ ] Smooth page transitions

**✅ Checkpoint:** Dashboard feels premium and alive.

---

## Step 11 — Testing (~2 hrs)

### 11.1 Backend tests
```bash
cd backend
uv add --dev pytest pytest-asyncio httpx
```
- `tests/conftest.py` — test DB setup
- `tests/test_api_forecasts.py`
- `tests/test_forecast_service.py`
- `tests/test_ml_pipeline.py`
- `tests/test_signal_ingestion.py`

### 11.2 Frontend tests
```bash
cd frontend
npm install -D vitest @testing-library/react @testing-library/jest-dom jsdom
```
- `tests/components/ForecastChart.test.jsx`

### 11.3 Run all tests
```bash
cd backend && uv run pytest tests/ -v
cd frontend && npx vitest run
```

**✅ Checkpoint:** All tests green.

---

## Step 12 — DevOps & Deployment (~2 hrs)

### 12.1 Create `backend/Dockerfile` and `frontend/Dockerfile`

### 12.2 Create `.github/workflows/ci.yml` — lint + test on every PR

### 12.3 Create `.github/workflows/deploy.yml` — deploy on merge to main

### 12.4 Deploy
- Frontend → **Vercel** (free, auto-deploy)
- Backend → **Railway** or **Render** (free tier)
- Database → **Neon** or **Railway Postgres** (free tier)
- Redis → **Upstash** (free tier)

### 12.5 Write killer [README.md](file:///c:/Users/admin/Documents/Forecastle/backend/README.md)
- Architecture diagram
- GIF/screenshot of dashboard
- One-command setup instructions
- Tech stack badges

**✅ Checkpoint:** Live URL shareable. CI green. README sells the project.

---

## Recommended Daily Schedule

| Day | Steps | Focus |
|---|---|---|
| **Day 1** | Steps 1–3 | Fix foundations, complete models & schemas |
| **Day 2** | Steps 4–5 | Complete API routes, seed data |
| **Day 3** | Step 6 (6.1–6.5) | Prophet + XGBoost pipeline |
| **Day 4** | Step 6 (6.6–6.9) + Step 7 | Finish ML, signal ingestion |
| **Day 5** | Step 8 + Step 9 (9.1–9.4) | Celery tasks, frontend scaffolding |
| **Day 6** | Step 9 (9.5–9.12) | Build all dashboard components |
| **Day 7** | Steps 10–12 | Polish, tests, deploy |

> [!TIP]
> **If short on time**, skip Step 8 (Celery) entirely and do Step 6 (ML) + Step 9 (Dashboard) first. The ML pipeline and the visual dashboard are the two things that will impress the most.
