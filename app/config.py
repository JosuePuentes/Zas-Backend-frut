"""Configuración de la aplicación."""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Configuración cargada desde variables de entorno."""
    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "zas_batidos"
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Obtener configuración cacheada."""
    return Settings()
