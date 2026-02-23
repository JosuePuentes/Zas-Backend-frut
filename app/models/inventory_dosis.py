"""Modelo para inventario de dosis preparadas (inventory_dosis)."""
from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId

from app.models.inventory_raw import PyObjectId


class InventoryDosis(BaseModel):
    """Stock de bolsitas/dosis ya preparadas."""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    recipe_id: str  # ObjectId de la receta
    cantidad_bolsitas_listas: int

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
