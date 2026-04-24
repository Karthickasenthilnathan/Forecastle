# PulseFlow — Codebase Audit Report

> Full audit of the Forecastle (PulseFlow) codebase as of April 5, 2026.

---

## 1. What's Actually Implemented ✅

### Backend — FastAPI + PostgreSQL

| Component | Status | Details |
|---|---|---|
| **Project scaffolding** | ✅ Done | `pyproject.toml`, `uv` setup, Python 3.13, all major dependencies installed |
| **Config** | ✅ Done | `pydantic-settings` based config in [config.py](file:///c:/Users/admin/Documents/Forecastle/backend/app/config.py) |
| **DB session** | ✅ Done | Async engine + session factory in [session.py](file:///c:/Users/admin/Documents/Forecastle/backend/app/db/session.py) |
| **ORM models** | ✅ Done | All 6 models: `Product`, `Sales`, `Signal`, `Forecast`, `AlertConfig`, `AlertHistory` |
| **Pydantic schemas** | ⚠️ Partial | Schemas exist for product, forecast, signal, alert — but `ProductCreate` is empty (inherits `BaseModel` with no fields) |
| **Products API** | ✅ Done | `GET /products` + `POST /products` — real DB queries with async SQLAlchemy |
| **Forecasts API** | ⚠️ Partial | `POST /generate` calls real ML pipeline; `GET /history` and `POST /override` are **stubs** returning hardcoded JSON |
| **Signals API** | ❌ Stub | All 3 endpoints return hardcoded responses, no DB interaction |
| **Alerts API** | ❌ Stub | All 3 endpoints return hardcoded responses, no DB interaction |
| **Health API** | ❌ Stub | Returns fake `"connected"` — no actual DB/Redis connectivity check |
| **ML Pipeline** | ⚠️ Partial | Prophet + XGBoost two-layer approach in [pipeline.py](file:///c:/Users/admin/Documents/Forecastle/backend/app/ml/pipeline.py) — the core idea works but has bugs (see below) |
| **Prophet model** | ✅ Done | Train + predict in [prophet_model.py](file:///c:/Users/admin/Documents/Forecastle/backend/app/ml/prophet_model.py) — clean and functional |
| **XGBoost model** | ✅ Done | Train + predict in [xgboost_model.py](file:///c:/Users/admin/Documents/Forecastle/backend/app/ml/xgboost_model.py) — clean and functional |
| **Feature engine** | ❌ Broken | [feature_engine.py](file:///c:/Users/admin/Documents/Forecastle/backend/app/ml/feature_engine.py) — missing imports (`AsyncSessionLocal`, `select`, `Signal`, `pd`), and pipeline calls `generate_signal_features()` which doesn't exist (only `get_signal_features()` exists) |
| **Ingestion base** | ❌ Broken | [base.py](file:///c:/Users/admin/Documents/Forecastle/backend/app/ingestion/base.py) — `@abstractmethod` decorators on bare functions, not inside a class |
| **Seed script** | ✅ Done | [seed.py](file:///c:/Users/admin/Documents/Forecastle/backend/app/db/seed.py) — seeds 5 products + loads sales from CSV |
| **Synthetic data gen** | ✅ Done | [generate_synthetic_data.py](file:///c:/Users/admin/Documents/Forecastle/scripts/generate_synthetic_data.py) — generates 2yr data with seasonality + shocks |
| **Alembic** | ✅ Init'd | `alembic.ini` exists, `alembic/` directory present |
| **Docker Compose** | ✅ Done | PostgreSQL, Redis, backend, frontend services configured |

### Frontend — React + Vite

| Component | Status | Details |
|---|---|---|
| **Vite scaffold** | ✅ Done | React 19, Vite 8, ESLint |
| **Dashboard page** | ❌ Empty | [Dashboard.jsx](file:///c:/Users/admin/Documents/Forecastle/frontend/src/pages/Dashboard.jsx) — literally just `<h1>DashBoard</h1>` |
| **Routing** | ❌ Missing | No `react-router-dom` installed, no router setup |
| **Tailwind CSS** | ❌ Missing | Not installed in `package.json` |
| **Zustand** | ❌ Missing | Not installed |
| **Axios** | ❌ Missing | Not installed |
| **Recharts** | ❌ Missing | Not installed |
| **Framer Motion** | ❌ Missing | Not installed |
| **All components** | ❌ Missing | No `Sidebar`, `Header`, `ForecastChart`, `ExplanationCard`, etc. |
| **All stores** | ❌ Missing | No Zustand stores |
| **All hooks** | ❌ Missing | No custom hooks |
| **API client layer** | ❌ Missing | No `api/` directory |

---

## 2. What's Still Missing for a Resume-Worthy Project 🔴

### Critical Path (Must-Have)

| # | Item | Priority | Effort |
|---|---|---|---|
| 1 | **Fix ML pipeline bugs** — broken imports in `feature_engine.py`, function name mismatch in `pipeline.py` | 🔴 P0 | ~1 hr |
| 2 | **Fix `ingestion/base.py`** — wrap methods in a proper `BaseCollector` class | 🔴 P0 | ~15 min |
| 3 | **Fix `ProductCreate` schema** — currently empty, can't create products properly | 🔴 P0 | ~15 min |
| 4 | **Build the full React dashboard** — this is ~50% of what makes the project impressive. Sidebar, charts, explanation cards, KPI tiles, override slider | 🔴 P0 | ~12-16 hrs |
| 5 | **Wire up stub API routes** — Signals, Alerts, Forecasts (history/override) need real DB queries | 🔴 P0 | ~4-6 hrs |
| 6 | **Add explanation engine** — `explanation_service.py` is completely missing. This is a key differentiator | 🔴 P0 | ~3-4 hrs |
| 7 | **Add signal collectors** — `news_collector.py`, `social_collector.py`, `weather_collector.py`, `supplier_collector.py` (even mocked) | 🔴 P0 | ~3-4 hrs |
| 8 | **Persist forecasts to DB** — currently the `/generate` endpoint runs ML but never saves results | 🔴 P0 | ~2 hrs |
| 9 | **Model registry** — `model_registry` table exists in plan but no ORM model or versioning logic | 🟡 P1 | ~2-3 hrs |

### Polish Layer (Resume Differentiators)

| # | Item | Priority | Effort |
|---|---|---|---|
| 10 | **Celery tasks** — scheduled retraining, periodic signal ingestion | 🟡 P1 | ~4-5 hrs |
| 11 | **Tests** — backend pytest + frontend Vitest (currently zero tests anywhere) | 🟡 P1 | ~4-6 hrs |
| 12 | **CI/CD** — GitHub Actions for lint + test on PR | 🟡 P1 | ~1-2 hrs |
| 13 | **Dockerfiles** — backend and frontend `Dockerfile`s are missing | 🟡 P1 | ~1 hr |
| 14 | **`.env.example`** — document required env vars | 🟡 P1 | ~15 min |
| 15 | **Real README** — architecture diagram, setup instructions, GIF demo | 🟡 P1 | ~2-3 hrs |
| 16 | **Dark mode + theme** — Tailwind dark mode, smooth toggle | 🟢 P2 | ~2 hrs |
| 17 | **Keyboard shortcuts** | 🟢 P2 | ~1 hr |
| 18 | **PDF export** | 🟢 P2 | ~2-3 hrs |
| 19 | **Deploy to Railway/Vercel** | 🟢 P2 | ~2-3 hrs |

---

## 3. Bugs in Current Code 🐛

### Bug 1: `feature_engine.py` — Missing Imports + Wrong Function Name

```python
# feature_engine.py uses these but never imports them:
# - AsyncSessionLocal
# - select 
# - Signal
# - pd (pandas)

# pipeline.py calls generate_signal_features() — but the actual function is get_signal_features()
# Also: get_signal_features is async, but pipeline.py calls generate_signal_features without await
```

### Bug 2: `ingestion/base.py` — Methods Outside a Class

```diff
 from abc import ABC, abstractmethod
 from datetime import datetime

-@abstractmethod
-async def collect_data(self, product_id:int, date:datetime):
-    pass
-@abstractmethod
-def source_name(self)->str:
-    pass
+class BaseCollector(ABC):
+    @abstractmethod
+    async def collect(self, product_id: int, date: datetime) -> dict:
+        ...
+
+    @abstractmethod
+    def source_name(self) -> str:
+        ...
```

### Bug 3: `ProductCreate` Schema is Empty

```python
class ProductCreate(BaseModel):
    pass  # ← Should inherit from ProductBase to get name, sku, category, unit fields
```

### Bug 4: `sales.py` Model — Revenue as Integer

```python
revenue = Column(Integer, nullable=False)  # ← Plan says DECIMAL(12,2), schema uses Integer
```

### Bug 5: `health.py` — Fake Health Check

Returns hardcoded `"connected"` without actually checking DB/Redis.

---

## 4. Recommended Pivot Strategy: Hackathon → Resume Project

> [!IMPORTANT]
> The project name in code is **"PulseFlow"** but repository and `pyproject.toml` call it **"Forecastle"**. You should pick one name and be consistent — for a resume project, I'd recommend going all-in on **PulseFlow**.

### What to Keep

- ✅ The entire backend architecture (models, schemas, API structure, config, DB session)
- ✅ The ML pipeline concept (Prophet Layer 1 → XGBoost Layer 2)
- ✅ Docker Compose setup  
- ✅ Synthetic data generation script
- ✅ `implementation_plan.md` as your roadmap (it's very well-written)

### What to Change

1. **Fix all bugs first** — the 5 bugs listed above should be your day-1 priority
2. **Build the frontend properly** — this is 100% where the "wow factor" lives for a resume project. A recruiter will look at the dashboard for 5 seconds. It needs to be stunning.
3. **Add the explanation engine** — this is the one feature that makes PulseFlow unique. "AI that explains WHY forecast changed" is a strong resume talking point.
4. **Wire everything end-to-end** — from signal ingestion → ML → forecast → dashboard. Right now the backend and frontend are disconnected.
5. **Add at least basic tests** — even 5-10 well-written tests show engineering discipline
6. **Write a killer README** — architecture diagram, screenshot/GIF, one-command setup

### Suggested Build Order

```
Week 1: Fix bugs → Wire up all API routes → Build Dashboard skeleton with Tailwind
Week 2: ForecastChart + ExplanationCard + KPI tiles → Signal collectors (mocked)  
Week 3: Explanation engine → Override flow → Alerts → Polish animations
Week 4: Tests → CI/CD → README → Deploy
```

---

## 5. Completion Scorecard

| Phase (from plan) | Completion | Notes |
|---|---|---|
| Phase 0 — Scaffolding | **80%** | Missing Dockerfiles, `.env.example`, frontend deps |
| Phase 1 — DB & Models | **70%** | Models done, schemas partial, seed works, CRUD only for products |
| Phase 2 — ML Pipeline | **50%** | Prophet + XGBoost exist but feature engine is broken, no model registry |
| Phase 3 — Signal Ingestion | **5%** | Only broken `base.py`, no actual collectors |
| Phase 4 — Forecast API + Explanation | **20%** | Generate endpoint works (with bugs), no explanation engine, no DB persistence |
| Phase 5 — React Dashboard | **2%** | Only an empty `<h1>DashBoard</h1>` |
| Phase 6 — Polish, Tests, Deploy | **0%** | Nothing done |

**Overall: ~25-30% complete**
