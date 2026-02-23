"""Endpoints de sucursales."""
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId

from app.database import get_database
from app.auth import require_auth, pwd_context
from app.config import get_settings
from pydantic import BaseModel

router = APIRouter(tags=["Sucursales"])


def _verify_pin(pin: str) -> bool:
    """Verificar PIN master (variable PIN_MASTER en .env, default 1234)."""
    settings = get_settings()
    return pin == settings.pin_master


def doc_to_response(doc: dict) -> dict:
    return {
        "id": str(doc["_id"]),
        "nombre": doc["nombre"],
        "direccion": doc.get("direccion", ""),
        "lat": doc.get("lat", 0),
        "lng": doc.get("lng", 0),
        "telefono": doc.get("telefono", ""),
        "activa": doc.get("activa", True),
        "createdAt": doc.get("createdAt"),
    }


def _verify_pin(pin: str) -> bool:
    """Verificar PIN master. Usa config o default 1234."""
    from app.config import get_settings
    settings = get_settings()
    stored = settings.pin_master_hash or DEFAULT_PIN_HASH
    return pwd_context.verify(pin, stored)


async def _require_master(current_user: dict = Depends(require_auth)):
    """Requerir rol master."""
    if current_user.get("rol") != "master":
        raise HTTPException(403, "Solo el rol master puede realizar esta acción")
    return current_user


class SucursalCreate(BaseModel):
    nombre: str
    direccion: str = ""
    lat: float = 0
    lng: float = 0
    telefono: str = ""
    activa: bool = True
    pin: str  # PIN master para crear


class SucursalUpdate(BaseModel):
    nombre: str | None = None
    direccion: str | None = None
    lat: float | None = None
    lng: float | None = None
    telefono: str | None = None
    activa: bool | None = None


@router.get("/sucursales")
async def listar_sucursales_activas(activa_only: bool = True):
    """Listar sucursales activas (público)."""
    db = get_database()
    query = {"activa": True} if activa_only else {}
    cursor = db["sucursales"].find(query)
    return [doc_to_response(d) async for d in cursor]


@router.get("/admin/sucursales")
async def listar_todas_sucursales(current_user: dict = Depends(_require_master)):
    """Listar todas las sucursales (solo master)."""
    db = get_database()
    cursor = db["sucursales"].find({})
    return [doc_to_response(d) async for d in cursor]


@router.post("/admin/sucursales")
async def crear_sucursal(data: SucursalCreate, current_user: dict = Depends(_require_master)):
    """Crear sucursal (solo master, requiere PIN en body)."""
    if not _verify_pin(data.pin):
        raise HTTPException(403, "PIN incorrecto")

    db = get_database()
    doc = {
        "nombre": data.nombre,
        "direccion": data.direccion,
        "lat": data.lat,
        "lng": data.lng,
        "telefono": data.telefono,
        "activa": data.activa,
        "createdAt": datetime.utcnow(),
    }
    result = await db["sucursales"].insert_one(doc)
    doc["_id"] = result.inserted_id
    return doc_to_response(doc)


@router.put("/admin/sucursales/{id}")
async def actualizar_sucursal(id: str, data: SucursalUpdate, current_user: dict = Depends(_require_master)):
    """Actualizar sucursal."""
    db = get_database()
    update = {k: v for k, v in data.model_dump().items() if v is not None}
    if not update:
        raise HTTPException(400, "Nada que actualizar")
    doc = await db["sucursales"].find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": update}, return_document=True
    )
    if not doc:
        raise HTTPException(404, "Sucursal no encontrada")
    return doc_to_response(doc)
