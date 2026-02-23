"""12.7 Catálogo Cliente - solo código, descripción, precio (público)."""
from fastapi import APIRouter

from app.database import get_database

router = APIRouter(prefix="/catalogo", tags=["Catálogo"])


@router.get("")
async def listar_catalogo():
    """Catálogo público: código, descripción, precio (sin costo vaso/etiqueta)."""
    db = get_database()
    cursor = db["inventario_venta"].find({})
    return [
        {
            "id": str(d["_id"]),
            "codigo": d.get("codigo", ""),
            "descripcion": d.get("descripcion", ""),
            "precio": d.get("precio", 0),
        }
        async for d in cursor
    ]
