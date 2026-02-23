"""CRUD Banners."""
from datetime import datetime
from fastapi import APIRouter, HTTPException
from bson import ObjectId

from app.database import get_database
from pydantic import BaseModel

router = APIRouter(prefix="/banners", tags=["Banners"])


class BannerCreate(BaseModel):
    imagen_url: str
    enlace: str = ""
    orden: int = 0
    activo: bool = True


class BannerUpdate(BaseModel):
    imagen_url: str | None = None
    enlace: str | None = None
    orden: int | None = None
    activo: bool | None = None


def doc_to_response(doc: dict) -> dict:
    return {
        "id": str(doc["_id"]),
        "imagen_url": doc["imagen_url"],
        "enlace": doc.get("enlace", ""),
        "orden": doc.get("orden", 0),
        "activo": doc.get("activo", True),
        "createdAt": doc.get("createdAt", datetime.utcnow()),
    }


@router.get("")
async def listar_banners(activo_only: bool = False):
    """Listar banners ordenados. activo_only=true para solo activos."""
    db = get_database()
    query = {"activo": True} if activo_only else {}
    cursor = db["banners"].find(query).sort("orden", 1)
    return [doc_to_response(d) async for d in cursor]


@router.post("")
async def crear_banner(data: BannerCreate):
    """Crear banner."""
    db = get_database()
    doc = {
        "imagen_url": data.imagen_url,
        "enlace": data.enlace,
        "orden": data.orden,
        "activo": data.activo,
        "createdAt": datetime.utcnow(),
    }
    result = await db["banners"].insert_one(doc)
    doc["_id"] = result.inserted_id
    return doc_to_response(doc)


@router.get("/{id}")
async def obtener_banner(id: str):
    """Obtener banner por ID."""
    db = get_database()
    doc = await db["banners"].find_one({"_id": ObjectId(id)})
    if not doc:
        raise HTTPException(404, "Banner no encontrado")
    return doc_to_response(doc)


@router.patch("/{id}")
async def actualizar_banner(id: str, data: BannerUpdate):
    """Actualizar banner."""
    db = get_database()
    update = {k: v for k, v in data.model_dump().items() if v is not None}
    if not update:
        raise HTTPException(400, "Nada que actualizar")
    doc = await db["banners"].find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": update}, return_document=True
    )
    if not doc:
        raise HTTPException(404, "Banner no encontrado")
    return doc_to_response(doc)


@router.delete("/{id}")
async def eliminar_banner(id: str):
    """Eliminar banner."""
    db = get_database()
    result = await db["banners"].delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(404, "Banner no encontrado")
    return {"message": "Eliminado"}
