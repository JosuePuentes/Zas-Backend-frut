"""Admin: listar y marcar mensajes de soporte."""
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId

from app.database import get_database
from app.auth import require_auth

router = APIRouter(prefix="/admin", tags=["Admin Soporte"])


async def _require_admin(current_user: dict = Depends(require_auth)):
    if current_user.get("rol") not in ("admin", "master"):
        raise HTTPException(403, "Solo admin o master")
    return current_user


def _soporte_response(doc: dict) -> dict:
    return {
        "id": str(doc["_id"]),
        "clienteId": doc.get("clienteId", ""),
        "mensaje": doc.get("mensaje", ""),
        "asunto": doc.get("asunto", ""),
        "leido": doc.get("leido", False),
        "createdAt": doc.get("createdAt", datetime.utcnow()),
    }


@router.get("/soporte")
async def listar_mensajes(limit: int = 50, _: dict = Depends(_require_admin)):
    """Listar mensajes de soporte (admin)."""
    db = get_database()
    cursor = db["soporte"].find().sort("createdAt", -1).limit(limit)
    return [_soporte_response(d) async for d in cursor]


@router.patch("/soporte/{id}/read")
async def marcar_leido(id: str, _: dict = Depends(_require_admin)):
    """Marcar mensaje como leído."""
    db = get_database()
    doc = await db["soporte"].find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": {"leido": True}}, return_document=True
    )
    if not doc:
        raise HTTPException(404, "Mensaje no encontrado")
    return _soporte_response(doc)
