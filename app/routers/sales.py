"""Endpoints para punto de venta (POS)."""
from fastapi import APIRouter, HTTPException

from app.schemas.sales import SaleCreate, SaleResponse
from app.services.sales_service import SalesService

router = APIRouter(prefix="/sales", tags=["Ventas"])


@router.post("", response_model=SaleResponse)
async def crear_venta(data: SaleCreate):
    """
    Cerrar venta (POS).
    Actualiza todos los inventarios de forma atómica:
    - Descuenta dosis o materia prima
    - Descuenta extras
    - Descuenta envases (vaso, tapa, pitillo)
    """
    try:
        items = [item.model_dump() for item in data.items]
        return await SalesService.crear_venta(
            items, cliente_id=data.cliente_id, sucursal_id=data.sucursal_id
        )
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get("")
async def listar_ventas(limit: int = 50):
    """Listar ventas recientes."""
    from app.database import get_database
    from datetime import datetime

    db = get_database()
    cursor = db["sales"].find().sort("fecha", -1).limit(limit)
    ventas = []
    async for doc in cursor:
        ventas.append({
            "id": str(doc["_id"]),
            "items": doc.get("items", []),
            "total_venta": doc.get("total_venta", 0),
            "costo_total_venta": doc.get("costo_total_venta", 0),
            "fecha": doc.get("fecha", datetime.utcnow()),
        })
    return ventas
