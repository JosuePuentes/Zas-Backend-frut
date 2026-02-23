"""Endpoints de soporte."""
from datetime import datetime
from fastapi import APIRouter, HTTPException
from bson import ObjectId

from app.database import get_database
from pydantic import BaseModel

router = APIRouter(prefix="/soporte", tags=["Soporte"])


class MensajeSoporteCreate(BaseModel):
    cliente_id: str
    mensaje: str
    asunto: str = ""


def doc_to_response(doc: dict) -> dict:
    return {
        "id": str(doc["_id"]),
        "clienteId": doc.get("clienteId", ""),
        "mensaje": doc.get("mensaje", ""),
        "asunto": doc.get("asunto", ""),
        "leido": doc.get("leido", False),
        "createdAt": doc.get("createdAt", datetime.utcnow()),
    }


@router.post("")
async def crear_mensaje(data: MensajeSoporteCreate):
    """Crear mensaje de soporte (cliente)."""
    db = get_database()
    doc = {
        "clienteId": data.cliente_id,
        "mensaje": data.mensaje,
        "asunto": data.asunto,
        "leido": False,
        "createdAt": datetime.utcnow(),
    }
    result = await db["soporte"].insert_one(doc)
    doc["_id"] = result.inserted_id
    return doc_to_response(doc)


@router.get("")
async def listar_mensajes(limit: int = 50):
    """Listar mensajes de soporte (admin)."""
    db = get_database()
    cursor = db["soporte"].find().sort("createdAt", -1).limit(limit)
    return [doc_to_response(d) async for d in cursor]


@router.patch("/{id}/read")
async def marcar_leido(id: str):
    """Marcar mensaje como leído."""
    db = get_database()
    doc = await db["soporte"].find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": {"leido": True}}, return_document=True
    )
    if not doc:
        raise HTTPException(404, "Mensaje no encontrado")
    return doc_to_response(doc)
