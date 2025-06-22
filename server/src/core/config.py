from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    LOG_LEVEL: str 
    LOG_DIR_PATH: str

    POSTGRES_URI: str

    ALGORITHM: str
    SECRET_KEY: str
    REFRESH_TOKEN_EXPIRES_DAYS: int
    ACCESS_TOKEN_EXPIRES_MINUTES: int  
    ALLOWED_ORIGINS: list[str] = Field(default_factory=list)

    model_config = SettingsConfigDict(
        env_file=('.env', '.env.local', '.env.production')
    )

settings = Settings() # type: ignore