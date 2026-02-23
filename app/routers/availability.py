"""Endpoints para disponibilidad de batidos."""
from fastapi import APIRouter

from app.schemas.inventory_dosis import DisponibilidadBatido
from app.services.availability_service import AvailabilityService

router = APIRouter(prefix="/availability", tags=["Disponibilidad"])


@router.get("/batidos", response_model=list[DisponibilidadBatido])
async def get_disponibilidad_batidos():
    """
    Disponibilidad de cada batido:
    - Stock de dosis listas
    - Cuántos se pueden producir con materia prima actual
    - Total disponible
    """
    return await AvailabilityService.get_disponibilidad_batidos()
