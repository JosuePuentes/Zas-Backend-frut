"""Endpoints de notificaciones."""
from fastapi import APIRouter, HTTPException
from bson import ObjectId

from app.database import get_database
from app.schemas.notification import NotificationResponse

router = APIRouter(prefix="/notifications", tags=["Notifications"])


def notification_to_response(doc: dict) -> dict:
    """Convertir documento a respuesta."""
    return {
        "id": str(doc["_id"]),
        "tipo": doc.get("tipo", ""),
        "mensaje": doc.get("mensaje", ""),
        "leida": doc.get("leida", False),
        "createdAt": doc.get("createdAt"),
    }


@router.get("", response_model=list[NotificationResponse])
async def listar_notificaciones():
    """Listar notificaciones."""
    db = get_database()
    cursor = db["notifications"].find().sort("createdAt", -1)
    return [notification_to_response(doc) async for doc in cursor]


@router.patch("/read-all")
async def marcar_todas_leidas():
    """Marcar todas las notificaciones como leídas."""
    db = get_database()
    await db["notifications"].update_many({}, {"$set": {"leida": True}})
    return {"message": "Todas las notificaciones marcadas como leídas"}


@router.patch("/{notification_id}/read")
async def marcar_como_leida(notification_id: str):
    """Marcar notificación como leída."""
    db = get_database()
    result = await db["notifications"].find_one_and_update(
        {"_id": ObjectId(notification_id)},
        {"$set": {"leida": True}},
        return_document=True,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    return notification_to_response(result)
