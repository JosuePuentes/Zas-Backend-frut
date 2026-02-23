"""Esquemas para ventas."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ExtraItemSchema(BaseModel):
    """Extra para un batido."""
    materia_prima_id: str
    nombre: str
    cantidad: int = 1
    precio_extra: float = 0


class EnvaseItemSchema(BaseModel):
    """Envase/desechable por batido (vaso, tapa, pitillo)."""
    materia_prima_id: str
    cantidad: int = 1


class SaleItemSchema(BaseModel):
    """Item de venta."""
    recipe_id: str
    nombre_batido: str
    cantidad: int = 1
    precio_unitario: float
    extras: list[ExtraItemSchema] = []
    costo_envase: float = 0
    envase_items: list[EnvaseItemSchema] = []  # vaso, tapa, pitillo a descontar


class SaleCreate(BaseModel):
    """Crear venta (desde POS). cliente_id opcional para compras de cliente."""
    items: list[SaleItemSchema]
    cliente_id: Optional[str] = None


class SaleResponse(BaseModel):
    """Respuesta de venta."""
    id: str
    items: list[SaleItemSchema]
    total_venta: float
    costo_total_venta: float
    fecha: datetime
