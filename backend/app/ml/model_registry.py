"""Model versioning and registry service.

Handles model registration, promotion, and lookup for the ML pipeline.
Provides a lightweight alternative to MLflow for portfolio projects.
"""

from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.model_registry import ModelRegistry


async def register_model(
    model_name: str,
    version: str,
    artifact_path: str,
    metrics: dict | None = None,
    session: AsyncSession | None = None,
) -> ModelRegistry:
    """Register a new model version after training.

    Args:
        model_name: e.g. 'prophet_base', 'xgboost_signal'
        version: e.g. 'v1', 'v2'
        artifact_path: Path to the serialized model file
        metrics: Training/validation metrics like {"mape": 0.12, "rmse": 450}
        session: Async DB session
    """
    from app.db.session import AsyncSessionLocal

    own_session = session is None
    if own_session:
        session = AsyncSessionLocal()

    try:
        entry = ModelRegistry(
            model_name=model_name,
            version=version,
            artifact_path=artifact_path,
            metrics=metrics,
            is_active=False,
            trained_at=datetime.utcnow(),
        )
        session.add(entry)
        await session.commit()
        await session.refresh(entry)
        return entry
    finally:
        if own_session:
            await session.close()


async def promote_model(
    model_name: str,
    version: str,
    session: AsyncSession | None = None,
) -> bool:
    """Promote a model version to active, deactivating all others of the same name.

    Returns True if the model was found and promoted.
    """
    from app.db.session import AsyncSessionLocal

    own_session = session is None
    if own_session:
        session = AsyncSessionLocal()

    try:
        # Deactivate all versions of this model
        await session.execute(
            update(ModelRegistry)
            .where(ModelRegistry.model_name == model_name)
            .values(is_active=False)
        )

        # Activate the target version
        result = await session.execute(
            select(ModelRegistry).where(
                ModelRegistry.model_name == model_name,
                ModelRegistry.version == version,
            )
        )
        entry = result.scalar_one_or_none()

        if not entry:
            return False

        entry.is_active = True
        await session.commit()
        return True
    finally:
        if own_session:
            await session.close()


async def get_active_model(
    model_name: str,
    session: AsyncSession | None = None,
) -> ModelRegistry | None:
    """Get the currently active model version for a given model name."""
    from app.db.session import AsyncSessionLocal

    own_session = session is None
    if own_session:
        session = AsyncSessionLocal()

    try:
        result = await session.execute(
            select(ModelRegistry).where(
                ModelRegistry.model_name == model_name,
                ModelRegistry.is_active == True,  # noqa: E712
            )
        )
        return result.scalar_one_or_none()
    finally:
        if own_session:
            await session.close()


async def get_all_models(session: AsyncSession) -> list[ModelRegistry]:
    """Get all registered model versions."""
    result = await session.execute(
        select(ModelRegistry).order_by(ModelRegistry.trained_at.desc())
    )
    return result.scalars().all()
