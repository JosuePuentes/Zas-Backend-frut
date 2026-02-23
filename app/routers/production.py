"""Endpoints para módulo de producción."""
from fastapi import APIRouter, HTTPException

from app.schemas.production import ProcesarDosisRequest
from app.services.production_service import ProductionService

router = APIRouter(prefix="/production", tags=["Producción"])


@router.post("/procesar-dosis")
async def procesar_dosis(data: ProcesarDosisRequest):
    """
    Procesar N dosis de un batido.
    Resta materia prima de inventory_raw y suma dosis a inventory_dosis.
    """
    try:
        result = await ProductionService.procesar_dosis(
            recipe_id=data.recipe_id,
            cantidad_dosis=data.cantidad_dosis,
        )
        return result
    except ValueError as e:
        raise HTTPException(400, str(e))
