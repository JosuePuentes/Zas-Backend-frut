"""Modelo para materia prima (inventory_raw)."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId


class PyObjectId(ObjectId):
    """Wrapper para ObjectId de MongoDB en Pydantic."""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("ObjectId inválido")
        return ObjectId(v)


class InventoryRaw(BaseModel):
    """Materia prima en inventario."""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    nombre: str  # ej. Cambur, Galletas, Pistacho
    cantidad_total: float  # en gramos/kg/ml
    costo_por_unidad: float
    unidad_medida: str = "g"  # g, kg, ml, L, unidades
    stock_minimo: float = 0  # para planificación de compras
    fecha_ingreso: Optional[datetime] = None  # para alertas de caducidad
    es_desechable: bool = False  # True para vasos, tapas, pitillos

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
