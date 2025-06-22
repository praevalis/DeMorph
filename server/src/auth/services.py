from typing import Any
from jwt import PyJWTError
from datetime import timedelta
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordBearer

from src.user.models import User
from src.core.config import settings
from src.user.schemas import UserCreateDto, UserDto
from src.auth.schemas import AuthData, TokenTypeEnum, TokenData
from src.core.exceptions import UnauthorizedException, BadRequestException
from src.auth.utils import (
    verify_password,
    hash_password,
    encode_jwt,
    decode_jwt
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

def create_access_token(data: dict[str, Any]) -> str:
    """
    Creates an access token.

    Args:
        data: Data to be encoded for token.

    Returns:
        str: Created access token.
    """
    return encode_jwt(
        data,
        secret_key=settings.SECRET_KEY.get_secret_value(),
        algorithm=settings.ALGORITHM,
        expires_delta=timedelta(settings.ACCESS_TOKEN_EXPIRES_MINUTES),
        token_type=TokenTypeEnum.ACCESS
    )

def create_refresh_token(data: dict[str, Any]) -> str:
    """
    Creates a refresh token.

    Args:
        data: Data to be encoded for token.

    Returns:
        str: Created refresh token.
    """
    return encode_jwt(
        data,
        secret_key=settings.SECRET_KEY.get_secret_value(),
        algorithm=settings.ALGORITHM,
        expires_delta=timedelta(settings.REFRESH_TOKEN_EXPIRES_DAYS),
        token_type=TokenTypeEnum.REFRESH
    )

async def create_user(user_data: UserCreateDto, session: Session) -> UserDto:
    """
    Creates a new user.

    Args:
        user_data: Data to create user.
        session: DB session.

    Returns:
        UserDto: Created user.
    """
    existing_query = select(User).where(
        or_(
            User.username == user_data.username,
            User.email == user_data.email
        )
    )

    existing_user = session.scalars(existing_query).first()
    if existing_user:
        raise BadRequestException('Username or Email already exists.')
    
    password_hash = hash_password(user_data.password)

    user = User(
        username=user_data.username,
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        password_hash=password_hash
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return UserDto.model_validate(user)

async def authenticate_user(
    username_or_email: str, 
    password: str, 
    session: Session
) -> UserDto | None:
    """
    Authenticates user using credentials.

    Args:
        username_or_email: Identifier used for authentication.
        password: Password to be validated.

    Returns:
        UserDto | None: User is returned if authenticated succeeds else None.
    """
    if '@' in username_or_email:
        query = select(User).where(User.email == username_or_email)
    else:
        query = select(User).where(User.username == username_or_email)

    user = session.scalars(query).first()
    if not user:
        return None
    
    if not verify_password(password, user.password_hash):
        return None
    
    return UserDto.model_validate(user)

async def verify_token(
    token: str, 
    expected_token_type: TokenTypeEnum
) -> TokenData | None:
    """
    Verifies given token and returns encoded payload if valid.

    Args:
        token: Token to verify.
        expected_token_type: Type of the token.

    Returns:
        TokenData | None: Data is returned if valid else None.
    """
    try:
        payload = decode_jwt(
            token, 
            settings.SECRET_KEY.get_secret_value(), 
            settings.ALGORITHM
        )
        
        token_type = payload.get('type')
        if token_type != expected_token_type.value:
            raise UnauthorizedException('Token type mismatch.')

        user_id = payload.get('sub')
        if not user_id:
            raise UnauthorizedException('Token payload missing required data.')

        return TokenData(sub=user_id)

    except (PyJWTError, KeyError):
        raise UnauthorizedException('Invalid or expired token.')