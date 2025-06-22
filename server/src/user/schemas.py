from uuid import UUID
from datetime import datetime
from pydantic import EmailStr, BaseModel, ConfigDict, Field

class UserDto(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    first_name: str
    last_name: str | None
    joined_at: datetime

    model_config = ConfigDict(
        extra='forbid',
        from_attributes=True # important for sqlalchemy compatibility
    )

class UserCreateDto(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr 
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str | None = Field(min_length=1, max_length=50)
    password: str = Field(min_length=3, max_length=8, pattern=r"^[A-Za-z\d@$!%*?&]+$")

    model_config = ConfigDict(
        str_strip_whitespace=True
    )

class UserUpdateDto(BaseModel):
    first_name: str | None = None
    last_name: str | None = None

    model_config = ConfigDict(
        str_strip_whitespace=True
    )

class UserResponseDto(BaseModel):
    message: str
    data: UserDto | None = None