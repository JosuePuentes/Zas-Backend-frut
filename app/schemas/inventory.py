"""Esquemas para materia prima."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class InventoryRawCreate(BaseModel):
    """Crear materia prima."""
    nombre: str
    cantidad_total: float
    costo_por_unidad: float
    unidad_medida: str = "g"
    stock_minimo: float = 0
    fecha_ingreso: Optional[datetime] = None
    es_desechable: bool = False


class InventoryRawUpdate(BaseModel):
    """Actualizar materia prima."""
    nombre: Optional[str] = None
    cantidad_total: Optional[float] = None
    costo_por_unidad: Optional[float] = None
    unidad_medida: Optional[str] = None
    stock_minimo: Optional[float] = None
    fecha_ingreso: Optional[datetime] = None
    es_desechable: Optional[bool] = None


class InventoryRawResponse(BaseModel):
    """Respuesta de materia prima."""
    id: str
    nombre: str
    cantidad_total: float
    costo_por_unidad: float
    unidad_medida: str
    stock_minimo: float
    fecha_ingreso: Optional[datetime] = None
    es_desechable: bool
