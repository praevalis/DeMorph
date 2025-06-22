from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Annotated, AsyncGenerator

from src.user.models import User
from src.user.schemas import UserDto
from src.auth.schemas import TokenTypeEnum
from src.core.database import SessionLocal
from src.core.exceptions import UnauthorizedException
from src.auth.services import verify_token, oauth2_scheme

async def get_db_session() -> AsyncGenerator[Session, None]:
    """Dependency Injector for DB Session."""
    try:
        db = SessionLocal()
        yield db
    finally: 
        db.close()

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[Session, Depends(get_db_session)] 
) -> UserDto:
    """
    Dependency Injector for current user.

    Args:
        token: Bearer token from Authorization header.
        session: DB session.

    Returns:   
        UserDto: Current user.
    """
    token_data = await verify_token(token, TokenTypeEnum.ACCESS)
    if not token_data:
        raise UnauthorizedException()
    
    query = select(User).where(User.id == token_data.sub)
    user = session.scalars(query).first()

    if not user:
        raise UnauthorizedException()

    return UserDto.model_validate(user)

