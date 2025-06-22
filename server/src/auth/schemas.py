from enum import Enum
from pydantic import BaseModel, Field

from src.user.schemas import UserDto

class TokenTypeEnum(str, Enum):
    """Enum to represent types of authentication tokens."""
    ACCESS = "access"
    REFRESH = "refresh"

class TokenData(BaseModel):
    sub: str

class AuthData(BaseModel):
    access_token: str
    refresh_token: str
    user: UserDto

class AuthResponseDto(BaseModel):
    message: str | None = Field(default='Authentication successful.')
    data: AuthData

class RefreshRequestDto(BaseModel):
    refresh_token: str

class RefreshResponseDto(BaseModel):
    message: str | None = Field(default='Refresh request successful.')
    data: dict