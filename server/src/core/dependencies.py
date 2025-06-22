from typing import Generator
from sqlalchemy.orm import Session

from src.user.schemas import UserDto
from src.core.database import SessionLocal

def get_db_session() -> Generator[Session, None, None]:
    """Dependency Injector for DB Session."""
    try:
        db = SessionLocal()
        yield db
    finally: 
        db.close()

def get_current_user() -> UserDto:
    return UserDto.model_validate({})