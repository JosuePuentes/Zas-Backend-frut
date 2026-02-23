"""Endpoints para alertas de caducidad."""
from fastapi import APIRouter, Query

from app.services.alerts_service import AlertsService

router = APIRouter(prefix="/alerts", tags=["Alertas"])


@router.get("/caducidad")
async def get_alertas_caducidad(dias_antiguedad: int = Query(3, ge=1)):
    """
    Materia prima ordenada por fecha_ingreso.
    Las más antiguas deberían usarse primero (frutas).
    """
    return await AlertsService.get_alertas_caducidad(dias_antiguedad)
