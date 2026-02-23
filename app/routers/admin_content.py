"""CRUD Admin: anuncios, banners, paneles. Requiere auth admin/master."""
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId

from app.database import get_database
from app.auth import require_auth
from pydantic import BaseModel

router = APIRouter(prefix="/admin", tags=["Admin Content"])


async def _require_admin(current_user: dict = Depends(require_auth)):
    if current_user.get("rol") not in ("admin", "master"):
        raise HTTPException(403, "Solo admin o master")
    return current_user


# --- Anuncios ---
class AnuncioCreate(BaseModel):
    texto: str


class AnuncioUpdate(BaseModel):
    texto: str | None = None
    orden: int | None = None
    activo: bool | None = None


def _anuncio_response(doc: dict) -> dict:
    return {
        "id": str(doc["_id"]),
        "texto": doc.get("texto", ""),
        "orden": doc.get("orden", 0),
        "activo": doc.get("activo", True),
    }


@router.post("/anuncios")
async def crear_anuncio(data: AnuncioCreate, _: dict = Depends(_require_admin)):
    db = get_database()
    doc = {"texto": data.texto, "orden": 0, "activo": True, "createdAt": datetime.utcnow()}
    result = await db["anuncios"].insert_one(doc)
    doc["_id"] = result.inserted_id
    return _anuncio_response(doc)


@router.put("/anuncios/{id}")
async def actualizar_anuncio(id: str, data: AnuncioUpdate, _: dict = Depends(_require_admin)):
    db = get_database()
    update = {k: v for k, v in data.model_dump().items() if v is not None}
    if not update:
        raise HTTPException(400, "Nada que actualizar")
    doc = await db["anuncios"].find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": update}, return_document=True
    )
    if not doc:
        raise HTTPException(404, "Anuncio no encontrado")
    return _anuncio_response(doc)


@router.delete("/anuncios/{id}")
async def eliminar_anuncio(id: str, _: dict = Depends(_require_admin)):
    db = get_database()
    result = await db["anuncios"].delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(404, "Anuncio no encontrado")
    return {"message": "Eliminado"}


# --- Banners ---
class BannerCreate(BaseModel):
    imagen: str
    titulo: str
    subtitulo: str = ""
    enlace: str = ""


class BannerUpdate(BaseModel):
    imagen: str | None = None
    titulo: str | None = None
    subtitulo: str | None = None
    enlace: str | None = None
    orden: int | None = None
    activo: bool | None = None


def _banner_response(doc: dict) -> dict:
    return {
        "id": str(doc["_id"]),
        "imagen": doc.get("imagen", ""),
        "titulo": doc.get("titulo", ""),
        "subtitulo": doc.get("subtitulo", ""),
        "enlace": doc.get("enlace", ""),
        "orden": doc.get("orden", 0),
        "activo": doc.get("activo", True),
    }


@router.post("/banners")
async def crear_banner(data: BannerCreate, _: dict = Depends(_require_admin)):
    db = get_database()
    doc = {
        "imagen": data.imagen,
        "titulo": data.titulo,
        "subtitulo": data.subtitulo,
        "enlace": data.enlace,
        "orden": 0,
        "activo": True,
        "createdAt": datetime.utcnow(),
    }
    result = await db["banners"].insert_one(doc)
    doc["_id"] = result.inserted_id
    return _banner_response(doc)


@router.put("/banners/{id}")
async def actualizar_banner(id: str, data: BannerUpdate, _: dict = Depends(_require_admin)):
    db = get_database()
    update = {k: v for k, v in data.model_dump().items() if v is not None}
    if not update:
        raise HTTPException(400, "Nada que actualizar")
    doc = await db["banners"].find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": update}, return_document=True
    )
    if not doc:
        raise HTTPException(404, "Banner no encontrado")
    return _banner_response(doc)


@router.delete("/banners/{id}")
async def eliminar_banner(id: str, _: dict = Depends(_require_admin)):
    db = get_database()
    result = await db["banners"].delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(404, "Banner no encontrado")
    return {"message": "Eliminado"}


# --- Paneles ---
class PanelCreate(BaseModel):
    imagen: str
    titulo: str
    subtitulo: str = ""


class PanelUpdate(BaseModel):
    imagen: str | None = None
    titulo: str | None = None
    subtitulo: str | None = None
    orden: int | None = None
    activo: bool | None = None


def _panel_response(doc: dict) -> dict:
    return {
        "id": str(doc["_id"]),
        "imagen": doc.get("imagen", ""),
        "titulo": doc.get("titulo", ""),
        "subtitulo": doc.get("subtitulo", ""),
        "orden": doc.get("orden", 0),
        "activo": doc.get("activo", True),
    }


@router.post("/paneles")
async def crear_panel(data: PanelCreate, _: dict = Depends(_require_admin)):
    db = get_database()
    doc = {
        "imagen": data.imagen,
        "titulo": data.titulo,
        "subtitulo": data.subtitulo,
        "orden": 0,
        "activo": True,
        "createdAt": datetime.utcnow(),
    }
    result = await db["paneles"].insert_one(doc)
    doc["_id"] = result.inserted_id
    return _panel_response(doc)


@router.put("/paneles/{id}")
async def actualizar_panel(id: str, data: PanelUpdate, _: dict = Depends(_require_admin)):
    db = get_database()
    update = {k: v for k, v in data.model_dump().items() if v is not None}
    if not update:
        raise HTTPException(400, "Nada que actualizar")
    doc = await db["paneles"].find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": update}, return_document=True
    )
    if not doc:
        raise HTTPException(404, "Panel no encontrado")
    return _panel_response(doc)


@router.delete("/paneles/{id}")
async def eliminar_panel(id: str, _: dict = Depends(_require_admin)):
    db = get_database()
    result = await db["paneles"].delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(404, "Panel no encontrado")
    return {"message": "Eliminado"}
