"""Esquemas para inventario de dosis."""
from pydantic import BaseModel


class InventoryDosisCreate(BaseModel):
    """Crear registro de inventario dosis."""
    recipe_id: str
    cantidad_bolsitas_listas: int = 0


class InventoryDosisResponse(BaseModel):
    """Respuesta de inventario dosis."""
    id: str
    recipe_id: str
    cantidad_bolsitas_listas: int


class DisponibilidadBatido(BaseModel):
    """Disponibilidad calculada de un batido."""
    recipe_id: str
    nombre_batido: str
    stock_dosis: int
    producibles_con_materia_prima: int
    total_disponible: int
    precio_sugerido: float
