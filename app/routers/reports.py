"""Endpoints para reportes."""
from datetime import datetime
from fastapi import APIRouter, Query

from app.schemas.reports import ReporteUtilidadResponse
from app.services.reports_service import ReportsService

router = APIRouter(prefix="/reports", tags=["Reportes"])


@router.get("/utilidad", response_model=ReporteUtilidadResponse)
async def get_reporte_utilidad(
    fecha_inicio: datetime | None = Query(None),
    fecha_fin: datetime | None = Query(None),
):
    """
    Reporte de utilidad:
    Precio de Venta - (Costo Dosis + Costo Extras + Costo Envase)
    """
    return await ReportsService.get_reporte_utilidad(fecha_inicio, fecha_fin)


@router.get("/mas-vendidos")
async def get_mas_vendidos(limite: int = Query(10, ge=1, le=50)):
    """Batidos más vendidos por cantidad."""
    return await ReportsService.get_mas_vendidos(limite)


@router.get("/mayor-margen")
async def get_mayor_margen(limite: int = Query(10, ge=1, le=50)):
    """Batidos con mayor margen de ganancia."""
    return await ReportsService.get_mayor_margen(limite)
