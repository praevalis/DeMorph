from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from src.core.logging import logger
from src.core.metadata import ApiTags
from src.user.schemas import UserCreateDto
from src.core.dependencies import get_db_session
from src.core.exceptions import InternalServerException, UnauthorizedException
from src.auth.schemas import (
    AuthData, 
    TokenData,
    TokenTypeEnum,
    AuthResponseDto, 
    RefreshRequestDto, 
    RefreshResponseDto
)
from src.auth.services import (
    create_user,
    verify_token,
    authenticate_user,
    create_access_token,
    create_refresh_token
)

router = APIRouter(
    prefix='/auth',
    tags=[ApiTags.auth]
)

@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=AuthResponseDto)
async def register_user_controller(
    reg_data: UserCreateDto, 
    session: Annotated[Session, Depends(get_db_session)]
) -> AuthResponseDto:
    """
    Endpoint to register user.

    Args:
        reg_data: Data to create user.
        session: DB session.

    Returns:
        AuthResponseDto: Message, auth tokens and created user.
    """
    try:
        created_user = await create_user(reg_data, session)

        token_data = TokenData(sub=str(created_user.id)).model_dump()

        data = AuthData(
            access_token=create_access_token(token_data),
            refresh_token=create_refresh_token(token_data),
            user=created_user
        )

        return AuthResponseDto(data=data)

    except Exception as e:
        logger.error(f'Error while registering user {reg_data.username}: {str(e)}')
        raise InternalServerException()
    
@router.post('/login', status_code=status.HTTP_200_OK, response_model=AuthResponseDto)
async def login_user_controller(
    login_data: Annotated[OAuth2PasswordRequestForm, Depends()], # Must be sent through form data by client
    session: Annotated[Session, Depends(get_db_session)]
) -> AuthResponseDto:
    """
    Endpoint to login user.

    Args:
        login_data: Username and password.
        session: DB Session.
    
    Returns:
        AuthResponseDto: Message, auth tokens and logged user.
    """
    try:
        user = await authenticate_user(
            login_data.username, 
            login_data.password, 
            session
        )
        if not user:
            raise UnauthorizedException('Invalid credentials.')
        
        token_data = TokenData(sub=str(user.id)).model_dump()
        data = AuthData(
            access_token=create_access_token(token_data),
            refresh_token=create_refresh_token(token_data),
            user=user
        )

        return AuthResponseDto(data=data)

    except Exception as e:
        logger.error(f'Error while logging in user {login_data.username}: {str(e)}')
        raise InternalServerException()
    
@router.post('/refresh', status_code=status.HTTP_200_OK, response_model=RefreshResponseDto)
async def refresh_token_controller(data: RefreshRequestDto) -> RefreshResponseDto:
    """
    Endpoint to refresh access token.

    Args
    """
    try:
        refresh_token = data.refresh_token
        user_data = await verify_token(refresh_token, TokenTypeEnum.REFRESH)

        if user_data:
            new_access_token = create_access_token({ 'sub': user_data.sub })
        
        return RefreshResponseDto(
            message='Token refreshed successfully.',
            data={
                'access_token': new_access_token
            }
        )

    except Exception as e: 
        raise InternalServerException()