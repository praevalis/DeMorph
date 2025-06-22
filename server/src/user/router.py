from uuid import UUID
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status

from src.core.logging import logger
from src.core.metadata import ApiTags
from src.user.services import update_user, delete_user
from src.core.exceptions import InternalServerException
from src.core.dependencies import get_db_session, get_current_user
from src.user.schemas import UserDto, UserResponseDto, UserUpdateDto

router = APIRouter(
    prefix='/users',
    tags=[ApiTags.user]
)

@router.patch('/{user_id}', status_code=status.HTTP_200_OK, response_model=UserResponseDto)
async def update_user_controller(
    user_id: UUID, 
    update_data: UserUpdateDto, 
    session: Annotated[Session, Depends(get_db_session)],
    current_user: Annotated[UserDto, Depends(get_current_user)]
) -> UserResponseDto:
    """
    Endpoint to update user.

    Args:
        user_id: ID of the user to update.
        update_data: Data used for update.
        session: DB Session.
        current_user: User making the request.
    
    Returns:
        UserResponseDto: Message and updated user.
    """
    try:
        updated_user = await update_user(user_id, update_data, session, current_user)
        return UserResponseDto(
            message='User updated successfully.',
            data=updated_user
        )
    
    except Exception as e:
        logger.error(f'Error while updating user {user_id}: {str(e)}')
        raise InternalServerException()
    
@router.delete('/{user_id}', status_code=status.HTTP_200_OK, response_model=UserResponseDto)
async def delete_user_controller(
    user_id: UUID,
    session: Annotated[Session, Depends(get_db_session)],
    current_user: Annotated[UserDto, Depends(get_current_user)] 
) -> UserResponseDto:
    """
    Endpoint to delete an user.

    Args:
        user_id: ID of the user to delete.
        session: DB session.
        current_user: User making the request.
    """
    try:
        await delete_user(user_id, session, current_user)
        return UserResponseDto(
            message='User deleted successfully.',
            data=None # returning empty body for a delete request as per convention
        )
    
    except Exception as e: 
        logger.error(f'Error while deleting user {user_id}: {str(e)}')
        raise InternalServerException()