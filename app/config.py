from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import platform

if platform.system() == "Darwin":
    env_name = "development"
elif platform.system() == "Linux":
    env_name = "production"


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
    env_name: str = env_name
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    UPLOAD_FOLDER: str = "./uploads"
    key: str = ""


@lru_cache(maxsize=256)
def getsettings() -> Settings:
    settings = Settings()
    print(f"Settings loaded: {settings.env_name}")
    return settings
