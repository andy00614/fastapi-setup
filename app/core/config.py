# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # v2 的正确写法：这里声明 .env 文件
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    PROJECT_NAME: str = "FastAPI App"
    VERSION: str = "0.1.0"
    SECRET_KEY: str = "dev-key"
    DATABASE_URL: str | None = None

settings = Settings()
