"""Finanzas globales (solo master)."""
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends

from app.database import get_database
from app.auth import require_auth

router = APIRouter(prefix="/admin", tags=["Admin"])


async def _require_master(current_user: dict = Depends(require_auth)):
    if current_user.get("rol") != "master":
        from fastapi import HTTPException
        raise HTTPException(403, "Solo master puede ver finanzas globales")
    return current_user


@router.get("/finanzas")
@router.get("/finanzas-global")
async def finanzas_globales(current_user: dict = Depends(_require_master)):
    """Suma de ventas de todas las sucursales (solo master)."""
    db = get_database()
    pipeline = [
        {"$group": {"_id": None, "total_ventas": {"$sum": "$total_venta"}, "total_costos": {"$sum": "$costo_total_venta"}}},
    ]
    cursor = db["sales"].aggregate(pipeline)
    result = await cursor.to_list(length=1)
    if not result:
        return {"total_ventas": 0, "total_costos": 0, "ganancia": 0}
    r = result[0]
    return {
        "total_ventas": r.get("total_ventas", 0),
        "total_costos": r.get("total_costos", 0),
        "ganancia": r.get("total_ventas", 0) - r.get("total_costos", 0),
    }
