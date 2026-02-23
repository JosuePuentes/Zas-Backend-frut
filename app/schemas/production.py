"""Esquemas para módulo de producción."""
from pydantic import BaseModel


class ProcesarDosisRequest(BaseModel):
    """Request para procesar dosis."""
    recipe_id: str
    cantidad_dosis: int
