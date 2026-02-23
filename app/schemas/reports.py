"""Esquemas para reportes."""
from datetime import datetime
from pydantic import BaseModel


class ReporteUtilidadItem(BaseModel):
    """Item del reporte de utilidad."""
    venta_id: str
    fecha: datetime
    total_venta: float
    costo_total: float
    ganancia_neta: float


class ReporteUtilidadResponse(BaseModel):
    """Reporte de utilidad."""
    periodo_inicio: datetime
    periodo_fin: datetime
    ventas: list[ReporteUtilidadItem]
    total_ventas: float
    total_costos: float
    ganancia_neta_total: float
