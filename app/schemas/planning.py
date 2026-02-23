"""Esquemas para planificación de compras."""
from pydantic import BaseModel


class ListaComprasItem(BaseModel):
    """Item para lista de compras."""
    materia_prima_id: str
    nombre: str
    stock_actual: float
    stock_minimo: float
    cantidad_a_comprar: float
    unidad_medida: str


class ListaComprasResponse(BaseModel):
    """Lista de compras generada."""
    items: list[ListaComprasItem]
    total_items: int
