"""Modelo para ventas (sales)."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId

from app.models.inventory_raw import PyObjectId


class ExtraItem(BaseModel):
    """Extra añadido a un batido (Galletas, Pistacho, etc.)."""
    materia_prima_id: str
    nombre: str
    cantidad: int = 1
    precio_extra: float = 0


class SaleItem(BaseModel):
    """Item de venta: batido + extras."""
    recipe_id: str
    nombre_batido: str
    cantidad: int = 1
    precio_unitario: float
    extras: list[ExtraItem] = []
    costo_envase: float = 0  # vaso + tapa + pitillo


class Sale(BaseModel):
    """Venta registrada."""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    items: list[SaleItem]
    total_venta: float
    costo_total_venta: float
    fecha: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
