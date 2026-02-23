"""Configuración de la aplicación."""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Configuración cargada desde variables de entorno."""
    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "zas_batidos"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    jwt_secret: str = "cambiar-en-produccion-secret-key-segura"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24 * 7  # 7 días

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Obtener configuración cacheada."""
    return Settings()
