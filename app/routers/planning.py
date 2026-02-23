"""Endpoints para planificación de compras."""
from fastapi import APIRouter

from app.schemas.planning import ListaComprasItem, ListaComprasResponse
from app.services.planning_service import PlanningService

router = APIRouter(prefix="/planning", tags=["Planificación"])


@router.get("/lista-compras", response_model=ListaComprasResponse)
async def get_lista_compras():
    """
    Compara stock actual vs stock mínimo.
    Genera lista de compras para reabastecimiento.
    """
    items = await PlanningService.get_lista_compras()
    return {
        "items": items,
        "total_items": len(items),
    }
