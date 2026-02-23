"""CRUD Paneles de publicidad."""
from datetime import datetime
from fastapi import APIRouter, HTTPException
from bson import ObjectId

from app.database import get_database
from pydantic import BaseModel

router = APIRouter(prefix="/paneles", tags=["Paneles Publicidad"])


class PanelCreate(BaseModel):
    imagen_url: str
    enlace: str = ""
    orden: int = 0
    activo: bool = True


class PanelUpdate(BaseModel):
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
async def listar_paneles(activo_only: bool = False):
    """Listar paneles ordenados. activo_only=true para solo activos."""
    db = get_database()
    query = {"activo": True} if activo_only else {}
    cursor = db["paneles"].find(query).sort("orden", 1)
    return [doc_to_response(d) async for d in cursor]


@router.post("")
async def crear_panel(data: PanelCreate):
    """Crear panel."""
    db = get_database()
    doc = {
        "imagen_url": data.imagen_url,
        "enlace": data.enlace,
        "orden": data.orden,
        "activo": data.activo,
        "createdAt": datetime.utcnow(),
    }
    result = await db["paneles"].insert_one(doc)
    doc["_id"] = result.inserted_id
    return doc_to_response(doc)


@router.get("/{id}")
async def obtener_panel(id: str):
    """Obtener panel por ID."""
    db = get_database()
    doc = await db["paneles"].find_one({"_id": ObjectId(id)})
    if not doc:
        raise HTTPException(404, "Panel no encontrado")
    return doc_to_response(doc)


@router.patch("/{id}")
async def actualizar_panel(id: str, data: PanelUpdate):
    """Actualizar panel."""
    db = get_database()
    update = {k: v for k, v in data.model_dump().items() if v is not None}
    if not update:
        raise HTTPException(400, "Nada que actualizar")
    doc = await db["paneles"].find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": update}, return_document=True
    )
    if not doc:
        raise HTTPException(404, "Panel no encontrado")
    return doc_to_response(doc)


@router.delete("/{id}")
async def eliminar_panel(id: str):
    """Eliminar panel."""
    db = get_database()
    result = await db["paneles"].delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(404, "Panel no encontrado")
    return {"message": "Eliminado"}
