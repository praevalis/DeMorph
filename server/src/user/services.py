from uuid import UUID
from sqlalchemy.orm import Session

from src.user.models import User
from src.user.schemas import UserDto, UserUpdateDto
from src.core.database import (
    get_by_id_or_404, 
    assert_entity_identity_match
)

async def update_user(
    user_id: UUID, 
    update_data: UserUpdateDto, 
    session: Session,
    current_user: UserDto
) -> UserDto:
    """
    Updates an user.
    
    Args:
        user_id: ID of the user to update.
        update_data: Data to update.
        session: DB session.
        current_user: User who sent the request.

    Returns: 
        UserDto: Updated user.
    """
    user_to_update = get_by_id_or_404(User, user_id, session)
    assert_entity_identity_match(UserDto.model_validate(user_to_update), current_user)

    update_dict = update_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(user_to_update, field, value)

    session.commit()
    session.refresh(user_to_update)

    return UserDto.model_validate(user_to_update)
    
async def delete_user(
    user_id: UUID,
    session: Session,
    current_user: UserDto
) -> None:
    """
    Deletes an user.

    Args:
        user_id: ID of the user to delete.
        session: DB session.
        current_user: User who sent the request.

    Returns:
        None
    """
    user_to_delete = get_by_id_or_404(User, user_id, session)
    assert_entity_identity_match(UserDto.model_validate(user_to_delete), current_user)

    session.delete(user_to_delete)
    session.flush()