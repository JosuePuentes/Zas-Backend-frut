"""CRUD Anuncios diarios."""
from datetime import datetime
from fastapi import APIRouter, HTTPException
from bson import ObjectId

from app.database import get_database
from pydantic import BaseModel

router = APIRouter(prefix="/anuncios", tags=["Anuncios"])


class AnuncioCreate(BaseModel):
    texto: str
    enlace: str = ""
    activo: bool = True


class AnuncioUpdate(BaseModel):
    texto: str | None = None
    enlace: str | None = None
    activo: bool | None = None


def doc_to_response(doc: dict) -> dict:
    return {
        "id": str(doc["_id"]),
        "texto": doc["texto"],
        "enlace": doc.get("enlace", ""),
        "activo": doc.get("activo", True),
        "createdAt": doc.get("createdAt", datetime.utcnow()),
    }


@router.get("")
async def listar_anuncios(activo_only: bool = False):
    """Listar anuncios. activo_only=true para solo activos."""
    db = get_database()
    query = {"activo": True} if activo_only else {}
    cursor = db["anuncios"].find(query).sort("createdAt", -1)
    return [doc_to_response(d) async for d in cursor]


@router.post("")
async def crear_anuncio(data: AnuncioCreate):
    """Crear anuncio."""
    db = get_database()
    doc = {
        "texto": data.texto,
        "enlace": data.enlace,
        "activo": data.activo,
        "createdAt": datetime.utcnow(),
    }
    result = await db["anuncios"].insert_one(doc)
    doc["_id"] = result.inserted_id
    return doc_to_response(doc)


@router.get("/{id}")
async def obtener_anuncio(id: str):
    """Obtener anuncio por ID."""
    db = get_database()
    doc = await db["anuncios"].find_one({"_id": ObjectId(id)})
    if not doc:
        raise HTTPException(404, "Anuncio no encontrado")
    return doc_to_response(doc)


@router.patch("/{id}")
async def actualizar_anuncio(id: str, data: AnuncioUpdate):
    """Actualizar anuncio."""
    db = get_database()
    update = {k: v for k, v in data.model_dump().items() if v is not None}
    if not update:
        raise HTTPException(400, "Nada que actualizar")
    doc = await db["anuncios"].find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": update}, return_document=True
    )
    if not doc:
        raise HTTPException(404, "Anuncio no encontrado")
    return doc_to_response(doc)


@router.delete("/{id}")
async def eliminar_anuncio(id: str):
    """Eliminar anuncio."""
    db = get_database()
    result = await db["anuncios"].delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(404, "Anuncio no encontrado")
    return {"message": "Eliminado"}
