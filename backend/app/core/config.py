from pydantic import BaseSettings, AnyUrl

class Settings(BaseSettings):
    PROJECT_NAME: str = "nexus-bot-platform"
    DATABASE_URL: str
    REDIS_URL: str = "redis://localhost:6379/0"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    BOT_MANAGER_URL: AnyUrl

    FERNET_KEY: str  # for encrypting telegram tokens

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
