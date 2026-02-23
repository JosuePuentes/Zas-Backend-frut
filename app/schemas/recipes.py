"""Esquemas para recetas de dosis."""
from typing import Optional
from pydantic import BaseModel


class IngredienteDosisSchema(BaseModel):
    """Ingrediente para receta."""
    materia_prima_id: str
    cantidad_gramos: float


class RecipeCreate(BaseModel):
    """Crear receta."""
    nombre_batido: str
    ingredientes: list[IngredienteDosisSchema]
    precio_sugerido: float


class RecipeUpdate(BaseModel):
    """Actualizar receta."""
    nombre_batido: Optional[str] = None
    ingredientes: Optional[list[IngredienteDosisSchema]] = None
    precio_sugerido: Optional[float] = None


class RecipeResponse(BaseModel):
    """Respuesta de receta."""
    id: str
    nombre_batido: str
    ingredientes: list[IngredienteDosisSchema]
    precio_sugerido: float
