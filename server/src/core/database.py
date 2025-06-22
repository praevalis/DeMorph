from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy import create_engine, select
from typing import TypeVar, Type, Protocol, runtime_checkable
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase, Mapped

from src.core.config import settings
from src.core.exceptions import NotFoundException, ForbiddenException

# DB globals for entire application
engine = create_engine(url=settings.POSTGRES_URI)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

class Base(DeclarativeBase):
    pass

# Helper functions for DB

# Generic database operations
T = TypeVar("T", bound=Base)  # Generic type for ORM models

@runtime_checkable
class ModelProto(Protocol):
    """Protocol to enforce ID presence."""
    id: UUID 

def get_by_id_or_404(model: Type[T], id: UUID, session: Session) -> T:
    """
    Generic function to fetch an entity by ID or raise 404.

    Args:
        model: SQLAlchemy model class (e.g., User, Conversation).
        id: UUID of the entity.
        session: SQLAlchemy session.

    Returns:
        The instance of the model.

    Raises:
        HTTPException: 404 if not found.
    """
    instance = session.scalar(select(model).where(model.id == id))  # type: ignore[attr-defined]
    if not instance:
        raise NotFoundException(f'{model.__name__} not found.')
    return instance

def assert_entity_identity_match(entity: ModelProto, actor: ModelProto) -> None:
    """
    Asserts that the actor's ID matches the target entity's ID.

    Args:
        entity: The target ORM model or object (must have an `id`).
        actor: The current user or requesting identity (must have an `id`).

    Raises:
        HTTPException: 403 if IDs don't match.
    """
    if getattr(entity, 'id', None) != getattr(actor, 'id', None):
        label = type(entity).__name__
        raise ForbiddenException(f'{label} identity mismatch.')