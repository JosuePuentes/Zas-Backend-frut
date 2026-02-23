"""Endpoints de soporte. POST público (cliente), GET/PATCH en /admin/soporte."""
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


def _soporte_response(doc: dict) -> dict:
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
    """Crear mensaje de soporte (cliente, público)."""
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
    return _soporte_response(doc)
