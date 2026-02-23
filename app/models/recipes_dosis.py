"""Modelo para recetas de dosis (recipes_dosis)."""
from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId

from app.models.inventory_raw import PyObjectId


class IngredienteDosis(BaseModel):
    """Ingrediente necesario para 1 dosis."""
    materia_prima_id: str  # ObjectId como string
    cantidad_gramos: float


class RecipesDosis(BaseModel):
    """Receta de batido (1 dosis = 1 bolsita)."""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    nombre_batido: str
    ingredientes: list[IngredienteDosis]
    precio_sugerido: float

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
