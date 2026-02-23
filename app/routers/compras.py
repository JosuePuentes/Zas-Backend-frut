"""Compras del cliente autenticado."""
from datetime import datetime
from fastapi import APIRouter, Depends

from app.database import get_database
from app.auth import require_auth

router = APIRouter(prefix="/compras", tags=["Compras"])


def venta_to_response(doc: dict) -> dict:
    return {
        "id": str(doc["_id"]),
        "items": doc.get("items", []),
        "total_venta": doc.get("total_venta", 0),
        "fecha": doc.get("fecha", datetime.utcnow()),
    }


@router.get("")
async def listar_mis_compras(current_user: dict = Depends(require_auth)):
    """Listar compras del cliente autenticado. Requiere Authorization: Bearer <token>."""
    user = current_user
    user_id = user.get("sub")

    db = get_database()
    cursor = db["sales"].find({"clienteId": user_id}).sort("fecha", -1)
    return [venta_to_response(d) async for d in cursor]
