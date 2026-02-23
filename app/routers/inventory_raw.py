"""Endpoints para materia prima (inventory_raw)."""
from fastapi import APIRouter, HTTPException
from bson import ObjectId

from app.database import get_database
from app.schemas.inventory import InventoryRawCreate, InventoryRawUpdate, InventoryRawResponse

router = APIRouter(prefix="/inventory-raw", tags=["Materia Prima"])


def doc_to_response(doc) -> dict:
    """Convertir documento MongoDB a respuesta."""
    return {
        "id": str(doc["_id"]),
        "nombre": doc["nombre"],
        "cantidad_total": doc["cantidad_total"],
        "costo_por_unidad": doc["costo_por_unidad"],
        "unidad_medida": doc.get("unidad_medida", "g"),
        "stock_minimo": doc.get("stock_minimo", 0),
        "fecha_ingreso": doc.get("fecha_ingreso"),
        "es_desechable": doc.get("es_desechable", False),
    }


@router.get("", response_model=list[InventoryRawResponse])
async def listar_materia_prima():
    """Listar toda la materia prima."""
    db = get_database()
    cursor = db["inventory_raw"].find({})
    return [doc_to_response(doc) async for doc in cursor]


@router.post("", response_model=InventoryRawResponse)
async def crear_materia_prima(data: InventoryRawCreate):
    """Crear materia prima."""
    db = get_database()
    doc = data.model_dump(exclude_none=True)
    result = await db["inventory_raw"].insert_one(doc)
    doc["_id"] = result.inserted_id
    return doc_to_response(doc)


@router.get("/{item_id}", response_model=InventoryRawResponse)
async def obtener_materia_prima(item_id: str):
    """Obtener materia prima por ID."""
    db = get_database()
    doc = await db["inventory_raw"].find_one({"_id": ObjectId(item_id)})
    if not doc:
        raise HTTPException(404, "Materia prima no encontrada")
    return doc_to_response(doc)


@router.patch("/{item_id}", response_model=InventoryRawResponse)
async def actualizar_materia_prima(item_id: str, data: InventoryRawUpdate):
    """Actualizar materia prima."""
    db = get_database()
    update = data.model_dump(exclude_none=True)
    result = await db["inventory_raw"].find_one_and_update(
        {"_id": ObjectId(item_id)},
        {"$set": update},
        return_document=True,
    )
    if not result:
        raise HTTPException(404, "Materia prima no encontrada")
    return doc_to_response(result)


@router.delete("/{item_id}")
async def eliminar_materia_prima(item_id: str):
    """Eliminar materia prima."""
    db = get_database()
    result = await db["inventory_raw"].delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count == 0:
        raise HTTPException(404, "Materia prima no encontrada")
    return {"message": "Eliminado correctamente"}
